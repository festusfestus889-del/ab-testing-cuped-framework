import pandas as pd, numpy as np, os
os.makedirs("data/raw", exist_ok=True)
np.random.seed(42)

n=10000
users = pd.DataFrame({
    'user_id': [f"u_{i}" for i in range(n)],
    'group': np.random.choice(['control','treatment'], size=n, p=[0.5,0.5]),
    # Pre-experiment spend (for CUPED)
    'pre_spend': np.random.normal(5000, 1500, n).clip(1000, 10000)
})
# Post-experiment spend: treatment lifts 3%
users['post_spend'] = users['pre_spend'] + np.random.normal(0, 500, n)
users.loc[users['group']=='treatment', 'post_spend'] *= 1.03

users.to_csv("data/raw/ab_data.csv", index=False)
print("A/B data: 10k users, 3% lift injected")
