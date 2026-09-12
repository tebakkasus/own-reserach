#!/usr/bin/env python3
"""
Build IKH 2026 Manuscript v5 (full paper) from PINMAS manuscript.
Applies ALL Final Pre-Edit Gate fixes:
  1. HKSJ sensitivity analysis added (OR 0.164; 95% CI 0.064-0.419; p = 0.042)
  2. Associational wording for pooled result ("were associated with lower odds")
  3. SCM wording ("objective assessment" - no "gold standard")
  4. Novelty wording ("To our knowledge...")
  5. Removed unsupported subgroup-analysis claim
  6. Search limitation disclosed (PubMed/OpenAlex/CENTRAL only)
  7. IKH-appropriate formatting (A4, margins 1.9/2.2cm, TNR fonts)
"""
import docx
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import os

OUTPUT = "Manuscript_ICSH_2026_v8.docx"

doc = docx.Document()
for section in doc.sections:
    section.top_margin = Cm(1.9)
    section.bottom_margin = Cm(1.9)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)

style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(11)

def add_p(text="", bold=False, italic=False, size=11, align=None, space_after=6, space_before=0, line_spacing=1.15):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
    return p

# ============================================================
# TITLE PAGE
# ============================================================
add_p("Research Article", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=12)

add_p("Effectiveness of Interventions to Reduce Non-Prescription Antibiotic Dispensing in LMIC Pharmacies: Meta-Analysis",
      bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12, line_spacing=1.15)

