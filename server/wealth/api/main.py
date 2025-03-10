from typing import Optional, Literal
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from wealth.database.database import get_db
from sqlalchemy.sql import text
from wealth.database.init_db import init_db
from contextlib import asynccontextmanager
from sqlalchemy import desc, asc, func, distinct, case

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


@app.get("/api/wealths")
async def get_wealths(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    name: Optional[str] = Query(None, description="Név alapján szűrés"),
    real_estates_count_op: Optional[Literal["eq", "gt", "lt"]] = Query(None),
    real_estates_count: Optional[int] = Query(None),
    vehicles_count_op: Optional[Literal["eq", "gt", "lt"]] = Query(None),
    vehicles_count: Optional[int] = Query(None),
    securities_count_op: Optional[Literal["eq", "gt", "lt"]] = Query(None),
    securities_count: Optional[int] = Query(None),
    income_count_op: Optional[Literal["eq", "gt", "lt"]] = Query(None),
    income_count: Optional[int] = Query(None),
    savings_amount_op: Optional[Literal["eq", "gt", "lt"]] = Query(None),
    savings_amount: Optional[int] = Query(None),
    liabilities_amount_op: Optional[Literal["eq", "gt", "lt"]] = Query(None),
    liabilities_amount: Optional[int] = Query(None),
    net_worth_op: Optional[Literal["eq", "gt", "lt"]] = Query(None),
    net_worth: Optional[int] = Query(None),
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
    ] = Query(None),
    order_direction: Optional[Literal["asc", "desc"]] = Query("asc"),
    db: Session = Depends(get_db),
):

    pagination = PaginationParams(page=page, page_size=page_size)

    # Először készítsünk egy subquery-t az értékpapírok összegével
    securities_sum = (
        db.query(
            Wealth.id.label("wealth_id"),
            func.coalesce(func.sum(Security.value_huf), 0).label("securities_sum"),
        )
        .outerjoin(Security)
        .group_by(Wealth.id)
    ).subquery()

    # Készítsünk egy subquery-t a tartozások összegével
    liabilities_sum = (
        db.query(
            Wealth.id.label("wealth_id"),
            func.sum(
                case(
                    (
                        Liability.id.isnot(None),
                        func.coalesce(Liability.public_debt_huf, 0)
                        + func.coalesce(Liability.bank_loans_huf, 0)
                        + func.coalesce(Liability.private_loans_huf, 0),
                    ),
                    else_=0,
                )
            ).label("liabilities_sum"),
        )
        .select_from(Wealth)
        .outerjoin(Liability)
        .group_by(Wealth.id)
    ).subquery()

    # Most készítsük el a fő subquery-t
    subquery = (
        db.query(
            Wealth.id.label("wealth_id"),
            func.count(distinct(RealEstate.id)).label("real_estates_count"),
            func.count(distinct(Vehicle.id)).label("vehicles_count"),
            func.count(distinct(Security.id)).label("securities_count"),
            func.count(distinct(IncomeItem.id)).label("income_count"),
            (
                func.coalesce(Savings.deposit_huf, 0)
                + func.coalesce(Savings.cash_huf, 0)
                + func.coalesce(Savings.bank_balance_huf, 0)
                + func.coalesce(Savings.bank_balance_foreign_currency, 0)
                * func.coalesce(Savings.exchange_rate, 0)
                + securities_sum.c.securities_sum
            ).label("savings_amount"),
            liabilities_sum.c.liabilities_sum.label("liabilities_amount"),
        )
        .select_from(Wealth)
        .outerjoin(RealEstate)
        .outerjoin(Vehicle)
        .outerjoin(Security)
        .outerjoin(IncomeItem)
        .outerjoin(Savings)
        .outerjoin(securities_sum, Wealth.id == securities_sum.c.wealth_id)
        .outerjoin(liabilities_sum, Wealth.id == liabilities_sum.c.wealth_id)
        .group_by(
            Wealth.id,
            Savings.deposit_huf,
            Savings.cash_huf,
            Savings.bank_balance_huf,
            Savings.bank_balance_foreign_currency,
            Savings.exchange_rate,
            securities_sum.c.securities_sum,
            liabilities_sum.c.liabilities_sum,
        )
    ).subquery()

    # Base query definíció
    base_query = (
        db.query(
            Wealth,
            subquery.c.real_estates_count,
            subquery.c.vehicles_count,
            subquery.c.securities_count,
            subquery.c.income_count,
            subquery.c.savings_amount,
            subquery.c.liabilities_amount,
            (subquery.c.savings_amount - subquery.c.liabilities_amount).label(
                "net_worth"
            ),
        )
        .select_from(Wealth)
        .join(subquery, Wealth.id == subquery.c.wealth_id)
    )

    # Név szerinti szűrés
    if name:
        base_query = base_query.join(Person).filter(Person.name.ilike(f"%{name}%"))

    # Számosság szerinti szűrések
    if real_estates_count is not None and real_estates_count_op:
        base_query = apply_comparison(
            base_query,
            subquery.c.real_estates_count,
            real_estates_count,
            real_estates_count_op,
        )
    if vehicles_count is not None and vehicles_count_op:
        base_query = apply_comparison(
            base_query, subquery.c.vehicles_count, vehicles_count, vehicles_count_op
        )
    if securities_count is not None and securities_count_op:
        base_query = apply_comparison(
            base_query,
            subquery.c.securities_count,
            securities_count,
            securities_count_op,
        )
    if income_count is not None and income_count_op:
        base_query = apply_comparison(
            base_query, subquery.c.income_count, income_count, income_count_op
        )
    if savings_amount is not None and savings_amount_op:
        base_query = apply_comparison(
            base_query, subquery.c.savings_amount, savings_amount, savings_amount_op
        )
    if liabilities_amount is not None and liabilities_amount_op:
        if liabilities_amount_op == "gt":
            base_query = base_query.filter(
                (subquery.c.liabilities_amount > liabilities_amount)
                & (subquery.c.liabilities_amount > 0)
            )
        elif liabilities_amount_op == "lt":
            base_query = base_query.filter(
                (subquery.c.liabilities_amount < liabilities_amount)
                & (subquery.c.liabilities_amount > 0)
            )
        elif liabilities_amount_op == "eq":
            base_query = base_query.filter(
                (subquery.c.liabilities_amount == liabilities_amount)
                & (subquery.c.liabilities_amount > 0)
            )

    if net_worth is not None and net_worth_op:
        base_query = apply_comparison(
            base_query,
            subquery.c.savings_amount - subquery.c.liabilities_amount,
            net_worth,
            net_worth_op,
        )

    # Rendezés
    if order_by:
        if order_by == "real_estates_count":
            base_query = base_query.order_by(
                asc(subquery.c.real_estates_count)
                if order_direction == "asc"
                else desc(subquery.c.real_estates_count)
            )
        elif order_by == "vehicles_count":
            base_query = base_query.order_by(
                asc(subquery.c.vehicles_count)
                if order_direction == "asc"
                else desc(subquery.c.vehicles_count)
            )
        elif order_by == "securities_count":
            base_query = base_query.order_by(
                asc(subquery.c.securities_count)
                if order_direction == "asc"
                else desc(subquery.c.securities_count)
            )
        elif order_by == "income_count":
            base_query = base_query.order_by(
                asc(subquery.c.income_count)
                if order_direction == "asc"
                else desc(subquery.c.income_count)
            )
        elif order_by == "savings_amount":
            base_query = base_query.order_by(
                asc(subquery.c.savings_amount)
                if order_direction == "asc"
                else desc(subquery.c.savings_amount)
            )
        elif order_by == "liabilities_amount":
            base_query = base_query.order_by(
                asc(subquery.c.liabilities_amount)
                if order_direction == "asc"
                else desc(subquery.c.liabilities_amount)
            )
        elif order_by == "net_worth":
            net_worth = subquery.c.savings_amount - subquery.c.liabilities_amount
            base_query = base_query.order_by(
                asc(net_worth) if order_direction == "asc" else desc(net_worth)
            )

    # Lapozás
    total = base_query.count()
    results = (
        base_query.offset((pagination.page - 1) * pagination.page_size)
        .limit(pagination.page_size)
        .all()
    )

    return {
        "results": [result[0].to_model() for result in results],
        "pagination": {
            "page": pagination.page,
            "page_size": pagination.page_size,
            "total": total,
            "total_pages": (total + pagination.page_size - 1) // pagination.page_size,
        },
    }


def apply_comparison(query, column, value, op):
    if op == "eq":
        return query.filter(column == value)
    elif op == "gt":
        return query.filter(column > value)
    elif op == "lt":
        return query.filter(column < value)
    return query


@app.get("/api/wealths/{id}")
async def get_wealth(id: int, db: Session = Depends(get_db)):
    wealth = db.query(Wealth).filter(Wealth.id == id).first()
    if not wealth:
        raise HTTPException(status_code=404, detail="Wealth not found")
    return wealth.to_model()
