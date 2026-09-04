import uuid
import random
import yaml
import os

with open("loci.yaml", "r") as file:
    loci_data = yaml.safe_load(file)
locus_names = loci_data["locus_names"]  

class dna_profile:
    #creates an empty profile with all loci set to None by default or initializes with a provided profile dictionary
    def __init__(self, profile: dict[str, int | None] = {locus: None for locus in locus_names}):
        self.profile = profile

    def set_profile(self, profile: dict[str, int | None]):
        self.profile = profile

    #returns the alleles for a given locus, or [None, None] if the locus is not present in the profile
    def get_locus_data(self, locus: str) -> list[int | None]:
        return self.profile.get(locus, [None, None])

    def set_locus(self, locus: str, alleles: list[int | float | str]):
        if locus == "Amelogenin":
            raise ValueError("Cannot edit Amelogenin locus using edit_locus method. Use edit_gender method instead.")
        with open("loci.yaml", "r") as file:
            loci_data = yaml.safe_load(file)
        locus_info = loci_data["loci"][locus]
        if locus in self.profile:
            sorted_alleles = sorted(alleles, key=float)
            allele1, allele2 = (str(allele) for allele in sorted_alleles)
            #organize alleles in descending order for consistency
            if allele1 not in locus_info["alleles"].keys():
                raise ValueError(f"One or both alleles {alleles} are not valid for locus '{locus}'.")
            self.profile[locus] = [allele1, allele2]
        else:
            #this should not happen
            raise ValueError(f"MAJOR PROFILE ERROR: Locus '{locus}' not found in the profile.")

    def set_gender(self, chromosomes: list[str]):
        if set(chromosomes) != {"X", "Y"} and set(chromosomes) != {"X", "X"}:
            raise ValueError("Invalid chromosomes for Amelogenin locus. Must be ['X', 'Y'] or ['X', 'X'].")
        self.profile["Amelogenin"] = chromosomes

class person_profile:
    def __init__(self, dna_profile: dna_profile = dna_profile(), parents: list['person_profile'] = [], siblings: list['person_profile'] = [], children: list['person_profile'] = [], name = None, age = None, sex = None):
        self.dna_profile = dna_profile
        self.parents = parents
        self.siblings = siblings
        self.children = children
        self.name = name
        self.sex = "M" if self.dna_profile.get_locus_data("Amelogenin") == ["X", "Y"] else "F" if self.dna_profile.get_locus_data("Amelogenin") == ["X", "X"] else None
        self.age = age
        self.uid = str(uuid.uuid4())

    #def set_gender(self, chromosomes: list[str]):
    #    if set(chromosomes) != {"X", "Y"} and set(chromosomes) != {"X", "X"}:
    #        raise ValueError("Invalid chromosomes for Amelogenin locus. Must be ['X', 'Y'] or ['X', 'X'].")
    #    self.dna_profile["Amelogenin"] = chromosomes
    #    self.sex = "M" if chromosomes == ["X", "Y"] else "F" if chromosomes == ["X", "X"] else None

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

    #def set_sex(self, sex: str):
    #    if self.dna_profile.get("Amelogenin") is not None:
    #        if self.dna_profile.get("Amelogenin") == ["X", "Y"] and sex != "M":
    #            raise ValueError("Sex does not match Amelogenin locus. Expected 'M' for ['X', 'Y'].")
    #        elif self.dna_profile.get("Amelogenin") == ["X", "X"] and sex != "F":
    #            raise ValueError("Sex does not match Amelogenin locus. Expected 'F' for ['X', 'X'].")
    #        self.sex = sex
    #    else:
    #        raise ValueError("Cannot set sex based on Amelogenin locus. Please ensure the Amelogenin locus is present in the DNA profile.")

    def set_dna_profile(self, dna_profile: dict[str, int | None]):
        self.dna_profile = dna_profile
        if dna_profile.get_locus_data("Amelogenin") is not None:
            self.sex = "M" if dna_profile.get_locus_data("Amelogenin") == ["X", "Y"] else "F" if dna_profile.get_locus_data("Amelogenin") == ["X", "X"] else None

    def get_dna_profile(self) -> dict[str, int | None]:
        return self.dna_profile

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

    def print_dna_profile(self):
        for locus, alleles in self.dna_profile.items():
            print(f"{locus}: {alleles}")

    def print_full_profile(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Sex: {self.sex}")
        print(f"Parents: {[parent.uid for parent in self.parents]}")
        print(f"Siblings: {[sibling.uid for sibling in self.siblings]}")
        print(f"Children: {[child.uid for child in self.children]}")
        print("DNA Profile:")
        for locus, alleles in self.dna_profile.profile.items():
            print(f"    {locus}: {alleles}")
