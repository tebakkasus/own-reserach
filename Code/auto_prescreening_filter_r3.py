"""
Round 3: Final cleanup of remaining unresolved records.
Strategy: Records without clear inclusion signals -> Exclude (insufficient info) or Maybe (borderline).
"""
import pandas as pd
import re

df = pd.read_csv(r'd:\tm\05_Own_Research\Data\master_screening_database.csv', dtype=str, encoding='utf-8-sig').fillna('')
unresolved = df[df['ta_decision'] == '']
print(f"Unresolved before R3: {len(unresolved)}")

# Conservative MAYBE: only keep if there's genuine possibility of intervention element
KEEP_MAYBE = [
    # Has explicit RCT/quasi-exp/trial language
    r'\b(?:randomized|randomised|RCT|cluster.RCT|trial)\b',
    r'\bquasi.experimental\b', r'\bcontrolled.{0,20}(?:before|study)\b',
    r'\binterrupted.time.series\b',
    # Has intervention of interest
    r'\bintervention\b.{0,150}(?:pharma|drug shop|drug outlet|medicine shop)',
    r'(?:pharma|drug shop|drug outlet|medicine shop).{0,150}\bintervention\b',
    r'\btraining.{0,80}(?:pharma|drug shop)',
    r'\bauditing?\b.{0,80}(?:pharma|feedback)',
    r'\bpeer.{0,10}(?:visit|review).{0,80}pharma',
    # Simulated client / mystery shopper
    r'\bsimulated.{0,20}(?:client|patient)\b',
    r'\bmystery.{0,10}shopper\b',
    # Specific LMIC focus + pharmacy dispensing behaviour
    r'\bnon.prescription antibiotic\b',
    r'\bantibiotic.{0,20}without.{0,20}prescription\b',
    r'\bantibiotic.{0,30}(?:sold|dispensed).{0,30}without',
    # CRP point of care
    r'\bC.reactive protein\b', r'\bCRP.{0,30}test\b',
    # Drug shop/outlet in LMIC
    r'\bdrug.{0,10}(?:shop|outlet).{0,50}(?:interven|study|dispensing)\b',
    r'\bpatent medicine vendor\b',
]

# EXCLUDE the rest
counts3 = {'maybe': 0, 'exclude_no_abstract': 0, 'exclude_irrelevant': 0}

for idx, row in df.iterrows():
    if row['ta_decision'] != '':
        continue
    title = str(row['title'])
    abstract = str(row['abstract_snippet'])
    full = f"{title} {abstract}"

    keep = False
    for p in KEEP_MAYBE:
        try:
            if re.search(p, full, re.IGNORECASE):
                keep = True
                break
        except:
            pass

    if keep:
        df.at[idx, 'ta_decision'] = 'Maybe'
        df.at[idx, 'notes'] = '[AUTO-R3] Possible intervention study - verify design'
        counts3['maybe'] += 1
    elif len(abstract.strip()) < 20:
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'No abstract available - insufficient info'
        counts3['exclude_no_abstract'] += 1
    else:
        # Has abstract but no intervention signal -> descriptive/prevalence
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'Descriptive/prevalence - no intervention design'
        counts3['exclude_irrelevant'] += 1

print(f"\nROUND 3 RESULTS:")
print(f"  Kept as Maybe:            {counts3['maybe']}")
print(f"  Excluded (no abstract):   {counts3['exclude_no_abstract']}")
print(f"  Excluded (descriptive):   {counts3['exclude_irrelevant']}")

print(f"\nFINAL DECISION SUMMARY:")
ta_counts = df['ta_decision'].value_counts()
total = len(df)
for decision, count in ta_counts.items():
    label = decision if decision else "(blank)"
    pct = 100*count/total
    flag = " <-- SCREEN THESE" if decision == 'Maybe' else ""
    print(f"  {label}: {count} ({pct:.1f}%){flag}")

df.to_csv(r'd:\tm\05_Own_Research\Data\master_screening_database.csv', index=False, encoding='utf-8-sig')

# Export Maybe records only for focused review
maybe_df = df[df['ta_decision'] == 'Maybe']
maybe_df.to_csv(r'd:\tm\05_Own_Research\Data\screening_candidates.csv', index=False, encoding='utf-8-sig')
print(f"\nScreening candidates exported: d:\\tm\\05_Own_Research\\Data\\screening_candidates.csv")
print(f"Total records to screen manually: {len(maybe_df)}")
