"""
Auto Pre-Screening Filter — Meta-Analysis PINMAS IV 2026
Search Protocol V1.1

Rules (from eligibility criteria):
- EXCLUDE: hospital / clinic setting
- EXCLUDE: HIC countries (Europe, Australia, USA, Canada, etc.) -- unless can't determine from title/abstract
- EXCLUDE: qualitative only / reviews / editorials / comments
- EXCLUDE: animal / in vitro studies
- EXCLUDE: non-antibiotic (antifungal, antiviral, antiparasitic only)
- EXCLUDE: pediatric ward / ICU (inpatient)
- EXCLUDE: COVID-only (unless antibiotic dispensing is an outcome)
- MAYBE: pharmacy dispensing in LMIC, no clear intervention
- INCLUDE: clear intervention study in community pharmacy/outlet reducing NPD
"""

import pandas as pd
import re

INPUT_FILE = r"d:\tm\05_Own_Research\Data\master_screening_database.csv"
OUTPUT_FILE = r"d:\tm\05_Own_Research\Data\master_screening_database.csv"

print("=" * 60)
print("AUTO PRE-SCREENING FILTER")
print("Protocol V1.1 — PINMAS IV 2026")
print("=" * 60)

df = pd.read_csv(INPUT_FILE, dtype=str, encoding='utf-8-sig')
df = df.fillna("")
total = len(df)
print(f"\nLoaded {total} records for filtering.\n")

# ─────────────────────────────────────────────────────────────
# EXCLUSION KEYWORD LISTS
# ─────────────────────────────────────────────────────────────

# E1: Hospital / inpatient setting (not community pharmacy)
hospital_terms = [
    r'\bhospital\b', r'\binpatient\b', r'\bICU\b', r'\bintensive care\b',
    r'\bemergency department\b', r'\bED\b', r'\bward\b', r'\bclinical pharmacy\b',
    r'\bhospital pharmacy\b', r'\bhospital pharmacist\b',
    r'\bsurgical ward\b', r'\bpediatric ward\b', r'\bneonatal\b',
    r'\bteaching hospital\b', r'\btertiary hospital\b', r'\btertiary care\b',
    r'\bsecondary care\b', r'\boutpatient clinic\b', r'\bhealth centre\b',
    r'\bprimary health cent(?:re|er)\b', r'\bclinician\b',
    r'\bprescription review\b.{0,50}hospital',
]

# E2: High-income country setting (clearly HIC)
hic_terms = [
    r'\bCroatia\b', r'\bFrance\b', r'\bFrench\b', r'\bGermany\b', r'\bGerman\b',
    r'\bItaly\b', r'\bItalian\b', r'\bSpain\b', r'\bSpanish\b',
    r'\bPortugal\b', r'\bPortuguese\b', r'\bNetherlands\b', r'\bDutch\b',
    r'\bBelgium\b', r'\bSweden\b', r'\bSwedish\b', r'\bNorway\b', r'\bNorwegian\b',
    r'\bDenmark\b', r'\bFinland\b', r'\bAustria\b', r'\bSwitzerland\b',
    r'\bUnited Kingdom\b', r'\bUK\b', r'\bEngland\b', r'\bScotland\b',
    r'\bWales\b', r'\bIreland\b', r'\bAustralia\b', r'\bAustralian\b',
    r'\bNew Zealand\b', r'\bCanada\b', r'\bCanadian\b',
    r'\bUnited States\b', r'\bUSA\b', r'\bAmerican\b',
    r'\bJapan\b', r'\bJapanese\b', r'\bSouth Korea\b', r'\bKorean\b',
    r'\bSingapore\b', r'\bIsrael\b', r'\bGreece\b', r'\bCzech\b',
    r'\bPoland\b', r'\bHungary\b', r'\bSlovakia\b', r'\bSlovenia\b',
]

