from statsmodels.stats.power import TTestIndPower
import pandas as pd

# Example: we want to detect 3% lift on 5000 avg spend = 150 naira effect
# std ~ 1500
analysis = TTestIndPower()
effect_size = 150/1500  # lift / std = 0.1

sample_size = analysis.solve_power(effect_size=effect_size, alpha=0.05, power=0.8)
print(f"Need {int(sample_size)} per group to detect 3% lift with 80% power")

# Power curve
import numpy as np
sizes = [1000,2000,5000,10000]
powers = [analysis.power(effect_size, n, 0.05) for n in sizes]
pd.DataFrame({'sample_per_group':sizes, 'power':powers}).to_csv("data/processed/power_curve.csv", index=False)
print("Power curve saved")
