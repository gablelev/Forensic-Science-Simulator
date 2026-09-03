#scripts for mass-editing the loci.yaml file if adding or removing data
import yaml
from pathlib import Path

path = Path(r"c:\Users\20cla\OneDrive\Desktop\Forensic Science Simulator\loci.yaml")
data = yaml.safe_load(path.read_text(encoding="utf-8"))

for locus in data.get("loci", {}).values():
    alleles = locus.get("alleles", {})
    for allele_name, allele in alleles.items():
        if not isinstance(allele, dict):
            continue
        allele.pop("sequences", None)
        allele["microvariant"] = "." in str(allele_name)

path.write_text(
    yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
    encoding="utf-8",
)