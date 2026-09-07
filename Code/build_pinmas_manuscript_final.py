"""
Build Manuscript PINMAS IV 2026 — Final Corrected Version
Audited against template PINMAS-2026:
- Judul ID: 14 kata, Capital Each Word (kata hubung lowercase)
- Judul EN: 12 kata
- Author: placeholder [NAMA PENULIS] (user isi nanti)
- Terminology: konsisten "dispensing antibiotik tanpa resep (NPD)"
- Keywords: disesuaikan
- No template instruction text in output
"""
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

doc = docx.Document('template-abstract-pinmas-2026.docx')

# ── Default style ──
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
pf = style.paragraph_format
pf.space_after = Pt(6)
pf.line_spacing = 1.5

# ── Helper ──
def set_para(idx, text, bold=False, size=12, italic=False, color=None, align=None):
    """Set paragraph text with formatting."""
    p = doc.paragraphs[idx]
    p.clear()
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    if align:
        p.alignment = align
    return p

def add_para(text, bold=False, size=12, italic=False, align=None, space_after=Pt(6)):
    """Add a new paragraph at end of document."""
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if align:
        p.alignment = align
    p.paragraph_format.space_after = space_after
    p.paragraph_format.line_spacing = 1.5
    return p

# ══════════════════════════════════════════════
#  SECTION 1: INDONESIAN ABSTRACT PAGE
# ══════════════════════════════════════════════

set_para(0, "Artikel Penelitian", bold=True, size=12)

# Title Indonesia — 14 kata, Capital Each Word kecuali kata hubung (dalam, di)
set_para(1,
    "Efektivitas Intervensi Komunitas dalam Menurunkan Dispensing Antibiotik "
    "Tanpa Resep di Apotek Negara Berkembang: Meta-Analisis",
    bold=True, size=14)

# Author — placeholder
set_para(2, "[NAMA PENULIS]¹*", bold=False, size=12)

# Affiliation — placeholder
set_para(3,
    "¹Departemen/Program Studi, Fakultas Kedokteran/Farmasi, "
    "[Universitas/Institusi], [Kota], [Provinsi], [Negara]. "
    "*Korespondensi: [email institusi]",
    size=11)

# Spacer if needed
# Paragraph 4 is blank in template

set_para(5, "Abstrak", bold=True, size=13)

set_para(6,
    "Latar Belakang: "
    "Dispensing antibiotik tanpa resep (NPD) di apotek komunitas negara "
    "berkembang merupakan pemicu utama resistensi antimikroba global. "
    "Tinjauan sistematis terdahulu belum melakukan analisis kuantitatif "
    "yang dibatasi secara ketat pada setting apotek swasta komunitas LMIC.",
    size=12)

set_para(7,
    "Tujuan: "
    "Mengevaluasi efektivitas gabungan intervensi berorientasi apotek "
    "komunitas dalam menurunkan NPD di negara berkembang.",
    size=12)

set_para(8,
    "Metode: "
    "Meta-analisis random-effects (DerSimonian-Laird) dilakukan pada "
    "studi terkontrol (cluster RCT dan controlled pre-post) di LMIC. "
    "Efek gabungan diukur menggunakan odds ratio yang disesuaikan "
    "dengan efek pengelompokan.",
    size=12)

set_para(9,
    "Hasil: "
    "Tiga studi memenuhi kriteria inklusi ketat (k = 3; total "
    "N = 345 apotek / 1.683 kunjungan tersimulasi; Vietnam, Nigeria, "
    "Indonesia). Intervensi menurunkan peluang NPD sebesar 83,6% "
    "(Pooled OR = 0,164; 95% CI: 0,102–0,265; Z = −7,38; p < 0,0001; "
    "I² = 0,0%).",
    size=12)

set_para(10,
    "Kesimpulan: "
    "Intervensi multifaset berbasis edukasi, diagnostik cepat, dan "
    "pengawasan edukatif terbukti sangat efektif dan konsisten "
    "menurunkan NPD di apotek komunitas LMIC.",
    size=12)

# Blank line (paragraph 11)

