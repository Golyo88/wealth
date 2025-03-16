# generated by datamodel-codegen:
#   filename:  wealth.schema.json
#   timestamp: 2025-03-15T21:49:47+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Role(Enum):
    országgyűlési_képviselő = "országgyűlési képviselő"
    házas__élettárs = "házas-/élettárs"
    gyermek = "gyermek"


class Person(BaseModel):
    name: str
    role: Role

    class Config:
        from_attributes = True


class RealEstateItem(BaseModel):
    location: str
    area_m2: int
    land_use: str
    building_type: Optional[str] = None
    building_size_m2: Optional[int] = None
    legal_status: Optional[str] = None
    ownership_status: str
    ownership_share: str
    acquisition_mode: str
    acquisition_date: str

    class Config:
        from_attributes = True


class MotorVehicleItem(BaseModel):
    type: str
    brand_model: str
    acquisition_year: int
    acquisition_mode: str

    class Config:
        from_attributes = True


class WatercraftOrAircraft(BaseModel):
    type: str
    brand_model: str
    acquisition_year: int
    acquisition_mode: str

    class Config:
        from_attributes = True


class Vehicles(BaseModel):
    motor_vehicle: Optional[List[MotorVehicleItem]] = Field(
        None, description="A) rész, II. Nagy értékű3 ingóságok, 1. Gépjárművek"
    )
    watercraft_or_aircraft: Optional[List[WatercraftOrAircraft]] = Field(
        None, description="A) rész, II. Nagy értékű3 ingóságok, 2. Vízi vagy légi jármű"
    )

    class Config:
        from_attributes = True


class Artwork(BaseModel):
    name: str
    quantity: int
    acquisition_year: Optional[int] = None
    acquisition_mode: Optional[str] = None

    class Config:
        from_attributes = True


class Collection(BaseModel):
    name: str
    quantity: int
    acquisition_year: int
    acquisition_mode: str

    class Config:
        from_attributes = True


class Artworks(BaseModel):
    artworks: Optional[List[Artwork]] = None
    collections: Optional[List[Collection]] = None

    class Config:
        from_attributes = True


class OtherAsset(BaseModel):
    name: str
    acquisition_year: Optional[int] = None
    acquisition_mode: Optional[str] = None

    class Config:
        from_attributes = True


class Security(BaseModel):
    type: str
    value_huf: int

    class Config:
        from_attributes = True


class SavingsDepositItem(BaseModel):
    value_huf: int
    exchange_rate: Optional[float] = None

    class Config:
        from_attributes = True


class Cash(BaseModel):
    value_huf: int
    exchange_rate: Optional[float] = None

    class Config:
        from_attributes = True


class BankDepositClaim(BaseModel):
    value_huf: int
    foreign_currency_value_in_huf: Optional[int] = None
    exchange_rate: Optional[float] = None

    class Config:
        from_attributes = True


class OtherClaim(BaseModel):
    value_huf: int
    exchange_rate: Optional[float] = None

    class Config:
        from_attributes = True


class Claims(BaseModel):
    bank_deposit_claims: Optional[List[BankDepositClaim]] = Field(
        None,
        description="A) rész, II. Nagy értékű ingóságok, 8. Hitelintézeti számlakövetelés vagy más, szerződés alapján fennálló pénzkövetelés, a)",
    )
    other_claims: Optional[List[OtherClaim]] = Field(
        None,
        description="A) rész, II. Nagy értékű ingóságok, 8. Hitelintézeti számlakövetelés vagy más, szerződés alapján fennálló pénzkövetelés, b)",
    )

    class Config:
        from_attributes = True


