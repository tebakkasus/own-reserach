"""
PubMed Search Script — Meta-Analysis PINMAS IV 2026
Search Protocol V1.1 — 3-Block Strategy
"""
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import csv
import time
import json
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# === SEARCH QUERY (3-block, no Block D) ===
QUERY = """
(
  "Community Pharmacy Services"[MeSH Terms]
  OR "Pharmacies"[MeSH Terms]
  OR "community pharmacy"[tiab]
  OR "community pharmacies"[tiab]
  OR "community pharmacist"[tiab]
  OR "community pharmacists"[tiab]
  OR "drug store"[tiab]
  OR "drug stores"[tiab]
  OR "drug shop"[tiab]
  OR "drug shops"[tiab]
  OR "drug outlet"[tiab]
  OR "drug outlets"[tiab]
  OR "drug retail"[tiab]
  OR "retail pharmacy"[tiab]
  OR "retail pharmacies"[tiab]
  OR "private pharmacy"[tiab]
  OR "private pharmacies"[tiab]
  OR "medicine shop"[tiab]
  OR "medicine shops"[tiab]
  OR "medicine store"[tiab]
  OR "medicine stores"[tiab]
  OR "pharmaceutical outlet"[tiab]
  OR "patent medicine"[tiab]
  OR "patent medicine vendor"[tiab]
)
AND
(
  "Anti-Bacterial Agents"[MeSH Terms]
  OR antibiotic[tiab]
  OR antibiotics[tiab]
  OR antimicrobial[tiab]
  OR antimicrobials[tiab]
  OR anti-bacterial[tiab]
  OR antibacterial[tiab]
)
AND
(
  "Nonprescription Drugs"[MeSH Terms]
  OR "Drug Dispensing"[tiab]
  OR "non-prescription"[tiab]
  OR "nonprescription"[tiab]
  OR "without prescription"[tiab]
  OR "without a prescription"[tiab]
  OR "over-the-counter"[tiab]
  OR "over the counter"[tiab]
  OR "OTC"[tiab]
  OR dispensing[tiab]
  OR "self-medication"[tiab]
  OR "self medication"[tiab]
  OR "inappropriate use"[tiab]
  OR "irrational use"[tiab]
  OR sale[tiab]
  OR sales[tiab]
  OR selling[tiab]
)
""".strip().replace("\n", " ").replace("  ", " ")

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUTPUT_CSV = r"d:\tm\05_Own_Research\Data\pubmed_search_results.csv"

