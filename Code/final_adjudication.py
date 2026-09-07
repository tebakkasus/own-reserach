"""
Final manual adjudication of the 28 'Include' records.
Categorize as:
  - KEEP: Eligible for full text review
  - FP: False positive (not meeting our PICO)
"""
import pandas as pd

df = pd.read_csv(r"d:\tm\05_Own_Research\Data\screening_candidates_screened.csv", dtype=str, encoding="utf-8-sig").fillna("")

# Adjudication decisions based on title review
# Format: {doi_or_title_fragment: ('decision', 'reason')}
ADJUDICATION = {
    # ── KEEP: Intervention in community pharmacy/drug shop in LMIC ──────────
    "10.1017/ash.2026.10401": ("Include", "CRP POCT intervention + stewardship - verify community pharmacy LMIC setting"),
    "10.1186/s12913-018-3486-y": ("Include", "Educational intervention → antibiotic dispensing practices - community pharmacy"),
    "10.1016/j.socscimed.2004.04.019": ("Include", "Multi-component intervention → dispensing at private pharmacies (Chalker 2005 candidate)"),
    "10.1046/j.1365-3156.2002.00934.x": ("Include", "RCT multi-component intervention → private pharmacies Vietnam (Chalker 2002)"),
    "10.1016/s0895-4356(02)00458-4": ("Include", "Multi-intervention experiment → private pharmacy Vietnam"),
    "10.1016/j.jiph.2023.11.027": ("Include", "Public commitment charter + non-prescription pad + info leaflet → antibiotic dispensing"),
    "10.2147/idr.s324865": ("Include", "Educational intervention → pharmacist knowledge and AB dispensing (Jordan = LMIC-adjacent; verify)"),
    "10.1371/journal.pone.0163246": ("Include", "ADDO (accredited drug dispensing outlet) knowledge study - verify if intervention component"),
    "10.1186/s40545-015-0044-4": ("Include", "ADDO accreditation intervention → Tanzania retail drug shops"),
    "10.1136/bmjph-2023-000758": ("Include", "KAP + intervention impact study - verify design"),
    # Education interventions - LMIC, antibiotic, community/pharmacy - need FT check
    "10.1371/journal.pmed.1002733": ("Include", "Educational intervention → antibiotic prescribing children - verify if pharmacy-based"),
    "10.1371/journal.pgph.0002938": ("Include", "Cluster RCT financial interventions → drug shops - verify antibiotic dispensing outcome"),
    "10.1093/ofid/ofae445": ("Include", "CRP POCT acceptability + willingness-to-pay - verify community pharmacy LMIC"),

    # ── FALSE POSITIVES: wrong setting (GP/dentist/hospital), wrong outcome, or HIC ──
    "10.3389/fphar.2024.1287321": ("Exclude", "Clinical drug trial (Phase II) - not pharmacy dispensing intervention"),
    "10.1016/j.lanwpc.2024.101236": ("Maybe", "Complex intervention → antibiotic prescribing rural China - verify if includes pharmacy dispensing"),
    "10.3389/fphar.2022.710617": ("Exclude", "Diabetes/Hypertension pharmacy program - wrong outcome"),
    "10.3390/antibiotics9080490": ("Exclude", "Prescriber commitment → GP prescribing - not community pharmacy dispensing"),
    "10.1136/bmjgh-2019-001417": ("Exclude", "TB case finding by pharmacists - wrong outcome"),
    "10.1093/ofid/ofy289": ("Exclude", "Gut microbial diversity study - not pharmacy dispensing"),
    "10.1093/jac/dkx542": ("Exclude", "GP online training → parent information - not pharmacy"),
    "10.1186/s12936-016-1658-y": ("Exclude", "Malaria RDT access through drug shops - wrong outcome (malaria, not NPD)"),
    "10.1371/journal.pmed.1002115": ("Exclude", "Audit feedback → dental prescribing - wrong setting"),
    "10.1093/jac/dkv328": ("Exclude", "Antibiotic prescribing in primary care (not community pharmacy dispensing)"),
    "10.1136/bmj.h1019": ("Exclude", "Malaria RDT in private sector - wrong outcome"),
    "10.1371/journal.pone.0129545": ("Exclude", "Malaria RDT in drug shops - wrong outcome"),
    "10.1016/j.aprim.2013.12.003": ("Exclude", "Patient antibiotic adherence during dispensing - Spain (HIC)"),
    "10.1542/peds.108.1.1": ("Exclude", "Reducing AB use in children - 12 practices (likely HIC/clinic setting)"),
}

# Also identify by partial title match for those without DOI
TITLE_ADJUDICATION = {
    "Impact of a face-to-face educational intervention on improving the management of acute res": ("Include", "Face-to-face educational intervention → ARTIs management - LMIC (East Africa)"),
    "Can community pharmacists improve tuberculosis case finding": ("Exclude", "TB case finding - wrong outcome"),
}

applied = 0
for idx, row in df.iterrows():
    if row['ta_decision'] != 'Include':
        continue

    doi = str(row['doi']).strip()
    title = str(row['title'])[:80]

    matched = False
    if doi in ADJUDICATION:
        dec, reason = ADJUDICATION[doi]
        df.at[idx, 'ta_decision'] = dec
        df.at[idx, 'ta_exclusion_reason'] = reason
        df.at[idx, 'ta_confidence'] = 'HIGH'
        applied += 1
        matched = True
    
    if not matched:
        for t_frag, (dec, reason) in TITLE_ADJUDICATION.items():
            if t_frag in title:
                df.at[idx, 'ta_decision'] = dec
                df.at[idx, 'ta_exclusion_reason'] = reason
                df.at[idx, 'ta_confidence'] = 'HIGH'
                applied += 1
                matched = True
                break

print(f"Adjudication applied to {applied} records.")

# Summary
ta = df['ta_decision'].value_counts()
total = len(df)
print("\nFINAL DECISION SUMMARY:")
for d, c in ta.items():
    label = d if d else "(blank)"
    flag = " *** FULL TEXT THESE ***" if d == "Include" else " * verify *" if d == "Maybe" else ""
    print(f"  {label}: {c} ({100*c/total:.1f}%){flag}")

# Save outputs
df.to_csv(r"d:\tm\05_Own_Research\Data\screening_candidates_screened.csv", index=False, encoding="utf-8-sig")
inc = df[df['ta_decision'] == 'Include']
mayb = df[df['ta_decision'] == 'Maybe']
inc.to_csv(r"d:\tm\05_Own_Research\Data\ta_included.csv", index=False, encoding="utf-8-sig")
mayb.to_csv(r"d:\tm\05_Own_Research\Data\ta_maybe.csv", index=False, encoding="utf-8-sig")

print(f"\n=== FINAL INCLUDED STUDIES ({len(inc)}) ===")
for i, (_, row) in enumerate(inc.iterrows(), 1):
    print(f"{i:2}. [{row['year']}] {str(row['title'])[:85]}")
    print(f"     Reason: {row['ta_exclusion_reason']}")

print(f"\nSaved: ta_included.csv ({len(inc)}), ta_maybe.csv ({len(mayb)})")