class OtherProperty(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Assets(BaseModel):
    real_estate: List[RealEstateItem] = Field(
        ...,
        description="A) rész, I. Ingatlanok (kivéve a nyilatkozatot adó, valamint a vele közös háztartásban élő 2 házastársa vagy élettársa és gyermeke(i) kizárólagos használatára fenntartott ingatlant)",
    )
    vehicles: Vehicles
    artworks: Artworks = Field(
        ...,
        description="A) rész, II. Nagy értékű ingóságok, 3. Védett műalkotás, védett gyűjtemény",
    )
    other_assets: List[OtherAsset] = Field(
        ..., description="A) rész, II. Nagy értékű ingóságok, 4. Egyéb ingóság"
    )
    securities: List[Security] = Field(
        ...,
        description="A) rész, II. Nagy értékű ingóságok, 5. Értékpapírban elhelyezett megtakarítás vagy egyéb befektetés (részvény, kötvény, részjegy, kincstárjegy, vagyonjegy, részesedés magántőkealapban, biztosítás stb.)",
    )
    savings_deposit: Optional[List[SavingsDepositItem]] = Field(
        None,
        description="A) rész, II. Nagy értékű ingóságok, 6. Takarékbetétben elhelyezett megtakarítás",
    )
    cash: List[Cash] = Field(
        ..., description="A) rész, II. Nagy értékű ingóságok, 7. Készpénz"
    )
    claims: Claims = Field(
        ...,
        description="A) rész, II. Nagy értékű ingóságok, 8. Hitelintézeti számlakövetelés vagy más, szerződés alapján fennálló pénzkövetelés",
    )
    other_properties: List[OtherProperty] = Field(
        ..., description="A) rész, II. Nagy értékű ingóságok, 9. Más vagyontárgy"
    )

    class Config:
        from_attributes = True


class PublicDebtItem(BaseModel):
    value_huf: int
    exchange_rate: Optional[float] = None

    class Config:
        from_attributes = True


class BankLoan(BaseModel):
    value_huf: int
    exchange_rate: Optional[float] = None

    class Config:
        from_attributes = True


class PrivateLoan(BaseModel):
    value_huf: int
    exchange_rate: Optional[float] = None

    class Config:
        from_attributes = True


class Liabilities(BaseModel):
    public_debt: List[PublicDebtItem] = Field(
        ..., description="A) rész, III. Tartozások, 1. Köztartozás"
    )
    bank_loans: List[BankLoan] = Field(
        ...,
        description="A) rész, III. Tartozások, 2. Hitelintézettel szembeni tartozás",
    )
    private_loans: List[PrivateLoan] = Field(
        ...,
        description="A) rész, III. Tartozások, 3. Magánszemélyekkel szembeni tartozás",
    )

    class Config:
        from_attributes = True


class IncomeCategory(Enum):
    díjazás_nélküli = "díjazás nélküli"
    field_1 = "1"
    field_2 = "2"
    field_3 = "3"
    field_4 = "4"
    field_5 = "5"


class PastRolesAndAffiliation(BaseModel):
    name: str
    role: Optional[str] = None
    income_category: IncomeCategory

    class Config:
        from_attributes = True


class IncomeCategory1(Enum):
    field_1 = "1"
    field_2 = "2"
    field_3 = "3"
    field_4 = "4"
    field_5 = "5"


class OngoingIncomeGeneratingActivity(BaseModel):
    name: str
    income_category: IncomeCategory1

    class Config:
        from_attributes = True


class HighValueOccasionalIncomeItem(BaseModel):
    name: str
    income_category: IncomeCategory1

    class Config:
        from_attributes = True


class Income(BaseModel):
    past_roles_and_affiliations: List[PastRolesAndAffiliation] = Field(
        ..., description="B) rész, JÖVEDELEMNYILATKOZAT, I."
    )
    ongoing_income_generating_activities: List[OngoingIncomeGeneratingActivity] = Field(
        ..., description="B) rész, JÖVEDELEMNYILATKOZAT, II."
    )
    high_value_occasional_income: List[HighValueOccasionalIncomeItem] = Field(
        ..., description="B) rész, JÖVEDELEMNYILATKOZAT, III."
    )

    class Config:
        from_attributes = True


class IncomeCategory3(Enum):
    díjazás_nélküli = "díjazás nélküli"
    field_1 = "1"
    field_2 = "2"
    field_3 = "3"
    field_4 = "4"
    field_5 = "5"


class OngoingCorporateAndTrustAffiliation(BaseModel):
    organization: str
    role: str
    income_category: IncomeCategory3

    class Config:
        from_attributes = True


class PoliticallyRelevantAndControllingBusinessInterest(BaseModel):
    organization: str
    role: str
    ownership_percentage: Optional[str] = None
    income_category: IncomeCategory3

    class Config:
        from_attributes = True


class EconomicInterests(BaseModel):
    ongoing_corporate_and_trust_affiliations: List[
        OngoingCorporateAndTrustAffiliation
    ] = Field(..., description="C) rész, GAZDASÁGI ÉRDEKELTSÉGI NYILATKOZAT, I.")
    politically_relevant_and_controlling_business_interests: List[
        PoliticallyRelevantAndControllingBusinessInterest
    ] = Field(..., description="C) rész, GAZDASÁGI ÉRDEKELTSÉGI NYILATKOZAT, II.")

    class Config:
        from_attributes = True


class Wealth(BaseModel):
    person: Person
    assets: Assets
    liabilities: Liabilities = Field(..., description="A) rész, III. Tartozások")
    income: Income = Field(..., description="B) rész, JÖVEDELEMNYILATKOZAT")
    economic_interests: EconomicInterests = Field(
        ..., description="C) rész, GAZDASÁGI ÉRDEKELTSÉGI NYILATKOZAT"
    )

    class Config:
        from_attributes = True
