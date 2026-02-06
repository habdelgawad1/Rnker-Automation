import pandas as pd
import re

# ============================================
# CONFIGURATION - Change these as needed
# ============================================
DIVISION = "Olympic"  # Options: "Cadets", "Juniors", "World Ranking", "Olympic"
TOLERANCE = 0.02  # Points difference tolerance

FILE1 = r"Feb Ranking All.xlsx"
FILE2 = r"Olympic_Kyorugi_Rankings_February_2026.xlsx"

# ============================================
# HELPER FUNCTIONS
# ============================================

def normalize_weight_category(weight_str, gender_prefix=None):
    """
    Convert weight category to standardized format.
    Example: 'M-58 kg' -> 'male58', 'W+67 kg' -> 'femaleAbove67'
    Example: 'M-45 kg' -> 'male45', 'F+68 kg' -> 'femaleAbove68'
    """
    if pd.isna(weight_str):
        return None
    
    weight_str = str(weight_str).strip()
    
    # Handle File2 format (e.g., "M-58 kg", "W+67 kg")
    if weight_str.startswith('M-') or weight_str.startswith('M+'):
        gender = 'male'
    elif weight_str.startswith('W-') or weight_str.startswith('W+'):
        gender = 'female'
    elif weight_str.startswith('F-') or weight_str.startswith('F+'):
        gender = 'female'
    elif weight_str.startswith('G-') or weight_str.startswith('G+'):
        gender = 'female'
    else:
        # For File1 format (e.g., "male45", "femaleAbove68")
        return weight_str
    
    # Extract weight value
    match = re.search(r'(\d+)', weight_str)
    if not match:
        return None
    
    weight = match.group(1)
    
    # Check if it's "above" category
    if '+' in weight_str:
        return f"{gender}Above{weight}"
    else:
        return f"{gender}{weight}"

def normalize_athlete_id(athlete_id):
    """
    Normalize athlete ID to handle country code variations.
    Converts MAR (Morocco) to MOR for consistency.
    """
    if pd.isna(athlete_id):
        return None
    
    athlete_id = str(athlete_id).strip()
    
    # Convert MAR to MOR for Morocco
    if athlete_id.startswith('MAR-'):
        athlete_id = 'MOR-' + athlete_id[4:]
    
    return athlete_id

def get_sheet_mapping(division):
    """Map division to appropriate sheets in both files"""
    division_map = {
        "Cadets": "Cadet Division",
        "Juniors": "Junior Division",
        "Wworld Ranking": "World Ranking",
        "Olympic": "Olympic"
    }
    return division_map.get(division, division)

# ============================================
# MAIN COMPARISON
# ============================================

print("="*80)
print(f"RANKING COMPARISON - {DIVISION} Division")
print("="*80 + "\n")

# Read File 1 (Feb_Ranking_All.xlsx)
print(f"Reading '{DIVISION}' sheet from File 1...")
df1 = pd.read_excel(FILE1, sheet_name=DIVISION)

# Get the date column (should be the last column with points)
date_columns = [col for col in df1.columns if isinstance(col, pd.Timestamp)]
if date_columns:
    points_col = date_columns[-1]  # Use the most recent date
    print(f"Using points from: {points_col}")
else:
    # If no timestamp columns, use the last column
    points_col = df1.columns[-1]
    print(f"Using points from column: {points_col}")

# Create standardized data from File 1
# Use composite key: (athlete_id, weight_category) to handle athletes in multiple categories
file1_data = {}
for idx, row in df1.iterrows():
    athlete_id = normalize_athlete_id(row['ID'])
    weight_cat = normalize_weight_category(row['Weight Category'], None)
    points = row[points_col]
    
    if pd.notna(athlete_id) and pd.notna(points) and pd.notna(weight_cat):
        key = (athlete_id, weight_cat)
        file1_data[key] = {
            'id': athlete_id,
            'weight': weight_cat,
            'points': float(points),
            'name': row.get('Name', 'Unknown'),
            'country': row.get('Country', 'Unknown')
        }

print(f"Found {len(file1_data)} athlete entries in File 1\n")

