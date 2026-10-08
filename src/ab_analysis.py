import pandas as pd
import numpy as np
from scipy import stats
import os
os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv("data/raw/ab_data.csv")

# 1. SRM Check (Randomization check) - should be ~50/50
from scipy.stats import chisquare
counts = df['group'].value_counts()
chi2, p_srm = chisquare([counts['control'], counts['treatment']])
print(f"SRM Check p={p_srm:.4f} -> {'PASS' if p_srm>0.05 else 'FAIL'}")

# 2. Standard A/B Test
ctrl = df[df.group=='control']['post_spend']
trt = df[df.group=='treatment']['post_spend']

lift = trt.mean() - ctrl.mean()
lift_pct = lift/ctrl.mean()*100
t_stat, p_val = stats.ttest_ind(trt, ctrl)
se = np.sqrt(ctrl.var()/len(ctrl) + trt.var()/len(trt))
ci_low, ci_high = lift - 1.96*se, lift + 1.96*se

print(f"Lift: {lift:.2f} ({lift_pct:.2f}%) | p={p_val:.4f} | CI=[{ci_low:.2f},{ci_high:.2f}]")

# 3. CUPED - Variance reduction using pre_spend
# theta = cov(post, pre)/var(pre)
theta = np.cov(df['post_spend'], df['pre_spend'])[0,1] / df['pre_spend'].var()
df['cuped_post'] = df['post_spend'] - theta*(df['pre_spend'] - df['pre_spend'].mean())

ctrl_c = df[df.group=='control']['cuped_post']
trt_c = df[df.group=='treatment']['cuped_post']
lift_c = trt_c.mean() - ctrl_c.mean()
t_stat_c, p_val_c = stats.ttest_ind(trt_c, ctrl_c)
se_c = np.sqrt(ctrl_c.var()/len(ctrl_c) + trt_c.var()/len(trt_c))
ci_low_c, ci_high_c = lift_c - 1.96*se_c, lift_c + 1.96*se_c

print(f"CUPED Lift: {lift_c:.2f} | p={p_val_c:.4f} | CI=[{ci_low_c:.2f},{ci_high_c:.2f}] | Var Reduction: {1-se_c/se:.1%}")

# Save results
pd.DataFrame([{
    'metric':'standard', 'lift':lift, 'lift_pct':lift_pct, 'p_value':p_val, 'ci_low':ci_low, 'ci_high':ci_high,
    'se':se
},{
    'metric':'cuped', 'lift':lift_c, 'lift_pct':lift_c/ctrl.mean()*100, 'p_value':p_val_c, 'ci_low':ci_low_c, 'ci_high':ci_high_c,
    'se':se_c
}]).to_csv("data/processed/ab_results.csv", index=False)
