"""
AI-Assisted Title/Abstract Screener — Meta-Analysis PINMAS IV 2026
Search Protocol V1.1 Eligibility Criteria

Eligibility hierarchy:
INCLUDE: Has intervention + concurrent control + community pharmacy/outlet + LMIC + antibiotic dispensing outcome
EXCLUDE: HIC, hospital, review, qualitative, descriptive only, wrong outcome
MAYBE: Design unclear from abstract, possible intervention, LMIC + pharmacy + dispensing but control unclear

This script uses rule-based NLP to simulate the T/A screening decision.
Final result: all 588 candidates get a decision.
"""

import pandas as pd
import re

INPUT_FILE = r"d:\tm\05_Own_Research\Data\screening_candidates.csv"
OUTPUT_FILE = r"d:\tm\05_Own_Research\Data\screening_candidates_screened.csv"

df = pd.read_csv(INPUT_FILE, dtype=str, encoding='utf-8-sig').fillna("")
print(f"Loaded {len(df)} screening candidates.")

# ─────────────────────────────────────────────────────────────────────────────
# PATTERN LIBRARIES
# ─────────────────────────────────────────────────────────────────────────────

# --- HARD EXCLUDE patterns (definitive) ---

HIC_COUNTRIES = [
    r'\bSpain\b', r'\bSpanish\b', r'\bFrance\b', r'\bFrench\b',
    r'\bGermany\b', r'\bGerman\b', r'\bItaly\b', r'\bItalian\b',
    r'\bPortugal\b', r'\bPortuguese\b', r'\bNetherlands\b', r'\bDutch\b',
    r'\bBelgium\b', r'\bSweden\b', r'\bSwedish\b', r'\bNorway\b',
    r'\bDenmark\b', r'\bFinland\b', r'\bAustria\b', r'\bSwitzerland\b',
    r'\bUnited Kingdom\b', r'\bEngland\b', r'\bScotland\b', r'\bWales\b',
    r'\bAustralia\b', r'\bAustralian\b', r'\bNew Zealand\b',
    r'\bCanada\b', r'\bCanadian\b',
    r'\bUnited States\b', r'\bUSA\b',
    r'\bJapan\b', r'\bJapanese\b', r'\bSouth Korea\b', r'\bKorean\b',
    r'\bSingapore\b', r'\bIsrael\b', r'\bGreece\b',
    r'\bCzech Republic\b', r'\bPoland\b', r'\bHungary\b',
    r'\bRomania\b', r'\bBulgaria\b', r'\bSlovakia\b', r'\bSlovenia\b',
    r'\bCroatia\b', r'\bSerbia\b',
]

REVIEW_TYPES = [
    r'\bsystematic review\b', r'\bmeta.analysis\b', r'\bscoping review\b',
    r'\bnarrative review\b', r'\bliterature review\b',
    r'\brapid review\b', r'\bintegrative review\b',
    r'\bcommentary\b', r'\beditorial\b',
    r'\bletter to the editor\b', r'\bletter to editor\b',
    r'\bstudy protocol\b', r'\bprotocol for\b',
]

QUALITATIVE_ONLY = [
    r'\bqualitative study\b', r'\bqualitative research\b',
    r'\bqualitative analysis\b', r'\bqualitative approach\b',
    r'\bin-depth interview\b', r'\bin depth interview\b',
    r'\bfocus group\b', r'\bthematic analysis\b',
    r'\bgrounded theory\b', r'\bethnograph\b',
    r'\bphenomenolog\b', r'\binterpretive\b',
    r'\bparticipant observation\b',
    r'\binterviewed\b.{0,50}\bpharmacist',
    r'\bpharmacist.{0,50}\binterviewed\b',
]

HOSPITAL_SETTING = [
    r'\bhospital pharmacy\b', r'\bhospital pharmacist\b',
    r'\bclinical pharmacy\b', r'\bward pharmacist\b',
    r'\bsurgical ward\b', r'\bpediatric ward\b', r'\bneonatal unit\b',
    r'\bintensive care unit\b', r'\bICU\b',
    r'\btertiary hospital\b', r'\bteaching hospital\b',
    r'\bsecondary care\b',
    r'\bhospital.based\b', r'\binpatient\b',
    r'\bemergency department\b',
]

