import pandas as pd
import os

# 📥 Load Crop Yield Dataset
crop_df = pd.read_csv("data/processed/crop_yield_with_yield.csv")
crop_df.columns = crop_df.columns.str.strip()
crop_df.rename(columns={"District_Name": "District", "State_Name": "State"}, inplace=True)

# Clean text fields
crop_df["District"] = crop_df["District"].str.lower().str.strip()
crop_df["State"] = crop_df["State"].str.lower().str.strip()
crop_df["Crop"] = crop_df["Crop"].str.lower().str.strip()

# 📥 Load NDVI Dataset
ndvi_df = pd.read_csv("data/processed/ndvi_by_district.csv")
ndvi_df["district"] = ndvi_df["district"].str.lower().str.strip()

# 📥 Load Temperature Dataset
temp_df = pd.read_csv("data/raw/TEMP_ANNUAL_SEASONAL_MEAN.csv")
temp_df.columns = temp_df.columns.str.strip()
temp_df.rename(columns={"YEAR": "Crop_Year"}, inplace=True)

# 🔗 Merge Crop + NDVI
merged = pd.merge(crop_df, ndvi_df, left_on="District", right_on="district", how="left")
merged.drop(columns=["district"], inplace=True)  # remove duplicate

# 🔗 Merge with Temperature on Year
merged = pd.merge(merged, temp_df, on="Crop_Year", how="left")

# ✅ Select and Rename Relevant Columns
final = merged[[
    "State", "District", "Crop_Year", "Season", "Crop", "Area", "Production", "Yield",
    "mean_ndvi", "ANNUAL", "JUN-SEP"
]].rename(columns={
    "ANNUAL": "Annual_Temp",
    "JUN-SEP": "Monsoon_Temp"
})


# 💾 Save final merged dataset
output_path = "data/processed/final_dataset.csv"
os.makedirs("data/processed", exist_ok=True)
final.to_csv(output_path, index=False)
print(f"✅ Final merged dataset saved at: {output_path}")