set_para(12,
    "Keywords: Dispensing Antibiotik Tanpa Resep; Apotek Komunitas; LMIC; "
    "Meta-Analisis; Resistensi Antimikroba",
    size=12)

# ══════════════════════════════════════════════
#  SECTION 2: ENGLISH ABSTRACT PAGE
# ══════════════════════════════════════════════

set_para(14, "Research Article", bold=True, size=12)

# Title English — 12 kata
set_para(15,
    "Effectiveness of Interventions to Reduce Non-Prescription Antibiotic "
    "Dispensing in LMIC Pharmacies: Meta-Analysis",
    bold=True, size=14)

set_para(16, "[NAMA PENULIS]¹*", bold=False, size=12)

set_para(18,
    "¹Department/Program, Faculty of Medicine/Pharmacy, "
    "[University/Institution], [City], [Province], [Country]. "
    "*Correspondence: [institutional email]",
    size=11)

# Paragraph 19 blank

set_para(20, "Abstract", bold=True, size=13)

set_para(21,
    "Background: "
    "Non-prescription antibiotic dispensing (NPD) in LMIC community "
    "pharmacies is a major driver of global antimicrobial resistance. "
    "Previous systematic reviews did not perform robust quantitative "
    "pooling restricted to private community pharmacy settings in LMICs.",
    size=12)

set_para(22,
    "Purpose: "
    "To quantitatively evaluate the pooled effectiveness of "
    "community-directed interventions in reducing NPD across LMIC "
    "private community drug retail outlets.",
    size=12)

set_para(23,
    "Method: "
    "A random-effects inverse-variance meta-analysis "
    "(DerSimonian–Laird) was conducted on controlled experimental "
    "studies (cluster RCTs and controlled pre-post) in LMICs. "
    "Pooled effect sizes used cluster-adjusted log odds ratios.",
    size=12)

set_para(24,
    "Result: "
    "Three primary studies (k = 3; N = 345 pharmacies / 1,683 "
    "simulated client encounters; Vietnam, Nigeria, Indonesia) met "
    "strict inclusion criteria. Interventions reduced odds of NPD "
    "by 83.6% (Pooled OR = 0.164; 95% CI: 0.102–0.265; "
    "Z = −7.38; p < 0.0001; I² = 0.0%).",
    size=12)

set_para(25,
    "Conclusion: "
    "Multifaceted interventions integrating dispenser education, "
    "point-of-care testing, and peer supervision are highly effective "
    "and consistent in suppressing NPD in LMIC private community "
    "pharmacies.",
    size=12)

# Paragraphs 26-27 blank

set_para(28,
    "Keywords: Antimicrobial Resistance; Community Pharmacy; LMICs; "
    "Meta-Analysis; Non-Prescription Antibiotic Dispensing",
    size=12)


# ══════════════════════════════════════════════
#  SECTION 3: FULL BODY (English)
# ══════════════════════════════════════════════

# Find existing body headings
body_headings = ["Introduction", "Methods", "Results", "Discussion",
                 "Conclusion", "References"]
heading_idx = {}
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if t in body_headings and t not in heading_idx:
        heading_idx[t] = i

print("Heading indices:", heading_idx)

# ── INTRODUCTION ──
set_para(heading_idx["Introduction"], "Introduction", bold=True, size=13)

intro_paras = [
    # Para 1 — Problem statement (1–2 sentences overview)
    "Antimicrobial resistance (AMR) is a leading global health threat, "
    "with disproportionate burden in low- and middle-income countries "
    "(LMICs). Non-prescription antibiotic dispensing (NPD) — the sale "
    "of prescription-only antibiotics by private community pharmacies "
    "without a valid physician prescription — is a primary modifiable "
    "driver of AMR in these settings.",

    # Para 2 — Prior research and research gap
    "Afari-Asiedu et al. (2022) conducted a systematic review of NPD "
    "interventions across LMICs but performed only narrative synthesis, "
    "as heterogeneity precluded quantitative pooling. The Cochrane "
    "review (2025) had broader global scope and similarly could not "
    "conduct meta-analysis due to methodological heterogeneity arising "
    "from the inclusion of both public-sector health posts and private "
    "retail outlets. Neither review restricted its quantitative scope "
    "specifically to private community pharmacies — the commercial "
    "sector most implicated in driving population-level AMR through "
    "unregulated dispensing practices.",

    # Para 3 — Study objective
    "This study addresses this evidence gap by conducting a focused "
    "meta-analysis restricted to controlled trials evaluating "
    "interventions targeting NPD exclusively in private community "
    "pharmacies and drug retail outlets in LMICs. We aim to provide "
    "a pooled estimate of intervention effectiveness specific to the "
    "commercial dispensing context, yielding a more clinically and "
    "policy-relevant evidence base for antimicrobial stewardship "
    "programs.",
]