# E3: Qualitative / review / editorial / commentary
review_terms = [
    r'\bsystematic review\b', r'\bmeta-analysis\b', r'\bscoping review\b',
    r'\bnarrative review\b', r'\bliterature review\b',
    r'\bqualitative study\b', r'\bqualitative research\b',
    r'\bqualitative interview\b', r'\bfocus group\b',
    r'\beditori(?:al)?\b', r'\bcommentary\b', r'\bletter to\b',
    r'\bcomment on\b', r'\bopinion\b.{0,30}\bpharma',
    r'\bprotocol\b.{0,40}\bstudy\b', r'\bstudy protocol\b',
    r'\bsynthesis\b.{0,40}\bqualitative\b',
]

# E4: Animal / lab / in vitro
lab_terms = [
    r'\bin vitro\b', r'\bin vivo\b', r'\bmouse\b', r'\bmice\b', r'\brat\b',
    r'\banimal model\b', r'\bmurine\b', r'\bzebrafish\b',
    r'\bcell culture\b', r'\bbacteria\b.{0,30}\bculture\b',
    r'\bmicrobiology\b', r'\bMIC\b.{0,20}\bminimum inhibitory\b',
]

# E5: Non-antibiotic antimicrobials ONLY (antifungal, antiviral, antiparasitic)
non_ab_terms = [
    r'\bantifungal\b(?!.{0,200}antibiotic)',
    r'\bantiviral\b(?!.{0,200}antibiotic)',
    r'\bantiparasitic\b(?!.{0,200}antibiotic)',
    r'\bHIV\b.{0,50}\bdrug\b(?!.{0,300}antibiotic)',
    r'\bmalaria\b(?!.{0,200}antibiotic)',
]

# E6: Irrelevant topics (clearly not pharmacy dispensing)
irrelevant_terms = [
    r'\bcurriculuum\b', r'\bgreening\b', r'\benvironmental sustainab\b',
    r'\bPDCA cycle\b', r'\bprescription audit system\b.{0,30}China',
    r'\bchildhood vaccination\b', r'\bimmunisation\b',
    r'\bcoronavirus\b(?!.{0,200}antibiotic)',
    r'\bCOVID-19\b(?!.{0,200}antibiotic)',
    r'\bpre-prescription audit\b', r'\bintelligent decision system\b',
    r'\bpharmaceutical education\b', r'\bcurriculum\b',
    r'\bwater sanitation\b', r'\benvironmental pollution\b',
    r'\bpediatric rational medication\b',
    r'\botitis media\b', r'\bpharyngitis\b',  # specific clinical conditions not NPD
]

# ─────────────────────────────────────────────────────────────
# INCLUSION SIGNALS — strong evidence this is a relevant paper
# ─────────────────────────────────────────────────────────────
strong_include_terms = [
    r'\bintervention\b.{0,100}\bcommunity pharma',
    r'\bsimulated client\b',
    r'\bmystery shopper\b',
    r'\bcluster.{0,10}randomized\b', r'\bcluster.{0,10}randomised\b',
    r'\bcluster.{0,10}RCT\b',
    r'\bC-reactive protein\b.{0,100}\bpharmac',
    r'\bCRP.{0,50}pharma\b',
    r'\baudit.{0,20}feedback.{0,100}\bpharmac',
    r'\bpeer.{0,10}visit.{0,100}\bpharmac',
    r'\btraining.{0,100}\bpharmac.{0,100}\bantibiotic\b',
    r'\beducation.{0,100}\bpharmac.{0,100}\bantibiotic\b',
    r'\bnon.prescription antibiotic dispensing\b',
    r'\bNPD\b.{0,100}\bpharmac',
    r'\bDAwP\b',  # Dispensing Antibiotics without Prescription
]

# MAYBE signal — descriptive study, might be useful for background
maybe_terms = [
    r'\bprevalence\b.{0,100}\bnon.prescription\b',
    r'\bcross.sectional\b.{0,100}\bpharmac\b',
    r'\bknowledge.{0,30}attitude\b.{0,100}\bpharmac\b',
    r'\bsurvey\b.{0,100}\bpharmac\b.{0,100}\bantibiotic\b',
    r'\bdispensi.{0,20}\bpractice\b.{0,100}\bpharmac\b',
]

