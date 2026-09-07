"""
Title-only rescue pass for the 502 'no-signal' records.
Since abstracts are truncated/garbled, we rely solely on the title.
"""
import pandas as pd
import re

df = pd.read_csv(r"d:\tm\05_Own_Research\Data\screening_candidates_screened.csv", dtype=str, encoding='utf-8-sig').fillna("")

no_signal_mask = df['ta_exclusion_reason'] == 'No relevant pharmacy + intervention signals identified'
print(f"Processing {no_signal_mask.sum()} 'no-signal' records via title-only screening...")

# HIC countries (title-level)
HIC = [
    r'\bSpain\b', r'\bSpanish\b', r'\bFrance\b', r'\bFrench\b', r'\bGermany\b',
    r'\bGerman\b', r'\bItaly\b', r'\bItalian\b', r'\bPortugal\b', r'\bNetherlands\b',
    r'\bBelgium\b', r'\bSweden\b', r'\bSwedish\b', r'\bNorway\b', r'\bDenmark\b',
    r'\bFinland\b', r'\bAustria\b', r'\bSwitzerland\b', r'\bUnited Kingdom\b',
    r'\bEngland\b', r'\bScotland\b', r'\bAustralia\b', r'\bNew Zealand\b',
    r'\bCanada\b', r'\bUnited States\b', r'\bUSA\b', r'\bJapan\b',
    r'\bSouth Korea\b', r'\bSingapore\b', r'\bIsrael\b', r'\bGreece\b',
    r'\bPoland\b', r'\bCzech\b', r'\bHungary\b', r'\bRomania\b',
]

# Review / qualitative (title-level)
REVIEW = [
    r'\bsystematic review\b', r'\bmeta-analysis\b', r'\bscoping review\b',
    r'\bnarrative review\b', r'\bliterature review\b', r'\brapid review\b',
    r'\bqualitative\b', r'\binterview study\b', r'\bfocus group\b',
    r'\bcommentary\b', r'\beditorial\b', r'\bletter\b.{0,15}\beditor\b',
]

# Hospital setting (title-level)
HOSPITAL = [
    r'\bhospital\b', r'\binpatient\b', r'\bICU\b', r'\bward\b',
    r'\bsurgical\b', r'\bneonatal\b', r'\btertiary\b',
    r'\bemergency department\b',
]

# Strong INCLUDE signals from title
TITLE_INCLUDE = [
    # Clear intervention studies
    r'\bimpact of.{0,60}(?:intervention|training|education|program)\b',
    r'\beffect of.{0,60}(?:intervention|training|education|program)\b',
    r'\befficacy of.{0,60}(?:intervention|training|program)\b',
    r'\beffectiveness of.{0,60}(?:intervention|training|program|stewardship)\b',
    r'\b(?:intervention|training|education).{0,60}(?:reduce|reduc|decreas|improv)\b',
    r'\b(?:reduce|reduc|decreas|improv).{0,60}(?:intervention|training|education)\b',
    r'\brandomized.{0,60}(?:trial|study)\b', r'\brandomised.{0,60}(?:trial|study)\b',
    r'\bcluster.{0,10}(?:RCT|randomized|randomised)\b',
    r'\bquasi.experimental\b',
    r'\bcontrolled.{0,20}(?:trial|study|before)\b',
    r'\baudit.{0,15}feedback\b',
    r'\bpeer.{0,10}(?:visit|review)\b.{0,40}\bpharmac',
    r'\bsimulated.{0,10}(?:client|patient).{0,60}(?:interven|before|after|program)\b',
    r'\bmystery.{0,10}shopper\b',
    r'\bC.reactive protein.{0,40}(?:pharma|steward|dispens)\b',
    r'\bCRP.{0,30}(?:test|point.of.care).{0,40}(?:pharma|steward)\b',
    r'\bpoint.of.care.{0,40}(?:pharma|steward|antibiotic)\b',
    r'\bADDO\b', r'\baccredited drug dispensing outlet\b',
    r'\bhappy patient\b', r'\bmprove project\b',
]

# Strong MAYBE signals from title  
TITLE_MAYBE = [
    # Descriptive but relevant (simulated client without explicit intervention)
    r'\bsimulated.{0,20}(?:client|patient)\b',
    r'\bnon.?prescription antibiotic\b',
    r'\bantibiotic.{0,20}without.{0,15}prescription\b',
    r'\bover.the.counter antibiotic\b',
    r'\bdispens.{0,20}antibiotic\b',
    r'\bantibiotic.{0,20}dispens\b',
    r'\bNPD\b', r'\bDAwP\b',
    r'\bstewardship.{0,50}(?:community pharma|drug shop|retail)\b',
    r'\b(?:community pharma|drug shop|retail pharma|medicine shop).{0,50}stewardship\b',
    r'\bpharmacy.{0,50}(?:training|education).{0,50}antibiotic\b',
    r'\bantibiotic.{0,50}(?:training|education).{0,50}pharma\b',
    r'\bfeasibility.{0,50}(?:CRP|point.of.care|stewardship)\b',
    r'\bregulat.{0,30}(?:antibiotic|pharma).{0,30}(?:LMIC|developing|low.income)\b',
]