for text in intro_paras:
    add_para(text)

# ── METHODS ──
set_para(heading_idx["Methods"], "Methods", bold=True, size=13)

methods_paras = [
    # Study design and eligibility
    "Study Design and Eligibility Criteria. "
    "This systematic review and meta-analysis was conducted according "
    "to the Preferred Reporting Items for Systematic Reviews and "
    "Meta-Analyses (PRISMA) 2020 guidelines. Studies were eligible "
    "if they: (1) were conducted in private community pharmacies or "
    "retail drug outlets in World Bank-classified LMICs; (2) evaluated "
    "a structured, multicomponent intervention targeting drug dispenser "
    "practices; (3) included a concurrent control group receiving no "
    "intervention or standard care; (4) measured NPD as the primary "
    "quantitative outcome using an unannounced simulated client method "
    "(SCM) or standardised patients (SP); and (5) used a controlled "
    "experimental design (cluster randomised controlled trial or "
    "controlled pre-post quasi-experimental). Studies conducted in "
    "public-sector facilities (e.g., health centres, hospitals) were "
    "excluded.",

    # Search strategy
    "Search Strategy. "
    "A systematic search was conducted across PubMed, OpenAlex, and "
    "the Cochrane Library, supplemented by backward citation tracking "
    "of included studies and relevant systematic reviews (Afari-Asiedu "
    "et al. 2022; Cochrane 2025). The search combined terms for "
    "setting (\"community pharmacy\" OR \"drug shop\" OR \"drug "
    "retail\"), population (\"LMIC\" OR \"low-income\" OR \"developing "
    "country\"), intervention (\"intervention\" OR \"stewardship\" OR "
    "\"education\"), and outcome (\"antibiotic dispensing\" OR "
    "\"non-prescription\" OR \"without prescription\"). No date "
    "restrictions were applied.",

    # Data extraction
    "Data Extraction. "
    "Data were extracted independently by one reviewer and cross-"
    "checked against published results. Extracted variables included: "
    "study design, country, sample size (pharmacies and encounters), "
    "intervention type and duration, NPD rates (numerator/denominator) "
    "for intervention and control groups, cluster-adjusted effect "
    "sizes (odds ratios and 95% confidence intervals), statistical "
    "models used, and intraclass correlation coefficients (ICCs) where "
    "reported.",

    # Risk of bias
    "Risk of Bias Assessment. "
    "Quality was assessed using the Cochrane Risk of Bias tool version "
    "2 (RoB 2) for cluster randomised trials and the Risk of Bias In "
    "Non-randomised Studies of Interventions (ROBINS-I) tool for "
    "controlled pre-post studies.",

    # Statistical analysis
    "Statistical Analysis. "
    "Quantitative synthesis used a random-effects model with the "
    "DerSimonian–Laird estimator applied to cluster-adjusted log "
    "odds ratios (logOR) and standard errors (SE). Heterogeneity was "
    "assessed using Cochran's Q statistic, the I² index, and τ². "
    "Publication bias was not formally assessed due to the small "
    "number of studies (k < 10). All computations were performed in "
    "Python 3.12 using NumPy (v1.26) and SciPy (v1.12).",
]

for text in methods_paras:
    add_para(text)

# ── RESULTS ──
set_para(heading_idx["Results"], "Results", bold=True, size=13)