# Read File 2 (Kyorugi_Ranking_February_2026.xlsx)
print(f"Reading '{DIVISION}' division sheets from File 2...")
xls2 = pd.ExcelFile(FILE2)

# Filter sheets for the specified division
division_keyword = get_sheet_mapping(DIVISION)
relevant_sheets = [sheet for sheet in xls2.sheet_names if division_keyword in sheet]

print(f"Found {len(relevant_sheets)} relevant sheets in File 2")

file2_data = {}
for sheet_name in relevant_sheets:
    df2 = pd.read_excel(FILE2, sheet_name=sheet_name)
    
    # Extract weight category from sheet name
    weight_cat = normalize_weight_category(sheet_name.split('|')[0].strip(), None)
    
    for idx, row in df2.iterrows():
        athlete_id = normalize_athlete_id(row['Member Number']) if 'Member Number' in row else None
        points = row['Total Points'] if 'Total Points' in row else None
        
        if pd.notna(athlete_id) and pd.notna(points) and pd.notna(weight_cat):
            key = (athlete_id, weight_cat)
            file2_data[key] = {
                'id': athlete_id,
                'weight': weight_cat,
                'points': float(points),
                'name': row.get('Member Name', 'Unknown'),
                'country': row.get('Country', 'Unknown')
            }

print(f"Found {len(file2_data)} athlete entries in File 2\n")

# ============================================
# COMPARISON & VALIDATION
# ============================================

print("\n" + "="*80)
print("COMPARISON RESULTS")
print("="*80 + "\n")

# Track all issues
point_discrepancies = []
weight_mismatches = []
only_in_file1 = []
only_in_file2 = []

# Get all unique keys (athlete_id, weight_category)
all_keys = set(file1_data.keys()) | set(file2_data.keys())

for key in sorted(all_keys):
    in_file1 = key in file1_data
    in_file2 = key in file2_data
    
    if in_file1 and in_file2:
        data1 = file1_data[key]
        data2 = file2_data[key]
        
        # Weight categories should already match since they're part of the key
        # But double-check in case of any normalization issues
        if data1['weight'] != data2['weight']:
            weight_mismatches.append({
                'ID': data1['id'],
                'Name': data1['name'],
                'Country': data1['country'],
                'File1_Weight': data1['weight'],
                'File2_Weight': data2['weight']
            })
        
        # Check points match (with tolerance)
        point_diff = abs(data1['points'] - data2['points'])
        if point_diff > TOLERANCE:
            point_discrepancies.append({
                'ID': data1['id'],
                'Name': data1['name'],
                'Weight': data1['weight'],
                'Country': data1['country'],
                'File1_Points': data1['points'],
                'File2_Points': data2['points'],
                'Difference': data2['points'] - data1['points']
            })
    
    elif in_file1 and not in_file2:
        data1 = file1_data[key]
        only_in_file1.append({
            'ID': data1['id'],
            'Name': data1['name'],
            'Weight': data1['weight'],
            'Points': data1['points'],
            'Country': data1['country']
        })
    
    elif in_file2 and not in_file1:
        data2 = file2_data[key]
        only_in_file2.append({
            'ID': data2['id'],
            'Name': data2['name'],
            'Weight': data2['weight'],
            'Points': data2['points'],
            'Country': data2['country']
        })

# ============================================
# HELPER FUNCTION TO FORMAT OUTPUT
# ============================================

