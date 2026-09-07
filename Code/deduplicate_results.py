import pandas as pd
import re
import os

PUBMED_FILE = r"d:\tm\05_Own_Research\Data\pubmed_search_results.csv"
OPENALEX_FILE = r"d:\tm\05_Own_Research\Data\openalex_search_results.csv"
OUTPUT_FILE = r"d:\tm\05_Own_Research\Data\master_screening_database.csv"

def clean_title(title):
    if pd.isna(title):
        return ""
    # Remove punctuation, convert to lowercase, remove extra spaces
    title = re.sub(r'[^\w\s]', '', str(title).lower())
    return " ".join(title.split())

def clean_doi(doi):
    if pd.isna(doi):
        return ""
    doi = str(doi).strip().lower()
    # Remove URL prefixes if present
    doi = doi.replace("https://doi.org/", "").replace("http://dx.doi.org/", "").replace("doi:", "")
    return doi

print("="*50)
print("DEDUPLICATION PROCESS")
print("="*50)

# 1. Load data
print("Loading datasets...")
try:
    df_pubmed = pd.read_csv(PUBMED_FILE)
    df_openalex = pd.read_csv(OPENALEX_FILE)
    print(f"Loaded {len(df_pubmed)} records from PubMed")
    print(f"Loaded {len(df_openalex)} records from OpenAlex")
except Exception as e:
    print(f"Error loading files: {e}")
    exit(1)

# Ensure required columns exist
cols = ['record_id', 'database_source', 'author', 'year', 'title', 'journal', 'doi', 'abstract_snippet']
df_pubmed = df_pubmed[[c for c in cols if c in df_pubmed.columns]]
df_openalex = df_openalex[[c for c in cols if c in df_openalex.columns]]

# 2. Combine
print("\nCombining datasets...")
df_combined = pd.concat([df_pubmed, df_openalex], ignore_index=True)
print(f"Total combined records: {len(df_combined)}")

# 3. Clean fields for matching
df_combined['clean_doi'] = df_combined['doi'].apply(clean_doi)
df_combined['clean_title'] = df_combined['title'].apply(clean_title)

# 4. Deduplicate by DOI
print("\nStep 1: Deduplicating by DOI...")
# Only consider rows with a valid DOI for this step
has_doi = df_combined['clean_doi'] != ""

# Sort so PubMed is kept over OpenAlex if duplicates exist (PubMed abstracts are usually cleaner)
df_combined['db_priority'] = df_combined['database_source'].apply(lambda x: 1 if x == 'PubMed' else 2)
df_combined = df_combined.sort_values(['db_priority', 'year'])

# Find duplicates by DOI
doi_duplicates = df_combined[has_doi].duplicated(subset=['clean_doi'], keep='first')
df_dedup_doi = pd.concat([
    df_combined[has_doi][~doi_duplicates],
    df_combined[~has_doi]
])
print(f"Removed {doi_duplicates.sum()} duplicates based on DOI.")
print(f"Records remaining: {len(df_dedup_doi)}")

# 5. Deduplicate by Title (Fuzzy/Exact clean title)
print("\nStep 2: Deduplicating by Title...")
# Only consider rows with a title > 10 chars
has_title = df_dedup_doi['clean_title'].str.len() > 10

title_duplicates = df_dedup_doi[has_title].duplicated(subset=['clean_title'], keep='first')
df_final = pd.concat([
    df_dedup_doi[has_title][~title_duplicates],
    df_dedup_doi[~has_title]
])
print(f"Removed {title_duplicates.sum()} duplicates based on Title.")
print(f"Records remaining: {len(df_final)}")

# 6. Prepare final output
print("\nPreparing final dataset...")
# Keep PubMed IDs or OpenAlex IDs in a general 'source_id' column if needed, 
# but for screening we just need the standard columns.
# We will regenerate a clean record_id
df_final = df_final.sort_values(['year', 'author'], ascending=[False, True]).reset_index(drop=True)
df_final['record_id'] = [f"REC-{i:04d}" for i in range(1, len(df_final) + 1)]

# Add screening columns
screening_cols = [
    'duplicate_of', 'ta_decision', 'ta_exclusion_reason', 
    'ft_available', 'ft_decision', 'ft_exclusion_reason', 
    'included_in_review', 'notes'
]
for col in screening_cols:
    df_final[col] = ""

output_cols = [
    'record_id', 'database_source', 'author', 'year', 'title', 'journal', 'doi', 'abstract_snippet'
] + screening_cols

df_final = df_final[output_cols]

# 7. Save
print(f"\nSaving to {OUTPUT_FILE}...")
df_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
print(f"Done! Final unique records for screening: {len(df_final)}")
print("="*50)