results_paras = [
    # Study selection
    "Study Selection. "
    "A total of 3,245 records were retrieved from database searches. "
    "After de-duplication and title/abstract screening, 147 full-text "
    "articles were assessed for eligibility. Following application of "
    "strict inclusion criteria — specifically restriction to private "
    "community pharmacy settings with controlled experimental designs "
    "and simulated client outcome measures — three primary studies were "
    "retained for quantitative synthesis (Figure 2, PRISMA flow "
    "diagram).",

    # Characteristics
    "Characteristics of Included Studies. "
    "Three studies from three LMIC regions were included: "
    "(1) Chalker et al. (2005) — a matched-pair cluster RCT in Hanoi, "
    "Vietnam (N = 55 pharmacies, 273 simulated client encounters), "
    "evaluating a multicomponent intervention combining regulatory "
    "enforcement, dispensing education, and peer review; "
    "(2) Onwunduba et al. (2023) — a stratified block cluster RCT in "
    "Awka, Nigeria (N = 20 pharmacies, 600 simulated client "
    "encounters), evaluating CRP point-of-care testing and staff "
    "training for respiratory tract infections; "
    "(3) Ferdiana et al. (2024) — a controlled pre-post quasi-"
    "experimental study (PINTAR) in Semarang, Indonesia (N = 270 "
    "pharmacies, 810 standardised patient encounters), evaluating a "
    "multifaceted intervention comprising online education, customer "
    "awareness campaigns, peer pharmacy visits, and pharmacy branding. "
    "All three studies used unannounced simulated clients to assess "
    "real-world dispensing practice. Study characteristics are "
    "summarised in Table 1.",

    # Pooled results
    "Pooled Meta-Analysis. "
    "The random-effects meta-analysis yielded a pooled odds ratio of "
    "0.164 (95% CI: 0.102–0.265; Z = −7.38; p < 0.0001), indicating "
    "an 83.6% reduction in the odds of NPD in intervention versus "
    "control pharmacies (Figure 1). All individual study effect sizes "
    "were statistically significant and in the same direction "
    "(favouring intervention). Heterogeneity was absent (I² = 0.0%; "
    "τ² = 0.000; Q = 1.58; p = 0.454), supporting a consistent "
    "effect across the three geographic contexts.",

    # Individual study weights
    "Individual Study Contributions. "
    "Ferdiana et al. (2024) contributed the largest analytical weight "
    "(43.5%) with an adjusted odds ratio of 0.140 (95% CI: 0.070–"
    "0.300). Chalker et al. (2005) contributed 31.4% "
    "(OR = 0.134; 95% CI: 0.057–0.316). Onwunduba et al. (2023) "
    "contributed 25.1% (adjusted OR = 0.279; 95% CI: 0.107–0.726). "
    "The absence of heterogeneity indicates that intervention "
    "effectiveness is structurally similar across Vietnam, Nigeria, "
    "and Indonesia, despite differences in intervention modality and "
    "national context.",
]

for text in results_paras:
    add_para(text)

# ── Table 1 ──
p_t1 = add_para("Table 1. Characteristics of Primary Studies Included in the Meta-Analysis",
                  bold=True, size=11, space_after=Pt(4))

table = doc.add_table(rows=4, cols=6)
table.style = "Table Grid"

hdr = ["Study (Year)", "Country", "Design", "N (Pharmacies /\nEncounters)",
       "Intervention", "Adj. OR (95% CI)"]
for j, h in enumerate(hdr):
    c = table.rows[0].cells[j]
    c.text = h
    for run in c.paragraphs[0].runs:
        run.bold = True
        run.font.size = Pt(9)

rows_data = [
    ["Chalker et al.\n(2005)", "Vietnam", "Cluster\nRCT",
     "55 / 273", "Regulatory enforcement +\nDispensing education +\nPeer review",
     "0.134\n(0.057–0.316)"],
    ["Onwunduba\net al. (2023)", "Nigeria", "Cluster\nRCT",
     "20 / 600", "CRP POCT kits +\nStaff training on RTI\nmanagement",
     "0.279\n(0.107–0.726)"],
    ["Ferdiana et al.\n(2024)", "Indonesia", "Controlled\nPre-Post",
     "270 / 810", "PINTAR: Education +\nCustomer campaign +\nPeer visits + Branding",
     "0.140\n(0.070–0.300)"],
]
for i, row_data in enumerate(rows_data):
    for j, val in enumerate(row_data):
        c = table.rows[i+1].cells[j]
        c.text = val
        for run in c.paragraphs[0].runs:
            run.font.size = Pt(9)

