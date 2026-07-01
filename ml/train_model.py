import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import joblib

# STEP 1: Load dataset
df = pd.read_csv("../results/fifo_coverage_log.csv")

print("Dataset loaded:")
print(df.head())

# STEP 2: Keep required columns
df = df[['write_en', 'read_en', 'fifo_state', 'data_type', 'gain_label']]

# STEP 3: Encoding mappings

state_map = {
    "EMPTY": 0,
    "MID": 1,
    "FULL": 2
}

type_map = {
    "ZERO": 0,
    "SMALL": 1,
    "LARGE": 2
}

df['fifo_state'] = df['fifo_state'].map(state_map)
df['data_type']  = df['data_type'].map(type_map)

# STEP 4: Ensure numeric types
df['write_en']   = df['write_en'].astype(int)
df['read_en']    = df['read_en'].astype(int)
df['gain_label'] = df['gain_label'].astype(int)

# STEP 5: Define features and target
X = df[['write_en', 'read_en', 'fifo_state', 'data_type']]
y = df['gain_label']

# STEP 6: Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

print("Model trained!")

# STEP 7: Predict probability of coverage gain
df['predicted_gain'] = model.predict_proba(X)[:, 1]

# STEP 8: Sort testcases
df_sorted = df.sort_values(by='predicted_gain', ascending=False)

print("Top prioritized testcases:")
print(df_sorted.head())

# STEP 9: Save prioritized list
df_sorted.to_csv("prioritized_tests.csv", index=False)
print("Saved prioritized_tests.csv")

# STEP 10: Save model
joblib.dump(model, "model.pkl")
print("Model saved as model.pkl")

# STEP 11: Plot graph
plt.plot(df_sorted['predicted_gain'].values)
plt.title("FIFO Testcase Priority Curve")
plt.xlabel("Testcases")
plt.ylabel("Predicted Coverage Gain")
plt.savefig("priority_plot.png")
print("Plot saved as priority_plot.png")