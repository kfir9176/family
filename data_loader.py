import csv
from models import Person

def load_people(path="people.csv"):
    people = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = Person(
                id=row["id"],
                name=row["name"],
                family=row["family"],
                birthday=row["birthday"],
                phone=row["phone"],
                address=row["address"],
                family_id=row["family_id"] or None
            )
    return people


def load_families(path="families.csv"):
    families = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            families[row["family_id"]] = {
                "title": row["title"],
                "parents": row["parents"].split(";") if row["parents"] else [],
                "children": row["children"].split(";") if row["children"] else []
            }
    return families