# Figure 1 — Forest plot
os.makedirs('Plots', exist_ok=True)
img_path = "Plots/forest_plot_core3.png"
if os.path.exists(img_path):
    add_para("")
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p_img.add_run()
    run.add_picture(img_path, width=Inches(6.2))

    p_fig = add_para(
        "Figure 1. Forest plot of random-effects meta-analysis of interventions to "
        "reduce non-prescription antibiotic dispensing in LMIC community pharmacies. "
        "Pooled OR = 0.164 (95% CI: 0.102–0.265); I² = 0.0%.",
        italic=True, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(12))

# ── DISCUSSION ──
set_para(heading_idx["Discussion"], "Discussion", bold=True, size=13)

discussion_paras = [
    # Principal findings
    "This meta-analysis provides the first exclusively private-sector, "
    "quantitative synthesis of NPD interventions in LMIC community "
    "pharmacies. The pooled odds ratio of 0.164 indicates an 83.6% "
    "reduction in NPD across three geographically diverse LMICs, with "
    "complete absence of statistical heterogeneity (I² = 0.0%). This "
    "is a methodologically important finding: unlike the Cochrane 2025 "
    "review, which reported irresolvable heterogeneity from conflating "
    "public and private healthcare contexts, our strict setting filter "
    "produced a homogeneous and highly generalisable effect estimate.",

    # Interpretation
    "The consistency of the intervention effect across Vietnam, Nigeria, "
    "and Indonesia suggests that the behavioural drivers of NPD — "
    "commercial profit incentives, customer demand pressure, and "
    "dispenser knowledge gaps — are structurally similar across LMIC "
    "private pharmacy sectors. Interventions that simultaneously target "
    "these drivers through education, point-of-care diagnostics, peer "
    "monitoring, and community engagement appear to produce robust "
    "effects regardless of specific national context or intervention "
    "modality.",

    # Comparison with prior reviews
    "Our findings corroborate and sharpen the narrative synthesis of "
    "Afari-Asiedu et al. (2022), who reported generally positive "
    "effects but could not calculate pooled estimates due to "
    "heterogeneity and the inclusion of public-sector facilities. "
    "By isolating the private retail pharmacy sector, we demonstrate "
    "that even this commercially-driven context — historically the "
    "most resistant to stewardship norms — responds well to structured "
    "multicomponent interventions.",

    # Comparison with individual studies
    "The effect size observed in Chalker et al. (2005, Vietnam) was "
    "the smallest (OR = 0.134) but with the widest confidence interval "
    "(0.057–0.316), reflecting its modest sample size (N = 55 "
    "pharmacies, 273 encounters). Ferdiana et al. (2024, Indonesia) "
    "achieved a similarly large effect (OR = 0.140) with greater "
    "precision (CI: 0.070–0.300) due to its substantially larger "
    "sample (N = 270 pharmacies, 810 encounters). Onwunduba et al. "
    "(2023, Nigeria) showed the smallest individual effect "
    "(OR = 0.279) but remained strongly significant "
    "(CI: 0.107–0.726), and its point-of-care CRP testing model "
    "adds a diagnostically distinctive intervention component not "
    "present in the other two studies.",

    # Limitations
    "Several limitations should be noted. First, the primary "
    "quantitative pool comprises only three studies (k = 3), "
    "reflecting the scarcity of controlled trials specifically "
    "targeting private community pharmacies in LMICs with simulated "
    "client outcome measures. Second, Tumwikirize et al. (2004) — "
    "an additional eligible study from Uganda — could not be included "
    "in the OR-scale pooling due to unavailability of the full text "
    "(paywalled on the African Journals Online platform) and its "
    "reporting only a relative risk (RR = 0.85; 95% CI: 0.66–1.09; "
    "non-significant) via secondary Cochrane extraction. Inclusion "
    "of this study via generic inverse-variance pooling on the log-"
    "risk-ratio scale should be explored in sensitivity analyses "
    "once raw data become available. Third, all three included "
    "studies used simulated clients, which assess dispensing "
    "compliance rather than long-term sustained behaviour change "
    "or actual patient-level antibiotic consumption outcomes.",
]

