"""
Auto Pre-Screening Filter Round 2 — Handle Unresolved Records
For records with no/minimal abstract, apply title-only filtering
+ broader pattern catch
"""
import pandas as pd
import re

INPUT_FILE = r"d:\tm\05_Own_Research\Data\master_screening_database.csv"
OUTPUT_FILE = r"d:\tm\05_Own_Research\Data\master_screening_database.csv"

df = pd.read_csv(INPUT_FILE, dtype=str, encoding='utf-8-sig')
df = df.fillna("")

unresolved = df[df['ta_decision'] == ""]
print(f"Unresolved records to process: {len(unresolved)}")

# ─────────────────────────────────────────────────────────────
# ROUND 2 PATTERNS (broader, safe to apply when title-only)
# ─────────────────────────────────────────────────────────────

# E-Hospital extended (title-level)
hospital_title = [
    r'\bhospital\b', r'\binpatient\b', r'\bICU\b', r'\bintensive care\b',
    r'\bemergency\b', r'\bward\b', r'\bteaching\b',
    r'\boutpatient\b', r'\bsurgical\b', r'\bneonatal\b',
    r'\bclinic\b(?!al pharmacy)', r'\bprimary care\b',
    r'\bhealth center\b', r'\bhealth centre\b',
]

# E-HIC extended
hic_title = [
    r'\bCroatia\b', r'\bFrance\b', r'\bFrench\b',
    r'\bGermany\b', r'\bGerman\b', r'\bItaly\b', r'\bItalian\b',
    r'\bSpain\b', r'\bSpanish\b', r'\bPortugal\b', r'\bNetherland\b',
    r'\bBelgium\b', r'\bSweden\b', r'\bNorway\b', r'\bDenmark\b',
    r'\bFinland\b', r'\bAustria\b', r'\bSwitzerland\b',
    r'\bUnited Kingdom\b', r'\bEngland\b', r'\bScotland\b',
    r'\bAustralia\b', r'\bNew Zealand\b', r'\bCanada\b',
    r'\bUnited States\b', r'\bAmerican\b', r'\bJapan\b',
    r'\bSouth Korea\b', r'\bSingapore\b', r'\bIsrael\b',
    r'\bGreece\b', r'\bPoland\b', r'\bCzech\b', r'\bHungary\b',
    r'\bRomania\b', r'\bBulgaria\b', r'\bSlovakia\b',
    r'\bMexico\b', r'\bArgentina\b', r'\bBrazil\b', r'\bChile\b',
    r'\bTurkey\b', r'\bTurkiye\b',
]

# E-Review extended (title-level)
review_title = [
    r'\bsystematic review\b', r'\bmeta-analysis\b', r'\bscoping review\b',
    r'\bnarrative review\b', r'\bliterature review\b',
    r'\bqualitative\b', r'\bfocus group\b', r'\bgrounded theory\b',
    r'\bthematic analysis\b', r'\bethnograph\b',
    r'\bcommentary\b', r'\beditorial\b',
    r'\bletter\b.{0,20}\beditor\b',
    r'\bstudy protocol\b', r'\bprotocol for\b',
    r'\bscoping\b', r'\brapid review\b', r'\bintegrative review\b',
]

# E-Irrelevant extended (title-level)
irrel_title = [
    r'\bcurriculum\b', r'\beducation\b.{0,30}\bmedical\b',
    r'\bvaccin\b', r'\bimmuniz\b',
    r'\bCOVID\b', r'\bcoronavirus\b', r'\bSARS-CoV\b',
    r'\bin vitro\b', r'\bin vivo\b', r'\bmurine\b', r'\bmouse\b',
    r'\brat model\b', r'\banimal\b', r'\bzebrafish\b',
    r'\bprescription audit\b', r'\bdrug interaction\b.{0,20}software',
    r'\bHIV\b.{0,30}(?:treatment|antiretroviral|ARV)',
    r'\btuberculosis\b(?!.{0,100}antibiotic)',
    r'\bTB\b.{0,30}(?:treatment|DOTs)',
    r'\bmalaria\b(?!.{0,100}antibiotic)',
    r'\bpharmaceutical supply chain\b',
    r'\bpharmacogenomics\b', r'\bpharmacovigilan\b',
    r'\bdrug delivery\b', r'\bnanoparticle\b',
    r'\bdrug pricing\b', r'\bcost.effectiveness\b.{0,30}(?:model|economic)',
    r'\bprescribing pattern\b.{0,30}(?:hospital|clinic|physician|doctor)',
    r'\bGPS\b.{0,20}mapping\b', r'\bgeospatial\b.{0,30}(?!pharmacy)',
    r'\bwater quality\b', r'\bsanitation\b',
    r'\bchildhood obesity\b', r'\bdiabetes\b', r'\bhypertension\b',
    r'\bcardiovascular\b', r'\bcancer\b', r'\boncology\b',
    r'\bdental\b', r'\bodontology\b', r'\bophthalm\b',
    r'\bdermatology\b', r'\bdermatit\b',
    r'\bphysical therapy\b', r'\brehabilitation\b',
    r'\bnursing home\b', r'\blog-term care\b',
    r'\btelehealth\b', r'\btelemedicine\b',
]

