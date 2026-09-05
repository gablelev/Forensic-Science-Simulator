from profile import person_profile, dna_profile
from generators import *

person = person_profile()
child = person_profile()

profile = random_dna_profile()
child = random_dna_profile()
person.set_dna_profile(profile)
child.set_dna_profile(child)

person.set_children([child])



#print(profile)
#person.print_profile()
#person.upload()