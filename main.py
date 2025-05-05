import pandas as pd

df = pd.read_csv('/Users/advisium/Documents/LVLeads/medspasLV.csv')

pd.set_option('display.max_rows', None)

filtered_df = df[["Name", "Email", "Phone", "Website"]]

filtered_df = filtered_df.dropna(subset=["Email"])

filtered_df = filtered_df.drop_duplicates(subset=["Email"], keep='first')

filtered_df = filtered_df.reset_index(drop=True)

filtered_df.to_csv("filtered_medspasLV.csv", index=False)

print(filtered_df[["Name", "Email", "Phone", "Website"]])

