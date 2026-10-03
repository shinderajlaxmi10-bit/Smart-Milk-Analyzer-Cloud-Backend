import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("dataset.csv")

# Input features
X = data[["pH", "Temperature", "TDS"]]

# Output
y = data["Risk"]

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train model
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("ML Model trained successfully!")
print("Model saved as model.pkl")
