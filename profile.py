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

    #updates gender of the dna profile, not the person profile
    def set_gender(self, chromosomes: list[str]):
        if set(chromosomes) != {"X", "Y"} and set(chromosomes) != {"X", "X"}:
            raise ValueError("Invalid chromosomes for Amelogenin locus. Must be ['X', 'Y'] or ['X', 'X'].")
        self.profile["Amelogenin"] = chromosomes

class person_profile:
    def __init__(self, dna_profile: dna_profile = dna_profile(), parents: list['person_profile'] = None, siblings: list['person_profile'] = None, children: list['person_profile'] = None, name = None, age = None, sex = None, uid = None):
        self.dna_profile = dna_profile
        self.parents = parents if parents is not None else []
        self.siblings = siblings if siblings is not None else []
        self.children = children if children is not None else []
        self.name = name
        self.sex = "M" if self.dna_profile.get_locus_data("Amelogenin") == ["X", "Y"] else "F" if self.dna_profile.get_locus_data("Amelogenin") == ["X", "X"] else None
        self.age = age
        self.uid = uid if uid is not None else str(uuid.uuid4())

    def add_siblings(self, siblings: 'person_profile | list[person_profile]'):
        if isinstance(siblings, person_profile):
            siblings = [siblings]
        #add the current person's uid to each sibling's siblings list and add each sibling's uid to the current person's siblings list
        for sibling in siblings:
            #prevent duplicate entries in the siblings list
            if self.uid not in sibling.siblings:
                sibling.siblings.append(self.uid)
        self.siblings.extend(sibling.uid for sibling in siblings)

    def add_children(self, children: 'person_profile | list[person_profile]'):
        if isinstance(children, person_profile):
            children = [children]
        #add the current person's uid to each child's parents list and add each child's uid to the current person's children list
        for child in children:
            #prevent duplicate entries in the children list
            if self.uid not in child.parents:
                child.parents.append(self.uid)
        self.children.extend(child.uid for child in children)

    def set_parents(self, parents: 'person_profile | list[person_profile]'):
        if isinstance(parents, person_profile):
            parents = [parents]
        if len(parents) > 2:
            raise ValueError("A person can have at most two parents.")
        for parent in parents:
            #prevent duplicate entries in the parents list and add the current person's uid to each parent's children list
            if parent.uid not in self.parents:
                self.parents.append(parent.uid)
                parent.children.append(self.uid)


    def set_name(self, name: str):
        self.name = name

    def set_age(self, age: int):
        if age < 0:
            raise ValueError("Age cannot be negative.")
        self.age = age

    def set_dna_profile(self, dna_profile: dict[str, int | None]):
        self.dna_profile = dna_profile
        if dna_profile.get_locus_data("Amelogenin") is not None:
            self.sex = "M" if dna_profile.get_locus_data("Amelogenin") == ["X", "Y"] else "F" if dna_profile.get_locus_data("Amelogenin") == ["X", "X"] else None

    def get_dna_profile(self) -> dict[str, int | None]:
        return self.dna_profile

    def print_dna_profile(self):
        for locus, alleles in self.dna_profile.items():
            print(f"{locus}: {alleles}")

    def print_full_profile(self):
        print(f"UUID: {self.uid}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Sex: {self.sex}")
        print(f"Parents: {self.parents}")
        print(f"Siblings: {self.siblings}")
        print(f"Children: {self.children}")
        print("DNA Profile:")
        for locus, alleles in self.dna_profile.profile.items():
            print(f"    {locus}: {alleles}")