# --- SOFT EXCLUDE (descriptive/cross-sectional - exclude unless intervention found) ---

DESCRIPTIVE_SIGNALS = [
    r'\bcross.sectional survey\b', r'\bcross.sectional study\b',
    r'\bpoint prevalence survey\b', r'\bprevalence survey\b',
    r'\bKAP study\b', r'\bknowledge.{0,15}attitude.{0,15}practice\b',
    r'\bsimulated.{0,10}(?:client|patient)\b.{0,200}\b(?:prevalence|assess|evaluat).{0,200}(?!interven|before|after|pre|post)',
    r'\bsurvey.{0,20}(?:pharmacist|pharmacy)\b.{0,100}(?!interven|trial|program)',
]

# --- STRONG INCLUDE: Intervention + control signals ---

INTERVENTION_SIGNALS = [
    # Study design
    r'\bcluster.{0,10}randomi[sz]ed\b',
    r'\bcluster.{0,5}RCT\b',
    r'\bcontrolled trial\b',
    r'\brandomised controlled\b', r'\brandomized controlled\b',
    r'\bquasi.experimental\b',
    r'\bcontrolled before.and.after\b', r'\bCBA study\b',
    r'\binterrupted time series\b',
    r'\bpilot (?:trial|RCT|study)\b.{0,100}\brandom',
    # Intervention terms
    r'\b(?:educational|training)\s+intervention\b',
    r'\bintervention\b.{0,80}\b(?:reduced?|decreas|improv|significant)\b',
    r'\b(?:reduced?|decreas|improv)\b.{0,80}\bintervention\b',
    r'\baudit.{0,15}feedback\b.{0,100}\bpharmac',
    r'\bpeer.{0,10}(?:visit|review)\b.{0,100}\bpharmac',
    # Key program types
    r'\bhappy patient project\b',
    r'\baccredited drug dispensing outlet\b', r'\bADDO\b',
    r'\bC.reactive protein\b.{0,100}\bpharmac',
    r'\bCRP.{0,30}(?:test|point.of.care)\b.{0,100}\bpharmac',
    r'\bAMFm\b', r'\bmProve\b',
    # Before-after with control
    r'\bintervention.{0,100}\bcontrol.{0,100}\bpharmac',
    r'\bpharmac.{0,100}\bintervention.{0,100}\bcontrol\b',
    r'\btreatment.{0,10}arm\b', r'\bcontrol.{0,10}arm\b',
    r'\bintervention.{0,10}arm\b',
    r'\bintervention.{0,50}\bgroup\b.{0,50}\bcontrol\b',
    r'\bcontrol.{0,50}\bgroup\b.{0,50}\bintervention\b',
    # Randomization explicit
    r'\bwere randoml?y\b', r'\bwere randomly assigned\b',
    r'\brandomly allocated\b', r'\ballocation ratio\b',
]

# Simulated client WITH intervention context
SIMULATED_INTERVENTION = [
    r'\bsimulated.{0,20}client\b.{0,400}\b(?:before|after|pre|post|intervention|training|program)\b',
    r'\b(?:before|after|pre|post|intervention|training|program)\b.{0,400}\bsimulated.{0,20}client\b',
    r'\bmystery.{0,10}shopper\b.{0,300}\b(?:before|after|intervention|training)\b',
    r'\b(?:before|after|intervention|training)\b.{0,300}\bmystery.{0,10}shopper\b',
]

# Simulated client WITHOUT intervention context (descriptive)
SIMULATED_DESCRIPTIVE = [
    r'\bsimulated.{0,20}client\b.{0,300}\b(?:prevalence|assess|evaluat|determin|survey|cross.sectional)\b',
    r'\bmystery.{0,10}shopper\b.{0,300}\b(?:prevalence|assess|evaluat|cross.sectional)\b',
]

# --- COMMUNITY PHARMACY SETTING IN LMIC ---

COMMUNITY_PHARMACY = [
    r'\bcommunity pharma\b', r'\bprivate pharma\b', r'\bretail pharma\b',
    r'\bdrug shop\b', r'\bdrug outlet\b', r'\bdrug store\b',
    r'\bmedicine shop\b', r'\bmedicine store\b', r'\bmedicine vendor\b',
    r'\bpatent medicine\b', r'\bPMV\b',
    r'\bdrug seller\b', r'\bpharmacy.based\b',
]

