"""Fetch remaining PubMed records (501-689)"""
import urllib.request, urllib.parse, xml.etree.ElementTree as ET, csv, time, json, sys
sys.stdout.reconfigure(encoding='utf-8')

QUERY = (
    '("Community Pharmacy Services"[MeSH Terms] OR "Pharmacies"[MeSH Terms] '
    'OR "community pharmacy"[tiab] OR "community pharmacies"[tiab] '
    'OR "community pharmacist"[tiab] OR "community pharmacists"[tiab] '
    'OR "drug store"[tiab] OR "drug stores"[tiab] '
    'OR "drug shop"[tiab] OR "drug shops"[tiab] '
    'OR "drug outlet"[tiab] OR "drug outlets"[tiab] '
    'OR "drug retail"[tiab] OR "retail pharmacy"[tiab] OR "retail pharmacies"[tiab] '
    'OR "private pharmacy"[tiab] OR "private pharmacies"[tiab] '
    'OR "medicine shop"[tiab] OR "medicine shops"[tiab] '
    'OR "medicine store"[tiab] OR "medicine stores"[tiab] '
    'OR "pharmaceutical outlet"[tiab] '
    'OR "patent medicine"[tiab] OR "patent medicine vendor"[tiab]) '
    'AND '
    '("Anti-Bacterial Agents"[MeSH Terms] OR antibiotic[tiab] OR antibiotics[tiab] '
    'OR antimicrobial[tiab] OR antimicrobials[tiab] '
    'OR anti-bacterial[tiab] OR antibacterial[tiab]) '
    'AND '
    '("Nonprescription Drugs"[MeSH Terms] OR "Drug Dispensing"[tiab] '
    'OR "non-prescription"[tiab] OR "nonprescription"[tiab] '
    'OR "without prescription"[tiab] OR "without a prescription"[tiab] '
    'OR "over-the-counter"[tiab] OR "over the counter"[tiab] '
    'OR "OTC"[tiab] OR dispensing[tiab] '
    'OR "self-medication"[tiab] OR "self medication"[tiab] '
    'OR "inappropriate use"[tiab] OR "irrational use"[tiab] '
    'OR sale[tiab] OR sales[tiab] OR selling[tiab])'
)

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# Search with retstart=500
params = urllib.parse.urlencode({
    "db": "pubmed", "term": QUERY,
    "retmax": 200, "retstart": 500, "retmode": "json"
})
req = urllib.request.Request(f"{BASE}/esearch.fcgi?{params}", headers={"User-Agent": "MA/1.0"})
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.loads(r.read().decode("utf-8"))

remaining_pmids = data["esearchresult"]["idlist"]
print(f"Remaining PMIDs to fetch: {len(remaining_pmids)}")

if remaining_pmids:
    params2 = urllib.parse.urlencode({
        "db": "pubmed", "id": ",".join(remaining_pmids),
        "retmode": "xml", "rettype": "abstract"
    })
    req2 = urllib.request.Request(f"{BASE}/efetch.fcgi?{params2}", headers={"User-Agent": "MA/1.0"})
    with urllib.request.urlopen(req2, timeout=60) as r2:
        xml_data = r2.read().decode("utf-8")
    root = ET.fromstring(xml_data)

    articles = []
    for art in root.findall(".//PubmedArticle"):
        pmid = art.findtext(".//PMID", "")
        title = art.findtext(".//ArticleTitle", "")
        authors = []
        for a in art.findall(".//Author"):
            ln = a.findtext("LastName", "")
            fn = a.findtext("ForeName", "")
            if ln:
                authors.append(f"{ln} {fn}".strip())
        author_str = "; ".join(authors[:5])
        if len(authors) > 5:
            author_str += " et al."
        year = art.findtext(".//PubDate/Year", "")
        if not year:
            md = art.findtext(".//PubDate/MedlineDate", "")
            if md:
                year = md[:4]
        journal = art.findtext(".//ISOAbbreviation", "") or art.findtext(".//Journal/Title", "")
        doi = ""
        for aid in art.findall(".//ArticleId"):
            if aid.get("IdType") == "doi":
                doi = aid.text or ""
                break
        if not doi:
            for eid in art.findall(".//ELocationID"):
                if eid.get("EIdType") == "doi":
                    doi = eid.text or ""
                    break
        abs_parts = []
        for at in art.findall(".//AbstractText"):
            lb = at.get("Label", "")
            tx = at.text or ""
            abs_parts.append(f"{lb}: {tx}" if lb else tx)
        abstract = " ".join(abs_parts)[:500]
        articles.append([pmid, author_str, year, title, journal, doi, abstract])

    with open(r"d:\tm\05_Own_Research\Data\pubmed_search_results.csv", "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        for idx, a in enumerate(articles, 501):
            writer.writerow([f"PM-{idx:04d}", "PubMed", a[0], a[1], a[2], a[3], a[4], a[5], a[6],
                             "", "", "", "", "", "", "", ""])
    print(f"Appended {len(articles)} records. Total should now be ~{500 + len(articles)}")
else:
    print("No remaining records.")