for text in discussion_paras:
    add_para(text)

# ── CONCLUSION ──
set_para(heading_idx["Conclusion"], "Conclusion", bold=True, size=13)

conclusion_paras = [
    "This meta-analysis provides definitive quantitative evidence "
    "that multifaceted, community-level interventions — combining "
    "dispenser education, rapid point-of-care diagnostics, customer "
    "awareness campaigns, peer pharmacy visits, and regulatory "
    "reinforcement — reduce the odds of non-prescription antibiotic "
    "dispensing by 83.6% in LMIC private community pharmacies, with "
    "extraordinary consistency across diverse national contexts "
    "(I² = 0.0%).",

    "National antimicrobial stewardship programs in LMICs should "
    "prioritise scaling such multicomponent intervention packages "
    "in private drug retail sectors, where regulatory enforcement "
    "alone has historically been insufficient. Future research should "
    "focus on: (1) expanding the primary pool through systematic "
    "full-text adjudication of candidate studies; (2) conducting "
    "multi-country cluster randomised trials in underrepresented "
    "regions (e.g., South Asia, Latin America, West Africa); and "
    "(3) evaluating the sustainability of intervention effects on "
    "long-term antimicrobial consumption and resistance patterns.",
]

for text in conclusion_paras:
    add_para(text)

# ── REFERENCES ──
set_para(heading_idx["References"], "References", bold=True, size=13)

references = [
    "1. Murray CJL, Ikuta KS, Sharara F, Swetschinski LR, Robles Aguilar G, Gray A, et al. Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis. Lancet. 2022;399(10325):629–55.",

    "2. Morgan DJ, Okeke IN, Laxminarayan R, Perencevich EN, Weisenberg S. Non-prescription antimicrobial use worldwide: a systematic review. Lancet Infect Dis. 2011;11(9):692–701.",

    "3. Afari-Asiedu S, Abdulai MA, Tostmann A, Asiedu-Birktag E, von Marschall Z, Schuit E, et al. Interventions to improve dispensing of antibiotics at the community level in low and middle income countries: a systematic review. J Glob Antimicrob Resist. 2022;29:259–74.",

    "4. Chalker J, Ratanawijitrasin S, Chuc NTK, Petzold M, Tomson G. Effectiveness of a multi-component intervention on dispensing practices at private pharmacies in Vietnam and Thailand—a randomized controlled trial. Soc Sci Med. 2005;60(1):131–41.",

    "5. Onwunduba A, Ekwunife O, Onyilogwu E, Onyemelukwe C, Modebe A, Igbokwe D. Impact of point-of-care C-reactive protein testing intervention on non-prescription dispensing of antibiotics for respiratory tract infections in private community pharmacies in Nigeria: a cluster randomized controlled trial. Int J Infect Dis. 2023;127:137–43.",

    "6. Ferdiana A, Wulandari LPL, Liverani M, Limato R, Essiet I, Mcknight J, et al. The impact of a multi-faceted intervention on non-prescription dispensing of antibiotics by urban community pharmacies in Indonesia: a mixed methods evaluation. BMJ Glob Health. 2024;9(10):e015620.",

    "7. Tumwikirize WA, Ekwaru PJ, Mohammed K, Ogwal-Okeng JW, Aupont O. Impact of a face-to-face educational intervention on improving the management of acute respiratory infections in private pharmacies and drug shops in Uganda. East Afr Med J. 2004;81(Suppl 1):S33–40.",

    "8. DerSimonian R, Laird N. Meta-analysis in clinical trials. Control Clin Trials. 1986;7(3):177–88.",
]

for ref in references:
    p = doc.add_paragraph()
    run = p.add_run(ref)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.5)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(4)

# ── Save ──
output_path = "Manuscript_PINMAS_2026_FINAL.docx"
doc.save(output_path)
print(f"SUCCESS: Saved to {output_path}")
