import pandas as pd

inc = pd.read_csv(r"d:\tm\05_Own_Research\Data\ta_included.csv", dtype=str, encoding="utf-8-sig").fillna("")
print(f"Total included: {len(inc)}")
print("=" * 70)
for i, (_, row) in enumerate(inc.iterrows(), 1):
    yr = str(row["year"])
    title = str(row["title"])[:90]
    journal = str(row["journal"])[:45]
    doi = str(row["doi"])[:40]
    print(f"{i:2}. [{yr}] {title}")
    print(f"     Journal: {journal}")
    print(f"     DOI: {doi}")
    print()
