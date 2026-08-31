import uuid
import random
import yaml
import os

with open("loci.yaml", "r") as file:
    loci_data = yaml.safe_load(file)
locus_names = loci_data["locus_names"]  

class person_profile:
    def __init__(self,dna_profile: dict[str, int | None] = {locus: None for locus in locus_names}, parents: list['person_profile'] = [], siblings: list['person_profile'] = [], children: list['person_profile'] = [], name = None, age = None, sex = None):
        self.dna_profile = dna_profile
        self.parents = parents
        self.siblings = siblings
        self.children = children
        self.name = name
        self.sex = sex if sex is not None else self.dna_profile.get("Amelogenin")
        self.age = age
        self.uid = str(uuid.uuid4())

    #for testing purposes, generates a random profile with random alleles for each locus
    #does not include possibility of microvarient alleles for sake of simplicity
    def random_profile(self):
        dna_profile = {locus: None for locus in locus_names}
        for locus in locus_names:
            if locus == "Amelogenin":
                dna_profile[locus] = ["X", random.choice(["X", "Y"])]
            else:
                with open("loci.yaml", "r") as file:
                    loci_data = yaml.safe_load(file)
                min_val = loci_data["loci"][locus]["min"]
                max_val = loci_data["loci"][locus]["max"]
                dna_profile[locus] = [f"{random.uniform(min_val, max_val):.0f}", f"{random.uniform(min_val, max_val):.0f}"]
        self.dna_profile = dna_profile

    def edit_locus(self, locus: str, alleles: list[str]):
        if locus in self.dna_profile:
            self.dna_profile[locus] = alleles
        else:
            raise ValueError(f"Locus '{locus}' not found in the profile.")

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