LMIC_INDICATORS = [
    # Africa
    r'\bNigeria\b', r'\bKenya\b', r'\bUganda\b', r'\bEthiopia\b',
    r'\bTanzania\b', r'\bGhana\b', r'\bZambia\b', r'\bZimbabwe\b',
    r'\bMalawi\b', r'\bMozambique\b', r'\bSenegal\b', r'\bCameroon\b',
    r'\bRwanda\b', r'\bSouth Africa\b', r'\bEgypt\b', r'\bSudan\b',
    r'\bDRC\b', r'\bCongo\b', r'\bMali\b', r'\bBurkina Faso\b',
    r'\bBenin\b', r'\bTogo\b', r'\bSierra Leone\b', r'\bLiberia\b',
    r'\bNamibia\b', r'\bBotswana\b', r'\bLesotho\b', r'\bEswatini\b',
    r'\bGuinea\b', r'\bGambia\b',
    # Asia
    r'\bBangladesh\b', r'\bPakistan\b', r'\bIndia\b', r'\bSri Lanka\b',
    r'\bNepal\b', r'\bMyanmar\b', r'\bCambodia\b', r'\bLaos\b',
    r'\bVietnam\b', r'\bPhilippines\b', r'\bIndonesia\b',
    r'\bMongolia\b', r'\bKyrgyzstan\b', r'\bUzbekistan\b',
    r'\bAfghanistan\b', r'\bIraq\b', r'\bIran\b', r'\bSyria\b',
    r'\bPalestine\b', r'\bWest Bank\b', r'\bGaza\b', r'\bYemen\b',
    r'\bJordan\b', r'\bLebanon\b', r'\bEgypt\b',
    r'\bThailand\b', r'\bMalaysia\b', r'\bChina\b',
    # Americas (LMIC)
    r'\bBolivia\b', r'\bPerou?\b', r'\bEcuador\b', r'\bParaguay\b',
    r'\bGuatemala\b', r'\bHonduras\b', r'\bNicaragua\b', r'\bEl Salvador\b',
    r'\bHaiti\b', r'\bDominican Republic\b', r'\bCuba\b',
    r'\bColombia\b',
    # Generic LMIC terms
    r'\bLMIC\b', r'\blow.and.middle.income\b', r'\blow.income countr\b',
    r'\bmiddle.income countr\b', r'\bdeveloping countr\b',
    r'\bsub.Saharan Africa\b', r'\bSoutheast Asia\b',
    r'\bSouth Asia\b', r'\bEast Africa\b', r'\bWest Africa\b',
    r'\bresource.limited\b', r'\bresource.constrained\b',
    r'\blow.resource\b',
]

ANTIBIOTIC_DISPENSING_OUTCOME = [
    r'\bnon.?prescription antibiotic\b',
    r'\bantibiotic.{0,30}without.{0,20}prescription\b',
    r'\bantibiotic.{0,30}dispens\b',
    r'\bdispens.{0,30}antibiotic\b',
    r'\bover.the.counter antibiotic\b',
    r'\bOTC antibiotic\b',
    r'\bantibiotic.{0,30}sale\b', r'\bsale.{0,30}antibiotic\b',
    r'\bnon.?prescription.{0,30}antimicrobial\b',
    r'\bdispens.{0,30}antimicrobial\b',
    r'\bantibiotic.{0,30}misuse\b', r'\bantibiotic.{0,30}overuse\b',
    r'\birrational.{0,30}antibiotic\b',
    r'\binappropriate.{0,30}antibiotic.{0,30}use\b',
    r'\bNPD\b', r'\bDAwP\b',
]

# ─────────────────────────────────────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────────────────────────────────────

def matches(text, patterns):
    for p in patterns:
        try:
            if re.search(p, text, re.IGNORECASE | re.DOTALL):
                return True
        except:
            pass
    return False

def first_match(text, patterns):
    for p in patterns:
        try:
            m = re.search(p, text, re.IGNORECASE | re.DOTALL)
            if m:
                return m.group(0)[:60]
        except:
            pass
    return ""

# ─────────────────────────────────────────────────────────────────────────────
# SCREENING LOGIC
# ─────────────────────────────────────────────────────────────────────────────

results = []

