#!/usr/bin/env python3
"""
AMBIGUITY & REVIEWER-INTERPRETATION AUDIT — in-place minimal fixes
Targets (no new files):
  1. Manuscript_ICSH_2026_FINAL.docx
  2. ICSH_2026_Abstract_Submission_FINAL.docx
Also syncs Code/build_ikh_manuscript_v8.py and Code/build_ikh_abstract_FINAL.py
Scientific content LOCKED: no number, no pooled estimate, no PRISMA count changes.
"""
import docx

M = 'D:/tm/05_Own_Research/Manuscript_ICSH_2026_FINAL.docx'
A = 'D:/tm/05_Own_Research/ICSH_2026_Abstract_Submission_FINAL.docx'

# ---------- helpers ----------
def set_single_run_text(p, new_text):
    """Keep first run's formatting, merge everything into it."""
    fmt = None
    if p.runs:
        r0 = p.runs[0]
        fmt = (r0.font.name, r0.font.size, r0.bold, r0.italic)
    else:
        return
    for r in p.runs[1:]:
        r._element.getparent().remove(r._element)
    p.runs[0].text = new_text
    name, size, bold, italic = fmt
    p.runs[0].font.name = name
    if size: p.runs[0].font.size = size
    p.runs[0].bold = bold
    p.runs[0].italic = italic

def replace_in_run(p, old, new):
    """Targeted string replacement across the paragraph's runs."""
    for r in p.runs:
        if old in r.text:
            r.text = r.text.replace(old, new)
            return True
    return False

# ============================================================
# 1. MANUSCRIPT — in-place edits
# ============================================================
doc = docx.Document(M)
changes = []

# --- P19: 'included trials' -> 'included studies' (Prioritas 1) ---
p = doc.paragraphs[19]
if 'citation tracking of included trials' in p.text:
    replace_in_run(p, 'included trials', 'included studies')
    changes.append('P19: "included trials" -> "included studies"')

# --- P20: 'qualitative evidence pool' -> 'systematic review evidence pool' (Prioritas 3) ---
p = doc.paragraphs[20]
if 'qualitative evidence pool' in p.text:
    replace_in_run(p, 'qualitative evidence pool', 'systematic review evidence pool')
    changes.append('P20: "qualitative evidence pool" -> "systematic review evidence pool"')

# --- P21: quasi-experimental -> precise (Prioritas 1) ---
p = doc.paragraphs[21]
if 'for quasi-experimental studies, with' in p.text:
    replace_in_run(p, 'for quasi-experimental studies, with',
                   'for the non-randomised controlled before-after study, with')
    changes.append('P21: "quasi-experimental studies" -> "non-randomised controlled before-after study"')

# --- P22: 'For each trial' -> 'For each study' + drop Matplotlib sentence (Prioritas 1 & 6) ---
p = doc.paragraphs[22]
t = p.text
t2 = t.replace('For each trial,', 'For each study,')
t2 = t2.replace(' Forest plots were generated with Matplotlib in Python 3.12.', '')
t2 = t2.replace('Forest plots were generated with Matplotlib in Python 3.12.', '')
if t2 != t:
    set_single_run_text(p, t2)
    changes.append('P22: "For each trial" -> "For each study"; removed Matplotlib/Python sentence')

# --- P24: scope clarifier — all 3 in private community pharmacies (Prioritas 2) ---
p = doc.paragraphs[24]
if 'three of them met the strict criteria for quantitative meta-analysis (Figure 1)' in p.text:
    replace_in_run(p, 'and three of them met the strict criteria for quantitative meta-analysis (Figure 1)',
                   'and three of them met the strict criteria for quantitative meta-analysis, all conducted in private community pharmacies (Figure 1)')
    changes.append('P24: added "all conducted in private community pharmacies" clarifier')

# --- P36: transferable -> narrower claim (Prioritas 4) ---
p = doc.paragraphs[36]
if 'may be transferable across settings' in p.text:
    replace_in_run(p, 'may be transferable across settings',
                   'may be transferable to comparable private community pharmacy settings in other LMICs')
    changes.append('P36: "transferable across settings" -> "transferable to comparable private community pharmacy settings in other LMICs"')

# --- P37: 'individual trials' -> 'individual studies' (Prioritas 1) ---
p = doc.paragraphs[37]
if 'the results of individual trials were consistent' in p.text:
    replace_in_run(p, 'individual trials', 'individual studies')
    changes.append('P37: "individual trials" -> "individual studies"')

# --- P38: soften 'Legislation alone is unlikely' + 'Our results support' (Prioritas 4) ---
p = doc.paragraphs[38]
t = p.text
t2 = t.replace('Legislation alone is unlikely to curb', 'Legislation alone may not be sufficient to curb')
t2 = t2.replace('Our results support the inclusion', 'Our findings are consistent with the inclusion')
if t2 != t:
    set_single_run_text(p, t2)
    changes.append('P38: "Legislation alone is unlikely" -> "may not be sufficient"; "Our results support" -> "Our findings are consistent with"')

# --- P41: scope precision (Prioritas 2) ---
p = doc.paragraphs[41]
if 'in LMIC community pharmacies (pooled OR' in p.text:
    replace_in_run(p, 'in LMIC community pharmacies (pooled OR',
                   'in private community pharmacies in LMICs (pooled OR')
    changes.append('P41: "in LMIC community pharmacies" -> "in private community pharmacies in LMICs"')