def format_results(point_discrepancies, weight_mismatches, only_in_file1, only_in_file2, file1_data, file2_data):
    """Format results for both terminal and file output"""
    output_lines = []
    
    output_lines.append("="*80)
    output_lines.append(f"RANKING COMPARISON - {DIVISION} Division")
    output_lines.append("="*80 + "\n")
    
    total_issues = len(point_discrepancies) + len(weight_mismatches) + len(only_in_file1) + len(only_in_file2)
    
    if total_issues == 0:
        output_lines.append("✅ PERFECT MATCH! No discrepancies found.")
        output_lines.append("   - All IDs match")
        output_lines.append("   - All weight categories match")
        output_lines.append("   - All points match within tolerance")
    else:
        output_lines.append(f"⚠️  TOTAL ISSUES FOUND: {total_issues}\n")
        
        # 1. Point Discrepancies
        if point_discrepancies:
            output_lines.append(f"\n{'='*80}")
            output_lines.append(f"❌ POINT DISCREPANCIES ({len(point_discrepancies)}):")
            output_lines.append("="*80 + "\n")
            for idx, disc in enumerate(point_discrepancies, 1):
                output_lines.append(f"{idx}. ATHLETE DETAILS:")
                output_lines.append(f"   ID:              {disc['ID']}")
                output_lines.append(f"   Name:            {disc['Name']}")
                output_lines.append(f"   Weight Category: {disc['Weight']}")
                output_lines.append(f"   Country:         {disc.get('Country', 'N/A')}")
                output_lines.append(f"   File1 Points:    {disc['File1_Points']:.2f}")
                output_lines.append(f"   File2 Points:    {disc['File2_Points']:.2f}")
                output_lines.append(f"   Difference:      {disc['Difference']:+.2f}")
                output_lines.append(f"   {'-' * 76}\n")
        
        # 2. Weight Category Mismatches
        if weight_mismatches:
            output_lines.append(f"\n{'='*80}")
            output_lines.append(f"❌ WEIGHT CATEGORY MISMATCHES ({len(weight_mismatches)}):")
            output_lines.append("="*80 + "\n")
            for idx, mismatch in enumerate(weight_mismatches, 1):
                output_lines.append(f"{idx}. ATHLETE DETAILS:")
                output_lines.append(f"   ID:                    {mismatch['ID']}")
                output_lines.append(f"   Name:                  {mismatch['Name']}")
                output_lines.append(f"   Country:               {mismatch.get('Country', 'N/A')}")
                output_lines.append(f"   File1 Weight Category: {mismatch['File1_Weight']}")
                output_lines.append(f"   File2 Weight Category: {mismatch['File2_Weight']}")
                output_lines.append(f"   {'-' * 76}\n")
        
        # 3. Only in File 1
        if only_in_file1:
            output_lines.append(f"\n{'='*80}")
            output_lines.append(f"⚠️  ONLY IN FILE 1 ({len(only_in_file1)}):")
            output_lines.append("="*80)
            for idx, athlete in enumerate(only_in_file1, 1):
                output_lines.append(f"{idx}. ID: {athlete['ID']} | {athlete['Name']} | {athlete['Weight']} | {athlete['Points']:.2f} pts | {athlete['Country']}")
        
        # 4. Only in File 2
        if only_in_file2:
            output_lines.append(f"\n{'='*80}")
            output_lines.append(f"⚠️  ONLY IN FILE 2 ({len(only_in_file2)}):")
            output_lines.append("="*80)
            for idx, athlete in enumerate(only_in_file2, 1):
                output_lines.append(f"{idx}. ID: {athlete['ID']} | {athlete['Name']} | {athlete['Weight']} | {athlete['Points']:.2f} pts | {athlete['Country']}")
    
    output_lines.append("\n" + "="*80)
    output_lines.append("SUMMARY")
    output_lines.append("="*80)
    # Count unique athletes in each file
    unique_file1_athletes = len(set(key[0] for key in file1_data.keys()))
    unique_file2_athletes = len(set(key[0] for key in file2_data.keys()))
    output_lines.append(f"Total athlete entries in File 1: {len(file1_data)}")
    output_lines.append(f"Total athlete entries in File 2: {len(file2_data)}")
    output_lines.append(f"Unique athletes in File 1: {unique_file1_athletes}")
    output_lines.append(f"Unique athletes in File 2: {unique_file2_athletes}")
    output_lines.append(f"Point discrepancies:      {len(point_discrepancies)}")
    output_lines.append(f"Weight mismatches:        {len(weight_mismatches)}")
    output_lines.append(f"Only in File 1:           {len(only_in_file1)}")
    output_lines.append(f"Only in File 2:           {len(only_in_file2)}")
    output_lines.append("="*80)
    
    return output_lines

