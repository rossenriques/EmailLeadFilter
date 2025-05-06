import requests
import pandas as pd
from bs4 import BeautifulSoup

# Load the filtered CSV file
df = pd.read_csv('filtered_leadsLV.csv')

# Ensure required columns exist
if "Website" in df.columns and "Name" in df.columns:
    businesses = df[["Name", "Website"]].dropna()
else:
    print("Required columns ('Name' and 'Website') not found in CSV.")
    exit()

# List to store results
valid_businesses = []

# Function to check for contact forms
def check_contact_form(name, url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        contact_form = soup.find("form") or soup.find("iframe")

        if contact_form:
            valid_businesses.append((name, url, False))  # Store Name, Website, and default Checkbox
            return "✅ Contact form found"
        else:
            return "❌ No contact form found"

    except requests.exceptions.RequestException:
        return "⚠️ Error accessing website"

# Iterate through businesses and check for contact forms
for index, row in businesses.iterrows():
    result = check_contact_form(row["Name"], row["Website"])
    print(f"{row['Website']}: {result}")

# Convert to DataFrame & save to CSV with checkbox column
contact_form_df = pd.DataFrame(valid_businesses, columns=["Name", "Website", "Email Outreach"])
contact_form_df.to_csv("businesses_with_contact_form.csv", index=False)

print("Filtered list saved to 'businesses_with_contact_form.csv'.")

