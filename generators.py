import random
import yaml
from profile import person_profile, dna_profile

#for testing purposes, generates a random profile with random alleles for each locus
def random_dna_profile() -> dna_profile:
    with open("loci.yaml", "r") as file:
                loci_data = yaml.safe_load(file)
    profile = {}
    for locus, locus_data in loci_data["loci"].items():
        if locus == "Amelogenin":
            profile[locus] = ["X", random.choice(["X", "Y"])]
        else:
            #get the list of alleles and their frequencies for the current locus
            alleles = list(locus_data["alleles"].keys())
            #get the frequencies of each allele at the current locus for weighted random selection
            frequencies = [locus_data["alleles"][allele]["frequency"] for allele in alleles]

            allele1, allele2 = random.choices(alleles, weights=frequencies, k=2)
            profile[locus] = sorted([allele1, allele2], key=float)
    return dna_profile(profile)

#generate a child profile based on the DNA profiles of two parent profiles
def generate_child_profile(parent1: 'person_profile', parent2: 'person_profile') -> dna_profile:
    #check that both parents have valid Amelogenin loci
    if parent1.dna_profile.get_locus_data("Amelogenin") is None or parent2.dna_profile.get_locus_data("Amelogenin") is None:
        raise ValueError("Both parents must have the Amelogenin locus in their DNA profiles.")

    #check that both parents have valid Amelogenin alleles
    if parent1.dna_profile.get_locus_data("Amelogenin") != ['X', 'Y'] and parent1.dna_profile.get_locus_data("Amelogenin") != ['X', 'X']:
        raise ValueError("Parent 1 has an invalid Amelogenin locus. Must be ['X', 'Y'] or ['X', 'X'].")
    if parent2.dna_profile.get_locus_data("Amelogenin") != ['X', 'Y'] and parent2.dna_profile.get_locus_data("Amelogenin") != ['X', 'X']:
        raise ValueError("Parent 2 has an invalid Amelogenin locus. Must be ['X', 'Y'] or ['X', 'X'].")
    
    #check that both parents are not the same gender
    if parent1.dna_profile.get_locus_data("Amelogenin") == ['X', 'Y'] and parent2.dna_profile.get_locus_data("Amelogenin") == ['X', 'Y'] or parent1.dna_profile.get_locus_data("Amelogenin") == ['X', 'X'] and parent2.dna_profile.get_locus_data("Amelogenin") == ['X', 'X']:
        raise ValueError("Parents cannot be the same gender.")
    
    #add check here that each locus in the parents' DNA profiles is valid and has values in the loci.yaml file
    with open("loci.yaml", "r") as file:
                loci_data = yaml.safe_load(file)
    child_profile = {}
    for locus, locus_data in loci_data["loci"].items():
        if locus == "Amelogenin":
            child_profile[locus] = ["X", random.choice(["X", "Y"])]
        else:
            # For other loci, inherit one allele from each parent
            child_alleles = [random.choice(parent1.dna_profile.get_locus_data(locus)), random.choice(parent2.dna_profile.get_locus_data(locus))]
            child_profile[locus] = sorted(child_alleles, key=float)
    return dna_profile(child_profile)