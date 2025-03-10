from typing import Optional, Literal
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import openai
from wealth.database.database import get_db
import os
from sqlalchemy.sql import text
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from wealth.database.init_db import init_db
from contextlib import asynccontextmanager
from sqlalchemy import desc, asc, func

from wealth.database.models import (
    IncomeItem,
    Wealth,
    Person,
    RealEstate,
    Vehicle,
    Security,
    Savings,
    Liability,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        db: Session = next(get_db())
        try:
            result = db.execute(text("SELECT COUNT(*) FROM persons")).scalar()
            if result == 0:
                print("Az adatbázis üres, inicializálás kezdése...")
                init_db()
                print("Adatbázis inicializálás befejezve.")
        except Exception as table_error:
            print("A persons tábla nem létezik, adatbázis inicializálás kezdése...")
            init_db()
            print("Adatbázis inicializálás befejezve.")
    except Exception as e:
        print(f"Hiba történt az adatbázis ellenőrzésekor: {str(e)}")
        raise e
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryModel(BaseModel):
    query: str


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 10


async def execute_sql_with_retry(
    client: openai.OpenAI,
    messages: list[dict[str, str]],
    pagination: PaginationParams,
    max_retries: int = 5,
) -> dict:
    last_error = None

    for attempt in range(max_retries):
        try:
            db: Session = next(get_db())
            # Kérjük le az SQL lekérdezést a ChatGPT-től
            response = client.beta.chat.completions.parse(
                model="o3-mini",
                messages=messages,
                response_format=QueryModel,
            )

            sql_query = QueryModel.model_validate_json(
                response.choices[0].message.content
            ).query

            # Számoljuk meg az összes találatot lapozás nélkül
            count_query = sql_query.split("LIMIT")[0].split("OFFSET")[0]
            count_query = f"SELECT COUNT(*) as total FROM ({count_query}) as subquery"
            total_result = db.execute(text(count_query)).scalar()

            # Próbáljuk végrehajtani
            result = db.execute(text(sql_query))
            results_as_dict = result.mappings().all()

            ids = [row["wealth_id"] for row in results_as_dict]
            query = select(Wealth).where(Wealth.id.in_(ids))
            result = db.execute(query)
            wealths = result.scalars().all()

            return {
                "query": sql_query,
                "results": [wealth.to_model() for wealth in wealths],
                "messages": messages,
                "pagination": {
                    "page": pagination.page,
                    "page_size": pagination.page_size,
                    "total": total_result,
                    "total_pages": (total_result + pagination.page_size - 1)
                    // pagination.page_size,
                },
            }

        except SQLAlchemyError as e:
            last_error = str(e)
            messages.extend(
                [
                    {"role": "assistant", "content": sql_query},
                    {
                        "role": "user",
                        "content": f"This query resulted in an error: {last_error}. Please fix it.",
                    },
                ]
            )

            if attempt == max_retries - 1:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed after {max_retries} attempts. Last error: {last_error}",
                )


