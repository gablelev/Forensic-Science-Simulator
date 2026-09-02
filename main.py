from profile import person_profile
from generators import *

person = person_profile()
#person.print_profile()
profile = random_profile()
print(profile)
person.set_dna_profile(profile)
#print("\nEditing D22S1045 locus to alleles [12, 10]...\n")
#person.edit_locus("D22S1045", [12, 10])
#person.print_profile()
person.upload()