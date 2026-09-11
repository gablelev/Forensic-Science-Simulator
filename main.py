from profile import person_profile, dna_profile
from generators import *
from database import get_person_profile_from_database, upload as get_person, upload
from faker import Faker

person = person_profile(age = random.randint(0, 100))

profile = random_dna_profile()

person.set_dna_profile(profile)

if person.sex == "M":
    person.set_name(Faker().name_male())
elif person.sex == "F":
    person.set_name(Faker().name_female())

person.print_full_profile()
upload(person)
