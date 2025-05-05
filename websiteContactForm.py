import requests
import pandas as pd
from bs4 import BeautifulSoup

# Load the filtered CSV file
df = pd.read_csv('filtered_medspasLV.csv')

# Ensure 'Website' column exists and clean it
if "Website" in df.columns:
    websites = df["Website"].dropna().unique()
else:
    print("No 'Website' column found in CSV.")
    exit()

valid_websites = []  # List to store websites with contact forms

# Function to check for contact forms
def check_contact_form(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        contact_form = soup.find("form", {"id": "contact-form"}) or soup.find("form")

        if contact_form:
            valid_websites.append(url)
            return "✅ Contact form found"
        else:
            return "❌ No contact form found"

    except requests.exceptions.RequestException as e:
        return f"⚠️ Error accessing {url}: {e}"

# Iterate through websites and check for contact forms
for website in websites:
    result = check_contact_form(website)
    print(f"{website}: {result}")

# Save only websites with contact forms to CSV
contact_form_df = pd.DataFrame(valid_websites, columns=["Website"])
contact_form_df.to_csv("websites_with_contact_form2.csv", index=False)

print("Filtered list saved to 'websites_with_contact_form.csv'.")
