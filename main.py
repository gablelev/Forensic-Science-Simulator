from profile import person_profile, dna_profile
from generators import *
from database import get_person_profile_from_database, upload as get_person, upload

person = person_profile()
child = person_profile()

profile = random_dna_profile()
childprofile = random_dna_profile()

person.set_dna_profile(profile)
child.set_dna_profile(childprofile)

child.set_parents(person)

upload(person)
