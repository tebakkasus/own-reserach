# ==============================================================================
# PINMAS IV Meta-Analysis — Primary Analysis Script (R)
# Systematic Review & Meta-Analysis: Interventions to Reduce Non-Prescription
# Antibiotic Dispensing (NPD) in LMIC Community Pharmacies
# ==============================================================================

# Required packages:
# install.packages(c("meta", "metafor", "readr", "dplyr"))

suppressPackageStartupMessages({
  library(meta)
  library(metafor)
  library(readr)
  library(dplyr)
})

# 1. Dataset Construction (Core 3 Cluster-Adjusted Studies)
data_core3 <- data.frame(
  study = c("Chalker et al. (2005)", "Onwunduba et al. (2023)", "Ferdiana et al. (2024)"),
  country = c("Vietnam", "Nigeria", "Indonesia"),
  design = c("Cluster RCT", "Cluster RCT", "Controlled Pre-Post"),
  n_pharmacies = c(55, 20, 270),
  n_encounters = c(273, 600, 810),
  events_int = c(98, 209, 133),
  total_int  = c(138, 300, 240),
  events_ctrl = c(128, 256, 469),
  total_ctrl  = c(135, 300, 570),
  adj_or = c(0.134, 0.279, 0.140),
  ci_low = c(0.057, 0.107, 0.070),
  ci_upp = c(0.316, 0.726, 0.300)
)

# Compute log-OR and standard errors
data_core3 <- data_core3 %>%
  mutate(
    yi = log(adj_or),
    sei = (log(ci_upp) - log(ci_low)) / (2 * 1.959964),
    vi = sei^2
  )

print("=== PINMAS IV: Primary Core Studies Dataset ===")
print(data_core3[, c("study", "country", "adj_or", "ci_low", "ci_upp", "yi", "sei")])

# 2. Generic Inverse-Variance Random-Effects Meta-Analysis (metafor)
res_metafor <- rma(yi = yi, sei = sei, data = data_core3, method = "DL")
print(summary(res_metafor))

# Exponentiate results for reporting
pooled_or <- exp(res_metafor$beta[1])
pooled_ci_low <- exp(res_metafor$ci.lb)
pooled_ci_upp <- exp(res_metafor$ci.ub)

cat("\n=======================================================\n")
cat(sprintf("POOLED ODDS RATIO (DerSimonian-Laird): %.3f (95%% CI: %.3f - %.3f)\n", pooled_or, pooled_ci_low, pooled_ci_upp))
cat(sprintf("Z-statistic: %.3f (p-value: %.4e)\n", res_metafor$zval, res_metafor$pval))
cat(sprintf("Heterogeneity: Q = %.3f (df = %d, p = %.3f), I^2 = %.1f%%, tau^2 = %.4f\n", 
            res_metafor$QE, res_metafor$k - 1, res_metafor$QEp, res_metafor$I2, res_metafor$tau2))
cat("=======================================================\n")

# 3. Meta-Analysis using 'meta' package (for standardized publication output)
m_gen <- metagen(
  TE = yi,
  seTE = sei,
  studlab = study,
  data = data_core3,
  sm = "OR",
  method.tau = "DL",
  common = FALSE,
  random = TRUE
)
print(summary(m_gen))

# 4. Publication-Ready Forest Plot (Saved to PDF & PNG)
if (!dir.exists("Plots")) dir.create("Plots")

# Save PNG
png("Plots/forest_plot_R_meta.png", width = 3000, height = 1500, res = 300)
forest(
  m_gen,
  sortvar = study,
  comb.random = TRUE,
  comb.common = FALSE,
  layout = "RevMan5",
  col.diamond = "red",
  col.diamond.lines = "darkred",
  col.square = "blue",
  col.study = "black",
  label.left = "Favours Intervention",
  label.right = "Favours Control",
  ff.xlab = "bold",
  xlab = "Odds Ratio (log scale)",
  leftcols = c("studlab", "country", "design"),
  leftlabs = c("Study", "Country", "Design"),
  rightcols = c("effect.ci", "w.random"),
  rightlabs = c("Adj. OR [95% CI]", "Weight (%)"),
  digits = 3,
  digits.weight = 1
)
dev.off()
cat("\nForest plot successfully generated via R: Plots/forest_plot_R_meta.png\n")
