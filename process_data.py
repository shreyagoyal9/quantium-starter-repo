import pandas as pd
import glob

# Read all CSV files from data folder
files = glob.glob("data/*.csv")

# Create empty list
dataframes = []

# Loop through files
for file in files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Combine all CSV files
combined_data = pd.concat(dataframes)

# Filter only pink morsel products
pink_morsel_data = combined_data[
    combined_data["product"] == "pink morsel"
]

# Remove $ sign from price column
pink_morsel_data["price"] = (
    pink_morsel_data["price"]
    .replace("[$]", "", regex=True)
    .astype(float)
)

# Create sales column
pink_morsel_data["sales"] = (
    pink_morsel_data["price"] *
    pink_morsel_data["quantity"]
)

# Keep only required columns
final_data = pink_morsel_data[
    ["sales", "date", "region"]
]

# Save cleaned data
final_data.to_csv(
    "formatted_sales_data.csv",
    index=False
)

print("Data processing completed successfully!")