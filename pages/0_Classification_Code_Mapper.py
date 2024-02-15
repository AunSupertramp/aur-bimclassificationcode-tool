import streamlit as st
import pandas as pd

# Function to load and prepare data
def load_and_prepare_data():
    # Load the UniFormat to MasterFormat mapping and MasterFormat descriptions
    uni_format_df = pd.read_csv('UniFormat_MasterFormat.csv')
    master_format_df = pd.read_csv('MasterFormat_Descriptions.csv')
    
    # Normalize the 'RelatedMasterFormatCodes' to be a list of codes
    uni_format_df['RelatedMasterFormatCodes'] = uni_format_df['RelatedMasterFormatCodes'].str.split(';')
    uni_format_df = uni_format_df.explode('RelatedMasterFormatCodes').reset_index(drop=True)
    
    # Merge the dataframes on the MasterFormat codes
    merged_df = pd.merge(uni_format_df, master_format_df, how='left', on='MasterFormatCode')
    return merged_df

# Load and prepare data
data = load_and_prepare_data()

# Streamlit UI layout
st.title("BIM QTO Tools - Code Mapper")

# Column layout for UniFormat selection and Related codes display
col1, col2 = st.columns([2, 3])

# Column for UniFormat Code selection
with col1:
    st.header("UniFormat Codes")
    selected_uni_format = st.selectbox("Select a UniFormat Code", options=data['UniFormatCode'].unique())

# Column for displaying related MasterFormat codes
with col2:
    st.header("Related MasterFormat Codes")
    # Filter data for selected UniFormat code
    filtered_data = data[data['UniFormatCode'] == selected_uni_format]
    
    if not filtered_data.empty:
        for _, row in filtered_data.iterrows():
            code = row['RelatedMasterFormatCodes']
            description = row['Description']
            st.markdown(f"**{code}**: {description}")
    else:
        st.write("No related MasterFormat codes found for the selected UniFormat code.")
 