import streamlit as st
import pandas as pd

# Function to load and merge data
def load_and_prepare_data(uni_format_file, master_format_file):
    # Load CSV files
    uni_format_df = pd.read_csv(uni_format_file)
    master_format_df = pd.read_csv(master_format_file)
    
    # Normalize the RelatedMasterFormatCodes column to have a single code per row
    uni_format_df['RelatedMasterFormatCodes'] = uni_format_df['RelatedMasterFormatCodes'].str.split(';')
    uni_format_df = uni_format_df.explode('RelatedMasterFormatCodes').reset_index(drop=True)
    
    # Merge the dataframes on the MasterFormat codes
    merged_df = pd.merge(uni_format_df, master_format_df, how='left', left_on='RelatedMasterFormatCodes', right_on='MasterFormatCode')
    return merged_df

# Load and prepare data
data = load_and_prepare_data('UniFormat_MasterFormat.csv', 'MasterFormat_Descriptions.csv')

# Streamlit UI
st.title('UniFormat to MasterFormat Mapper')

# Display UniFormat codes with descriptions for selection
uni_format_options = data[['UniFormatCode', 'Description_x']].drop_duplicates()
selected_uni_format = st.selectbox('Select a UniFormat Code', options=uni_format_options.apply(lambda x: f"{x['UniFormatCode']} - {x['Description_x']}", axis=1))

# Extract the selected UniFormat code
selected_code = selected_uni_format.split(' - ')[0]

# Filter data for selected UniFormat code
filtered_data = data[data['UniFormatCode'] == selected_code]

if not filtered_data.empty:
    st.subheader('Related MasterFormat Codes and Descriptions:')
    
    # Create a new dataframe for display
    display_df = filtered_data[['RelatedMasterFormatCodes', 'Description_y']].rename(columns={'Description_y': 'Description'}).drop_duplicates()
    
    # Display the dataframe using st.dataframe
    st.dataframe(display_df)
else:
    st.write("No related MasterFormat codes found for the selected UniFormat code.")
