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
left_column, right_column = st.columns(2)

# Left Column for UniFormat Code selection
with left_column:
    st.subheader("UniFormat Codes")
    # Display UniFormat codes and descriptions in a table
    # This creates an interactive table where you can select rows
    selected_indices = st.multiselect("Select a UniFormat Code", options=merged_df.index, format_func=lambda x: f"{merged_df.loc[x, 'UniFormatCode']} - {merged_df.loc[x, 'Description_x']}")
    selected_rows = merged_df.loc[selected_indices]

# Right Column for displaying related MasterFormat codes
with right_column:
    st.subheader("Related MasterFormat Codes")
    # Check if there's any selection
    if not selected_rows.empty:
        for _, row in selected_rows.iterrows():
            code = row['RelatedMasterFormatCodes']
            description = row['Description_y']  # Ensure this column name matches the description column in your MasterFormat descriptions CSV
            st.markdown(f"**{code}**: {description}")
    else:
        st.write("No UniFormat code selected.")

# Make sure to adjust the column names 'Description_x' and 'Description_y' if they differ in your CSV files.
