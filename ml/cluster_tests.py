import pandas as pd
from sklearn.cluster import KMeans

# Load data
df = pd.read_csv("prioritized_tests.csv")

print("Original size:", len(df))

# ============================================
# 🔥 REMOVE IDLE CYCLES (IMPORTANT)
# ============================================
df = df[(df['write_en'] == 1) | (df['read_en'] == 1)]

# ============================================
# 🔥 REMOVE DUPLICATES
# ============================================
df = df.drop_duplicates()

print("After cleaning:", len(df))

# ============================================
# FEATURES (must be numeric)
# ============================================
X = df[['write_en', 'read_en', 'fifo_state', 'data_type', 'predicted_gain']]

# ============================================
# 🔥 SAFE CLUSTER COUNT
# ============================================
k = min(len(df), 35)

kmeans = KMeans(n_clusters=k, random_state=42)
df['cluster'] = kmeans.fit_predict(X)

# ============================================
# PICK BEST TEST PER CLUSTER
# ============================================
best_tests = df.loc[df.groupby('cluster')['predicted_gain'].idxmax()]

# Sort by importance
best_tests = best_tests.sort_values(by='predicted_gain', ascending=False)

# ============================================
# SAVE FOR TEST SEQUENCE
# ============================================
best_tests[['write_en','read_en','fifo_state','data_type']].to_csv(
    "clustered_tests.csv", index=False
)

print("Reduced size:", len(best_tests))
print(best_tests.head())