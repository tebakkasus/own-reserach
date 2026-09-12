#!/usr/bin/env python3
"""
Test IKH Abstract with explicit Objective section and validate word count (200-300 words).
"""
import re

ABSTRACT_SECTIONS = [
    ("Background: ", "Non-prescription antibiotic dispensing (NPD) in community pharmacies contributes to antimicrobial resistance, yet no quantitative review has pooled intervention effect estimates specifically from private community pharmacies in low- and middle-income countries (LMICs). "),
    ("Objective: ", "To evaluate the pooled effectiveness of interventions intended to reduce non-prescription antibiotic dispensing in private community pharmacies in LMICs. "),
    ("Methods: ", "We conducted a systematic review and meta-analysis following PRISMA 2020 guidelines. PubMed, OpenAlex, and the Cochrane Central Register of Controlled Trials were searched up to September 2026. Eligible studies were controlled intervention studies evaluating interventions to reduce NPD in private community pharmacies in LMICs, with outcomes assessed by unannounced simulated client methods. Cluster-adjusted odds ratios were pooled using a random-effects model with the DerSimonian-Laird estimator and inverse-variance weighting. A Hartung-Knapp-Sidik-Jonkman sensitivity analysis was performed to assess the robustness of the confidence interval given the small number of included studies. "),
    ("Results: ", "Three controlled studies from Vietnam, Nigeria, and Indonesia met eligibility criteria (k = 3; 345 pharmacies; 1,683 simulated client encounters). The odds of NPD were 83.6% lower in intervention pharmacies compared with control pharmacies (pooled OR = 0.164; 95% CI: 0.102 to 0.265; Z = -7.38; p < 0.0001). The Hartung-Knapp-Sidik-Jonkman method yielded a wider interval (OR = 0.164; 95% CI: 0.064 to 0.419; t(2) = -8.31, p = 0.014). Statistical heterogeneity was not detected (I-squared = 0.0%; Q = 1.58, df = 2, p = 0.454). "),
    ("Conclusion: ", "To our knowledge, this is the first meta-analysis to pool controlled intervention data on NPD interventions from private community pharmacies in LMICs. Multifaceted interventions combining dispenser education, rapid diagnostic testing, and peer supervision were associated with lower odds of non-prescription antibiotic dispensing.")
]

full_abstract_text = "".join([lbl + txt for lbl, txt in ABSTRACT_SECTIONS])

# Count words excluding section headers
cleaned_text = re.sub(r'(Background|Objective|Methods|Results|Conclusion):\s*', '', full_abstract_text)
words = ' '.join(cleaned_text.split()).split()
word_count = len(words)

print("=" * 60)
print("IKH ABSTRACT FINAL WORD COUNT VALIDATION")
print("=" * 60)
print(f"Total abstract body word count: {word_count}")
print(f"Target range: 200-300 words")
print(f"Status: {'PASS' if 200 <= word_count <= 300 else 'FAIL'}")
print()
print("Abstract Text:")
print(full_abstract_text)
