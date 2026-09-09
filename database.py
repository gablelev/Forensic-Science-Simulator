import os
import yaml
from profile import person_profile, dna_profile

#return a person_profile from the database from their uuid
def get_person_profile_from_database(uuid: str) -> 'person_profile':
    if os.path.exists("database.yaml"):
        with open("database.yaml", "r") as f:
            database = yaml.safe_load(f)
        if uuid in database["profiles"]:
            person_data = database["profiles"][uuid]
            dna = dna_profile(person_data["dna_profile"])
            parents = person_data.get("parents", [])
            siblings = person_data.get("siblings", [])
            children = person_data.get("children", [])
            return person_profile(
                uid=uuid,
                dna_profile=dna,
                name=person_data["name"],
                age=person_data["age"],
                sex=person_data["sex"],
                parents=parents,
                siblings=siblings,
                children=children
            )

def upload(person: 'person_profile'):
    if os.path.exists("database.yaml"):
        with open("database.yaml", "r") as file:
            existing_data = yaml.safe_load(file) or {}
    else:
        existing_data = {}

    if "profiles" not in existing_data:
        existing_data['profiles'] = {}

    data = {
        "dna_profile": person.dna_profile.profile,
        "name": person.name,
        "age": person.age,
        "sex": person.sex,
        "parents": person.parents,
        "siblings": person.siblings,
        "children": person.children
    }

    existing_data['profiles'][person.uid] = data

    try:
        with open("database.yaml", "w") as file:
            yaml.safe_dump(existing_data, file)
            print(f"Successfully uploaded {person.name} to database.yaml.")
    except Exception as e:
        print(f"Error writing to database.yaml: {e}")