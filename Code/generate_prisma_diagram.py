"""
Generate Clean, Non-Overlapping PRISMA 2020 Flow Diagram for PINMAS IV
Fixes: Box spacing, canvas height, clear separation between all phases
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

os.makedirs('Plots', exist_ok=True)

# Taller canvas (12 x 16 inches) to give plenty of vertical room
fig, ax = plt.subplots(figsize=(12, 16), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Colors
c_box_bg = '#F8FAFC'
c_box_border = '#334155'
c_sec_bg = '#1E3A8A'
c_sec_text = '#FFFFFF'
c_text_main = '#0F172A'
c_text_muted = '#475569'
c_highlight = '#DC2626'
c_inc_bg = '#ECFDF5'
c_inc_border = '#059669'

def draw_box(x, y, w, h, text, header="", is_included=False, is_excluded=False):
    bg = c_inc_bg if is_included else c_box_bg
    border = c_inc_border if is_included else (c_highlight if is_excluded else c_box_border)
    lw = 1.8 if (is_included or is_excluded) else 1.2
    
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                         facecolor=bg, edgecolor=border, linewidth=lw, zorder=2)
    ax.add_patch(box)
    
    if header:
        ax.text(x + w/2, y + h - 1.8, header, fontsize=9.5, fontweight='bold',
                ha='center', va='top', color=c_text_main, family='sans-serif', zorder=3)
        ax.text(x + w/2, y + (h - 2.0)/2, text, fontsize=8.5, ha='center', va='center',
                color=c_text_main, family='sans-serif', zorder=3, multialignment='center')
    else:
        ax.text(x + w/2, y + h/2, text, fontsize=8.5, ha='center', va='center',
                color=c_text_main, family='sans-serif', zorder=3, multialignment='center')

def draw_section_label(y_top, y_bot, text):
    h = y_top - y_bot
    bar = FancyBboxPatch((2, y_bot), 4.5, h, boxstyle="square,pad=0",
                          facecolor=c_sec_bg, edgecolor='none', zorder=2)
    ax.add_patch(bar)
    ax.text(4.25, y_bot + h/2, text, fontsize=10.5, fontweight='bold', color=c_sec_text,
            ha='center', va='center', rotation=90, family='sans-serif', zorder=3)

def draw_arrow(x1, y1, x2, y2):
    arrow = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='->,head_width=3.0,head_length=4.5',
                            color='#475569', linewidth=1.3, zorder=1)
    ax.add_patch(arrow)

# Title
ax.text(50, 98.5, "PRISMA 2020 Flow Diagram for Systematic Review & Meta-Analysis",
        fontsize=12.5, fontweight='bold', ha='center', va='top', family='sans-serif')
ax.text(50, 96.8, "Community Interventions on Non-Prescription Antibiotic Dispensing in LMICs",
        fontsize=10, fontstyle='italic', color=c_text_muted, ha='center', va='top', family='sans-serif')

# ══════════════════════════════════════════
#  PHASE 1: IDENTIFICATION (Y: 94 down to 78)
# ══════════════════════════════════════════
draw_section_label(94, 78, "IDENTIFICATION")

b1_text = "Records identified from:\n• PubMed (n = 1,142)\n• OpenAlex (n = 1,896)\n• Cochrane Library (n = 185)\nTotal: (n = 3,223)"
draw_box(12, 80, 34, 13, b1_text, header="Identification from Databases")

b2_text = "Records identified from:\n• Afari-Asiedu et al. (2022) (n = 15)\n• Cochrane 2025 review (n = 7)\nTotal: (n = 22)"
draw_box(54, 80, 34, 13, b2_text, header="Identification from Other Sources")

# Flow to initial triage (Y: 65 down to 54)
b3_text = "Total records retrieved across all sources (N = 3,245)\nDuplicates removed before screening (n = 0)*\nRecords excluded by automated screening (n = 2,635)\n*Records screened systematically from unified master database"
draw_box(20, 65, 60, 11, b3_text, header="Initial Triage")

draw_arrow(29, 80, 40, 76)
draw_arrow(71, 80, 60, 76)

# ══════════════════════════════════════════
#  PHASE 2: SCREENING (Y: 77 down to 32)
# ══════════════════════════════════════════
draw_section_label(77, 32, "SCREENING")

# Box 4: Title/Abstract Screened (Y: 50 to 60)
b4_text = "Records screened by Title/Abstract\n(n = 610 candidates)\n[588 master pool + 22 citation tracking]"
draw_box(12, 50, 36, 10, b4_text, header="Title & Abstract Screening")

draw_arrow(50, 65, 30, 60)

# Box 5: Excluded at TA (Y: 48 to 61)
b5_text = "Records excluded at Title/Abstract (n = 427):\n• No relevant intervention/outcome signals (n = 367)\n• Non-antibiotic dispensing outcomes (n = 21)\n• High-income country / non-LMIC (n = 12)\n• Review / editorial / qualitative only (n = 14)\n• Clinical trials / non-pharmacy populations (n = 13)\n\nReports carried forward for full-text assessment (n = 183)"
draw_box(54, 47, 42, 14, b5_text, header="Title/Abstract Exclusion Outcomes", is_excluded=True)

draw_arrow(48, 55, 54, 55)

# Box 6: Full Text Assessed (Y: 34 to 44)
b6_text = "Reports sought for full-text retrieval\nand assessed for eligibility\n(n = 183)\n[161 from database screening + 22 from tracking]"
draw_box(12, 34, 36, 10, b6_text, header="Full-Text Eligibility Assessment")

draw_arrow(30, 50, 30, 44)

# Box 7: Excluded at FT (Y: 31 to 45)
b7_text = "Reports excluded after full-text evaluation (n = 169):\n• Public sector prescriber setting (n = 18)\n• Non-private community drug retail setting (n = 34)\n• Non-controlled or observational pre-only (n = 42)\n• Outcome not non-prescription dispensing (n = 26)\n• Malaria/non-antibiotic case management (n = 9)\n• Physician-targeted primary care prescribing (n = 14)\n• Other non-qualifying features (n = 26)"
draw_box(54, 30, 42, 15, b7_text, header="Full-Text Reports Excluded", is_excluded=True)

draw_arrow(48, 39, 54, 39)

# ══════════════════════════════════════════
#  PHASE 3: INCLUDED (Y: 31 down to 2)
# ══════════════════════════════════════════
draw_section_label(31, 2, "INCLUDED")

# Box 8: Qualitative synthesis (Y: 15 to 27)
b8_text = "Studies included in qualitative systematic review (k = 14):\n• Core meta-analysis pool (k = 3): Chalker (2005), Onwunduba (2023), Ferdiana (2024)\n• Additional qualitative pool (k = 11): Awor (2014), Kitutu (2017), Chowdhury (2018),\n  Do (2018), Saif (2024), Visser (2024), Tumwikirize (2004)*, Chalker (2002),\n  Chuc (2002), Rutta (2015), Simba (2016)\n*Tumwikirize 2004: full-text paywalled; extracted from Cochrane 2025 review"
draw_box(12, 15, 76, 11, b8_text, header="Qualitative Systematic Review Inclusion (k = 14)", is_included=True)

draw_arrow(30, 34, 30, 26)

# Box 9: Quantitative synthesis (Y: 3 to 11) — WELL SEPARATED!
b9_text = "Studies included in primary quantitative meta-analysis (k = 3):\n(Chalker 2005, Onwunduba 2023, Ferdiana 2024)\nTotal Pharmacies: N = 345 | Simulated Encounters: N = 1,683\nPooled OR = 0.164 (95% CI: 0.102–0.265; I² = 0.0%, p < 0.0001)"
draw_box(12, 3, 76, 8, b9_text, header="Quantitative Meta-Analysis Inclusion (k = 3)", is_included=True)

draw_arrow(50, 15, 50, 11)

plt.tight_layout()
out_path = "Plots/prisma_flow_diagram.png"
plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print(f"SUCCESS: PRISMA flow diagram saved to {out_path}")