# --- P44: ethics — 'trial data' -> 'study data' + no primary participants (Prioritas 9) ---
p = doc.paragraphs[44]
if 'published trial data' in p.text:
    replace_in_run(p, 'published trial data', 'published study data. No primary human participants were recruited')
    changes.append('P44: "published trial data" -> "published study data" + "No primary human participants were recruited"')

doc.save(M)
print('== MANUSCRIPT CHANGES ==')
for c in changes:
    print('  -', c)

# ============================================================
# 2. ABSTRACT — in-place edits
# ============================================================
docA = docx.Document(A)
a_changes = []

# --- P9: rebuild runs preserving bold section labels ---
p9 = docA.paragraphs[9]
new_p9_text = (
    "Background: Non-prescription antibiotic dispensing (NPD) in community pharmacies contributes to antimicrobial resistance, "
    "yet no quantitative review has pooled intervention effect estimates specifically from private community pharmacies in "
    "low- and middle-income countries (LMICs). "
    "Objective: To evaluate the pooled effectiveness of interventions intended to reduce non-prescription antibiotic dispensing "
    "in private community pharmacies in LMICs. "
    "Methods: We conducted a systematic review and meta-analysis following PRISMA 2020 guidelines. PubMed, OpenAlex, and the "
    "Cochrane Central Register of Controlled Trials were searched up to September 2026. Eligible studies were controlled "
    "intervention studies evaluating interventions to reduce NPD in private community pharmacies or private retail drug shops "
    "in LMICs, with outcomes assessed by unannounced simulated client methods. Cluster-adjusted odds ratios were pooled using "
    "a random-effects model with the DerSimonian-Laird estimator and inverse-variance weighting. A Hartung-Knapp-Sidik-Jonkman "
    "sensitivity analysis was performed to assess the robustness of the confidence interval given the small number of included studies. "
    "Results: Three controlled studies from Vietnam, Nigeria, and Indonesia met eligibility criteria (k = 3; 345 pharmacies; "
    "1,683 simulated client encounters). The odds of NPD were 83.6% lower in intervention pharmacies compared with control "
    "pharmacies (pooled OR = 0.164; 95% CI: 0.102 to 0.265; Z = -7.38; p < 0.0001). The Hartung-Knapp-Sidik-Jonkman method "
    "yielded a wider interval (OR = 0.164; 95% CI: 0.064 to 0.419; t(2) = -8.31, p = 0.014). Statistical heterogeneity was not "
    "detected, although the test has limited power with only three studies (I-squared = 0.0%; Q = 1.58, df = 2, p = 0.454). "
    "Conclusion: To our knowledge, this is the first meta-analysis to pool controlled intervention data on NPD interventions "
    "from private community pharmacies in LMICs. Multifaceted interventions combining dispenser education, rapid diagnostic "
    "testing, and peer supervision were associated with lower odds of non-prescription antibiotic dispensing."
)

segments = []
for label in ["Background:", "Objective:", "Methods:", "Results:", "Conclusion:"]:
    start = new_p9_text.index(label)
    end = len(new_p9_text)
    for nl in ["Background:", "Objective:", "Methods:", "Results:", "Conclusion:"]:
        idx = new_p9_text.index(nl)
        if idx > start:
            end = min(end, idx)
    segments.append((label, new_p9_text[start + len(label):end]))

# rebuild runs
if p9.runs:
    base_font = None
    base_size = None
    for r in p9.runs:
        if r.font.name:
            base_font = r.font.name
        if r.font.size:
            base_size = r.font.size
    # remove all runs
    for r in list(p9.runs):
        r._element.getparent().remove(r._element)
    for label, txt in segments:
        rl = p9.add_run(label)
        rl.bold = True
        rl.font.name = base_font or 'Times New Roman'
        if base_size: rl.font.size = base_size
        rt = p9.add_run(txt)
        rt.bold = False
        rt.font.name = base_font or 'Times New Roman'
        if base_size: rt.font.size = base_size
    a_changes.append('P9: Methods + "or private retail drug shops"; Results + low-power caveat on I-squared')

# word count check
cleaned = new_p9_text
import re
cleaned = re.sub(r'(Background|Objective|Methods|Results|Conclusion):\s*', '', cleaned)
wc = len(' '.join(cleaned.split()).split())
print(f'\nAbstract word count after edit: {wc} (target 200-300) -> {"PASS" if 200 <= wc <= 300 else "FAIL"}')

# --- P13: ethics 'trial data' -> 'study data', subjects -> participants ---
p13 = docA.paragraphs[13]
t13 = p13.text
t13b = t13.replace('published trial data. No primary human subjects were involved.',
                   'published study data. No primary human participants were recruited.')
if t13b != t13:
    # single run holds all four declarations
    if len(p13.runs) == 1:
        p13.runs[0].text = t13b
    else:
        set_single_run_text(p13, t13b)
    a_changes.append('P13: "published trial data" -> "published study data"; "subjects" -> "participants"')

print('== ABSTRACT CHANGES ==')
for c in a_changes:
    print('  -', c)

docA.save(A)
print('\nSaved in place: Manuscript_ICSH_2026_FINAL.docx & ICSH_2026_Abstract_Submission_FINAL.docx')