@app.get("/api/query/openai")
async def query_with_openai(
    prompt: str,
    page: int = Query(default=1, ge=1, description="Az oldal száma"),
    page_size: int = Query(default=10, ge=1, le=100, description="Az oldal mérete"),
):
    try:
        pagination = PaginationParams(page=page, page_size=page_size)
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        messages = [
            {
                "role": "system",
                "content": """You are a SQL expert. Generate SQL queries for a PostgreSQL database with the following schema:
                CREATE TABLE
                      public.persons (
                        id serial NOT NULL,
                        name character varying NOT NULL,
                        role role NOT NULL
                      );

                    ALTER TABLE
                      public.persons
                    ADD
                      CONSTRAINT persons_pkey PRIMARY KEY (id);

                    CREATE TABLE
                      public.wealth (id serial NOT NULL, person_id integer NULL);

                    ALTER TABLE
                      public.wealth
                    ADD
                      CONSTRAINT wealth_pkey PRIMARY KEY (id);

                    CREATE TABLE
                      public.economic_interests (
                        id serial NOT NULL,
                        wealth_id integer NULL,
                        organization character varying NOT NULL,
                        role character varying NOT NULL,
                        ownership_percentage character varying NULL,
                        income_category incomecategory NOT NULL
                      );

                    ALTER TABLE
                      public.economic_interests
                    ADD
                      CONSTRAINT economic_interests_pkey PRIMARY KEY (id);

                      CREATE TABLE
                        public.income_items (
                          id serial NOT NULL,
                          wealth_id integer NULL,
                          "position_name" character varying NOT NULL,
                          income_category incomecategory NOT NULL
                        );

                      ALTER TABLE
                        public.income_items
                      ADD
                        CONSTRAINT income_items_pkey PRIMARY KEY (id);
                      
                      CREATE TABLE
                        public.liabilities (
                          id serial NOT NULL,
                          wealth_id integer NULL,
                          public_debt_huf integer NULL,
                          bank_loans_huf integer NULL,
                          private_loans_huf integer NULL
                        );

                      ALTER TABLE
                        public.liabilities
                      ADD
                        CONSTRAINT liabilities_pkey PRIMARY KEY (id);

                      CREATE TABLE
                        public.real_estates (
                          id serial NOT NULL,
                          wealth_id integer NULL,
                          location character varying NOT NULL,
                          area_m2 integer NOT NULL,
                          land_use character varying NOT NULL,
                          building_type character varying NULL,
                          building_size_m2 integer NULL,
                          legal_status character varying NULL,
                          ownership_status character varying NOT NULL,
                          ownership_share character varying NOT NULL,
                          acquisition_mode character varying NOT NULL,
                          acquisition_date character varying NOT NULL
                        );

                      ALTER TABLE
                        public.real_estates
                      ADD
                        CONSTRAINT real_estates_pkey PRIMARY KEY (id);

                      CREATE TABLE
                        public.savings (
                          id serial NOT NULL,
                          wealth_id integer NULL,
                          deposit_huf integer NULL,
                          cash_huf integer NULL,
                          bank_balance_huf integer NULL,
                          bank_balance_foreign_currency integer NULL,
                          exchange_rate double precision NULL
                        );

                      ALTER TABLE
                        public.savings
                      ADD
                        CONSTRAINT savings_pkey PRIMARY KEY (id);

                      Important: Always query for the wealth_id.
                      Important: Add OFFSET and LIMIT for pagination.
              """,
            },
            {
                "role": "user",
                "content": f"To answer the following question: {prompt} LIMIT {pagination.page_size} OFFSET {(pagination.page - 1) * pagination.page_size}",
            },
        ]

        return await execute_sql_with_retry(client, messages, pagination)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.get("/api/query/raw")
