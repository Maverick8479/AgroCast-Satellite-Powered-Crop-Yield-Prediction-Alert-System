import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import numpy as np

# Load dataset
df = pd.read_csv("data/processed/final_dataset.csv")

# Drop rows with missing values
df.dropna(inplace=True)

# Select features and target
features = ["Crop", "Season", "District", "Area", "mean_ndvi", "Annual_Temp", "Monsoon_Temp"]
target = "Yield"

# One-hot encode categorical variables
# Combine all features
df["District"] = df["District"].astype(str)
df["Crop"] = df["Crop"].astype(str)
df["Season"] = df["Season"].astype(str)

features = ["Crop", "Season", "District", "Area", "mean_ndvi", "Annual_Temp", "Monsoon_Temp"]
X = df[features]

# One-hot encode all categorical columns
X = pd.get_dummies(X, columns=["Crop", "Season", "District"], drop_first=True)

# Target variable
y = df["Yield"]

y = df[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost model
model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)
# 🔍 Compute anomaly threshold
mean_yield = y_train.mean()
std_dev = y_train.std()
#threshold = mean_yield - 0.5 * std_dev

# 🔁 Predict for full dataset
df["Yield_Predicted"] = model.predict(X)

low_threshold = df["Yield_Predicted"].quantile(0.10)
df["Alert"] = np.where(df["Yield_Predicted"] < low_threshold, "🚨 Low Yield", "✅ OK")


# 💾 Save alerts
import os
os.makedirs("data/outputs", exist_ok=True)
df.to_csv("data/outputs/agrocast_alerts.csv", index=False)

print("📤 Alert report saved: data/outputs/agrocast_alerts.csv")

# Evaluation
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"✅ Model trained!")
print(f"📈 RMSE: {rmse:.3f}")
print(f"📊 R² Score: {r2:.3f}")
