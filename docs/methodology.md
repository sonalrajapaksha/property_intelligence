# Analytical methodology

The overview reports counts over stored canonical properties and transactions. Tracked transaction value is the sum of recorded sales, **not** a market-size estimate. Sale price and yield summaries use medians. Missing yield stays NULL and is excluded from the median; the yield sample size is displayed.

Comparable distance combines geographic distance (30%), land-area difference (22%), building-area difference (13%), sale age (15%) and sector mismatch (20%). Distance is capped at 100 km; age is capped at ten years. Missing area contributes a neutral 50% difference. Missing coordinates use same-region proximity as a fallback. The displayed similarity is `1 − weighted distance`; it is a ranking aid, not a valuation probability.

The demo is fixed-seed synthetic data and is not evidence of New Zealand market levels, trends or coverage. Import thresholds flag suspicious values for review; they do not declare a transaction wrong.