# async def execute_raw_query(
#     query: str = Query(..., description="Az SQL lekérdezés"),
#     db: Session = Depends(get_db),
# ):
#     try:
#         result = db.execute(query)
#         return {"results": [dict(row) for row in result]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/wealths")
async def get_wealths(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    name: Optional[str] = Query(None, description="Név alapján szűrés"),
    real_estates_count_op: Optional[Literal["eq", "gt", "lt"]] = Query(
        None, description="Ingatlanok számának összehasonlító operátora"
    ),
    real_estates_count: Optional[int] = Query(None, description="Ingatlanok száma"),
    vehicles_count_op: Optional[Literal["eq", "gt", "lt"]] = Query(
        None, description="Járművek számának összehasonlító operátora"
    ),
    vehicles_count: Optional[int] = Query(None, description="Járművek száma"),
    securities_count_op: Optional[Literal["eq", "gt", "lt"]] = Query(
        None, description="Értékpapírok számának összehasonlító operátora"
    ),
    securities_count: Optional[int] = Query(None, description="Értékpapírok száma"),
    income_count_op: Optional[Literal["eq", "gt", "lt"]] = Query(
        None, description="Jövedelmek számának összehasonlító operátora"
    ),
    income_count: Optional[int] = Query(None, description="Jövedelmek száma"),
    savings_amount_op: Optional[Literal["eq", "gt", "lt"]] = Query(
        None, description="Megtakarítások összegének összehasonlító operátora"
    ),
    savings_amount: Optional[int] = Query(None, description="Megtakarítások összege"),
    liabilities_amount_op: Optional[Literal["eq", "gt", "lt"]] = Query(
        None, description="Tartozások összegének összehasonlító operátora"
    ),
    liabilities_amount: Optional[int] = Query(None, description="Tartozások összege"),
    net_worth_op: Optional[Literal["eq", "gt", "lt"]] = Query(
        None, description="Vagyon összegének összehasonlító operátora"
    ),
    net_worth: Optional[int] = Query(None, description="Vagyon összege"),
    order_by: Optional[
        Literal[
            "real_estates_count",
            "vehicles_count",
            "securities_count",
            "income_count",
            "savings_amount",
            "liabilities_amount",
            "net_worth",
        ]
    ] = Query(None, description="Rendezés mező"),
    order_direction: Optional[Literal["asc", "desc"]] = Query(
        "asc", description="Rendezés iránya"
    ),
    db: Session = Depends(get_db),
):
    pagination = PaginationParams(page=page, page_size=page_size)
    query = (
        db.query(
            Wealth,
            func.count(RealEstate.id).label("real_estates_count"),
            func.count(Vehicle.id).label("vehicles_count"),
            func.count(Security.id).label("securities_count"),
            func.count(IncomeItem.id).label("income_count"),
            (
                func.coalesce(
                    func.sum(
                        Savings.deposit_huf
                        + Savings.cash_huf
                        + Savings.bank_balance_huf
                        + Savings.bank_balance_foreign_currency * Savings.exchange_rate
                    ),
                    0,
                )
            ).label("savings_amount"),
            (
                func.coalesce(
                    func.sum(
                        Liability.public_debt_huf
                        + Liability.bank_loans_huf
                        + Liability.private_loans_huf
                    ),
                    0,
                )
            ).label("liabilities_amount"),
        )
        .outerjoin(RealEstate)
        .outerjoin(Vehicle)
        .outerjoin(Security)
        .outerjoin(IncomeItem)
        .outerjoin(Savings)
        .outerjoin(Liability)
        .group_by(Wealth.id)
    )

    if name:
        query = query.join(Person).filter(Person.name.ilike(f"%{name}%"))

    def add_filter(query, value, op, column):
        if value is not None and op is not None:
            if op == "eq":
                return query.having(column == value)
            elif op == "gt":
                return query.having(column > value)
            elif op == "lt":
                return query.having(column < value)
        return query

    query = add_filter(
        query, real_estates_count, real_estates_count_op, func.count(RealEstate.id)
    )
    query = add_filter(query, vehicles_count, vehicles_count_op, func.count(Vehicle.id))
    query = add_filter(
        query, securities_count, securities_count_op, func.count(Security.id)
    )
    query = add_filter(query, income_count, income_count_op, func.count(IncomeItem.id))
    query = add_filter(
        query,
        savings_amount,
        savings_amount_op,
        func.sum(
            Savings.deposit_huf
            + Savings.cash_huf
            + Savings.bank_balance_huf
            + Savings.bank_balance_foreign_currency * Savings.exchange_rate
        ),
    )
    query = add_filter(
        query,
        liabilities_amount,
        liabilities_amount_op,
        func.sum(
            Liability.public_debt_huf
            + Liability.bank_loans_huf
            + Liability.private_loans_huf
        ),
    )

    if net_worth is not None and net_worth_op is not None:
        net_worth_expr = func.coalesce(
            func.sum(
                Savings.deposit_huf
                + Savings.cash_huf
                + Savings.bank_balance_huf
                + Savings.bank_balance_foreign_currency * Savings.exchange_rate
            ),
            0,
        ) - func.coalesce(
            func.sum(
                Liability.public_debt_huf
                + Liability.bank_loans_huf
                + Liability.private_loans_huf
            ),
            0,
        )

        if net_worth_op == "eq":
            query = query.having(net_worth_expr == net_worth)
        elif net_worth_op == "gt":
            query = query.having(net_worth_expr > net_worth)
        elif net_worth_op == "lt":
            query = query.having(net_worth_expr < net_worth)

    if order_by:
        order_column = None
        if order_by == "real_estates_count":
            order_column = func.count(RealEstate.id)
        elif order_by == "vehicles_count":
            order_column = func.count(Vehicle.id)
        elif order_by == "securities_count":
            order_column = func.count(Security.id)
        elif order_by == "income_count":
            order_column = func.count(IncomeItem.id)
        elif order_by == "savings_amount":
            order_column = func.sum(
                Savings.deposit_huf
                + Savings.cash_huf
                + Savings.bank_balance_huf
                + Savings.bank_balance_foreign_currency * Savings.exchange_rate
            )
        elif order_by == "liabilities_amount":
            order_column = func.sum(
                Liability.public_debt_huf
                + Liability.bank_loans_huf
                + Liability.private_loans_huf
            )
        elif order_by == "net_worth":
            order_column = func.coalesce(
                func.sum(
                    Savings.deposit_huf
                    + Savings.cash_huf
                    + Savings.bank_balance_huf
                    + Savings.bank_balance_foreign_currency * Savings.exchange_rate
                ),
                0,
            ) - func.coalesce(
                func.sum(
                    Liability.public_debt_huf
                    + Liability.bank_loans_huf
                    + Liability.private_loans_huf
                ),
                0,
            )

        if order_by:
            query = query.order_by(
                desc(order_column) if order_direction == "desc" else asc(order_column)
            )

    total = query.count()
    query = query.offset((pagination.page - 1) * pagination.page_size).limit(
        pagination.page_size
    )

    results = query.all()

    return {
        "results": [wealth[0].to_model() for wealth in results],
        "pagination": {
            "page": pagination.page,
            "page_size": pagination.page_size,
            "total": total,
            "total_pages": (total + pagination.page_size - 1) // pagination.page_size,
        },
    }


@app.get("/api/wealths/{id}")
async def get_wealth(id: int, db: Session = Depends(get_db)):
    wealth = db.query(Wealth).filter(Wealth.id == id).first()
    if not wealth:
        raise HTTPException(status_code=404, detail="Wealth not found")
    return wealth.to_model()
