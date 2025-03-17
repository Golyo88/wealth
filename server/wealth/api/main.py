from typing import Optional, Literal, TypeVar, Generic
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from wealth.database.database import get_db
from sqlalchemy.sql import text
from wealth.database.init_db import init_db
from contextlib import asynccontextmanager
from sqlalchemy import desc, asc, func, distinct
from wealth.api.views.wealth_view import WealthView

from wealth.database.models import (
    Cash,
    HighValueOccasionalIncomeItem,
    MotorVehicle,
    OngoingIncomeGeneratingActivity,
    PastRolesAndAffiliation,
    PublicDebt,
    SavingsDeposit,
    Person,
    RealEstate,
    Security,
    BankLoan,
    PrivateLoan,
    OtherClaim,
    BankDepositClaim,
    WatercraftOrAircraft,
)

T = TypeVar("T", bound=BaseModel)


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 10
    total: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    results: list[T]
    pagination: PaginationParams


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

    subquery = (
        db.query(
            Person.id,
            func.count(distinct(RealEstate.id)).label("real_estates_count"),
            (
                func.count(distinct(MotorVehicle.id))
                + func.count(distinct(WatercraftOrAircraft.id))
            ).label("vehicles_count"),
            func.count(distinct(Security.id)).label("securities_count"),
            (
                func.count(distinct(PastRolesAndAffiliation.id))
                + func.count(distinct(OngoingIncomeGeneratingActivity.id))
                + func.count(distinct(HighValueOccasionalIncomeItem.id))
            ).label("income_count"),
            (
                func.sum(distinct(func.coalesce(Security.value_huf, 0)))
                + func.sum(distinct(func.coalesce(SavingsDeposit.value_huf, 0)))
                + func.sum(distinct(func.coalesce(Cash.value_huf, 0)))
                + func.sum(distinct(func.coalesce(BankDepositClaim.value_huf, 0)))
                + func.sum(distinct(func.coalesce(OtherClaim.value_huf, 0)))
            ).label("savings_amount"),
            func.sum(distinct(func.coalesce(PublicDebt.value_huf, 0))).label(
                "public_debt_amount"
            ),
            func.sum(distinct(func.coalesce(BankLoan.value_huf, 0))).label(
                "bank_loan_amount"
            ),
            func.sum(distinct(func.coalesce(PrivateLoan.value_huf, 0))).label(
                "private_loan_amount"
            ),
            (
                func.sum(distinct(func.coalesce(PublicDebt.value_huf, 0)))
                + func.sum(distinct(func.coalesce(BankLoan.value_huf, 0)))
                + func.sum(distinct(func.coalesce(PrivateLoan.value_huf, 0)))
            ).label("liabilities_amount"),
        )
        .outerjoin(RealEstate)
        .outerjoin(MotorVehicle)
        .outerjoin(WatercraftOrAircraft)
        .outerjoin(Security)
        .outerjoin(PastRolesAndAffiliation)
        .outerjoin(OngoingIncomeGeneratingActivity)
        .outerjoin(HighValueOccasionalIncomeItem)
        .outerjoin(SavingsDeposit)
        .outerjoin(Cash)
        .outerjoin(BankDepositClaim)
        .outerjoin(OtherClaim)
        .outerjoin(PublicDebt)
        .outerjoin(BankLoan)
        .outerjoin(PrivateLoan)
        .group_by(Person.id)
    ).subquery()

    query = db.query(Person, subquery)
    query = query.join(subquery, Person.id == subquery.c.id)

    if name:
        query = query.filter(Person.name.ilike(f"%{name}%"))

    if real_estates_count_op:
        query = apply_comparison(
            query,
            subquery.c.real_estates_count,
            real_estates_count,
            real_estates_count_op,
        )

    if vehicles_count_op:
        query = apply_comparison(
            query, subquery.c.vehicles_count, vehicles_count, vehicles_count_op
        )

    if securities_count_op:
        query = apply_comparison(
            query, subquery.c.securities_count, securities_count, securities_count_op
        )

    if income_count_op:
        query = apply_comparison(
            query, subquery.c.income_count, income_count, income_count_op
        )

    if savings_amount_op:
        query = apply_comparison(
            query, subquery.c.savings_amount, savings_amount, savings_amount_op
        )

    if liabilities_amount_op:
        query = apply_comparison(
            query,
            subquery.c.liabilities_amount,
            liabilities_amount,
            liabilities_amount_op,
        )

    if net_worth_op:
        net_worth_expr = subquery.c.savings_amount - subquery.c.liabilities_amount
        query = apply_comparison(query, net_worth_expr, net_worth, net_worth_op)

    if order_by:
        if order_by == "real_estates_count":
            query = query.order_by(
                asc(subquery.c.real_estates_count)
                if order_direction == "asc"
                else desc(subquery.c.real_estates_count)
            )
        elif order_by == "vehicles_count":
            query = query.order_by(
                asc(subquery.c.vehicles_count)
                if order_direction == "asc"
                else desc(subquery.c.vehicles_count)
            )
        elif order_by == "securities_count":
            query = query.order_by(
                asc(subquery.c.securities_count)
                if order_direction == "asc"
                else desc(subquery.c.securities_count)
            )
        elif order_by == "income_count":
            query = query.order_by(
                asc(subquery.c.income_count)
                if order_direction == "asc"
                else desc(subquery.c.income_count)
            )
        elif order_by == "savings_amount":
            query = query.order_by(
                asc(subquery.c.savings_amount)
                if order_direction == "asc"
                else desc(subquery.c.savings_amount)
            )
        elif order_by == "liabilities_amount":
            query = query.order_by(
                asc(subquery.c.liabilities_amount)
                if order_direction == "asc"
                else desc(subquery.c.liabilities_amount)
            )
        elif order_by == "net_worth":
            net_worth = subquery.c.savings_amount - subquery.c.liabilities_amount
            query = query.order_by(
                asc(net_worth) if order_direction == "asc" else desc(net_worth)
            )

    total = query.count()

    results = (
        query.offset((pagination.page - 1) * pagination.page_size)
        .limit(pagination.page_size)
        .all()
    )

    return {
        "results": [WealthView.from_person(result[0]) for result in results],
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


@app.get("/api/people/{id}/wealth")
async def get_wealth(id: int, db: Session = Depends(get_db)) -> WealthView:
    person = db.query(Person).filter(Person.id == id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return WealthView.from_person(person)
