import random
import yaml

#for testing purposes, generates a random profile with random alleles for each locus
def random_profile():
    with open("loci.yaml", "r") as file:
                loci_data = yaml.safe_load(file)
    dna_profile = {}
    for locus, locus_data in loci_data["loci"].items():
        if locus == "Amelogenin":
            dna_profile[locus] = ["X", random.choice(["X", "Y"])]
        else:
            #get the list of alleles and their frequencies for the current locus
            alleles = list(locus_data["alleles"].keys())
            #get the frequencies of each allele at the current locus for weighted random selection
            frequencies = [locus_data["alleles"][allele]["frequency"] for allele in alleles]

            allele1, allele2 = random.choices(alleles, weights=frequencies, k=2)
            dna_profile[locus] = sorted([allele1, allele2], key=float)
    return dna_profile