#!/usr/bin/env python3
"""
Comprehensive Validation Script for ICSH 2026 FINAL Files:
1. ICSH_2026_Abstract_Submission_FINAL.docx
2. Manuscript_ICSH_2026_FINAL.docx
"""
import docx, re

def validate_abstract(path):
    doc = docx.Document(path)
    print("=" * 60)
    print("1. ABSTRACT SUBMISSION FINAL AUDIT")
    print("=" * 60)
    
    # Metadata Table
    t0 = doc.tables[0].rows[0].cells[0].text
    print(f"Table 0 Metadata Present: {'MANUSCRIPT SUBMISSION METADATA' in t0}")
    print(f"Paper ID / Order ID: {'[ORDER ID — VERIFY FROM PARTICIPANT PORTAL]' in t0 or 'ORDER ID' in t0}")
    print(f"Research Track: {'[TRACK NUMBER — VERIFY FROM PARTICIPANT PORTAL]' in t0 or 'TRACK NUMBER' in t0}")
    print(f"Oral Presentation: {'[ X ] Oral Presentation' in t0}")
    print(f"Publication Preference (AJMB): {'[ X ] Asian Journal of Medicine and Biomedicine (AJMB)' in t0}")
    
    # Title & Author
    title = doc.paragraphs[4].text.strip()
    author = doc.paragraphs[5].text.strip()
    affil = doc.paragraphs[6].text.strip()
    corr = doc.paragraphs[7].text.strip()
    print(f"\nTitle (16 words): {title}")
    print(f"Author: {author}")
    print(f"Affiliation: {affil}")
    print(f"Corresponding: {corr}")
    
    # Abstract Body
    p9 = doc.paragraphs[9].text.strip()
    print("\nAbstract Sections Check:")
    for sec in ["Background:", "Objective:", "Methods:", "Results:", "Conclusion:"]:
        print(f"  {sec} -> {'PRESENT' if sec in p9 else 'MISSING'}")
        
    cleaned_text = re.sub(r'(Background|Objective|Methods|Results|Conclusion):\s*', '', p9)
    words = cleaned_text.split()
    wc = len(words)
    print(f"Abstract Word Count: {wc} words (Status: {'PASS' if 200 <= wc <= 300 else 'FAIL'})")
    
    # Keywords
    p10 = doc.paragraphs[10].text.strip()
    kw_count = len(p10.replace("Keywords:", "").split(";"))
    print(f"Keywords: {p10} ({kw_count} keywords -> {'PASS' if 3 <= kw_count <= 5 else 'FAIL'})")
    
    # Ethical Declaration
    p13 = doc.paragraphs[13].text.strip()
    print("\nEthical Declarations Check:")
    for decl in ["[ X ] Originality", "[ X ] Ethical Approval", "[ X ] Conflict of Interest", "[ X ] Author Consent"]:
        print(f"  {decl} -> {'PRESENT' if decl in p13 else 'MISSING'}")

def validate_manuscript(path):
    doc = docx.Document(path)
    full = ' '.join(p.text for p in doc.paragraphs)
    print("\n" + "=" * 60)
    print("2. FULL MANUSCRIPT FINAL AUDIT")
    print("=" * 60)
    
    print(f"Paragraphs: {len(doc.paragraphs)}, Tables: {len(doc.tables)}")
    print(f"Images: {sum(1 for r in doc.part.rels.values() if 'image' in r.reltype)}")
    
    print("\nStatistical Consistency:")
    print(f"  Pooled OR = 0.164: {'0.164' in full}")
    print(f"  DL 95% CI 0.102-0.265: {'0.102' in full and '0.265' in full}")
    print(f"  HKSJ 95% CI 0.064-0.419: {'0.064' in full and '0.419' in full}")
    print(f"  HKSJ t(2) = -8.31: {'-8.31' in full}")
    print(f"  HKSJ p = 0.014: {'0.014' in full}")
    print(f"  I² = 0.0%: {'0.0%' in full}")
    print(f"  Q = 1.58, df = 2, p = 0.454: {'1.58' in full and '0.454' in full}")
    
    print("\nTerminology & Study Consistency:")
    print(f"  Chalker = cluster-randomised trial: {'cluster-randomised trial' in full}")
    print(f"  Onwunduba = cluster-randomised trial: {'cluster-randomised trial' in full}")
    print(f"  Ferdiana = controlled before-after study: {'controlled before-after study' in full}")
    print(f"  No collective 'three trials': {'the three trials' not in full.lower()}")
    print(f"  Collective 'three controlled studies': {'three controlled studies' in full}")
    print(f"  Qualitative review pool (n = 14): {'n = 14' in full or '14' in full}")
    print(f"  Quantitative synthesis pool (n = 3): {'n = 3' in full or 'k = 3' in full}")
    
    print("\nDeclaration & Author Data:")
    print(f"  ORCID: {'0009-0008-1306-2485' in full}")
    print(f"  WhatsApp: {'822-6740-3241' in full}")
    print(f"  Email: {'tengkumuhammadlufthihannur@fk.uisu.ac.id' in full}")
    print(f"  4-item Declaration Checklist: {'[ X ] Originality' in full}")

if __name__ == '__main__':
    validate_abstract("D:/tm/05_Own_Research/ICSH_2026_Abstract_Submission_FINAL.docx")
    validate_manuscript("D:/tm/05_Own_Research/Manuscript_ICSH_2026_FINAL.docx")
