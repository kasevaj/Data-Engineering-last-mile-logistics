import kagglehub, shutil
from pathlib import Path

DATASET_ID = "sujalsuthar/amazon-delivery-dataset"
src_root = Path(kagglehub.dataset_download(DATASET_ID))
dst_root = Path("data/amazon")
dst_root.mkdir(parents=True, exist_ok=True)

# Kopioi kaikki jsonit (tai vaihda *.csv jos datasetissä on csv)
for p in src_root.rglob("*.csv"):
    shutil.copy2(p, dst_root / p.name)
    print("Copied:", p.name)

print("Local data dir:", dst_root.resolve())