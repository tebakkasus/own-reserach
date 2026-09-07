# Kumpulan Script Template RStudio diluar Revman
# Made by and Courtesy of: ResearchClassbyAyers


# 1. Metaprop

# Install package
Install.packages("meta")

# Load data
data <- read.csv("data_prop.csv")

atau

data <- data.frame(
  study = c("Study A", "Study B", "Study C"),
  event = c(10, 25, 5),
  n = c(100, 200, 50)
)

# Meta-analysis
m_prop <- metaprop(
  event = event,
  n = n,
  studlab = study,
  data = data,
  sm = "PLOGIT" # recommended
)

# Forest plot
forest(m_prop)

# Summary
summary(m_prop)


# 2. Meta for mean change

# 1. Install & Load Package

if (!requireNamespace("metafor", quietly = TRUE)) {
  install.packages("metafor")
}
library(metafor)

# 2. Input Data (Mean Change)

study <- c("Study A", "Study B", "Study C")

mean_change <- c(-6.8, -4.5, -9.1) # negative = improvement


# 3. Convert SD → Standard Error

se_change <- sd_change / sqrt(n)


# 4. Random-Effects Meta-analysis

model <- rma(
  yi = mean_change, # effect size
  sei = se_change, # standard error
  method = "REML", # recommended
  slab = study
)


# 5. Summary Result

summary(model)


# 6. Forest Plot

forest(
  model,
  xlab = "Mean Change (negative = improvement)",
  slab = study
)


# 7. Extract Key Results

cat("Pooled Mean Change:", round(model$beta, 2), "\n")
cat("95% CI:", round(model$ci.lb, 2), "to", round(model$ci.ub, 2), "\n")


# 8. Prediction Interval (IMPORTANT)

pred <- predict(model)

cat(
  "Prediction Interval:",
  round(pred$pi.lb, 2),
  "to",
  round(pred$pi.ub, 2),
  "\n"
)