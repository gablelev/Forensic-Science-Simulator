import uuid
import random
import yaml

locus_names = [
    "D8S1179",
    "D21S11",
    "D7S820",
    "CSF1PO",
    "D3S1358",
    "TH01",
    "D13S317",
    "D16S539",
    "D2S1338",
    "D19S433",
    "vWA",
    "TPOX",
    "D18S51",
    "D5S818",
    "FGA",
    "Amelogenin"
]

class person_profile:
    def __init__(self,dna_profile: dict[str, int | None] = {locus: None for locus in locus_names}, parents: list['person_profile'] = [], siblings: list['person_profile'] = [], children: list['person_profile'] = [], name = None, age = None, sex = None):
        self.dna_profile = dna_profile
        self.parents = parents
        self.siblings = siblings
        self.children = children
        self.name = name
        self.sex = sex if sex is not None else dna_profile.get("Amelogenin")
        self.age = age
        self.uid = str(uuid.uuid4())

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
                dna_profile[locus] = [random.randint(min_val, max_val), random.randint(min_val, max_val)]
        self.dna_profile = dna_profile

    def upload(self):
        global data
        data["profiles"][self.uid] = {
            "dna_profile": self.dna_profile,
            "name": self.name,
            "age": self.age,
            "sex": self.sex,
            "parents": [parent.uid for parent in self.parents],
            "siblings": [sibling.uid for sibling in self.siblings],
            "children": [child.uid for child in self.children]
        }

        with open("database.yaml", "w") as file:
            yaml.safe_dump(data, file)

    def print_profile(self):
        for locus, allele in self.dna_profile.items():
            print(f"{locus}: {allele}")