# ─────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────

def check_patterns(text, patterns, flags=re.IGNORECASE):
    for p in patterns:
        try:
            if re.search(p, text, flags):
                return True
        except:
            continue
    return False

counts = {
    'Exclude_Hospital': 0,
    'Exclude_HIC': 0,
    'Exclude_Review_Qualitative': 0,
    'Exclude_Lab_Animal': 0,
    'Exclude_Irrelevant': 0,
    'Include_Strong': 0,
    'Maybe': 0,
    'Unresolved': 0,
}

for idx, row in df.iterrows():
    text = f"{row['title']} {row['abstract_snippet']}".strip()
    
    # Skip already decided rows
    if row['ta_decision'] != "":
        continue

    # Check strong inclusion first
    if check_patterns(text, strong_include_terms):
        df.at[idx, 'ta_decision'] = 'Maybe'
        df.at[idx, 'ta_exclusion_reason'] = ''
        df.at[idx, 'notes'] = '[AUTO] Strong inclusion signal'
        counts['Include_Strong'] += 1
        continue

    # Exclusion checks (order matters)
    if check_patterns(text, lab_terms):
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'Animal/lab/in vitro study'
        counts['Exclude_Lab_Animal'] += 1
        continue

    if check_patterns(text, irrelevant_terms):
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'Irrelevant topic'
        counts['Exclude_Irrelevant'] += 1
        continue

    if check_patterns(text, review_terms):
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'Review/qualitative/editorial'
        counts['Exclude_Review_Qualitative'] += 1
        continue

    if check_patterns(text, hic_terms):
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'High-income country (HIC)'
        counts['Exclude_HIC'] += 1
        continue

    if check_patterns(text, hospital_terms):
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'Hospital/inpatient/clinic setting'
        counts['Exclude_Hospital'] += 1
        continue

    # Maybe checks
    if check_patterns(text, maybe_terms):
        df.at[idx, 'ta_decision'] = 'Maybe'
        df.at[idx, 'ta_exclusion_reason'] = ''
        df.at[idx, 'notes'] = '[AUTO] Descriptive/prevalence - verify design'
        counts['Maybe'] += 1
        continue

    # Unresolved - needs manual review
    df.at[idx, 'ta_decision'] = ''
    counts['Unresolved'] += 1

# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────
print("AUTO-FILTER RESULTS:")
print("-" * 40)
total_excluded = sum(v for k, v in counts.items() if k.startswith('Exclude'))
total_maybe = counts['Include_Strong'] + counts['Maybe']

print(f"  Strong inclusion signals (->Maybe): {counts['Include_Strong']}")
print(f"  Descriptive/survey (->Maybe):       {counts['Maybe']}")
print(f"  --- Total flagged for review:      {total_maybe}")
print()
print(f"  Excluded: Hospital/clinic setting: {counts['Exclude_Hospital']}")
print(f"  Excluded: HIC country:             {counts['Exclude_HIC']}")
print(f"  Excluded: Review/qualitative:      {counts['Exclude_Review_Qualitative']}")
print(f"  Excluded: Lab/animal:              {counts['Exclude_Lab_Animal']}")
print(f"  Excluded: Irrelevant:              {counts['Exclude_Irrelevant']}")
print(f"  --- Total auto-excluded:           {total_excluded}")
print()
print(f"  Unresolved (need manual check):    {counts['Unresolved']}")
print(f"  Grand total:                       {total_maybe + total_excluded + counts['Unresolved']}")
print()

# Status summary
ta_counts = df['ta_decision'].value_counts()
print("DECISION SUMMARY:")
for decision, count in ta_counts.items():
    pct = 100*count/total
    print(f"  {decision if decision else '(blank/unresolved)'}: {count} ({pct:.1f}%)")

# Save
df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
print(f"\nSaved filtered database to: {OUTPUT_FILE}")
print("=" * 60)
