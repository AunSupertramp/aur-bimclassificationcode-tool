import streamlit as st
import pandas as pd

# Assuming your csv files are named 'UniFormat_MasterFormat.csv' and 'MasterFormat_Descriptions.csv'
# and are structured correctly according to your previous messages.

def load_data():
    uni_format = pd.read_csv('UniFormat_MasterFormat.csv')
    master_format = pd.read_csv('MasterFormat_Descriptions.csv')
    # Normalize the RelatedMasterFormatCodes to be a list of codes
    uni_format['RelatedMasterFormatCodes'] = uni_format['RelatedMasterFormatCodes'].str.split(';')
    uni_format = uni_format.explode('RelatedMasterFormatCodes').reset_index(drop=True)
    # Merge on the MasterFormat codes
    merged = pd.merge(uni_format, master_format, how='left', left_on='RelatedMasterFormatCodes', right_on='MasterFormatCode')
    return uni_format.drop_duplicates(), merged

# Load the data
uni_format_df, merged_df = load_data()

# Streamlit UI layout
st.title("BIM QTO Tools - Code Mapper")

# Display UniFormat codes and descriptions in a table
st.subheader("UniFormat Codes")
uni_format_table = uni_format_df[['UniFormatCode', 'Description']]

# Using a button to select the UniFormat code
selected_code = None
for index, row in uni_format_table.iterrows():
    if st.button(f"{row['UniFormatCode']} - {row['Description']}"):
        selected_code = row['UniFormatCode']

# If a code is selected, display the related MasterFormat codes
if selected_code:
    st.subheader(f"Related MasterFormat Codes for {selected_code}")
    related_codes = merged_df[merged_df['UniFormatCode'] == selected_code]
    for _, rel_row in related_codes.iterrows():
        st.text(f"{rel_row['RelatedMasterFormatCodes']} - {rel_row['Description']}")
else:
    st.subheader("Select a UniFormat code from the list above")