# Author line with superscript
p_auth = add_p("", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
r1 = p_auth.add_run("Tengku Muhammad Lufthi Hannur")
r1.bold = True; r1.font.name = 'Times New Roman'; r1.font.size = Pt(11)
r2 = p_auth.add_run("1*")
r2.bold = True; r2.font.name = 'Times New Roman'; r2.font.size = Pt(10); r2.font.superscript = True

p_aff = add_p("", size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
ra1 = p_aff.add_run("1 ")
ra1.font.name = 'Times New Roman'; ra1.font.size = Pt(8.5); ra1.font.superscript = True
ra2 = p_aff.add_run("Study Program of Medicine, Faculty of Medicine, Universitas Islam Sumatera Utara, Medan, North Sumatra, Indonesia")
ra2.font.name = 'Times New Roman'; ra2.font.size = Pt(9.5)

add_p("* Corresponding Author: Tengku Muhammad Lufthi Hannur | Email: tengkumuhammadlufthihannur@fk.uisu.ac.id | WhatsApp: +62 822-6740-3241 | ORCID: https://orcid.org/0009-0008-1306-2485",
      italic=True, size=9.0, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)

doc.add_page_break()

# ============================================================
# ABSTRACT
# ============================================================
add_p("ABSTRACT", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)

abstract_sections = [
    ("Background: ", "Non-prescription antibiotic dispensing (NPD) in community pharmacies contributes to antimicrobial resistance, yet no quantitative review has pooled intervention effect estimates specifically from private community pharmacies in low- and middle-income countries (LMICs). "),
    ("Methods: ", "We conducted a systematic review and meta-analysis following PRISMA 2020 guidelines. PubMed, OpenAlex, and the Cochrane Central Register of Controlled Trials were searched up to September 2026. Eligible studies were controlled intervention studies evaluating interventions to reduce NPD in private community pharmacies in LMICs, with outcomes assessed by unannounced simulated client methods. Cluster-adjusted odds ratios were pooled using a random-effects model with the DerSimonian-Laird estimator and inverse-variance weighting. A Hartung-Knapp-Sidik-Jonkman sensitivity analysis was performed to assess the robustness of the confidence interval given the small number of included studies. "),
    ("Results: ", "Three controlled studies from Vietnam, Nigeria, and Indonesia met eligibility criteria (k = 3; 345 pharmacies; 1,683 simulated client encounters). The odds of NPD were 83.6% lower in intervention pharmacies compared with control pharmacies (pooled OR = 0.164; 95% CI: 0.102 to 0.265; Z = -7.38; p < 0.0001). The Hartung-Knapp-Sidik-Jonkman method yielded a wider interval (OR = 0.164; 95% CI: 0.064 to 0.419; t(2) = -8.31, p = 0.014). Statistical heterogeneity was not detected (I-squared = 0.0%; Q = 1.58, df = 2, p = 0.454). "),
    ("Conclusion: ", "To our knowledge, this is the first meta-analysis to pool controlled intervention data on NPD interventions from private community pharmacies in LMICs. Multifaceted interventions combining dispenser education, rapid diagnostic testing, and peer supervision were associated with lower odds of non-prescription antibiotic dispensing.")
]
for label, text in abstract_sections:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    rl = p.add_run(label); rl.bold = True; rl.font.name='Times New Roman'; rl.font.size = Pt(10.5)
    rt = p.add_run(text); rt.font.name='Times New Roman'; rt.font.size = Pt(10.5)

p_kw = doc.add_paragraph()
p_kw.paragraph_format.space_after = Pt(14)
rkl = p_kw.add_run("Keywords: "); rkl.bold = True; rkl.font.name='Times New Roman'; rkl.font.size = Pt(9.5)
rkv = p_kw.add_run("Antimicrobial Resistance; Community Pharmacy; Non-Prescription Antibiotic Dispensing; Meta-Analysis; Low- and Middle-Income Countries")
rkv.font.name='Times New Roman'; rkv.font.size = Pt(9.5)

doc.add_page_break()

# ============================================================
# INTRODUCTION
# ============================================================
add_p("Introduction", bold=True, size=12, space_before=6, space_after=6)

add_p("Antimicrobial resistance (AMR) was associated with an estimated 4.95 million deaths in 2019, and the burden falls disproportionately on low- and middle-income countries (LMICs). One modifiable contributor to this burden is non-prescription antibiotic dispensing (NPD), defined here as the sale of prescription-only systemic antibiotics by private retail drug outlets without a valid prescription. In many LMICs, private community pharmacies are the first point of care for common illnesses because they are close to patients' homes, involve no appointment, and avoid the consultation fees charged by formal health facilities.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_p("Earlier reviews have assessed interventions aimed at improving antibiotic dispensing in developing countries, but they faced important limitations. Afari-Asiedu et al. (2022) provided a narrative synthesis only, because heterogeneity across studies prevented quantitative pooling. The Cochrane review (2025) likewise could not pool effect estimates owing to differences in design and setting. Both reviews combined public facilities, such as primary health centres and government clinics, with private retail pharmacies. Yet private and public outlets operate under different pressures. Private pharmacies depend on customer sales, face competition, and are subject to weaker regulatory oversight, so their dispensing behaviour may not respond to interventions in the same way as public facilities.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_p("We therefore conducted a systematic review and meta-analysis restricted to controlled studies of interventions to reduce NPD in private community pharmacies in LMICs. By focusing on a single sector and on outcomes measured with unannounced simulated client methods, we aimed to obtain a pooled estimate that accounts for clustering and that can inform antibiotic stewardship policy at the community level.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

# ============================================================
# METHODS
# ============================================================
add_p("Methods", bold=True, size=12, space_before=6, space_after=6)

add_p("Study Design and Protocol: This systematic review and meta-analysis followed the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA 2020) checklist.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_p("Eligibility Criteria: Studies were eligible when they (1) were conducted in private community pharmacies or private retail drug shops in World Bank-classified LMICs; (2) evaluated an educational, managerial, diagnostic, or regulatory intervention targeting antibiotic dispensing; (3) included a concurrent comparison group, that is, a cluster-randomised trial or a controlled before-after study; (4) measured non-prescription antibiotic dispensing quantitatively using unannounced simulated client methods; and (5) reported cluster-adjusted effect estimates or the data needed to calculate them. Studies conducted in public health posts, hospital outpatient clinics, or without a control group were excluded.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_p("Information Sources and Search Strategy: We searched PubMed, OpenAlex, and the Cochrane Central Register of Controlled Trials (CENTRAL) up to September 2026. The search combined controlled vocabulary and free-text terms, including (\"community pharmacy\" OR \"private pharmacy\" OR \"drug retail\" OR \"drug shop\") AND (\"antibiotic\" OR \"antimicrobial\") AND (\"non-prescription\" OR \"without prescription\" OR \"dispensing\") AND (\"intervention\" OR \"stewardship\" OR \"education\"). We also performed backward and forward citation tracking of included studies and of earlier systematic reviews. Searching was restricted to these three sources; non-indexed regional studies not captured in these databases may have been omitted.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_p("Study Selection and Data Extraction: Records were screened by title and abstract and then assessed in full text against the eligibility criteria. The systematic review synthesis retained a broader systematic review evidence pool (n = 14) evaluating antimicrobial stewardship and dispensing practices across community and retail settings, whereas the primary quantitative synthesis was strictly restricted to controlled intervention studies conducted in private community pharmacies in LMICs that reported cluster-adjusted effect estimates using unannounced simulated client methods (n = 3). Data were extracted into a standardised matrix covering first author, year, country, design, number of randomised and analysed pharmacies, number of simulated client encounters, intervention components, comparator, raw dispensing events and denominators per arm, reported effect estimates with 95% confidence intervals (CI), p-values, the clustering model used (e.g., GLIMMIX, GLMER, xtlogit), and any reported intraclass correlation coefficients (ICC).",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_p("Risk of Bias Assessment: Risk of bias was assessed with the revised Cochrane risk-of-bias tool for cluster-randomised trials (RoB 2) and, for the non-randomised controlled before-after study, with the Risk Of Bias In Non-randomised Studies of Interventions (ROBINS-I) tool.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_p("Statistical Synthesis: Effect sizes were pooled with a random-effects (DerSimonian-Laird) model using inverse-variance weighting, implemented in R with the metafor and meta packages. For each study, the cluster-adjusted odds ratio (aOR) and its 95% CI were log-transformed to obtain the effect size (yi = ln[aOR]) and its standard error (sei = {ln[CI upper] - ln[CI lower]} / 3.92). Heterogeneity was assessed with Cochran's Q (p < 0.10), the I² statistic, and the between-study variance τ². Because only three studies contributed to the quantitative synthesis, a Hartung-Knapp-Sidik-Jonkman (HKSJ) sensitivity analysis was performed to assess the robustness of the confidence interval.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

# ============================================================
# RESULTS
# ============================================================
add_p("Results", bold=True, size=12, space_before=6, space_after=6)

add_p("Study Selection: The database search retrieved 3,223 records, and citation tracking added 22 more, for a total of 3,245 records. After removing 2,635 records before title/abstract screening and conducting title/abstract evaluation (n = 610; 427 excluded), 183 full texts were assessed for eligibility, of which 169 were excluded (public-sector prescriber settings, n=18; non-private community drug retail settings, n=34; uncontrolled or observational designs, n=42; outcome other than non-prescription dispensing, n=26; physician-targeted interventions, n=14; malaria case management alone, n=9; other reasons, n=26). Fourteen studies met the broader criteria for systematic review inclusion (n = 14), and three of them met the strict criteria for quantitative meta-analysis, all conducted in private community pharmacies (Figure 1).",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

if os.path.exists("Plots/prisma_flow_diagram.png"):
    p_img1 = doc.add_paragraph()
    p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img1.paragraph_format.space_before = Pt(6)
    p_img1.paragraph_format.space_after = Pt(4)
    run1 = p_img1.add_run()
    run1.add_picture("Plots/prisma_flow_diagram.png", width=Inches(5.5))
    add_p("Figure 1. PRISMA 2020 flow diagram of study selection",
          bold=True, size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

add_p("Characteristics of Included Studies: The three controlled studies came from three countries (Table 1). Chalker et al. (2005) conducted a matched-pair cluster-randomised trial in Hanoi, Vietnam, testing a three-phase strategy of regulatory enforcement, inspector visits, educational seminars, and peer-review meetings across 55 private pharmacies (273 simulated client encounters). Onwunduba et al. (2023) conducted a stratified cluster-randomised trial in Awka, Nigeria, testing point-of-care C-reactive protein (CRP) testing and staff training in 20 private community pharmacies (600 encounters). Ferdiana et al. (2024) conducted a controlled before-after evaluation of the PINTAR package (online modules, customer awareness campaigns, peer outreach, and pharmacy branding) in Semarang, Indonesia, across 270 private pharmacies, with 80 intervention and 190 comparison pharmacies (810 encounters). All three controlled studies used unannounced simulated clients presenting fixed clinical scenarios (acute respiratory infection, urinary tract infection, and childhood diarrhoea).",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

add_p("Table 1. Characteristics of the studies included in the quantitative synthesis",
      bold=True, size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)

table = doc.add_table(rows=4, cols=6)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER

headers = ["Study (Year)", "Country", "Design", "Sample (pharmacies / encounters)", "Intervention", "Adjusted OR (95% CI)"]
hdr_row = table.rows[0]
for j, h in enumerate(headers):
    cell = hdr_row.cells[j]
    cell.text = h
    cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
    cell.paragraphs[0].runs[0].font.size = Pt(8.5)
    cell.paragraphs[0].runs[0].bold = True
    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

table_data = [
    ["Chalker et al. (2005)", "Vietnam (Hanoi)", "Cluster-randomised, matched-pair", "55 / 273", "Enforcement, inspection, education, peer review", "0.134 (0.057-0.316)"],
    ["Onwunduba et al. (2023)", "Nigeria (Awka)", "Cluster-randomised, stratified", "20 / 600", "Point-of-care CRP testing plus staff training", "0.279 (0.107-0.726)"],
    ["Ferdiana et al. (2024)", "Indonesia (Semarang)", "Controlled before-after", "270 / 810", "PINTAR: online education, campaigns, peer outreach, branding", "0.140 (0.070-0.300)"]
]
for i, row in enumerate(table_data):
    r = table.rows[i+1]
    for j, val in enumerate(row):
        c = r.cells[j]
        c.text = val
        p = c.paragraphs[0]
        if len(p.runs) > 0:
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(8.5)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j in [1, 2, 5] else WD_ALIGN_PARAGRAPH.LEFT

add_p("", space_after=6)

add_p("Meta-Analysis: In the random-effects meta-analysis (Figure 2), the pooled odds ratio for NPD was 0.164 (95% CI: 0.102 to 0.265; Z = -7.38; p < 0.0001). This corresponds to 83.6% lower odds of dispensing without a prescription in intervention pharmacies than in control pharmacies. Individual aORs ranged from 0.134 to 0.279, all in the same direction.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_p("Sensitivity Analysis: Because only three studies contributed to the quantitative synthesis, a Hartung-Knapp-Sidik-Jonkman (HKSJ) sensitivity analysis was performed to assess the robustness of the confidence interval. The HKSJ method yielded the same point estimate with a wider confidence interval (OR = 0.164; 95% CI: 0.064 to 0.419; t(2) = -8.31; p = 0.014). The wider interval reflects the small number of studies, and the pooled effect remained statistically significant under both models.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_p("Heterogeneity: Heterogeneity was not statistically significant (Q = 1.58, df = 2, p = 0.454; I² = 0.0%; τ² = 0.000). Study weights were 43.5% for Ferdiana et al., 31.4% for Chalker et al., and 25.1% for Onwunduba et al. With only three studies, the test for heterogeneity has low statistical power, and the I² of 0.0% should be interpreted as the absence of statistically detectable heterogeneity rather than proof of homogeneity (Higgins et al., 2003).",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

if os.path.exists("Plots/forest_plot_core3.png"):
    p_img2 = doc.add_paragraph()
    p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img2.paragraph_format.space_before = Pt(6)
    p_img2.paragraph_format.space_after = Pt(4)
    run2 = p_img2.add_run()
    run2.add_picture("Plots/forest_plot_core3.png", width=Inches(6.2))
    add_p("Figure 2. Forest plot of the random-effects meta-analysis",
          bold=True, size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

# ============================================================
# DISCUSSION
# ============================================================
add_p("Discussion", bold=True, size=12, space_before=6, space_after=6)

add_p("Principal Findings: This meta-analysis is, to our knowledge, the first to pool effect estimates exclusively from controlled intervention studies conducted in private community pharmacies in LMICs. Across the three controlled studies, the pooled OR was 0.164 (95% CI: 0.102-0.265), equivalent to 83.6% lower odds of NPD in intervention pharmacies. Effect sizes were similar across South-East Asia and sub-Saharan Africa, which suggests that pharmacy-based stewardship models may be transferable to comparable private community pharmacy settings in other LMICs.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_p("Comparison with Previous Reviews: Afari-Asiedu et al. (2022) and the Cochrane review (2025) could not pool results because of heterogeneity in design, setting, and outcome measurement. When the scope is limited to private retail outlets assessed with simulated clients, however, the results of individual studies were consistent. Dispensers in private settings face comparable pressures, including customer demand, fear of losing sales, and limited enforcement of dispensing regulations. Interventions that combine staff training, diagnostic support such as point-of-care CRP testing, and peer supervision appear to help counter these pressures.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_p("Policy Implications: Legislation alone may not be sufficient to curb non-prescription antibiotic sales in LMICs, where enforcement capacity is often limited. Our findings are consistent with the inclusion of pharmacy-focused packages, comprising dispenser education, rapid diagnostics, customer awareness campaigns, and peer supervision, in national action plans for antimicrobial resistance. Within the Sustainable Health 5.0 framework, community pharmacy stewardship represents a sustainable, decentralised intervention platform that aligns with the health-related Sustainable Development Goals (SDG 3 and its target 3.d on strengthening capacity for early warning and risk reduction).",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_p("Limitations: The meta-analysis includes only three controlled studies, reflecting how few controlled studies have been conducted in private pharmacies in LMICs. With k = 3, tests of heterogeneity have low statistical power, and the I² of 0.0% should be read as the absence of statistically detectable heterogeneity rather than proof of homogeneity. Tumwikirize et al. (2004), a quasi-experimental study from Uganda (RR 0.85, 95% CI: 0.66-1.09), could not be included in the pooled estimate because the full text is paywalled and its summary statistic could not be converted reliably to a cluster-adjusted odds ratio. Simulated client encounters measure dispensing at a single visit and may not reflect long-term consumption trends. Finally, searching was restricted to PubMed, OpenAlex, and CENTRAL, and non-indexed regional studies may have been missed.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

# ============================================================
# CONCLUSION
# ============================================================
add_p("Conclusion", bold=True, size=12, space_before=6, space_after=6)

add_p("Multifaceted interventions that combine dispenser education, rapid diagnostic testing, customer awareness, and peer supervision were associated with significantly lower odds of non-prescription antibiotic dispensing in private community pharmacies in LMICs (pooled OR = 0.164, 95% CI: 0.102-0.265). National programmes should consider adapting and scaling these pharmacy-focused models, ideally within multi-country cluster-randomised trials that assess long-term sustainability.",
      align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)

# ============================================================
# ETHICAL STATEMENT
# ============================================================
add_p("Ethical Statement & Author Declaration", bold=True, size=12, space_before=6, space_after=6)

decl_lines = [
    "[ X ] Originality: The authors certify that this manuscript is original, has not been published previously, and is not under consideration elsewhere.",
    "[ X ] Ethical Approval: Ethical approval was not required as this study is a secondary systematic review and meta-analysis of publicly available, published study data. No primary human participants were recruited.",
    "[ X ] Conflict of Interest: The authors declare that they have no financial, personal, or professional conflicts of interest regarding this work.",
    "[ X ] Author Consent: The listed author has reviewed, approved this submission, and agreed to present at ICSH 2026 if accepted.",
]
for line in decl_lines:
    add_p(line, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4)
add_p("", space_after=8)

# ============================================================
# REFERENCES
# ============================================================
add_p("References", bold=True, size=12, space_before=6, space_after=6)

references_list = [
    # 1. Murray et al. 2022 — AMR burden (cited in Introduction)
    "Murray CJL, Ikuta KS, Sharara F, Swetschinski LR, Robles Aguilar G, Gray A, et al. Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis. Lancet. 2022;399(10325):629-55.",
    # 2. Morgan et al. 2011 — Non-prescription antimicrobial use (cited in Introduction)
    "Morgan DJ, Okeke IN, Laxminarayan R, Perencevich EN, Weisenberg S. Non-prescription antimicrobial use worldwide: a systematic review. Lancet Infect Dis. 2011;11(9):692-701.",
    # 3. Afari-Asiedu et al. 2022 — Earlier review (cited in Introduction & Discussion)
    "Afari-Asiedu S, Abdulai MA, Tostmann A, Asiedu-Birktag E, von Marschall Z, Schuit E, et al. Interventions to improve dispensing of antibiotics at the community level in low and middle income countries: a systematic review. J Glob Antimicrob Resist. 2022;29:259-74.",
    # 4. Thandar et al. 2025 — Cochrane review (cited in Introduction & Discussion) [NEW]
    "Thandar MM, Baba T, Matsuoka S, Ota E. Interventions to reduce non-prescription antimicrobial sales in community pharmacies. Cochrane Database Syst Rev. 2025;(1):CD013722. doi: 10.1002/14651858.CD013722.pub2.",
    # 5. Page et al. 2021 — PRISMA 2020 (cited in Methods) [NEW]
    "Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ. 2021;372:n71. doi: 10.1136/bmj.n71.",
    # 6. Chalker 2002 — 14-study pool (PRISMA Box 8) [NEW]
    "Chalker J, Chuc NTK, Falkenberg T, Tomson G. Private pharmacies in Hanoi, Vietnam: a randomized trial of a 2-year multi-component intervention on knowledge and stated practice regarding ARI, STD and antibiotic/steroid requests. Trop Med Int Health. 2002;7(9):803-10. doi: 10.1046/j.1365-3156.2002.00934.x.",
    # 7. Chuc 2002 — 14-study pool (PRISMA Box 8) [NEW]
    "Chuc NTK, Larsson M, Do NT, Diwan VK, Tomson GB, Falkenberg T. Improving private pharmacy practice: a multi-intervention experiment in Hanoi, Vietnam. J Clin Epidemiol. 2002;55(11):1148-55. doi: 10.1016/s0895-4356(02)00458-4.",
    # 8. Chalker et al. 2005 — Quantitative pool & 14-study pool
    "Chalker J, Ratanawijitrasin S, Chuc NTK, Petzold M, Tomson G. Effectiveness of a multi-component intervention on dispensing practices at private pharmacies in Vietnam and Thailand: a randomized controlled trial. Soc Sci Med. 2005;60(1):131-41. doi: 10.1016/j.socscimed.2004.04.019.",
    # 9. Onwunduba et al. 2023 — Quantitative pool & 14-study pool
    "Onwunduba A, Ekwunife O, Onyilogwu E, Onyemelukwe C, Modebe A, Igbokwe D. Impact of point-of-care C-reactive protein testing intervention on non-prescription dispensing of antibiotics for respiratory tract infections in private community pharmacies in Nigeria: a cluster randomized controlled trial. Int J Infect Dis. 2023;127:137-43. doi: 10.1016/j.ijid.2022.12.012.",
    # 10. Ferdiana et al. 2024 — Quantitative pool & 14-study pool
    "Ferdiana A, Wulandari LPL, Liverani M, Limato R, Essiet I, Mcknight J, et al. The impact of a multi-faceted intervention on non-prescription dispensing of antibiotics by urban community pharmacies in Indonesia: a mixed methods evaluation. BMJ Glob Health. 2024;9(10):e015620. doi: 10.1136/bmjgh-2024-015620.",
    # 11. Tumwikirize et al. 2004 — 14-study pool (Limitation note)
    "Tumwikirize WA, Ekwaru PJ, Mohammed K, Ogwal-Okeng JW, Aupont O. Impact of a face-to-face educational intervention on improving the management of acute respiratory infections in private pharmacies and drug shops in Uganda. East Afr Med J. 2004;81(Suppl 1):S33-40.",
    # 12. Rutta et al. 2015 — 14-study pool (PRISMA Box 8) [NEW]
    "Rutta E, Liana J, Embrey M, Johnson K, Kimatta S, et al. Accrediting retail drug shops to strengthen Tanzania's public health system: an ADDO case study. J Pharm Policy Pract. 2015;8(1):23. doi: 10.1186/s40545-015-0044-4.",
    # 13. Simba et al. 2016 — 14-study pool (PRISMA Box 8) [NEW]
    "Simba D, Kakoko D, Semali I, Kessy A, Embrey M. Household knowledge of antimicrobials and antimicrobial resistance in the wake of an accredited drug dispensing outlet (ADDO) program rollout in Tanzania. PLoS One. 2016;11(9):e0163246. doi: 10.1371/journal.pone.0163246.",
    # 14. Chowdhury et al. 2018 — 14-study pool (PRISMA Box 8) [NEW]
    "Chowdhury F, Sturm-Ramirez K, Mamun AA, Iuliano AD, Chisti MJ, et al. Effectiveness of an educational intervention to improve antibiotic dispensing practices for acute respiratory illness among drug sellers in pharmacies, a pilot study in Bangladesh. BMC Health Serv Res. 2018;18(1):680. doi: 10.1186/s12913-018-3486-y.",
    # 15. Wei et al. 2019 — 14-study pool (PRISMA Box 8) [NEW]
    "Wei X, Zhang Z, Hicks JP, Walley J, King R, et al. Long-term outcomes of an educational intervention to reduce antibiotic prescribing for childhood upper respiratory tract infections in rural China: follow-up of a cluster-randomised controlled trial. PLoS Med. 2019;16(2):e1002733. doi: 10.1371/journal.pmed.1002733.",
    # 16. Saleh et al. 2021 — 14-study pool (PRISMA Box 8) [NEW]
    "Saleh D, Abu Farha R, Alefishat E. Impact of educational intervention to promote Jordanian community pharmacists' knowledge and perception towards antimicrobial stewardship: pre-post interventional study. Infect Drug Resist. 2021;14:2229-39. doi: 10.2147/IDR.S324865.",
    # 17. Bocquier et al. 2023 — 14-study pool (PRISMA Box 8) [NEW]
    "Bocquier A, Essilini A, Pereira O, Welter A, Pulcini C, et al. Impact of a public commitment charter, a non-prescription pad and an antibiotic information leaflet to improve antibiotic prescription among general practitioners: a randomised controlled study. J Infect Public Health. 2023;16(1):12-20. doi: 10.1016/j.jiph.2023.11.027.",
    # 18. Saif et al. 2024 — 14-study pool (PRISMA Box 8) [NEW]
    "Saif A, Khan TM, Bukhsh A, Yaseen MO, Saif A. Cross-sectional survey to explore knowledge, attitude, practices and impact of an intervention programme related to antibiotic misuse and self-medication among general population of Pakistan. BMJ Public Health. 2024;2:e000758. doi: 10.1136/bmjph-2023-000758.",
    # 19. Visser et al. 2024 — 14-study pool (PRISMA Box 8) [NEW]
    "Visser T, Laktabai J, Kimachas E, Kipkoech J, Menya D, et al. A cluster-randomized trial of client and provider directed financial interventions to align incentives with appropriate case management in private medicine retailers: results of the TESTsmART trial in Lagos, Nigeria. PLOS Glob Public Health. 2024;4(5):e0002938. doi: 10.1371/journal.pgph.0002938.",
    # 20. Nguyen et al. 2024 — 14-study pool (PRISMA Box 8) [NEW]
    "Nguyen VN, Do NTT, Vu HTL, Bui PB, Pham TQ, et al. Understanding acceptability and willingness-to-pay for a C-reactive protein point-of-care testing service to improve antibiotic dispensing for respiratory infections in Vietnamese pharmacies: a mixed-methods study. Open Forum Infect Dis. 2024;11(9):ofae445. doi: 10.1093/ofid/ofae445.",
    # 21. Saha et al. 2026 — 14-study pool (PRISMA Box 8) [NEW]
    "Saha SK, Muleme M, Van Hecke O, Chatterton ML, Athan E. Feasibility of C-reactive protein point-of-care testing for antibiotic stewardship in rural GP-pharmacy settings. Antimicrob Steward Healthc Epidemiol. 2026;6(1):e10401. doi: 10.1017/ash.2026.10401.",
    # 22. DerSimonian & Laird 1986 — Random-effects model (cited in Methods)
    "DerSimonian R, Laird N. Meta-analysis in clinical trials. Control Clin Trials. 1986;7(3):177-88.",
    # 23. Higgins et al. 2003 — I² statistic (cited in Discussion/Results)
    "Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. BMJ. 2003;327(7414):557-60.",
    # 24. Hartung & Knapp 2001 — HKSJ method (cited in Methods/Results) [NEW]
    "Hartung J, Knapp G. A refined method for the meta-analysis of controlled clinical trials with binary outcome. Stat Med. 2001;20(24):3875-89.",
    # 25. Sidik & Jonkman 2002 — HKSJ method (cited in Methods/Results) [NEW]
    "Sidi K, Jonkman JN. A comparison of heterogeneity variance estimators in combining results of studies. Stat Med. 2002;21(11):1521-32.",
]

for idx, ref in enumerate(references_list, 1):
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.left_indent = Inches(0.3)
    p_ref.paragraph_format.first_line_indent = Inches(-0.3)
    p_ref.paragraph_format.space_after = Pt(4)
    p_ref.paragraph_format.line_spacing = 1.15
    run = p_ref.add_run(f"{idx}.  {ref}")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(9.5)

doc.save(OUTPUT)
print(f"SUCCESS: IKH manuscript saved to {OUTPUT}")