for _, row in df.iterrows():
    title = str(row['title'])
    abstract = str(row['abstract_snippet'])
    full = f"{title} {abstract}"
    has_abstract = len(abstract.strip()) > 30

    decision = ""
    reason = ""
    confidence = ""
    screen_notes = []

    # ── HARD EXCLUDES (order matters) ──────────────────────────────────────

    if matches(full, HIC_COUNTRIES):
        decision = "Exclude"
        reason = "HIC country"
        confidence = "HIGH"
        results.append((decision, reason, confidence, "; ".join(screen_notes)))
        continue

    if matches(full, REVIEW_TYPES):
        decision = "Exclude"
        reason = "Review/meta-analysis/editorial"
        confidence = "HIGH"
        results.append((decision, reason, confidence, ""))
        continue

    if matches(full, QUALITATIVE_ONLY):
        decision = "Exclude"
        reason = "Qualitative only"
        confidence = "HIGH"
        results.append((decision, reason, confidence, ""))
        continue

    if matches(full, HOSPITAL_SETTING):
        decision = "Exclude"
        reason = "Hospital/inpatient setting"
        confidence = "HIGH"
        results.append((decision, reason, confidence, ""))
        continue

    # ── POSITIVE SIGNALS ───────────────────────────────────────────────────

    has_intervention = matches(full, INTERVENTION_SIGNALS)
    has_sim_intervention = matches(full, SIMULATED_INTERVENTION)
    has_sim_descriptive = matches(full, SIMULATED_DESCRIPTIVE)
    has_pharmacy = matches(full, COMMUNITY_PHARMACY)
    has_lmic = matches(full, LMIC_INDICATORS)
    has_ab_outcome = matches(full, ANTIBIOTIC_DISPENSING_OUTCOME)
    has_descriptive = matches(full, DESCRIPTIVE_SIGNALS)

    # ── INCLUDE: Strong intervention signals ───────────────────────────────
    if has_intervention and has_pharmacy and has_ab_outcome:
        if has_lmic:
            decision = "Include"
            reason = "Intervention + community pharmacy + LMIC + antibiotic dispensing outcome"
            confidence = "HIGH"
        else:
            # Has intervention + pharmacy + outcome but country not clearly identified as LMIC
            decision = "Maybe"
            reason = "Intervention + pharmacy + AB outcome - verify LMIC status"
            confidence = "MEDIUM"
        results.append((decision, reason, confidence, first_match(full, INTERVENTION_SIGNALS)))
        continue

    if has_sim_intervention and has_pharmacy and has_ab_outcome:
        if has_lmic:
            decision = "Include"
            reason = "Simulated client + intervention context + LMIC"
            confidence = "HIGH"
        else:
            decision = "Maybe"
            reason = "Simulated client intervention - verify LMIC and control arm"
            confidence = "MEDIUM"
        results.append((decision, reason, confidence, "simulated client + intervention context"))
        continue

    # ── MAYBE: Possible intervention, needs verification ───────────────────

    if has_intervention and has_pharmacy and not has_ab_outcome:
        decision = "Maybe"
        reason = "Intervention + pharmacy - verify AB dispensing outcome specifically"
        confidence = "MEDIUM"
        results.append((decision, reason, confidence, first_match(full, INTERVENTION_SIGNALS)))
        continue

    if has_intervention and has_ab_outcome and not has_pharmacy:
        decision = "Maybe"
        reason = "Intervention + AB outcome - verify community pharmacy setting"
        confidence = "MEDIUM"
        results.append((decision, reason, confidence, ""))
        continue

    # Simulated client (descriptive context) — could still be pre-post
    if has_sim_descriptive and has_pharmacy and has_lmic:
        decision = "Maybe"
        reason = "Simulated client study (descriptive context) - verify if pre-post intervention exists"
        confidence = "MEDIUM"
        results.append((decision, reason, confidence, "simulated client - check for pre-post design"))
        continue

    # Simulated client anywhere + pharmacy = always Maybe (simulated client is core method for our studies)
    if (matches(full, SIMULATED_DESCRIPTIVE) or matches(full, SIMULATED_INTERVENTION)) and has_pharmacy:
        decision = "Maybe"
        reason = "Simulated client method in pharmacy setting - verify intervention and LMIC"
        confidence = "MEDIUM"
        results.append((decision, reason, confidence, "simulated client detected"))
        continue

    # LMIC + pharmacy + AB outcome but explicit descriptive tag
    if has_pharmacy and has_lmic and has_ab_outcome and has_descriptive:
        decision = "Exclude"
        reason = "Descriptive/prevalence - no intervention arm identified"
        confidence = "HIGH"
        results.append((decision, reason, confidence, ""))
        continue

    # LMIC + pharmacy + AB dispensing outcome - no intervention signal, no descriptive tag
    # Keep as Maybe: abstract may be truncated and miss intervention language
    if has_pharmacy and has_lmic and has_ab_outcome:
        decision = "Maybe"
        reason = "Community pharmacy + LMIC + AB dispensing - verify study design for intervention arm"
        confidence = "MEDIUM"
        results.append((decision, reason, confidence, ""))
        continue

    # Has pharmacy + LMIC but unclear outcome or design
    if has_pharmacy and has_lmic and not has_ab_outcome:
        decision = "Exclude"
        reason = "Wrong outcome - not AB dispensing"
        confidence = "MEDIUM" if has_abstract else "LOW"
        results.append((decision, reason, confidence, ""))
        continue

    # No abstract available
    if not has_abstract:
        decision = "Maybe"
        reason = "No abstract - cannot screen; retrieve full text"
        confidence = "LOW"
        results.append((decision, reason, confidence, ""))
        continue

    # Catchall for anything remaining with abstract
    decision = "Exclude"
    reason = "No relevant pharmacy + intervention signals identified"
    confidence = "MEDIUM"
    results.append((decision, reason, confidence, ""))

