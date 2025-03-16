from wealth.database.models import Person
from wealth.model import (
    Artwork,
    Artworks,
    BankDepositClaim,
    BankLoan,
    Cash,
    Claims,
    Collection,
    HighValueOccasionalIncomeItem,
    MotorVehicleItem,
    OngoingCorporateAndTrustAffiliation,
    OngoingIncomeGeneratingActivity,
    OtherAsset,
    OtherClaim,
    OtherProperty,
    PastRolesAndAffiliation,
    PoliticallyRelevantAndControllingBusinessInterest,
    PrivateLoan,
    PublicDebtItem,
    RealEstateItem,
    SavingsDepositItem,
    Security,
    Vehicles,
    WatercraftOrAircraft,
    Wealth,
    Person as PersonModel,
    Assets,
    Liabilities,
    Income,
    EconomicInterests,
)


class PersonView(PersonModel):
    id: int

    class Config:
        from_attributes = True


class WealthView(Wealth):
    person: PersonView

    total_real_estate_count: int
    total_vehicle_count: int
    total_artwork_count: int
    total_security_count: int
    total_income_count: int
    total_savings: int
    total_liabilities: int
    net_worth: int

    class Config:
        from_attributes = True

    @classmethod
    def from_person(cls, person: Person):

        total_real_estate_count = len(person.real_estates)
        total_vehicle_count = len(person.motor_vehicles) + len(
            person.watercraft_or_aircraft
        )
        total_artwork_count = len(person.artworks) + len(person.collections)
        total_security_count = len(person.securities)
        total_income_count = (
            len(person.past_roles_and_affiliations)
            + len(person.ongoing_income_generating_activities)
            + len(person.high_value_occasional_income_items)
        )

        total_savings = (
            sum(cash.value_huf for cash in person.cash)
            + sum(
                savings_deposit.value_huf for savings_deposit in person.savings_deposits
            )
            + sum(security.value_huf for security in person.securities)
            + sum(
                (
                    bank_deposit_claim.value_huf
                    if bank_deposit_claim.value_huf is not None
                    else bank_deposit_claim.foreign_currency_value_in_huf
                )
                for bank_deposit_claim in person.bank_deposit_claims
            )
            + sum((other_claim.value_huf) for other_claim in person.other_claims)
        )

        total_liabilities = (
            sum(bank_loan.value_huf for bank_loan in person.bank_loans)
            + sum(private_loan.value_huf for private_loan in person.private_loans)
            + sum(public_debt.value_huf for public_debt in person.public_debts)
        )

        net_worth = total_savings - total_liabilities

        return cls(
            total_real_estate_count=total_real_estate_count,
            total_vehicle_count=total_vehicle_count,
            total_artwork_count=total_artwork_count,
            total_security_count=total_security_count,
            total_income_count=total_income_count,
            total_savings=total_savings,
            total_liabilities=total_liabilities,
            net_worth=net_worth,
            person=PersonView(
                id=person.id,
                name=person.name,
                role=person.role,
            ),
            assets=Assets(
                real_estate=[
                    RealEstateItem.model_validate(real_estate)
                    for real_estate in person.real_estates
                ],
                vehicles=Vehicles(
                    motor_vehicle=[
                        MotorVehicleItem.model_validate(motor_vehicle)
                        for motor_vehicle in person.motor_vehicles
                    ],
                    watercraft_or_aircraft=[
                        WatercraftOrAircraft.model_validate(watercraft_or_aircraft)
                        for watercraft_or_aircraft in person.watercraft_or_aircraft
                    ],
                ),
                artworks=Artworks(
                    artworks=[
                        Artwork.model_validate(artwork) for artwork in person.artworks
                    ],
                    collections=[
                        Collection.model_validate(collection)
                        for collection in person.collections
                    ],
                ),
                other_assets=[
                    OtherAsset.model_validate(other_asset)
                    for other_asset in person.other_assets
                ],
                securities=[
                    Security.model_validate(security) for security in person.securities
                ],
                savings_deposit=[
                    SavingsDepositItem.model_validate(savings_deposit)
                    for savings_deposit in person.savings_deposits
                ],
                cash=[Cash.model_validate(cash) for cash in person.cash],
                claims=Claims(
                    bank_deposit_claims=[
                        BankDepositClaim.model_validate(bank_deposit_claim)
                        for bank_deposit_claim in person.bank_deposit_claims
                    ],
                    other_claims=[
                        OtherClaim.model_validate(other_claim)
                        for other_claim in person.other_claims
                    ],
                ),
                other_properties=[
                    OtherProperty.model_validate(other_property)
                    for other_property in person.other_properties
                ],
            ),
            liabilities=Liabilities(
                public_debt=[
                    PublicDebtItem.model_validate(public_debt)
                    for public_debt in person.public_debts
                ],
                bank_loans=[
                    BankLoan.model_validate(bank_loan)
                    for bank_loan in person.bank_loans
                ],
                private_loans=[
                    PrivateLoan.model_validate(private_loan)
                    for private_loan in person.private_loans
                ],
            ),
            income=Income(
                past_roles_and_affiliations=[
                    PastRolesAndAffiliation.model_validate(past_role_and_affiliation)
                    for past_role_and_affiliation in person.past_roles_and_affiliations
                ],
                ongoing_income_generating_activities=[
                    OngoingIncomeGeneratingActivity.model_validate(
                        ongoing_income_generating_activity
                    )
                    for ongoing_income_generating_activity in person.ongoing_income_generating_activities
                ],
                high_value_occasional_income=[
                    HighValueOccasionalIncomeItem.model_validate(
                        high_value_occasional_income
                    )
                    for high_value_occasional_income in person.high_value_occasional_income_items
                ],
            ),
            economic_interests=EconomicInterests(
                ongoing_corporate_and_trust_affiliations=[
                    OngoingCorporateAndTrustAffiliation.model_validate(
                        ongoing_corporate_and_trust_affiliation
                    )
                    for ongoing_corporate_and_trust_affiliation in person.ongoing_corporate_and_trust_affiliations
                ],
                politically_relevant_and_controlling_business_interests=[
                    PoliticallyRelevantAndControllingBusinessInterest.model_validate(
                        politically_relevant_and_controlling_business_interest
                    )
                    for politically_relevant_and_controlling_business_interest in person.politically_relevant_and_controlling_business_interests
                ],
            ),
        )