# LMIC in title
LMIC_TITLE = [
    r'\bNigeria\b', r'\bKenya\b', r'\bUganda\b', r'\bEthiopia\b', r'\bTanzania\b',
    r'\bGhana\b', r'\bZambia\b', r'\bZimbabwe\b', r'\bMalawi\b', r'\bSenegal\b',
    r'\bCameroon\b', r'\bRwanda\b', r'\bSouth Africa\b', r'\bEgypt\b', r'\bSudan\b',
    r'\bCongo\b', r'\bMozambique\b', r'\bGuinea\b', r'\bGambia\b',
    r'\bBangladesh\b', r'\bPakistan\b', r'\bIndia\b', r'\bSri Lanka\b',
    r'\bNepal\b', r'\bMyanmar\b', r'\bCambodia\b', r'\bVietnam\b',
    r'\bPhilippines\b', r'\bIndonesia\b', r'\bLao\b', r'\bMongolia\b',
    r'\bAfghanistan\b', r'\bIraq\b', r'\bIran\b', r'\bSyria\b',
    r'\bPalestine\b', r'\bWest Bank\b', r'\bYemen\b', r'\bJordan\b',
    r'\bLebanon\b', r'\bThailand\b', r'\bChina\b', r'\bMalaysia\b',
    r'\bBolivia\b', r'\bPeru\b', r'\bEcuador\b', r'\bColombia\b',
    r'\bGuatemala\b', r'\bHonduras\b', r'\bHaiti\b',
    r'\bLMIC\b', r'\blow.and.middle.income\b', r'\bLow.Income\b',
    r'\bSub.Saharan\b', r'\bSoutheast Asia\b', r'\bSouth Asia\b',
    r'\bdeveloping countr\b', r'\bresource.limited\b', r'\bLao PDR\b',
]

def match(text, pats):
    for p in pats:
        try:
            if re.search(p, text, re.IGNORECASE):
                return True
        except:
            pass
    return False

counts = {'include': 0, 'maybe': 0, 'exclude_hic': 0, 'exclude_review': 0,
          'exclude_hosp': 0, 'exclude_no_signal': 0}

for idx, row in df.iterrows():
    if not no_signal_mask[idx]:
        continue
    
    title = str(row['title'])
    
    # Hard excludes first
    if match(title, HIC):
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'HIC country (title)'
        counts['exclude_hic'] += 1
        continue
    
    if match(title, REVIEW):
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'Review/qualitative/editorial (title)'
        counts['exclude_review'] += 1
        continue
    
    if match(title, HOSPITAL):
        df.at[idx, 'ta_decision'] = 'Exclude'
        df.at[idx, 'ta_exclusion_reason'] = 'Hospital/inpatient setting (title)'
        counts['exclude_hosp'] += 1
        continue
    
    # Include signals
    if match(title, TITLE_INCLUDE):
        df.at[idx, 'ta_decision'] = 'Include'
        df.at[idx, 'ta_exclusion_reason'] = 'Intervention study - community pharmacy/antibiotic dispensing'
        df.at[idx, 'ta_confidence'] = 'MEDIUM'
        counts['include'] += 1
        continue
    
    # Maybe signals
    if match(title, TITLE_MAYBE):
        df.at[idx, 'ta_decision'] = 'Maybe'
        df.at[idx, 'ta_exclusion_reason'] = 'Possible relevance - verify study design'
        df.at[idx, 'ta_confidence'] = 'MEDIUM'
        counts['maybe'] += 1
        continue
    
    # Default: exclude
    df.at[idx, 'ta_decision'] = 'Exclude'
    df.at[idx, 'ta_exclusion_reason'] = 'No relevant signals in title or abstract'
    counts['exclude_no_signal'] += 1

print(f"\nRESCUE PASS RESULTS:")
print(f"  Include:         {counts['include']}")
print(f"  Maybe:           {counts['maybe']}")
print(f"  Excl HIC:        {counts['exclude_hic']}")
print(f"  Excl Review:     {counts['exclude_review']}")
print(f"  Excl Hospital:   {counts['exclude_hosp']}")
print(f"  Excl no signal:  {counts['exclude_no_signal']}")

print(f"\nFINAL TOTALS:")
ta = df['ta_decision'].value_counts()
total = len(df)
for d, c in ta.items():
    label = d if d else "(blank)"
    flag = " <-- FULL TEXT" if d == "Include" else " <-- VERIFY" if d == "Maybe" else ""
    print(f"  {label}: {c} ({100*c/total:.1f}%){flag}")

# Save
df.to_csv(r"d:\tm\05_Own_Research\Data\screening_candidates_screened.csv", index=False, encoding='utf-8-sig')

# Export final Include + Maybe
inc = df[df['ta_decision'] == 'Include']
mayb = df[df['ta_decision'] == 'Maybe']
inc.to_csv(r"d:\tm\05_Own_Research\Data\ta_included.csv", index=False, encoding='utf-8-sig')
mayb.to_csv(r"d:\tm\05_Own_Research\Data\ta_maybe.csv", index=False, encoding='utf-8-sig')

print(f"\nSaved Include: {len(inc)} records -> ta_included.csv")
print(f"Saved Maybe:   {len(mayb)} records -> ta_maybe.csv")

print(f"\n=== INCLUDED STUDIES ===")
for _, row in inc.iterrows():
    print(f"  [{row['year']}] {row['title'][:85]}")
