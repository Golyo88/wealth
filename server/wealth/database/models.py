from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from wealth.model import (
    Role,
    IncomeCategory,
    Person as PersonModel,
    Assets as AssetsModel,
    Liabilities as LiabilitiesModel,
    IncomeItem as IncomeItemModel,
    EconomicInterest as EconomicInterestModel,
    Wealth as WealthModel,
    RealEstateItem as RealEstateModel,
    Vehicle as VehicleModel,
    Security as SecurityModel,
    Savings as SavingsModel,
    WealthModelWithId,
)


Base = declarative_base()


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)

    wealth = relationship("Wealth", back_populates="person")


class RealEstate(Base):
    __tablename__ = "real_estates"

    id = Column(Integer, primary_key=True)
    wealth_id = Column(Integer, ForeignKey("wealth.id"))
    location = Column(String, nullable=False)
    area_m2 = Column(Integer, nullable=False)
    land_use = Column(String, nullable=False)
    building_type = Column(String)
    building_size_m2 = Column(Integer)
    legal_status = Column(String)
    ownership_status = Column(String, nullable=False)
    ownership_share = Column(String, nullable=False)
    acquisition_mode = Column(String, nullable=False)
    acquisition_date = Column(String, nullable=False)


class Savings(Base):
    __tablename__ = "savings"

    id = Column(Integer, primary_key=True)
    wealth_id = Column(Integer, ForeignKey("wealth.id"))
    deposit_huf = Column(Integer)
    cash_huf = Column(Integer)
    bank_balance_huf = Column(Integer)
    bank_balance_foreign_currency = Column(Integer)
    exchange_rate = Column(Float)


class Liability(Base):
    __tablename__ = "liabilities"

    id = Column(Integer, primary_key=True)
    wealth_id = Column(Integer, ForeignKey("wealth.id"))
    public_debt_huf = Column(Integer, nullable=True)
    bank_loans_huf = Column(Integer, nullable=True)
    private_loans_huf = Column(Integer, nullable=True)


class IncomeItem(Base):
    __tablename__ = "income_items"

    id = Column(Integer, primary_key=True)
    wealth_id = Column(Integer, ForeignKey("wealth.id"))
    position_name = Column(String, nullable=False)
    income_category = Column(Enum(IncomeCategory), nullable=False)

    def to_model(self):
        return IncomeItemModel(
            position=self.position_name,
            income_category=self.income_category,
        )


class EconomicInterest(Base):
    __tablename__ = "economic_interests"

    id = Column(Integer, primary_key=True)
    wealth_id = Column(Integer, ForeignKey("wealth.id"))
    organization = Column(String, nullable=False)
    role = Column(String, nullable=False)
    ownership_percentage = Column(String)
    income_category = Column(Enum(IncomeCategory), nullable=False)


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)
    wealth_id = Column(Integer, ForeignKey("wealth.id"))
    type = Column(String, nullable=False)
    brand_model = Column(String, nullable=False)
    acquisition_year = Column(Integer, nullable=False)
    acquisition_mode = Column(String, nullable=False)


class Security(Base):
    __tablename__ = "securities"

    id = Column(Integer, primary_key=True)
    wealth_id = Column(Integer, ForeignKey("wealth.id"))
    type = Column(String, nullable=False)
    value_huf = Column(Integer, nullable=False)


class Wealth(Base):
    __tablename__ = "wealth"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"))

    person = relationship("Person", back_populates="wealth")
    real_estates = relationship("RealEstate", backref="wealth")
    vehicles = relationship("Vehicle", backref="wealth")
    securities = relationship("Security", backref="wealth")
    savings = relationship("Savings", backref="wealth", uselist=False)
    liabilities = relationship("Liability", backref="wealth")
    income_items = relationship("IncomeItem", backref="wealth")
    economic_interests = relationship("EconomicInterest", backref="wealth")

    def to_model(self):
        return WealthModelWithId(
            id=self.id,
            person=PersonModel.model_validate(self.person),
            assets=AssetsModel.model_validate(
                {
                    "real_estate": (
                        [
                            RealEstateModel.model_validate(real_estate)
                            for real_estate in self.real_estates
                        ]
                        if self.real_estates
                        else None
                    ),
                    "vehicles": (
                        [
                            VehicleModel.model_validate(vehicle)
                            for vehicle in self.vehicles
                        ]
                        if self.vehicles
                        else None
                    ),
                    "securities": (
                        [
                            SecurityModel.model_validate(security)
                            for security in self.securities
                        ]
                        if self.securities
                        else None
                    ),
                    "savings": (
                        SavingsModel.model_validate(self.savings)
                        if self.savings
                        else None
                    ),
                }
            ),
            liabilities=LiabilitiesModel.model_validate(self.liabilities[0]),
            income=(
                [IncomeItem.to_model(income) for income in self.income_items]
                if self.income_items
                else []
            ),
            economic_interests=(
                [
                    EconomicInterestModel.model_validate(interest)
                    for interest in self.economic_interests
                ]
                if self.economic_interests
                else []
            ),
        )
