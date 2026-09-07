import pandas as pd
df = pd.read_csv(r"d:\tm\05_Own_Research\Data\ta_maybe.csv", dtype=str, encoding="utf-8-sig").fillna("")

targets = ["multi-faceted intervention on non-prescription", "c-reactive protein testing intervention on non-prescript",
           "magnitude of non-prescribed antibiotic", "assessment of non-prescription antibiotic dispensing at community pharmacies in"]

print("=== KEY RECORDS IN ta_maybe.csv ===\n")
for _, row in df.iterrows():
    txt = (str(row["title"]) + " " + str(row["author"])).lower()
    found = False
    for t in targets:
        if t.lower() in txt:
            found = True
            break
    if found:
        yr = str(row["year"])
        title = str(row["title"])
        author = str(row["author"])[:60]
        doi = str(row["doi"])
        abstract = str(row["abstract_snippet"])[:500]
        record_id = str(row["record_id"])
        print(f"[{yr}] {record_id}")
        print(f"Title: {title}")
        print(f"Author: {author}")
        print(f"DOI: {doi}")
        print(f"Abstract: {abstract}")
        print("-" * 60)
