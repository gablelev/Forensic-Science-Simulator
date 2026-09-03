import uuid
import random
import yaml
import os

with open("loci.yaml", "r") as file:
    loci_data = yaml.safe_load(file)
locus_names = loci_data["locus_names"]  

class person_profile:
    def __init__(self, dna_profile: dict[str, int | None] = {locus: None for locus in locus_names}, parents: list['person_profile'] = [], siblings: list['person_profile'] = [], children: list['person_profile'] = [], name = None, age = None, sex = None):
        self.dna_profile = dna_profile
        self.parents = parents
        self.siblings = siblings
        self.children = children
        self.name = name
        self.sex = "M" if self.dna_profile.get("Amelogenin") == ["X", "Y"] else "F" if self.dna_profile.get("Amelogenin") == ["X"] else None
        self.age = age
        self.uid = str(uuid.uuid4())

    def edit_locus(self, locus: str, alleles: list[int]):
        with open("loci.yaml", "r") as file:
            loci_data = yaml.safe_load(file)
        locus_info = loci_data["loci"][locus]
        #print(locus_info)
        print(locus_info["alleles"].keys())
        if locus in self.dna_profile:
            sorted_alleles = sorted(alleles, key=float)
            allele1, allele2 = (str(allele) for allele in sorted_alleles)
            print(allele1, allele2)
            if locus == "Amelogenin":
                if set(alleles) != {"X", "Y"} and set(alleles) != {"X", "X"}:
                    raise ValueError("Invalid alleles for Amelogenin locus. Must be ['X', 'Y'] or ['X', 'X'].")
            #organize alleles in descending order for consistency
            if allele1 not in locus_info["alleles"].keys():
                raise ValueError(f"One or both alleles {alleles} are not valid for locus '{locus}'.")
            self.dna_profile[locus] = [allele1, allele2]
        else:
            #this should not happen
            raise ValueError(f"MAJOR PROFILE ERROR: Locus '{locus}' not found in the profile.")

    def add_siblings(self, siblings: list['person_profile']):
        self.siblings.extend(siblings)

    def add_children(self, children: list['person_profile']):
        self.children.extend(children)

    def set_parents(self, parents: list['person_profile']):
        self.parents = parents

    def set_name(self, name: str):
        self.name = name

    def set_age(self, age: int):
        if age < 0:
            raise ValueError("Age cannot be negative.")
        self.age = age

    def set_sex(self, sex: str):
        if self.dna_profile.get("Amelogenin") is not None:
            self.sex = sex
        else:
            raise ValueError("Cannot set sex based on Amelogenin locus. Please ensure the Amelogenin locus is present in the DNA profile.")

    def set_dna_profile(self, dna_profile: dict[str, int | None]):
        self.dna_profile = dna_profile
        if "Amelogenin" in dna_profile:
            self.sex = "M" if dna_profile["Amelogenin"] == ["X", "Y"] else "F" if dna_profile["Amelogenin"] == ["X", "X"] else None

    def upload(self):
        if os.path.exists("database.yaml"):
            with open("database.yaml", "r") as file:
                existing_data = yaml.safe_load(file) or {}
        else:
            existing_data = {}

        if "profiles" not in existing_data:
            existing_data['profiles'] = {}

        data = {
            "dna_profile": self.dna_profile,
            "name": self.name,
            "age": self.age,
            "sex": self.sex,
            "parents": [parent.uid for parent in self.parents],
            "siblings": [sibling.uid for sibling in self.siblings],
            "children": [child.uid for child in self.children]
        }

        existing_data['profiles'][self.uid] = data

        with open("database.yaml", "w") as file:
            yaml.safe_dump(existing_data, file)

    def print_profile(self):
        for locus, alleles in self.dna_profile.items():
            print(f"{locus}: {alleles}")
