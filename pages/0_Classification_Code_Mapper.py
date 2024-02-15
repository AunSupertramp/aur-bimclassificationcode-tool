import streamlit as st
import pandas as pd

# Load your data
uni_format_df = pd.read_csv('UniFormat_MasterFormat.csv')
master_format_df = pd.read_csv('MasterFormat_Descriptions.csv')

# Normalize the RelatedMasterFormatCodes column to have a single code per row
uni_format_df['RelatedMasterFormatCodes'] = uni_format_df['RelatedMasterFormatCodes'].str.split(';')
uni_format_df = uni_format_df.explode('RelatedMasterFormatCodes').reset_index(drop=True)
uni_format_df['RelatedMasterFormatCodes'] = uni_format_df['RelatedMasterFormatCodes'].str.strip()

# Merge the dataframes on the MasterFormat codes
merged_df = pd.merge(uni_format_df, master_format_df, how='left', left_on='RelatedMasterFormatCodes', right_on='MasterFormatCode')

# Streamlit UI layout
st.title("BIM QTO Tools - Code Mapper")

# Display UniFormat codes and descriptions in a table
st.subheader("UniFormat Codes")
unique_uni_codes = uni_format_df[['UniFormatCode', 'Description']].drop_duplicates().reset_index(drop=True)

# Create an empty placeholder for displaying related codes
related_codes_placeholder = st.empty()

# Variable to store the selected UniFormat code
selected_uni_format_code = None

# Display buttons for each UniFormat code to allow for selection
for index, row in unique_uni_codes.iterrows():
    if st.button(f"{row['UniFormatCode']} - {row['Description']}", key=f"btn_{index}"):
        selected_uni_format_code = row['UniFormatCode']
        related_codes_placeholder.subheader(f"Related MasterFormat Codes for {selected_uni_format_code}:")
        # Filter the data for the selected UniFormat code
        related_codes = merged_df[merged_df['UniFormatCode'] == selected_uni_format_code]
        for _, rel_row in related_codes.iterrows():
            related_codes_placeholder.text(f"{rel_row['RelatedMasterFormatCodes']} - {rel_row['Description']}")

# If no code is selected yet, prompt the user
if not selected_uni_format_code:
    related_codes_placeholder.subheader("Select a UniFormat code from the list above")
