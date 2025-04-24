import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import lightgbm as lgb
import os

# Load dataset
df = pd.read_csv("data/processed/final_dataset.csv")
df.dropna(inplace=True)

# Clean & encode
df["District"] = df["District"].astype(str).str.lower().str.strip()
df["Crop"] = df["Crop"].astype(str).str.lower().str.strip()
df["Season"] = df["Season"].astype(str).str.lower().str.strip()

# Features & target
features = ["Crop", "Season", "District", "Area", "mean_ndvi", "Annual_Temp", "Monsoon_Temp"]
target = "Yield"

X = pd.get_dummies(df[features], columns=["Crop", "Season", "District"], drop_first=True)
y = df[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Models
models = {
    "XGBoost": xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42),
    "LightGBM": lgb.LGBMRegressor(n_estimators=100, learning_rate=0.1, random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
}

results = []

# Train & evaluate
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    results.append((name, model, rmse, r2))
    print(f"{name} → RMSE: {rmse:.2f} | R²: {r2:.4f}")

# Select best model
best_model_name, best_model, best_rmse, best_r2 = max(results, key=lambda x: x[3])
print(f"\n✅ Best Model: {best_model_name} (R²: {best_r2:.4f})")

# Predict full dataset
df["Yield_Predicted"] = best_model.predict(X)

# Trigger alerts (bottom 10% yield)
threshold = df["Yield_Predicted"].quantile(0.10)
df["Alert"] = np.where(df["Yield_Predicted"] < threshold, "🚨 Low Yield", "✅ OK")

# Save output
os.makedirs("data/outputs", exist_ok=True)
df.to_csv("data/outputs/agrocast_alerts.csv", index=False)
print("📤 Alert report saved: data/outputs/agrocast_alerts.csv")
