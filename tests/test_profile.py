from profiles import person_profile, dna_profile, evidence
import pytest
import yaml

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

#test creating a blank person profile
def test_create_person_profile():
    person = person_profile()
    #person profile exists but is blank
    assert person is not None
    assert person.dna_profile is not None
    assert person.parents == []
    assert person.siblings == []
    assert person.children == []
    assert person.name is None
    assert person.sex is None
    assert person.age is None
    assert person.uid is not None

