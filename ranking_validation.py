import pandas as pd
import json

# Read the Excel file
df = pd.read_excel("C:\\Users\\nerme\\Downloads\\Jan Ranking Validation.xlsx")

# The column for January 2026 points
jan_26_col = pd.Timestamp('2026-01-26 00:00:00')

# Filter for  weight category
male_df = df[df['Weight Category'] == 'male37'].copy()

# Get ID and January 26 points
excel_data = {}
for idx, row in male_df.iterrows():
    athlete_id = row['ID']
    points = row[jan_26_col]
    excel_data[athlete_id] = points

# Load JSON data from data.json file
with open("data.json", "r") as f:
    json_data = json.load(f)

# Find discrepancies
discrepancies = []
for athlete_id in excel_data:
    if athlete_id in json_data:
        excel_points = excel_data[athlete_id]
        json_points = float(json_data[athlete_id])
        
        # Compare with tolerance for floating point
        if abs(excel_points - json_points) > 0.02:
            discrepancies.append({
                'ID': athlete_id,
                'Excel_Points': excel_points,
                'JSON_Points': json_points
            })

# Sort by JSON points in descending order
discrepancies.sort(key=lambda x: x['JSON_Points'], reverse=True)

# Print results
print("Mistakes Found (ID, Actual Correct Points in JSON):\n")
for idx, disc in enumerate(discrepancies, 1):
    print(f"{idx}. {disc['ID']}, {disc['JSON_Points']}")

print(f"\nTotal discrepancies found: {len(discrepancies)}")