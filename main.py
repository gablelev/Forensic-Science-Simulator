from profile import person_profile, dna_profile
from generators import *
from database import *
from faker import Faker

parent = person_profile()
parent_profile = random_dna_profile()
child = person_profile()
child_profile = random_dna_profile()
parent.set_dna_profile(parent_profile)
child.set_dna_profile(child_profile)
parent.add_children([child, parent])

parent.print_full_profile()
child.print_full_profile()

# suspect = person_profile()
# victim = person_profile()
# profile = random_dna_profile()
# profile2 = random_dna_profile()
# suspect.set_dna_profile(profile)
# victim.set_dna_profile(profile2)
# suspect.print_full_profile()
# victim.print_full_profile
#
# case = case_profile()
#
# case.add_suspect(suspect)
# case.add_victim(victim)
#
# case.print_full_case_profile()

#if person.sex == "M":
#    person.set_name(Faker().name_male())
#elif person.sex == "F":
#    person.set_name(Faker().name_female())

#upload(person)