# ============================================
# DISPLAY RESULTS
# ============================================

# Sort lists by points (descending)
point_discrepancies.sort(key=lambda x: x['File2_Points'], reverse=True)
only_in_file1.sort(key=lambda x: x['Points'], reverse=True)
only_in_file2.sort(key=lambda x: x['Points'], reverse=True)

total_issues = len(point_discrepancies) + len(weight_mismatches) + len(only_in_file1) + len(only_in_file2)

total_issues = len(point_discrepancies) + len(weight_mismatches) + len(only_in_file1) + len(only_in_file2)

# Generate formatted output
output_lines = format_results(point_discrepancies, weight_mismatches, only_in_file1, only_in_file2, 
                               file1_data, file2_data)

# Write to file
output_filename = f"{DIVISION}_validation_results.txt"
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"✅ Full results written to: {output_filename}\n")

# Display to terminal (show summary only)
if total_issues == 0:
    print("✅ PERFECT MATCH! No discrepancies found.")
    print("   - All IDs match")
    print("   - All weight categories match")
    print("   - All points match within tolerance")
else:
    print(f"⚠️  TOTAL ISSUES FOUND: {total_issues}\n")
    
    # Show point discrepancies (first 10 only for terminal)
    if point_discrepancies:
        print(f"❌ POINT DISCREPANCIES ({len(point_discrepancies)}):")
        print("-" * 80)
        display_count = min(10, len(point_discrepancies))
        for idx, disc in enumerate(point_discrepancies[:display_count], 1):
            print(f"\n{idx}. ATHLETE DETAILS:")
            print(f"   ID:              {disc['ID']}")
            print(f"   Name:            {disc['Name']}")
            print(f"   Weight Category: {disc['Weight']}")
            print(f"   Country:         {disc.get('Country', 'N/A')}")
            print(f"   File1 Points:    {disc['File1_Points']:.2f}")
            print(f"   File2 Points:    {disc['File2_Points']:.2f}")
            print(f"   Difference:      {disc['Difference']:+.2f}")
            print(f"   {'-' * 76}")
        
        if len(point_discrepancies) > display_count:
            print(f"\n... and {len(point_discrepancies) - display_count} more point discrepancies")
            print(f"(See {output_filename} for complete list)")
    
    # Show weight mismatches summary (first 5 only)
    if weight_mismatches:
        print(f"\n❌ WEIGHT CATEGORY MISMATCHES ({len(weight_mismatches)}):")
        print("-" * 80)
        display_count = min(5, len(weight_mismatches))
        for idx, mismatch in enumerate(weight_mismatches[:display_count], 1):
            print(f"{idx}. {mismatch['ID']} | {mismatch['Name']} | File1: {mismatch['File1_Weight']} | File2: {mismatch['File2_Weight']}")
        
        if len(weight_mismatches) > display_count:
            print(f"... and {len(weight_mismatches) - display_count} more weight mismatches")
            print(f"(See {output_filename} for complete list)")
    
    # Show summary for only in file1/file2
    if only_in_file1:
        print(f"\n⚠️  ONLY IN FILE 1: {len(only_in_file1)} athletes")
        print(f"   (See {output_filename} for complete list)")
    
    if only_in_file2:
        print(f"\n⚠️  ONLY IN FILE 2: {len(only_in_file2)} athletes")
        print(f"   (See {output_filename} for complete list)")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
# Count unique athletes in each file
unique_file1_athletes = len(set(key[0] for key in file1_data.keys()))
unique_file2_athletes = len(set(key[0] for key in file2_data.keys()))
print(f"Total athlete entries in File 1: {len(file1_data)}")
print(f"Total athlete entries in File 2: {len(file2_data)}")
print(f"Unique athletes in File 1: {unique_file1_athletes}")
print(f"Unique athletes in File 2: {unique_file2_athletes}")
print(f"Point discrepancies:      {len(point_discrepancies)}")
print(f"Weight mismatches:        {len(weight_mismatches)}")
print(f"Only in File 1:           {len(only_in_file1)}")
print(f"Only in File 2:           {len(only_in_file2)}")
print("="*80)