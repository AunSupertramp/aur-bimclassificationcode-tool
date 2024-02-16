import streamlit as st
import pandas as pd

# Load your data
@st.cache(allow_output_mutation=True)
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Save the modified data back to the CSV
def save_data(file_path, data):
    data.to_csv(file_path, index=False)

# Path to the CSV file
file_path = 'UniFormat_MasterFormat.csv'

# Load the data
data = load_data(file_path)

# Streamlit UI
st.title('UniFormat to MasterFormat Editor')

# Display DataFrame in edit mode
st.subheader('Edit Data')
edited_data = st.text_area("Edit the data in CSV format:", data.to_csv(index=False))

# Parse the edited data back to a DataFrame and save it
if st.button('Save Changes'):
    # Attempt to parse the edited data
    try:
        data = pd.read_csv(pd.StringIO(edited_data))
        save_data(file_path, data)
        st.success('Data saved successfully!')
    except Exception as e:
        st.error(f'An error occurred:\n{e}')

# Display the DataFrame
st.subheader('Current Data')
st.write(data)
