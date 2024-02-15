import streamlit as st
import pandas as pd

# Function to load and prepare data
def load_and_prepare_data():
    # Assuming your csv files are named 'UniFormat_MasterFormat.csv' and 'MasterFormat_Descriptions.csv'
    uni_format_df = pd.read_csv('UniFormat_MasterFormat.csv')
    master_format_df = pd.read_csv('MasterFormat_Descriptions.csv')

    # Normalize and merge
    uni_format_df['RelatedMasterFormatCodes'] = uni_format_df['RelatedMasterFormatCodes'].str.split(';')
    uni_format_df = uni_format_df.explode('RelatedMasterFormatCodes').reset_index(drop=True)
    merged_df = pd.merge(uni_format_df, master_format_df, how='left', left_on='RelatedMasterFormatCodes', right_on='MasterFormatCode')
    return merged_df

# Load the data
data = load_and_prepare_data()

# Streamlit UI layout
st.title("BIM QTO Tools")

# Column layout for UniFormat selection and Related codes display
col1, col2 = st.columns([1, 2])

# Column for UniFormat Code selection
with col1:
    st.header("UniFormat")
    selected_uni_format = st.selectbox("Choose a UniFormat Code", data['UniFormatCode'].unique())

# Column for displaying related MasterFormat codes
with col2:
    st.header("Related MasterFormat Codes")
    if st.button('Show Related Codes'):
        # Filter data for selected UniFormat code
        filtered_data = data[data['UniFormatCode'] == selected_uni_format]
        if not filtered_data.empty:
            for _, row in filtered_data.iterrows():
                st.text(f"{row['RelatedMasterFormatCodes']} - {row['Description']}")
        else:
            st.write("No related MasterFormat codes found.")

