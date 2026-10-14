from profiles import person_profile, dna_profile, evidence
import pytest
import yaml
import uuid

with open("loci.yaml", "r") as file:
    loci_data = yaml.safe_load(file)
locus_names = loci_data["locus_names"]

with open("evidence.yaml", "r") as file:
    evidence_data = yaml.safe_load(file)
sources = evidence_data["sources"]

#test creating a blank dna profile
def test_create_dna_profile():
    profile = dna_profile()
    #dna profile exists but is blank
    assert profile is not None
    assert profile.source is None
    for locus in profile.dna:
        assert profile.dna[locus] == [None, None]

#set the source of a dna profile
def test_dna_profile_set_source():
    profile = dna_profile()
    profile.set_source("blood")
    assert profile.source == "blood"

#set the source of a dna profile to an invalid source should raise a ValueError
def test_dna_profile_set_invalid_source():
    profile = dna_profile()
    with pytest.raises(ValueError):
        profile.set_source("invalid_source")

#setting the locus of a dna profile to a valid locus
def test_dna_profile_set_locus():
    profile = dna_profile()
    profile.set_locus("D3S1358", ["15", "16"])
    assert profile.dna["D3S1358"] == ["15", "16"]

#setting the locus of a dna profile to an invalid locus should raise a ValueError
def test_dna_profile_set_invalid_locus():
    profile = dna_profile()
    with pytest.raises(KeyError):
        profile.set_locus("INVALID_LOCUS", ["15", "16"])

#setting the locus of a dna profile to an invalid allele should raise a ValueError
def test_dna_profile_set_invalid_allele():
    profile = dna_profile()
    with pytest.raises(ValueError):
        profile.set_locus("D3S1358", ["15", "INVALID_ALLELE"])

#test creating blank evidence
def test_create_evidence():
    test_evidence = evidence()
    #evidence exists but is blank
    assert test_evidence is not None
    assert test_evidence.source is None
    assert test_evidence.person_source is None
    assert test_evidence.date_collected is None
    assert test_evidence.evidence_id is not None
    assert test_evidence.dna_profile is None

#test setting dna profile of evidence
def test_evidence_set_dna_profile():
    test_evidence = evidence()
    dna = dna_profile()
    test_evidence.set_dna_profile(dna)
    assert test_evidence.dna_profile == dna

#test setting source of evidence
def test_evidence_set_source():
    test_evidence = evidence()
    test_evidence.set_source("blood")
    assert test_evidence.source == "blood"

#test setting person source of evidence
def test_evidence_set_person_source():
    test_evidence = evidence()
    test_person_uid = str(uuid.uuid4())
    test_evidence.set_person_source(test_person_uid)
    assert test_evidence.person_source == test_person_uid

#test setting person source of evidence to an invalid uuid should raise a ValueError
def test_evidence_set_person_source_invalid():
    test_evidence = evidence()
    with pytest.raises(ValueError):
        test_evidence.set_person_source("invalid_uuid")

#test setting date collected of evidence
def test_evidence_set_date_collected():
    test_evidence = evidence()
    test_evidence.set_date_collected("2023-01-01")
    assert test_evidence.date_collected == "2023-01-01"

#test creating a blank person profile
def test_create_person_profile():
    person = person_profile()
    #person profile exists but is blank
    assert person is not None
    assert person.dna_profile is not None
    assert person.mother is None
    assert person.father is None
    assert person.siblings == []
    assert person.children == []
    assert person.name is None
    assert person.sex is None
    assert person.age is None
    assert person.uid is not None

#test setting dna of person profile
def test_person_profile_set_dna():
    person = person_profile()
    dna = dna_profile()
    person.set_dna_profile(dna)
    assert person.dna_profile == dna

#test adding sibling to person profile
def test_person_profile_add_siblings():
    person = person_profile()
    sibling = person_profile()
    person.add_siblings(sibling)
    assert person.siblings == [sibling.uid]
    assert sibling.siblings == [person.uid]

#test adding a mother to person profile
def test_person_profile_set_mother():
    person = person_profile()
    mother = person_profile()
    mother.sex = "F"
    person.set_mother(mother)
    assert person.mother == mother.uid

#test adding a father to person profile
def test_person_profile_set_father():
    person = person_profile()
    father = person_profile()
    father.sex = "M"
    person.set_father(father)
    assert person.father == father.uid

#test setting a mother with wrong sex
def test_person_profile_set_mother_invalid():
    person = person_profile()
    mother = person_profile()
    mother.sex = "M"
    with pytest.raises(ValueError):
        person.set_mother(mother)

#test setting a father with wrong sex
def test_person_profile_set_father_invalid():
    person = person_profile()
    father = person_profile()
    father.sex = "F"
    with pytest.raises(ValueError):
        person.set_father(father)

#test adding a child to person profile
def test_person_profile_add_child():
    person = person_profile()
    person.sex = "F"
    child = person_profile()
    person.add_children(child)
    assert person.children == [child.uid]
    assert child.mother == person.uid

#test adding a child to person profile with invalid type
def test_person_profile_add_child_invalid():
    person = person_profile()
    with pytest.raises(TypeError):
        person.add_children("invalid")
    
