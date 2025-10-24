import pandas as pd
import re

# Read the CSV file (replace with your file path)
df = pd.read_csv("First_20pincodes.csv")

# Function to extract the 6-digit PIN code
def extract_pincode(address):
    if not isinstance(address, str):
        return None
    # Find a 6-digit number just before a comma or end of string
    match = re.search(r'(\d{6})(?=\s*,|\s*$)', address)
    return match.group(1) if match else None

# Apply the function to your address column (change column name if needed)
df['Pincode'] = df['Address'].apply(extract_pincode)

# Save the result
df.to_csv("addresses_with_pincode.csv", index=False)

print("✅ Pincode extraction completed! Saved as 'addresses_with_pincode.csv'")
