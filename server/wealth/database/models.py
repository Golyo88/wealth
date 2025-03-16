from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from wealth.model import (
    IncomeCategory1,
    IncomeCategory3,
    Role,
    IncomeCategory,
    Person as PersonModel,
)


Base = declarative_base()


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)

    real_estates = relationship("RealEstate", back_populates="person")
    motor_vehicles = relationship("MotorVehicle", back_populates="person")
    watercraft_or_aircraft = relationship(
        "WatercraftOrAircraft", back_populates="person"
    )
    artworks = relationship("Artwork", back_populates="person")
    collections = relationship("Collection", back_populates="person")
    other_assets = relationship("OtherAsset", back_populates="person")
    securities = relationship("Security", back_populates="person")
    cash = relationship("Cash", back_populates="person")
    savings_deposits = relationship("SavingsDeposit", back_populates="person")
    bank_deposit_claims = relationship("BankDepositClaim", back_populates="person")
    other_claims = relationship("OtherClaim", back_populates="person")
    other_properties = relationship("OtherProperty", back_populates="person")
    public_debts = relationship("PublicDebt", back_populates="person")
    bank_loans = relationship("BankLoan", back_populates="person")
    private_loans = relationship("PrivateLoan", back_populates="person")
    past_roles_and_affiliations = relationship(
        "PastRolesAndAffiliation", back_populates="person"
    )
    ongoing_income_generating_activities = relationship(
        "OngoingIncomeGeneratingActivity", back_populates="person"
    )
    high_value_occasional_income_items = relationship(
        "HighValueOccasionalIncomeItem", back_populates="person"
    )
    ongoing_corporate_and_trust_affiliations = relationship(
        "OngoingCorporateAndTrustAffiliation", back_populates="person"
    )
    politically_relevant_and_controlling_business_interests = relationship(
        "PoliticallyRelevantAndControllingBusinessInterest",
        back_populates="person",
    )


class RealEstate(Base):
    __tablename__ = "real_estates"

    id = Column(Integer, primary_key=True)
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

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="real_estates")


class MotorVehicle(Base):
    __tablename__ = "motor_vehicles"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    brand_model = Column(String, nullable=False)
    acquisition_year = Column(Integer, nullable=False)
    acquisition_mode = Column(String, nullable=False)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="motor_vehicles")


class WatercraftOrAircraft(Base):
    __tablename__ = "watercraft_or_aircraft"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    brand_model = Column(String, nullable=False)
    acquisition_year = Column(Integer, nullable=False)
    acquisition_mode = Column(String, nullable=False)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="watercraft_or_aircraft")


class Artwork(Base):
    __tablename__ = "artworks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    acquisition_year = Column(Integer)
    acquisition_mode = Column(String)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="artworks")


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    acquisition_year = Column(Integer, nullable=False)
    acquisition_mode = Column(String, nullable=False)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="collections")


class OtherAsset(Base):
    __tablename__ = "other_assets"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    acquisition_year = Column(Integer)
    acquisition_mode = Column(String)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="other_assets")


class Security(Base):
    __tablename__ = "securities"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    value_huf = Column(Integer, nullable=False)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="securities")


class SavingsDeposit(Base):
    __tablename__ = "savings_deposits"

    id = Column(Integer, primary_key=True)
    value_huf = Column(Integer, nullable=False)
    exchange_rate = Column(Float)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="savings_deposits")


class Cash(Base):
    __tablename__ = "cash"

    id = Column(Integer, primary_key=True)
    value_huf = Column(Integer, nullable=False)
    exchange_rate = Column(Float)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="cash")


class BankDepositClaim(Base):
    __tablename__ = "bank_deposit_claims"

    id = Column(Integer, primary_key=True)
    value_huf = Column(Integer, nullable=False)
    foreign_currency_value_in_huf = Column(Integer)
    exchange_rate = Column(Float)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="bank_deposit_claims")


class OtherClaim(Base):
    __tablename__ = "other_claims"

    id = Column(Integer, primary_key=True)
    value_huf = Column(Integer, nullable=False)
    exchange_rate = Column(Float)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="other_claims")


class OtherProperty(Base):
    __tablename__ = "other_properties"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="other_properties")


class PublicDebt(Base):
    __tablename__ = "public_debts"

    id = Column(Integer, primary_key=True)
    value_huf = Column(Integer, nullable=False)
    exchange_rate = Column(Float)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="public_debts")


class BankLoan(Base):
    __tablename__ = "bank_loans"

    id = Column(Integer, primary_key=True)
    value_huf = Column(Integer, nullable=False)
    exchange_rate = Column(Float)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="bank_loans")


class PrivateLoan(Base):
    __tablename__ = "private_loans"

    id = Column(Integer, primary_key=True)
    value_huf = Column(Integer, nullable=False)
    exchange_rate = Column(Float)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="private_loans")


class PastRolesAndAffiliation(Base):
    __tablename__ = "past_roles_and_affiliations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String)
    income_category = Column(Enum(IncomeCategory), nullable=False)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="past_roles_and_affiliations")


class OngoingIncomeGeneratingActivity(Base):
    __tablename__ = "ongoing_income_generating_activities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    income_category = Column(Enum(IncomeCategory1), nullable=False)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship(
        "Person", back_populates="ongoing_income_generating_activities"
    )


class HighValueOccasionalIncomeItem(Base):
    __tablename__ = "high_value_occasional_income_items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    income_category = Column(Enum(IncomeCategory1), nullable=False)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship("Person", back_populates="high_value_occasional_income_items")


class OngoingCorporateAndTrustAffiliation(Base):
    __tablename__ = "ongoing_corporate_and_trust_affiliations"

    id = Column(Integer, primary_key=True)
    organization = Column(String, nullable=False)
    role = Column(String, nullable=False)
    income_category = Column(Enum(IncomeCategory3), nullable=False)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship(
        "Person", back_populates="ongoing_corporate_and_trust_affiliations"
    )


class PoliticallyRelevantAndControllingBusinessInterest(Base):
    __tablename__ = "politically_relevant_and_controlling_business_interests"

    id = Column(Integer, primary_key=True)
    organization = Column(String, nullable=False)
    role = Column(String, nullable=False)
    ownership_percentage = Column(String)
    income_category = Column(Enum(IncomeCategory3), nullable=False)

    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person = relationship(
        "Person",
        back_populates="politically_relevant_and_controlling_business_interests",
    )
