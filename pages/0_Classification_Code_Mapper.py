import streamlit as st
import pandas as pd

# Function to load data
def load_data():
    uni_format_df = pd.read_csv('UniFormat_MasterFormat.csv')
    master_format_df = pd.read_csv('MasterFormat_Descriptions.csv')
    merged_df = uni_format_df.merge(master_format_df, left_on='RelatedMasterFormatCodes', right_on='MasterFormatCode')
    return uni_format_df.drop_duplicates(), merged_df

# Load the data
uni_format_df, merged_df = load_data()

# Streamlit UI layout
st.title("BIM QTO Tools - Code Mapper")

# Interactive table for UniFormat selection
st.subheader("UniFormat Codes")
# Display the dataframe
st.dataframe(uni_format_df.style.applymap(lambda _: 'background-color: lightgrey', subset=['UniFormatCode']))

# Placeholder for related MasterFormat codes
related_placeholder = st.empty()

# Session state to store the selected UniFormat code
if 'selected_uni_format_code' not in st.session_state:
    st.session_state['selected_uni_format_code'] = None

# Function to set the selected UniFormat code and display related MasterFormat codes
def show_related_master_format(uniformat_code):
    st.session_state['selected_uni_format_code'] = uniformat_code
    related_placeholder.write(f"Related MasterFormat Codes for {uniformat_code}:")
    related_codes = merged_df[merged_df['UniFormatCode'] == uniformat_code]
    related_placeholder.write(related_codes)

# Buttons for each UniFormat code
for uniformat_code in uni_format_df['UniFormatCode'].unique():
    st.button(f"Select {uniformat_code}", on_click=show_related_master_format, args=(uniformat_code,))

# Display related MasterFormat codes if a UniFormat code is selected
if st.session_state['selected_uni_format_code']:
    show_related_master_format(st.session_state['selected_uni_format_code'])
