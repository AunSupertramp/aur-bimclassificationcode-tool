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

# Splitting the layout into two columns
left_column, right_column = st.columns([1, 2])

selected_uni_format_code = None

# Left Column for UniFormat Code selection
with left_column:
    st.subheader("UniFormat Codes")
    # Display a static table of UniFormat codes and descriptions
    st.table(uni_format_df[['UniFormatCode', 'Description']].drop_duplicates())

    # Place buttons in front of each UniFormat code to allow for selection
    for i, row in uni_format_df[['UniFormatCode', 'Description']].drop_duplicates().iterrows():
        if st.button(f"Select {row['UniFormatCode']}"):
            selected_uni_format_code = row['UniFormatCode']

# Right Column for displaying related MasterFormat codes
with right_column:
    st.subheader("Related MasterFormat Codes")
    if selected_uni_format_code:
        st.write(f"Related codes for {selected_uni_format_code}:")
        # Filter the data for the selected UniFormat code
        related_codes = merged_df[merged_df['UniFormatCode'] == selected_uni_format_code]
        for _, related_row in related_codes.iterrows():
            code = related_row['RelatedMasterFormatCodes']
            description = related_row['Description']  # Adjust column name if necessary
            st.markdown(f"**{code}**: {description}")
    else:
        st.write("No UniFormat code selected. Please select a code from the left column.")

# Note: Replace 'Description' with the correct column names from your 'master_format_df' if they differ.
