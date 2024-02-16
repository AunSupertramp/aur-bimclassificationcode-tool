import streamlit as st
import pandas as pd

# Load your data
@st.cache(allow_output_mutation=True)
def load_data(file_path):
    return pd.read_csv(file_path)

# Save the modified data back to the CSV
def save_data(file_path, data):
    data.to_csv(file_path, index=False)

# Path to the CSV file
file_path = 'UniFormat_MasterFormat.csv'

# Load the data
data = load_data(file_path)

# Streamlit UI
st.title('UniFormat to MasterFormat Editor')

# Display the data editor
st.subheader('Edit Data')
edited_data = st.data_editor(data)

# Button to save the changes made using the data editor
if st.button('Save Changes'):
    save_data(file_path, edited_data)
    st.success('Data saved successfully!')

# Display the current data below the editor for reference
st.subheader('Current Data')
st.write(data)
