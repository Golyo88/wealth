from wealth.database.database import engine, SessionLocal
from wealth.database.models import (
    Base,
    Person,
    Security,
    Vehicle,
    Wealth,
    RealEstate,
    Savings,
    Liability,
    IncomeItem,
    EconomicInterest,
)
from pathlib import Path
from wealth.model import Wealth as WealthModel


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
                    # Person létrehozása
                    person = Person(name=data.person.name, role=data.person.role)
                    db.add(person)
                    db.flush()

                    # Wealth létrehozása
                    wealth = Wealth(person_id=person.id)
                    db.add(wealth)
                    db.flush()

                    # Real Estates
                    if data.assets.real_estate:
                        for re in data.assets.real_estate:
                            real_estate = RealEstate(
                                wealth_id=wealth.id, **re.model_dump()
                            )
                            db.add(real_estate)

                    # Savings
                    if data.assets.savings:
                        savings = Savings(
                            wealth_id=wealth.id, **data.assets.savings.model_dump()
                        )
                        db.add(savings)

                    # Liabilities - módosított rész
                    if data.liabilities:
                        liability = Liability(
                            wealth_id=wealth.id,
                            public_debt_huf=data.liabilities.public_debt_huf,
                            bank_loans_huf=data.liabilities.bank_loans_huf,
                            private_loans_huf=data.liabilities.private_loans_huf,
                        )
                        db.add(liability)

                    # Income Items
                    if data.income:
                        for income in data.income:
                            income_db = IncomeItem(
                                wealth_id=wealth.id,
                                position_name=income.position,
                                income_category=income.income_category,
                            )
                        db.add(income_db)

                    # Economic Interests
                    if data.economic_interests:
                        for interest in data.economic_interests:
                            interest_db = EconomicInterest(
                                wealth_id=wealth.id, **interest.model_dump()
                            )
                        db.add(interest_db)

                    if data.assets.vehicles:
                        for vehicle in data.assets.vehicles:
                            vehicle_db = Vehicle(
                                wealth_id=wealth.id, **vehicle.model_dump()
                            )
                            db.add(vehicle_db)

                    if data.assets.securities:
                        for security in data.assets.securities:
                            security_db = Security(
                                wealth_id=wealth.id, **security.model_dump()
                            )
                            db.add(security_db)

                    db.commit()
                except Exception as e:

                    print(f"Error processing {json_file}: {str(e)}")
                    db.rollback()
                finally:
                    db.close()


if __name__ == "__main__":
    init_db()
