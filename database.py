import os
import yaml
from profile import person_profile, dna_profile, case_profile, evidence

#return a person_profile from the database from their uuid
#function built with intention to be used in the future for a GUI to search for profiles by uuid
def get_profile_from_database_uuid(uuid: str) -> 'person_profile':
    if not is_valid_uuid(uuid):
        raise ValueError("Invalid UUID")

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

#return a list of person_profiles from the database that match/include a given name
#function built with intention to be used in the future for a GUI to search for profiles by name
def get_profile_from_database_name(name: str) -> list['person_profile']:
    profiles = []
    if os.path.exists("database.yaml"):
        with open("database.yaml", "r") as f:
            database = yaml.safe_load(f)

    for uuid, person_data in database["profiles"].items():
        if person_data["name"].lower() == name.lower() or person_data["name"].lower() == name.lower().replace(" ", ""):
            dna = dna_profile(person_data["dna_profile"])
            parents = person_data.get("parents", [])
            siblings = person_data.get("siblings", [])
            children = person_data.get("children", [])
            profiles.append(person_profile(
                uid=uuid,
                dna_profile=dna,
                name=person_data["name"],
                age=person_data["age"],
                sex=person_data["sex"],
                parents=parents,
                siblings=siblings,
                children=children
            ))
    return profiles

#uploads data to database - can accept person profiles, case profiles, or evidence as argument
def upload(profile: person_profile or case_profile or evidence):
    if os.path.exists("database.yaml"):
        with open("database.yaml", "r") as file:
            existing_data = yaml.safe_load(file) or {}
    else:
        existing_data = {}

    #instantiate profiles, cases, and evidence if not present in existing data
    if "profiles" not in existing_data:
        existing_data['profiles'] = {}
    if "cases" not in existing_data:
        existing_data['cases'] = {}
    if "evidence" not in existing_data:
        existing_data['evidence'] = {}

    #format data for cases section of database
    if isinstance(profile, case_profile):
        pass

    #format data for evidence section of database
    elif isinstance(profile, evidence):
        pass

    #format data for person profile section of database
    elif isinstance(profile, person_profile):
        data = {
            "dna_profile": profile.dna_profile.dna,
            "dna_source": profile.dna_profile.source,
            "name": profile.name,
            "age": profile.age,
            "sex": profile.sex,
            "parents": profile.parents,
            "siblings": profile.siblings,
            "children": profile.children
        }

        existing_data['profiles'][profile.uid] = data

    #finalize writing data to database
    try:
        with open("database.yaml", "w") as file:
            yaml.safe_dump(existing_data, file, sort_keys=False)
            print(f"Successfully uploaded {profile.name} to database.yaml.")
    except Exception as e:
        print(f"Error writing to database.yaml: {e}")