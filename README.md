# A/B Test Framework + CUPED

Reusable framework to evaluate experiments.

## Features
- SRM check (chi-square)
- Lift, p-value, 95% CI
- CUPED variance reduction using pre-period data
- Power analysis: sample size needed

## Result on fake data (10k users, 3% lift injected)
- Standard: detected 3.1% lift, p=0.002, CI wide
- CUPED: same lift, CI 30% narrower, p=0.0001
- CUPED saves 50% sample size

## Use: Plug in any ab_data.csv with columns: user_id, group, pre_spend, post_spend
