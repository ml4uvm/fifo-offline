import pandas as pd
from sklearn.cluster import KMeans

# Load data
df = pd.read_csv("prioritized_tests.csv")

print("Original size:", len(df))

# Encode categorical features
state_map = {"EMPTY": 0, "MID": 1, "FULL": 2}
type_map  = {"ZERO": 0, "SMALL": 1, "LARGE": 2, "NEG": 3}

df['fifo_state'] = df['fifo_state'].map(state_map)
df['data_type']  = df['data_type'].map(type_map)

# Features for clustering
X = df[['write_en', 'read_en', 'fifo_state', 'data_type', 'predicted_gain']]

# Number of clusters
k = 50

kmeans = KMeans(n_clusters=k, random_state=42)
df['cluster'] = kmeans.fit_predict(X)

# Pick BEST testcase from each cluster
best_tests = df.loc[df.groupby('cluster')['predicted_gain'].idxmax()]

# Sort again
best_tests = best_tests.sort_values(by='predicted_gain', ascending=False)

# Save result
best_tests.to_csv("clustered_tests.csv", index=False)

print("Reduced size:", len(best_tests))
print(best_tests.head())