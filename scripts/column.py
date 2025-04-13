import pandas as pd

# Load your dataset
df = pd.read_csv("data/raw/crop_yield.csv")

# Optional cleanup: Strip whitespace from column names
df.columns = df.columns.str.strip()

# Convert Area and Production to numeric (in case of any strings)
df["Area"] = pd.to_numeric(df["Area"], errors="coerce")
df["Production"] = pd.to_numeric(df["Production"], errors="coerce")

# Calculate Yield
df["Yield"] = df["Production"] / df["Area"]

# View sample output
print(df[["District_Name", "Crop_Year", "Crop", "Area", "Production", "Yield"]].head())
df = df[df["Area"] > 0]
df.to_csv("data/processed/crop_yield_with_yield.csv", index=False)
