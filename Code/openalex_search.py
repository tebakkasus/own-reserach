"""
OpenAlex Search Script (Scopus alternative) — Meta-Analysis PINMAS IV 2026
Search Protocol V1.1 — 3-Block Strategy
OpenAlex covers >200M works including Scopus-indexed content
"""
import urllib.request
import urllib.parse
import json
import csv
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_CSV = r"d:\tm\05_Own_Research\Data\openalex_search_results.csv"
BASE_URL = "https://api.openalex.org/works"

# We'll use OpenAlex's search API with a broad query
# OpenAlex doesn't support complex boolean per-field, so we use search + filter
# Strategy: search for the key concepts broadly, then filter

# Build multiple targeted queries to maximize recall
QUERIES = [
    # Query 1: Core query
    '"community pharmacy" antibiotic dispensing',
    # Query 2: Non-prescription focus
    '"community pharmacy" antibiotic "non-prescription"',
    # Query 3: Drug shop/outlet variant
    '"drug shop" OR "drug outlet" antibiotic dispensing',
    # Query 4: Over-the-counter
    '"community pharmacy" antibiotic "over-the-counter"',
    # Query 5: Self-medication pharmacy
    '"community pharmacy" antibiotic "self-medication"',
    # Query 6: Private pharmacy
    '"private pharmacy" antibiotic dispensing',
    # Query 7: Retail pharmacy
    '"retail pharmacy" antibiotic dispensing',
    # Query 8: Medicine store
    '"medicine store" OR "medicine shop" antibiotic',
    # Query 9: Patent medicine vendor (Nigeria)
    '"patent medicine" antibiotic dispensing',
    # Query 10: Antimicrobial stewardship pharmacy
    '"community pharmacy" antimicrobial stewardship dispensing',
    # Query 11: Without prescription
    '"community pharmacy" antibiotic "without prescription"',
    # Query 12: Drug retail
    '"drug retail" antibiotic',
    # Query 13: Irrational use
    '"community pharmacy" antibiotic "irrational use"',
    # Query 14: Inappropriate use
    '"community pharmacy" antibiotic "inappropriate use"',
]

def search_openalex(query, per_page=200, page=1):
    """Search OpenAlex and return works."""
    params = urllib.parse.urlencode({
        "search": query,
        "per_page": per_page,
        "page": page,
        "mailto": "research@example.com",
    })
    url = f"{BASE_URL}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "MetaAnalysis/1.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data
    except Exception as e:
        print(f"    Error: {e}")
        return None

def extract_article(work):
    """Extract article info from OpenAlex work object."""
    # OpenAlex ID
    oa_id = work.get("id", "").replace("https://openalex.org/", "")
    
    # Title
    title = work.get("title", "") or ""
    
    # Year
    year = str(work.get("publication_year", ""))
    
    # Authors
    authorships = work.get("authorships", [])
    authors = []
    for a in authorships[:5]:
        name = a.get("author", {}).get("display_name", "")
        if name:
            authors.append(name)
    author_str = "; ".join(authors)
    if len(authorships) > 5:
        author_str += " et al."
    
    # Journal
    source = work.get("primary_location", {}) or {}
    source_obj = source.get("source", {}) or {}
    journal = source_obj.get("display_name", "")
    
    # DOI
    doi = work.get("doi", "") or ""
    doi = doi.replace("https://doi.org/", "")
    
    # Abstract (OpenAlex inverted index → reconstruct)
    abstract = ""
    abstract_inv = work.get("abstract_inverted_index", None)
    if abstract_inv:
        try:
            # Reconstruct from inverted index
            word_positions = []
            for word, positions in abstract_inv.items():
                for pos in positions:
                    word_positions.append((pos, word))
            word_positions.sort()
            abstract = " ".join([w for _, w in word_positions])
            if len(abstract) > 500:
                abstract = abstract[:497] + "..."
        except:
            abstract = ""
    
    return {
        "oa_id": oa_id,
        "author": author_str,
        "year": year,
        "title": title,
        "journal": journal,
        "doi": doi,
        "abstract_snippet": abstract,
    }

def main():
    print("=" * 60)
    print("OpenAlex Search (Scopus Alternative)")
    print("Meta-Analysis PINMAS IV 2026 — Protocol V1.1")
    print("=" * 60)
    print()
    
    all_works = {}  # doi -> article (for dedup)
    
    for i, query in enumerate(QUERIES, 1):
        print(f"[Query {i}/{len(QUERIES)}] '{query[:60]}...'")
        
        # Fetch up to 2 pages (400 results) per query
        for page in range(1, 3):
            data = search_openalex(query, per_page=200, page=page)
            if not data:
                break
            
            results = data.get("results", [])
            total = data.get("meta", {}).get("count", 0)
            
            if page == 1:
                print(f"    Total matches: {total}")
            
            for work in results:
                doi = work.get("doi", "") or ""
                oa_id = work.get("id", "")
                
                # Use DOI for dedup if available, otherwise OpenAlex ID
                key = doi if doi else oa_id
                if key and key not in all_works:
                    article = extract_article(work)
                    all_works[key] = article
            
            if len(results) < 200:
                break  # No more pages
            
            time.sleep(0.2)
        
        time.sleep(0.3)
    
    print()
    print(f"Total unique works found: {len(all_works)}")
    
    # Save to CSV
    print(f"Saving to {OUTPUT_CSV}...")
    articles = list(all_works.values())
    
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "record_id", "database_source", "oa_id", "author", "year",
            "title", "journal", "doi", "abstract_snippet",
            "duplicate_of", "ta_decision", "ta_exclusion_reason",
            "ft_available", "ft_decision", "ft_exclusion_reason",
            "included_in_review", "notes"
        ])
        
        for idx, art in enumerate(articles, 1):
            writer.writerow([
                f"OA-{idx:04d}",
                "OpenAlex",
                art["oa_id"],
                art["author"],
                art["year"],
                art["title"],
                art["journal"],
                art["doi"],
                art["abstract_snippet"],
                "", "", "", "", "", "", "", ""
            ])
    
    print(f"Saved {len(articles)} records.")
    print()
    print("=" * 60)
    print(f"SEARCH COMPLETE")
    print(f"Unique articles: {len(articles)}")
    print(f"Output: {OUTPUT_CSV}")
    print("=" * 60)

if __name__ == "__main__":
    main()
