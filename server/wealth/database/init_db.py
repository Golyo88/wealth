from wealth.database.database import engine, SessionLocal
from wealth.database.models import (
    Base,
    MotorVehicle,
    Person,
    Security,
    WatercraftOrAircraft,
    RealEstate,
    Cash,
    SavingsDeposit,
    Artwork,
    Collection,
    OtherAsset,
    BankDepositClaim,
    OtherClaim,
    OtherProperty,
    PublicDebt,
    BankLoan,
    PrivateLoan,
    PastRolesAndAffiliation,
    OngoingIncomeGeneratingActivity,
    HighValueOccasionalIncomeItem,
    OngoingCorporateAndTrustAffiliation,
    PoliticallyRelevantAndControllingBusinessInterest,
)
from pathlib import Path
from wealth.model import (
    Wealth as WealthModel,
)


def init_db():
    Base.metadata.create_all(bind=engine)

    output_dir = Path("output")
    for json_file in output_dir.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip():
                data = WealthModel.model_validate_json(content)
                db = SessionLocal()

                try:
                    person = Person(name=data.person.name, role=data.person.role)
                    db.add(person)
                    db.flush()

                    if data.assets.real_estate:
                        for re in data.assets.real_estate:
                            real_estate = RealEstate(
                                **re.model_dump(), person_id=person.id
                            )
                            db.add(real_estate)

                    if data.assets.vehicles.motor_vehicle:
                        for vehicle in data.assets.vehicles.motor_vehicle:
                            vehicle_db = MotorVehicle(
                                **vehicle.model_dump(), person_id=person.id
                            )
                            db.add(vehicle_db)

                    if data.assets.vehicles.watercraft_or_aircraft:
                        for vehicle in data.assets.vehicles.watercraft_or_aircraft:
                            vehicle_db = WatercraftOrAircraft(
                                **vehicle.model_dump(), person_id=person.id
                            )
                            db.add(vehicle_db)

                    if data.assets.artworks.artworks:
                        for artwork in data.assets.artworks.artworks:
                            artwork_db = Artwork(
                                **artwork.model_dump(), person_id=person.id
                            )
                            db.add(artwork_db)

                    if data.assets.artworks.collections:
                        for collection in data.assets.artworks.collections:
                            collection_db = Collection(
                                **collection.model_dump(), person_id=person.id
                            )
                            db.add(collection_db)

                    if data.assets.other_assets:
                        for other_asset in data.assets.other_assets:
                            other_asset_db = OtherAsset(
                                **other_asset.model_dump(), person_id=person.id
                            )
                            db.add(other_asset_db)

                    if data.assets.securities:
                        for security in data.assets.securities:
                            security_db = Security(
                                **security.model_dump(), person_id=person.id
                            )
                            db.add(security_db)

                    if data.assets.savings_deposit:
                        for savings_deposit in data.assets.savings_deposit:
                            savings_deposit_db = SavingsDeposit(
                                **savings_deposit.model_dump(), person_id=person.id
                            )
                            db.add(savings_deposit_db)

                    if data.assets.cash:
                        for cash in data.assets.cash:
                            cash_db = Cash(**cash.model_dump(), person_id=person.id)
                            db.add(cash_db)

                    if data.assets.claims.bank_deposit_claims:
                        for (
                            bank_deposit_claim
                        ) in data.assets.claims.bank_deposit_claims:
                            bank_deposit_claim_db = BankDepositClaim(
                                **bank_deposit_claim.model_dump(), person_id=person.id
                            )
                            db.add(bank_deposit_claim_db)

                    if data.assets.claims.other_claims:
                        for other_claim in data.assets.claims.other_claims:
                            other_claim_db = OtherClaim(
                                **other_claim.model_dump(), person_id=person.id
                            )
                            db.add(other_claim_db)

                    if data.assets.other_properties:
                        for other_property in data.assets.other_properties:
                            other_property_db = OtherProperty(
                                **other_property.model_dump(), person_id=person.id
                            )
                            db.add(other_property_db)

                    if data.liabilities.public_debt:
                        for public_debt in data.liabilities.public_debt:
                            public_debt_db = PublicDebt(
                                **public_debt.model_dump(), person_id=person.id
                            )
                            db.add(public_debt_db)

                    if data.liabilities.bank_loans:
                        for bank_loan in data.liabilities.bank_loans:
                            bank_loan_db = BankLoan(
                                **bank_loan.model_dump(), person_id=person.id
                            )
                            db.add(bank_loan_db)

                    if data.liabilities.private_loans:
                        for private_loan in data.liabilities.private_loans:
                            private_loan_db = PrivateLoan(
                                **private_loan.model_dump(), person_id=person.id
                            )
                            db.add(private_loan_db)

                    if data.income.past_roles_and_affiliations:
                        for (
                            past_role_and_affiliation
                        ) in data.income.past_roles_and_affiliations:
                            past_role_and_affiliation_db = PastRolesAndAffiliation(
                                **past_role_and_affiliation.model_dump(),
                                person_id=person.id,
                            )
                            db.add(past_role_and_affiliation_db)

                    if data.income.ongoing_income_generating_activities:
                        for (
                            ongoing_income_generating_activity
                        ) in data.income.ongoing_income_generating_activities:
                            ongoing_income_generating_activity_db = (
                                OngoingIncomeGeneratingActivity(
                                    **ongoing_income_generating_activity.model_dump(),
                                    person_id=person.id,
                                )
                            )
                            db.add(ongoing_income_generating_activity_db)

                    if data.income.high_value_occasional_income:
                        for (
                            high_value_occasional_income
                        ) in data.income.high_value_occasional_income:
                            high_value_occasional_income_db = (
                                HighValueOccasionalIncomeItem(
                                    **high_value_occasional_income.model_dump(),
                                    person_id=person.id,
                                )
                            )
                            db.add(high_value_occasional_income_db)

                    if data.economic_interests.ongoing_corporate_and_trust_affiliations:
                        for (
                            ongoing_corporate_and_trust_affiliation
                        ) in (
                            data.economic_interests.ongoing_corporate_and_trust_affiliations
                        ):
                            ongoing_corporate_and_trust_affiliation_db = OngoingCorporateAndTrustAffiliation(
                                **ongoing_corporate_and_trust_affiliation.model_dump(),
                                person_id=person.id,
                            )
                            db.add(ongoing_corporate_and_trust_affiliation_db)

                    if (
                        data.economic_interests.politically_relevant_and_controlling_business_interests
                    ):
                        for (
                            politically_relevant_and_controlling_business_interest
                        ) in (
                            data.economic_interests.politically_relevant_and_controlling_business_interests
                        ):
                            politically_relevant_and_controlling_business_interest_db = PoliticallyRelevantAndControllingBusinessInterest(
                                **politically_relevant_and_controlling_business_interest.model_dump(),
                                person_id=person.id,
                            )
                            db.add(
                                politically_relevant_and_controlling_business_interest_db
                            )

                    db.commit()
                except Exception as e:
                    print(f"Error processing {json_file}: {str(e)}")
                    db.rollback()
                finally:
                    db.close()


if __name__ == "__main__":
    init_db()
