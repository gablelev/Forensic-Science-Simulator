import uuid
import random
import yaml
import os
import re
import warnings

with open("loci.yaml", "r") as file:
    loci_data = yaml.safe_load(file)
locus_names = loci_data["locus_names"]

with open("evidence.yaml", "r") as file:
    evidence_data = yaml.safe_load(file)
sources = evidence_data["sources"]

def validate_name(name: str) -> str:
    if not isinstance(name, str):
        raise TypeError("Name must be a string.")
    #removing leading and trailing whitespace
    name = name.strip()
    #detect invalid characters in the name
    if not re.fullmatch(r"^[a-zA-Z\s\-]+$", name):
        raise ValueError("Name contains invalid characters. Only letters, spaces, and hyphens are allowed.")
    #capitalize the first letter of each word in the name
    name = name.title()
    return name

#used to validate a user inputted age for a person profile - to be used before the age is converted to an integer
def validate_age(age: str) -> int:
    try:
        age = int(age.strip())
    except ValueError:
        raise ValueError("Age must be a valid integer.")
    if age < 0:
        raise ValueError("Age cannot be negative.")
    return age

#checks validity of a uuid
def is_valid_uuid(value: str) -> bool:
    if not isinstance(value, str):
        return False
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False

#a case profile stores lists of evidence and lists of person profiles. evidence and person_profiles can store a dna profile

#dna profile of a person or evidence, including alleles for each locus - source points to an evidence id
class dna_profile:
    #creates an empty profile with all loci set to None by default or initializes with a provided profile dictionary
    #with implementation of a gui, the initilization of a dna profile will only be done to make a blank profile
    def __init__(self, dna = None, source: str = None):
        if dna is None:
            dna = {
                locus: [None, None]
                for locus in locus_names
            }
        self.dna = dna
        self.source = source
        
    #returns the alleles for a given locus, or [None, None] if the locus is not present in the profile
    def get_locus_data(self, locus: str) -> list[int | None]:
        if not isinstance(locus, str):
            raise TypeError("Locus must be a string.")
        return self.dna.get(locus, [None, None])

    def set_locus(self, locus: str, alleles: list[int | float | str]):
        if not isinstance(locus, str):
            raise TypeError("Locus must be a string.")
        if not isinstance(alleles, list) or len(alleles) != 2 or not all(isinstance(a, (int, float, str)) for a in alleles):
            raise TypeError("Alleles must be a list of two integers, floats, or strings.")
        if locus == "Amelogenin":
            raise ValueError("Cannot edit Amelogenin locus using edit_locus method. Use edit_gender method instead.")
        
        if locus not in locus_names:
            raise KeyError(f"Locus '{locus}' is not a valid locus.")

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

    def set_source(self, source: str):
        if not isinstance(source, str):
            raise TypeError("Source must be a string.")
        if source not in sources:
            raise ValueError(f"Invalid source '{source}'. Must be one of {sources}.")
        else:
            self.source = source

    #updates gender of the dna profile - overwrites the sex of the person profile if it is set
    def set_gender(self, chromosomes: list[str]):
        if not isinstance(chromosomes, list) or len(chromosomes) != 2 or not all(isinstance(c, str) for c in chromosomes):
            raise TypeError("Chromosomes must be a list of two strings.")
        if set(chromosomes) != {"X", "Y"} and set(chromosomes) != {"X", "X"}:
            raise ValueError("Invalid chromosomes for Amelogenin locus. Must be ['X', 'Y'] or ['X', 'X'].")
        if set(chromosomes) == {"X", "Y"}:
            self.sex = "M"
        elif set(chromosomes) == {"X", "X"}:
            self.sex = "F"
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
        if not isinstance(dna, dna_profile):
            raise TypeError("Expected a dna_profile instance.")
        self.dna_profile = dna

    #set the substance from which the evidence was collected
    def set_source(self, source: str):
        if not isinstance(source, str):
            raise TypeError("Source must be a string.")
        if source not in sources:
            raise ValueError(f"Invalid source '{source}'. Must be one of {sources}.")
        self.source = source

    #set the unique id of the person from whom the evidence was collected
    def set_person_source(self, person_source: str):
        if not isinstance(person_source, str):
            raise TypeError("Person source must be a string representing a UUID.")
        if not is_valid_uuid(person_source):
            raise ValueError(f"Invalid person source '{person_source}'. Must be a valid UUID.")
        self.person_source = person_source
    
    def set_date_collected(self, date: str):
        self.date_collected = date

