from profile import person_profile, dna_profile
from generators import *

parent1 = person_profile()
parent2 = person_profile()
#person.print_profile()

profile1 = random_dna_profile()
profile2 = random_dna_profile()

profile1.set_gender(["X", "Y"])
profile2.set_gender(["X", "X"])

parent1.set_dna_profile(profile1)
parent2.set_dna_profile(profile2)

print("Parent 1 DNA Profile:")
parent1.print_full_profile()
print("\nParent 2 DNA Profile:")
parent2.print_full_profile()

generated_child_profile = generate_child_profile(parent1, parent2)
child = person_profile()
child.set_dna_profile(generated_child_profile)
print("\nGenerated Child DNA Profile:")
child.print_full_profile()

#print(profile)
#person.set_dna_profile(profile)
#person.edit_locus("D22S1045", [12, 10])
#print("\nEditing D22S1045 locus to alleles [12, 10]...\n")
#person.print_profile()
#person.upload()