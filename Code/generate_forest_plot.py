"""
Generate Publication-Quality Forest Plot — PINMAS IV Meta-Analysis
Approach: Dual-subplot (left=table, right=forest plot) to eliminate ALL overlaps
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import os

os.makedirs('Plots', exist_ok=True)

# Colors
C_BLUE   = '#2563EB'
C_DARK   = '#1E40AF'
C_RED    = '#DC2626'
C_DARKRED = '#991B1B'
C_GREY   = '#94A3B8'
C_BLACK  = '#0F172A'
C_MUTED  = '#475569'
C_BG     = '#FFFFFF'

# Data
studies = [
    {"name": "Chalker et al. (2005)",      "loc": "Vietnam",   "or": 0.134, "lo": 0.057, "hi": 0.316, "w": "31.4%"},
    {"name": "Onwunduba et al. (2023)",     "loc": "Nigeria",   "or": 0.279, "lo": 0.107, "hi": 0.726, "w": "25.1%"},
    {"name": "Ferdiana et al. (2024)",      "loc": "Indonesia", "or": 0.140, "lo": 0.070, "hi": 0.300, "w": "43.5%"},
]
pooled = {"name": "Pooled (Random-Effects)", "or": 0.164, "lo": 0.102, "hi": 0.265, "w": "100.0%"}

# ══════════════════════════════════════════
#  FIGURE SETUP: 2 columns via GridSpec
#  Left column = text table (wide)
#  Right column = forest plot graphics
# ══════════════════════════════════════════
fig = plt.figure(figsize=(14, 7), dpi=300)
gs = GridSpec(1, 2, width_ratios=[3.8, 1.8], wspace=0.08)

ax_table = fig.add_subplot(gs[0])  # Left: text table
ax_plot  = fig.add_subplot(gs[1])  # Right: forest plot

# ══════════════════════════════════════════
#  LEFT PANEL: TEXT TABLE
# ══════════════════════════════════════════
ax_table.axis('off')
ax_table.set_xlim(0, 10)
ax_table.set_ylim(-3, 9)

# Column headers
y_hdr = 8.0
ax_table.text(0.0, y_hdr, "Study", fontsize=11, fontweight='bold', va='bottom', fontfamily='sans-serif')
ax_table.text(4.8, y_hdr, "OR [95% CI]", fontsize=11, fontweight='bold', va='bottom', fontfamily='sans-serif')
ax_table.text(9.2, y_hdr, "Weight", fontsize=11, fontweight='bold', va='bottom', fontfamily='sans-serif', ha='right')

# Header line
ax_table.plot([0, 9.5], [y_hdr - 0.15, y_hdr - 0.15], color=C_BLACK, lw=0.8)

# Study rows
y_positions = [6.5, 5.5, 4.5]
for i, s in enumerate(studies):
    y = y_positions[i]
    ax_table.text(0.0, y, f'{s["name"]}', va='center', fontsize=10.5, fontfamily='sans-serif')
    ax_table.text(0.0, y - 0.35, f'  {s["loc"]}', va='center', fontsize=9, color=C_MUTED, fontfamily='sans-serif')
    ax_table.text(4.8, y, f'{s["or"]:.3f}  [{s["lo"]:.3f}, {s["hi"]:.3f}]', va='center', fontsize=10.5, fontfamily='sans-serif')
    ax_table.text(9.2, y, s["w"], va='center', fontsize=10.5, fontfamily='sans-serif', ha='right')

# Separator line above pooled
y_sep = 3.5
ax_table.plot([0, 9.5], [y_sep, y_sep], color=C_BLACK, lw=0.8)

# Pooled row
y_pooled = 2.5
ax_table.text(0.0, y_pooled, pooled["name"], va='center', fontsize=10.5, fontweight='bold', fontfamily='sans-serif')
ax_table.text(4.8, y_pooled, f'{pooled["or"]:.3f}  [{pooled["lo"]:.3f}, {pooled["hi"]:.3f}]', va='center', fontsize=10.5, fontweight='bold', fontfamily='sans-serif')
ax_table.text(9.2, y_pooled, pooled["w"], va='center', fontsize=10.5, fontweight='bold', fontfamily='sans-serif', ha='right')

# Statistics at bottom of table
ax_table.text(0.0, 0.5, r"$I^2$ = 0.0%,  $\tau^2$ = 0.000,  $Q$ = 1.58  ($p$ = 0.454)",
              fontsize=9.5, style='italic', fontfamily='sans-serif')
ax_table.text(0.0, -0.1, r"Test for overall effect:  $Z$ = −7.38  ($p$ < 0.0001)",
              fontsize=9.5, style='italic', fontfamily='sans-serif')

# ══════════════════════════════════════════
#  RIGHT PANEL: FOREST PLOT GRAPHICS
# ══════════════════════════════════════════
ax_plot.set_xlim(-2.5, 1.0)   # log(OR) range: log(0.05)=-3 to log(5)=1.6
ax_plot.set_ylim(-3, 9)
ax_plot.set_xscale('log')
ax_plot.set_xlim(0.02, 6.0)

# Same Y positions as table
for i, s in enumerate(studies):
    y = y_positions[i]
    # CI whisker
    ax_plot.plot([s["lo"], s["hi"]], [y, y], color=C_BLUE, lw=2.5, solid_capstyle='round', zorder=2)
    # Point estimate
    ms = float(s["w"].replace("%","")) * 1.3
    ax_plot.scatter(s["or"], y, color=C_BLUE, s=ms, marker='s', zorder=3, edgecolors=C_DARK, linewidths=0.5)

# Separator line
ax_plot.plot([0.02, 6.0], [y_sep, y_sep], color=C_BLACK, lw=0.8)

# Pooled diamond
dw = 0.22
dx = [pooled["lo"], pooled["or"], pooled["hi"], pooled["or"], pooled["lo"]]
dy = [y_pooled, y_pooled+dw, y_pooled, y_pooled-dw, y_pooled]
ax_plot.fill(dx, dy, color=C_RED, alpha=0.88, zorder=4)
ax_plot.plot(dx, dy, color=C_DARKRED, lw=1.8, zorder=5)

# Reference lines
ax_plot.axvline(1.0, color=C_GREY, linestyle='--', lw=1.2, zorder=1, ymin=0, ymax=0.85)
ax_plot.axvline(pooled["or"], color=C_RED, linestyle=':', lw=1.0, alpha=0.5, zorder=1, ymin=0, ymax=0.85)

# X-axis
ax_plot.set_xticks([0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0])
ax_plot.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax_plot.tick_params(axis='x', labelsize=9, length=3, pad=3)
ax_plot.set_xlabel("Odds Ratio (log scale)", fontsize=10, fontweight='bold', fontfamily='sans-serif', labelpad=8)

# Direction labels below axis
ax_plot.text(0.025, -1.2, "<── Favours Intervention", fontsize=9.5, fontweight='bold', color=C_BLUE, va='top', fontfamily='sans-serif')
ax_plot.text(1.5, -1.2, "Favours Control ──>", fontsize=9.5, fontweight='bold', color=C_GREY, va='top', fontfamily='sans-serif')

# Clean borders
ax_plot.spines['top'].set_visible(False)
ax_plot.spines['right'].set_visible(False)
ax_plot.spines['left'].set_visible(False)
ax_plot.spines['bottom'].set_linewidth(0.8)

# Hide y ticks
ax_plot.set_yticks([])

# ══════════════════════════════════════════
#  MAIN TITLE — above both panels
# ══════════════════════════════════════════
fig.text(0.5, 0.96, "Forest Plot: Interventions to Reduce Non-Prescription Antibiotic Dispensing",
         fontsize=12, fontweight='bold', ha='center', va='top', fontfamily='sans-serif')
fig.text(0.5, 0.925, "in LMIC Community Pharmacies (PINMAS IV)",
         fontsize=10, fontstyle='italic', color=C_MUTED, ha='center', va='top', fontfamily='sans-serif')

plt.subplots_adjust(top=0.89, bottom=0.14, left=0.02, right=0.98)

plot_path = "Plots/forest_plot_core3.png"
plt.savefig(plot_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print(f"SUCCESS: Forest plot saved to {plot_path}")