# MAYBE signals — things that MIGHT be relevant (keep for manual review)
maybe_title = [
    r'non.?prescription.{0,40}antibiotic',
    r'antibiotic.{0,40}without.{0,20}prescription',
    r'antibiotic.{0,40}dispensing.{0,50}(?:pharma|shop|outlet|vendor)',
    r'(?:pharma|shop|outlet|vendor).{0,50}antibiotic.{0,40}dispensing',
    r'over.the.counter.{0,40}antibiotic',
    r'antibiotic.{0,40}over.the.counter',
    r'self.medication.{0,40}antibiotic',
    r'antibiotic.{0,40}self.medication',
    r'stewardship.{0,50}(?:pharma|community)',
    r'community.{0,20}pharma.{0,100}(?:interven|program|train|education)',
    r'pharma.{0,50}(?:interven|program|train|education).{0,100}antibiotic',
    r'simulated.{0,20}(?:client|patient)',
    r'mystery.{0,10}shopper',
    r'drug.{0,10}(?:shop|outlet|vendor).{0,50}antibiotic',
    r'medicine.{0,10}(?:shop|store|vendor).{0,50}antibiotic',
    r'dispensing.{0,30}practice.{0,50}(?:pharma|LMIC|low)',
    r'antibiotic.{0,30}(?:use|misuse|overuse|irrational|inappropriate).{0,50}(?:pharma|community)',
    r'antimicrobial.{0,30}resistance.{0,50}pharma',
    r'(?:pharma|shop|outlet).{0,50}LMIC',
    r'(?:pharma|shop|outlet).{0,50}low.{0,10}(?:income|resource)',
    r'(?:pharma|shop|outlet).{0,50}developing.{0,20}countr',
    r'(?:pharma|shop|outlet).{0,50}Africa',
    r'(?:pharma|shop|outlet).{0,50}Asia',
    r'(?:pharma|shop|outlet).{0,50}(?:Nigeria|Uganda|Ethiopia|Kenya|Ghana|Tanzania|Zambia|Zimbabwe)',
    r'(?:pharma|shop|outlet).{0,50}(?:Indonesia|Bangladesh|Pakistan|Nepal|Cambodia|Vietnam|Myanmar|Philippines)',
    r'(?:pharma|shop|outlet).{0,50}(?:India|Sri Lanka)',
    r'AMR.{0,50}pharma',
    r'patent.{0,10}medicine.{0,20}vendor',
    r'drug.{0,10}seller',
]

def match(text, patterns):
    for p in patterns:
        try:
            if re.search(p, text, re.IGNORECASE):
                return True
        except:
            pass
    return False

counts2 = {'maybe': 0, 'excl_hospital': 0, 'excl_hic': 0,
           'excl_review': 0, 'excl_irrel': 0, 'still_unresolved': 0}

for idx, row in df.iterrows():
    if row['ta_decision'] != "":
        continue

    title_text = str(row['title'])
    full_text = f"{title_text} {row['abstract_snippet']}"

    # Check MAYBE first (if title strongly matches relevant pattern)
    if match(title_text, maybe_title):
        df.at[idx, 'ta_decision'] = 'Maybe'
        df.at[idx, 'notes'] = '[AUTO-R2] Title match - verify'
        counts2['maybe'] += 1
        continue

    # Exclusions on title+abstract
    if match(full_text, irrel_title):
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'Irrelevant topic'
        counts2['excl_irrel'] += 1
        continue

    if match(full_text, review_title):
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'Review/qualitative/editorial'
        counts2['excl_review'] += 1
        continue

    if match(full_text, hic_title):
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'High-income country (HIC)'
        counts2['excl_hic'] += 1
        continue

    if match(full_text, hospital_title):
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'Hospital/inpatient/clinic setting'
        counts2['excl_hospital'] += 1
        continue

    counts2['still_unresolved'] += 1

print("\nROUND 2 RESULTS:")
print(f"  Maybe (title signal):    {counts2['maybe']}")
print(f"  Excl Hospital:           {counts2['excl_hospital']}")
print(f"  Excl HIC:                {counts2['excl_hic']}")
print(f"  Excl Review/Qualitative: {counts2['excl_review']}")
print(f"  Excl Irrelevant:         {counts2['excl_irrel']}")
print(f"  Still unresolved:        {counts2['still_unresolved']}")

print("\nFINAL DECISION SUMMARY:")
ta_counts = df['ta_decision'].value_counts()
total = len(df)
for decision, count in ta_counts.items():
    label = decision if decision else "(blank/unresolved)"
    pct = 100*count/total
    print(f"  {label}: {count} ({pct:.1f}%)")

df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
print(f"\nSaved to: {OUTPUT_FILE}")
