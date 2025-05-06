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

# Function to check for both standard and embedded forms
def check_contact_form(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for standard contact forms
        form_found = soup.find("form") is not None

        # Check for embedded forms inside iframes
        embedded_forms = False
        for iframe in soup.find_all("iframe"):
            if "src" in iframe.attrs:
                iframe_url = iframe["src"]
                try:
                    iframe_response = requests.get(iframe_url, timeout=5)
                    iframe_soup = BeautifulSoup(iframe_response.text, 'html.parser')
                    if iframe_soup.find("form"):
                        embedded_forms = True
                        break  # Exit loop if we find an embedded form
                except requests.exceptions.RequestException:
                    pass  # Ignore errors from iframe URLs

        return form_found or embedded_forms  # Returns True if any form is found

    except requests.exceptions.RequestException:
        return False  # Handle errors gracefully

# Store websites with contact forms
valid_websites = []

for website in websites:
    if check_contact_form(website):
        valid_websites.append(website)

# Convert to DataFrame and save results to CSV
contact_form_df = pd.DataFrame(valid_websites, columns=["Website"])
contact_form_df.to_csv("websites_with_contact_form2.csv", index=False)

print("Filtered list saved to 'websites_with_contact_form.csv'.")
