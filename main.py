from profile import person_profile, dna_profile
from generators import *
from database import get_person_profile_from_database as get_person

person = person_profile()
child = person_profile()

profile = random_dna_profile()
childprofile = random_dna_profile()

person.set_dna_profile(profile)
child.set_dna_profile(childprofile)

child.set_parents(person)

person_fetched = get_person('2517bbe0-4607-4354-9f24-4978224f50ea')
person_fetched.print_full_profile()