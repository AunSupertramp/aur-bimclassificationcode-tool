import streamlit as st
import pandas as pd

# Load and prepare the data
@st.cache
def load_and_prepare_data(uni_format_file, master_format_file):
    uni_format_df = pd.read_csv(uni_format_file)
    master_format_df = pd.read_csv(master_format_file)
    uni_format_df['RelatedMasterFormatCodes'] = uni_format_df['RelatedMasterFormatCodes'].str.split(';')
    uni_format_df = uni_format_df.explode('RelatedMasterFormatCodes').reset_index(drop=True)
    merged_df = pd.merge(uni_format_df, master_format_df, how='left', on='MasterFormatCode')
    return merged_df

# Function to determine if a UniFormat code has related MasterFormat codes
def has_related_codes(code, data):
    return data[data['UniFormatCode'] == code]['RelatedMasterFormatCodes'].notna().any()

data = load_and_prepare_data('UniFormat_MasterFormat.csv', 'MasterFormat_Descriptions.csv')

# Generate dropdown options with an indicator for related codes
options = {code: f"{code} - {desc}" + (" (Related Codes Available)" if has_related_codes(code, data) else "") 
           for code, desc in zip(data['UniFormatCode'].dropna().unique(), data['Description_x'].dropna().unique())}

# UI for selecting UniFormat code
st.title('UniFormat to MasterFormat Mapper')
selected_uni_format = st.selectbox('Select a UniFormat Code', options=list(options.values()))

# Extract the actual selected code
selected_code = selected_uni_format.split(' - ')[0]

# Filter the data for the selected UniFormat code
filtered_data = data[data['UniFormatCode'] == selected_code]

# Display related MasterFormat codes and descriptions
if not filtered_data.empty:
    st.subheader('Related MasterFormat Codes and Descriptions:')
    display_df = filtered_data[['RelatedMasterFormatCodes', 'Description_y']].drop_duplicates()
    display_df.rename(columns={'Description_y': 'Description'}, inplace=True)
    st.table(display_df)
else:
    st.write("No related MasterFormat codes found for the selected UniFormat code.")

# Ensure that your CSV files are named 'UniFormat_MasterFormat.csv' and 'MasterFormat_Descriptions.csv'
# and are located in the same directory as your Streamlit app script.
