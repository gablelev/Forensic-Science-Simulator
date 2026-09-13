import uuid
import random
import yaml
import os

with open("loci.yaml", "r") as file:
    loci_data = yaml.safe_load(file)
locus_names = loci_data["locus_names"]

with open("evidence.yaml", "r") as file:
    evidence_data = yaml.safe_load(file)
sources = evidence_data["sources"]

#a case profile stores lists of evidence and lists of person profiles. evidence and person_profiles can store a dna profile

#dna profile of a person or evidence, including alleles for each locus - source points to an evidence id
class dna_profile:
    #creates an empty profile with all loci set to None by default or initializes with a provided profile dictionary
    def __init__(self, dna = None, source: str = None):
        if dna is None:
            dna = {
                locus: [None, None]
                for locus in locus_names
            }
        self.dna = dna
        self.source = source
            
    def set_profile(self, dna: dict[str, int | None]):
        self.dna = profile

    #returns the alleles for a given locus, or [None, None] if the locus is not present in the profile
    def get_locus_data(self, locus: str) -> list[int | None]:
        return self.dna.get(locus, [None, None])

    def set_locus(self, locus: str, alleles: list[int | float | str]):
        if locus == "Amelogenin":
            raise ValueError("Cannot edit Amelogenin locus using edit_locus method. Use edit_gender method instead.")
            
        locus_info = loci_data["loci"][locus]
        if locus in self.dna:
            sorted_alleles = sorted(alleles, key=float)
            allele1, allele2 = (str(allele) for allele in sorted_alleles)
            #organize alleles in descending order for consistency
            if allele1 not in locus_info["alleles"].keys():
                raise ValueError(f"One or both alleles {alleles} are not valid for locus '{locus}'.")
            self.dna[locus] = [allele1, allele2]
        else:
            #this should not happen
            raise ValueError(f"MAJOR PROFILE ERROR: Locus '{locus}' not found in the profile.")

    #updates gender of the dna profile
    def set_gender(self, chromosomes: list[str]):
        if set(chromosomes) != {"X", "Y"} and set(chromosomes) != {"X", "X"}:
            raise ValueError("Invalid chromosomes for Amelogenin locus. Must be ['X', 'Y'] or ['X', 'X'].")
        self.dna["Amelogenin"] = chromosomes

#a piece of evidence, such as a blood sample, hair sample, or other biological material, that can be used to generate a DNA profile
class evidence:
    def __init__(self, dna: dna_profile = None, source: str = None, person_source: str = None, date_collected: str = None):
        self.dna_profile = dna
        if source is not None and source not in sources:
            raise ValueError(f"Invalid source '{source}'. Must be one of {sources}.")
        self.source = source
        self.person_source = source
        self.date_collected = date_collected
        self.evidence_id = str(uuid.uuid4())

    def set_dna_profile(self, dna: dna_profile):
        self.dna_profile = dna

    def set_source(self, source: str):
        if source not in sources:
            raise ValueError(f"Invalid source '{source}'. Must be one of {sources}.")
        self.source = source

    def set_person_source(self, person_source: str):
        self.person_source = person_source
    
    def set_date_collected(self, date: str):
        self.date_collected = date

#full profile of a person, including their dna profile and family relationships
class person_profile:
    def __init__(self, dna: dna_profile = None, parents: list['person_profile'] = None, siblings: list['person_profile'] = None, children: list['person_profile'] = None, name = None, age = None, sex = None, uid = None):
        #generate an empty dna profile if none is given
        if dna is None:
            dna = dna_profile()
        self.dna_profile = dna
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
        for locus, alleles in self.dna_profile.dna.items():
            print(f"{locus}: {alleles}")

    def print_full_profile(self):
        print(f"UUID: {self.uid}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Sex: {self.sex}")
        print(f"Parents: {self.parents}")
        print(f"Siblings: {self.siblings}")
        print(f"Children: {self.children}")
        print(f"DNA Profile Information:")
        print(f"    Source: {self.dna_profile.source}")
        print("DNA Profile:")
        for locus, alleles in self.dna_profile.dna.items():
            print(f"    {locus}: {alleles}")

#full profile of a case, including the case ID, list of evidence, list of suspects, and list of victims, along with related dna profiles and family relationships for each person
class case_profile:
    def __init__(self, case_id: str = None, evidence_list: list['evidence'] = None, suspect_list: list['person_profile'] = None, victim_list: list['person_profile'] = None):
        self.case_id = case_id if case_id is not None else str(uuid.uuid4())
        self.evidence_list = evidence_list
        self.suspect_list = suspect_list
        self.victim_list = victim_list

    def print_evidence_list(self):
        print(f"Case ID: {self.case_id}")
        for evidence in evidence_list:
            print(f"Evidence ID: {evidence.evidence_id}")
            print(f"Person Source: {evidence.person_source}")
            print(f"Source: {evidence.source}")
            print(f"Date Collected: {evidence.date_collected}")
