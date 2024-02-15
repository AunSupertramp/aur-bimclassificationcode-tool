import streamlit as st
import pandas as pd

# Function to load data
def load_data():
    uni_format_df = pd.read_csv('UniFormat_MasterFormat.csv')
    master_format_df = pd.read_csv('MasterFormat_Descriptions.csv')
    return uni_format_df, master_format_df

uni_format_df, master_format_df = load_data()

# Layout the sidebar with UniFormat selection
st.sidebar.title("UniFormat Codes")
# Assuming the 'UniFormatCode' column contains unique values
uni_format_selection = st.sidebar.selectbox("Choose a UniFormat Code", uni_format_df['UniFormatCode'].unique())

# Main area
st.title("Welcome to BIM QTO Tools")
st.markdown("## Related MasterFormat Codes")

# Find related MasterFormat codes
selected_uni_format = uni_format_df[uni_format_df['UniFormatCode'] == uni_format_selection]
related_codes = selected_uni_format['RelatedMasterFormatCodes'].iloc[0].split(';')

# Display related codes and descriptions
if related_codes:
    for code in related_codes:
        # Assuming there's one row per MasterFormatCode in the master_format_df
        description = master_format_df[master_format_df['MasterFormatCode'] == code.strip()]['Description'].iloc[0]
        st.markdown(f"**{code.strip()}**: {description}")
else:
    st.write("No related MasterFormat codes found.")