def search_pubmed(query, retmax=500):
    """Search PubMed and return list of PMIDs."""
    params = urllib.parse.urlencode({
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json",
        "usehistory": "y"
    })
    url = f"{BASE_URL}/esearch.fcgi?{params}"
    print(f"[1/3] Searching PubMed...")
    
    req = urllib.request.Request(url, headers={"User-Agent": "MetaAnalysis/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))
    
    result = data["esearchresult"]
    count = int(result["count"])
    pmids = result["idlist"]
    webenv = result.get("webenv", "")
    query_key = result.get("querykey", "")
    
    print(f"    Total results: {count}")
    print(f"    PMIDs retrieved: {len(pmids)}")
    
    return pmids, count, webenv, query_key

def fetch_details(pmids, batch_size=50):
    """Fetch article details for a list of PMIDs."""
    articles = []
    total = len(pmids)
    
    for i in range(0, total, batch_size):
        batch = pmids[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size
        print(f"[2/3] Fetching details... batch {batch_num}/{total_batches}")
        
        params = urllib.parse.urlencode({
            "db": "pubmed",
            "id": ",".join(batch),
            "retmode": "xml",
            "rettype": "abstract"
        })
        url = f"{BASE_URL}/efetch.fcgi?{params}"
        
        req = urllib.request.Request(url, headers={"User-Agent": "MetaAnalysis/1.0"})
        with urllib.request.urlopen(req, timeout=60) as response:
            xml_data = response.read().decode("utf-8")
        
        root = ET.fromstring(xml_data)
        
        for article in root.findall(".//PubmedArticle"):
            try:
                pmid = article.findtext(".//PMID", "")
                title = article.findtext(".//ArticleTitle", "")
                
                # Authors
                authors = []
                for author in article.findall(".//Author"):
                    last = author.findtext("LastName", "")
                    first = author.findtext("ForeName", "")
                    if last:
                        authors.append(f"{last} {first}".strip())
                author_str = "; ".join(authors[:5])
                if len(authors) > 5:
                    author_str += " et al."
                
                # Year
                year = article.findtext(".//PubDate/Year", "")
                if not year:
                    medline_date = article.findtext(".//PubDate/MedlineDate", "")
                    if medline_date:
                        year = medline_date[:4]
                
                # Journal
                journal = article.findtext(".//Journal/Title", "")
                journal_abbr = article.findtext(".//ISOAbbreviation", "")
                
                # DOI
                doi = ""
                for aid in article.findall(".//ArticleId"):
                    if aid.get("IdType") == "doi":
                        doi = aid.text or ""
                        break
                if not doi:
                    for eid in article.findall(".//ELocationID"):
                        if eid.get("EIdType") == "doi":
                            doi = eid.text or ""
                            break
                
                # Abstract
                abstract_parts = []
                for abs_text in article.findall(".//AbstractText"):
                    label = abs_text.get("Label", "")
                    text = abs_text.text or ""
                    if label:
                        abstract_parts.append(f"{label}: {text}")
                    else:
                        abstract_parts.append(text)
                abstract = " ".join(abstract_parts)
                
                # Truncate abstract for CSV
                if len(abstract) > 500:
                    abstract_snippet = abstract[:497] + "..."
                else:
                    abstract_snippet = abstract
                
                articles.append({
                    "pmid": pmid,
                    "author": author_str,
                    "year": year,
                    "title": title,
                    "journal": journal_abbr or journal,
                    "doi": doi,
                    "abstract_snippet": abstract_snippet
                })
            except Exception as e:
                print(f"    Warning: Could not parse article: {e}")
                continue
        
        # Rate limiting
        if i + batch_size < total:
            time.sleep(0.5)
    
    return articles

def save_to_csv(articles, filepath):
    """Save articles to screening CSV."""
    print(f"[3/3] Saving to {filepath}...")
    
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "record_id", "database_source", "pmid", "author", "year", 
            "title", "journal", "doi", "abstract_snippet",
            "duplicate_of", "ta_decision", "ta_exclusion_reason",
            "ft_available", "ft_decision", "ft_exclusion_reason",
            "included_in_review", "notes"
        ])
        
        for idx, art in enumerate(articles, 1):
            writer.writerow([
                f"PM-{idx:04d}",
                "PubMed",
                art["pmid"],
                art["author"],
                art["year"],
                art["title"],
                art["journal"],
                art["doi"],
                art["abstract_snippet"],
                "", "", "", "", "", "", "", ""
            ])
    
    print(f"    Saved {len(articles)} records.")

def main():
    print("=" * 60)
    print("PubMed Search — Meta-Analysis PINMAS IV 2026")
    print("Protocol V1.1 — 3-Block Strategy")
    print("=" * 60)
    print()
    
    # Step 1: Search
    pmids, total_count, webenv, query_key = search_pubmed(QUERY)
    
    if not pmids:
        print("No results found. Check your search query.")
        return
    
    # Step 2: Fetch details
    articles = fetch_details(pmids)
    
    # Step 3: Save
    save_to_csv(articles, OUTPUT_CSV)
    
    print()
    print("=" * 60)
    print(f"SEARCH COMPLETE")
    print(f"Total PubMed results: {total_count}")
    print(f"Articles retrieved: {len(articles)}")
    print(f"Output: {OUTPUT_CSV}")
    print("=" * 60)

if __name__ == "__main__":
    main()