# ─────────────────────────────────────────────────────────────────────────────
# APPLY RESULTS
# ─────────────────────────────────────────────────────────────────────────────

decisions, reasons, confidences, sig_notes = zip(*results)
df['ta_decision'] = decisions
df['ta_exclusion_reason'] = reasons
df['ta_confidence'] = confidences
df['screening_signal'] = sig_notes

# ── SUMMARY ──────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("SCREENING COMPLETE — FINAL RESULTS")
print("="*60)
total = len(df)
for dec in ['Include', 'Maybe', 'Exclude']:
    subset = df[df['ta_decision'] == dec]
    pct = 100 * len(subset) / total
    tag = " <-- PROCEED TO FULL TEXT" if dec == 'Include' else ""
    tag2 = " <-- VERIFY MANUALLY" if dec == 'Maybe' else ""
    print(f"  {dec}: {len(subset)} ({pct:.1f}%){tag}{tag2}")

print()
if len(df[df['ta_decision'] == 'Include']) > 0:
    print("=== INCLUDED STUDIES ===")
    for _, row in df[df['ta_decision'] == 'Include'].iterrows():
        print(f"  [{row['year']}] {row['title'][:80]}")
        print(f"         Reason: {row['ta_exclusion_reason']}")
        if row.get('screening_signal', ''):
            print(f"         Signal: {row['screening_signal']}")

print()
print("=== MAYBE STUDIES (manual verification needed) ===")
for _, row in df[df['ta_decision'] == 'Maybe'].head(20).iterrows():
    print(f"  [{row['year']}] {row['title'][:80]}")
    print(f"         Reason: {row['ta_exclusion_reason']}")

print()
exc_reasons = df[df['ta_decision'] == 'Exclude']['ta_exclusion_reason'].value_counts()
print("=== EXCLUSION REASONS ===")
for r, c in exc_reasons.items():
    print(f"  {r}: {c}")

# Save
df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

# Save Include-only
include_df = df[df['ta_decision'] == 'Include']
include_df.to_csv(r"d:\tm\05_Own_Research\Data\ta_included.csv", index=False, encoding='utf-8-sig')

# Save Maybe-only
maybe_df = df[df['ta_decision'] == 'Maybe']
maybe_df.to_csv(r"d:\tm\05_Own_Research\Data\ta_maybe.csv", index=False, encoding='utf-8-sig')

print(f"\nSaved:")
print(f"  Full screened: {OUTPUT_FILE}")
print(f"  Include only:  d:\\tm\\05_Own_Research\\Data\\ta_included.csv ({len(include_df)} records)")
print(f"  Maybe only:    d:\\tm\\05_Own_Research\\Data\\ta_maybe.csv ({len(maybe_df)} records)")
