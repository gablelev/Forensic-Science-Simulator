from profile import person_profile

person = person_profile()
person.random_profile()
person.print_profile()
print("\nEditing D22S1045 locus to alleles ['10', '12']...\n")
person.edit_locus("D22S1045", ["10", "12"])
person.print_profile()
person.upload()