#full profile of a person, including their dna profile and family relationships
#relationships are stored as UIDs
class person_profile:
    def __init__(self, dna: dna_profile = None, mother: str = None, father: str = None, siblings: list[str] = None, children: list[str] = None, name = None, age = None, sex = None, uid = None):
        #generate an empty dna profile if none is given
        if dna is None:
            dna = dna_profile()
        self.dna_profile = dna
        self.mother = mother
        self.father = father
        self.siblings = siblings if siblings is not None else []
        self.children = children if children is not None else []
        self.name = name
        self.sex = "M" if self.dna_profile.get_locus_data("Amelogenin") == ["X", "Y"] else "F" if self.dna_profile.get_locus_data("Amelogenin") == ["X", "X"] else None
        self.age = age
        self.uid = uid if uid is not None else str(uuid.uuid4())

    def add_siblings(self, siblings: 'person_profile | list[person_profile]'):
        if isinstance(siblings, person_profile):
            siblings = [siblings]
        elif not isinstance(siblings, list) or not all(isinstance(s, person_profile) for s in siblings):
            raise TypeError("Siblings must be a person_profile or a list of person_profiles.")
        #add the current person's uid to each sibling's siblings list and add each sibling's uid to the current person's siblings list
        for sibling in siblings:
            try:
                if self.uid == sibling.uid:
                    raise ValueError("Cannot make someone their own sibling. Cancelling...")

                #prevent duplicate entries in the siblings list
                if self.uid not in sibling.siblings:
                    sibling.siblings.append(self.uid)
                #add sibling's uid to their siblings list
                if sibling.uid not in self.siblings:
                    self.siblings.append(sibling.uid)
            except ValueError as e:
                print(f"Error: {e}")

    #remove a sibling from the person profile
    def remove_sibling(self, sibling: 'person_profile | list[person_profile]'):
        if isinstance(sibling, person_profile):
            sibling = [sibling]
        elif not isinstance(sibling, list) or not all(isinstance(s, person_profile) for s in sibling):
            raise TypeError("Sibling must be a person_profile or a list of person_profiles.")
        #remove sibling from current person's siblings list and remove current person's uid from the sibling's sibling list
        for s in sibling:
            if s.uid in self.siblings:
                self.siblings.remove(s.uid)
            if self.uid in s.siblings:
                s.siblings.remove(self.uid)

    #add a child to the person profile - self is the parent
    def add_children(self, children: 'person_profile | list[person_profile]'):
        if isinstance(children, person_profile):
            children = [children]
        elif not isinstance(children, list) or not all(isinstance(child, person_profile) for child in children):
            raise TypeError("Children must be a person_profile or a list of person_profiles.")
        #add the current person's uid to each child's parents list and add each child's uid to the current person's children list
        for child in children:
            try:
                if self.uid == child.uid:
                    raise ValueError("Cannot make someone their own child. Cancelling...")
                
                #check if the parent is the mother or father and add them to the child's profile
                if self.sex == "F":
                    if self.uid != child.mother:
                        child.mother = self.uid
                if self.sex == "M":
                    if self.uid != child.father:
                        child.father = self.uid

                #add child's uid to their parent's children list
                if child.uid not in self.children:
                    self.children.append(child.uid)
            except ValueError as e:
                print(f"Error: {e}")

    #remove a child from the person profile
    def remove_children(self, children: 'person_profile | list[person_profile]'):
        if isinstance(children, person_profile):
            children = [children]
        elif not isinstance(children, list) or not all(isinstance(c, person_profile) for c in children):
            raise TypeError("Children must be a person_profile or a list of person_profiles.")
        for c in children:
            if c.uid in self.children:
                self.children.remove(c.uid)

    #explicity add a mother to the person profile
    def set_mother(self, mother: 'person_profile'):
        if not isinstance(mother, person_profile):
            raise TypeError("Expected a person_profile instance for mother.")
        if self.uid == mother.uid:
            raise ValueError("Cannot make someone their own mother. Cancelling...")
        if mother.sex == "M":
            raise ValueError("The provided profile is not a female.")
        if mother.uid != self.mother:
            self.mother = mother.uid
        if self.uid not in mother.children:
            mother.children.append(self.uid)

    #explicitly add a father to the person profile
    def set_father(self, father: 'person_profile'):
        if not isinstance(father, person_profile):
            raise TypeError("Expected a person_profile instance for father.")
        if father.dna_profile is None:
            warnings.warn("Father's DNA profile is not set.")
        if father.sex == "F":
            raise ValueError("The provided profile is not a male.")
        if self.uid == father.uid:
            raise ValueError("Cannot make someone their own father. Cancelling...")
        if father.uid != self.father:
            self.father = father.uid
        if self.uid not in father.children:
            father.children.append(self.uid)

    #remove a mother from the person profile
    def remove_mother(self):
        if self.mother is not None:
            mother_uid = self.mother
            self.mother = None
            #remove the current person's uid from the mother's children list
            mother_profile = get_person_profile_by_uid(mother_uid)
            if mother_profile:
                if self.uid in mother_profile.children:
                    mother_profile.remove_children(self)
            else:
                raise ValueError(f"Mother with UID {mother_uid} not found in the database.")

    #remove a father from the person profile
    def remove_father(self):
        if self.father is not None:
            father_uid = self.father
            self.father = None
            #remove the current person's uid from the father's children list
            father_profile = get_person_profile_by_uid(father_uid)
            if father_profile:
                if self.uid in father_profile.children:
                    father_profile.remove_children(self)
            else:
                raise ValueError(f"Father with UID {father_uid} not found in the database.")

    #sets name of the person profile - user input function, requires sanitization
    def set_name(self, name: str):
        validated_name = validate_name(name)
        self.name = validated_name

    #sets age of the person profile - user input function, requires sanitization
    def set_age(self, age: str):
        validated_age = validate_age(age)
        self.age = validated_age

    #sets the dna profile of a person profile
    def set_dna_profile(self, dna: 'dna_profile'):
        if not isinstance(dna, dna_profile):
            raise TypeError("DNA profile must be an instance of dna_profile.")
        self.dna_profile = dna
        if dna.get_locus_data("Amelogenin") is not None:
            self.sex = "M" if dna.get_locus_data("Amelogenin") == ["X", "Y"] else "F" if dna.get_locus_data("Amelogenin") == ["X", "X"] else None

    def get_dna_profile(self) -> 'dna_profile':
        if self.dna_profile is None:
            raise ValueError("DNA profile is not set for this person.")
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
    def __init__(self, case_id: str = None, evidence_list: list[str] = None, suspect_list: list[str] = None, victim_list: list[str] = None):
        self.case_id = case_id if case_id is not None else str(uuid.uuid4())
        #suspect, victim, and evidence lists point to unique ids to avoid redundancy of data
        self.evidence_list = evidence_list if evidence_list is not None else []
        self.suspect_list = suspect_list if suspect_list is not None else []
        self.victim_list = victim_list if victim_list is not None else []

    def add_victim(self, victim: str or person_profile):
        #if given argument is a person_profile, strip the unique id
        if isinstance(victim, person_profile):
            victim = victim.uid
        #check validity of unique id
        if is_valid_uuid(victim):
            self.victim_list.append(victim)
        else:
            print(f"Victim ID either does not exist in profile or was given incorrectly.")

    def add_suspect(self, suspect: person_profile):
        suspect_id = suspect.uid
        if is_valid_uuid(suspect_id):
            self.suspect_list.append(suspect_id)
        else:
            print(f"Person profile contains an invalid unique ID: {suspect_id}")

    def add_evidence(self, ev: str or evidence):
        #if given argument is an evidence object, strip the unique id
        if isinstance(ev, evidence):
            ev = ev.evidence_id
        #check validity of unique id
        if is_valid_uuid(ev):
            self.evidence_list.append(ev)
        else:
            print(f"Evidence ID either does not exist in evidence profile or was given incorrectly.")

    def print_evidence_list(self):
        print(f"Evidence List:")
        if self.evidence_list:
            for evidence in self.evidence_list:
                print(f"    Evidence ID: {evidence.evidence_id}")
                print(f"    Person Source: {evidence.person_source}")
                print(f"    Source: {evidence.source}")
                print(f"    Date Collected: {evidence.date_collected}")
        else:
            print(f"    Empty")

    def print_suspect_list(self):
        print(f"Suspect List:")
        index = 1
        if self.suspect_list:
            for person_id in self.suspect_list:
                print(f"    Suspect {index} ID: {person_id}")
                index += 1
        else:
            print(f"    Empty")

    def print_victim_list(self):
        print(f"Victim List:")
        index = 1
        if self.victim_list:
            for person_id in self.victim_list:
                print(f"    Victim {index} ID: {person_id}")
                index += 1
        else:
            print(f"    Empty")

    def print_full_case_profile(self):
        print(f"Case ID: {self.case_id}")
        self.print_evidence_list()
        self.print_suspect_list()
        self.print_victim_list()

