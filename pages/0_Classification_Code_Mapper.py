import streamlit as st
import pandas as pd

@st.cache
def load_data():
    # Dummy data loading function
    data = pd.DataFrame({
        'UniFormatCode': ['A1010', 'A1020', 'A1030'],
        'Description': ['Foundation', 'Structural Frame', 'Exterior Walls']
    })
    return data

data = load_data()

# Display a static table
st.write("UniFormat Codes and Descriptions")
st.dataframe(data)

# Placeholder for displaying related MasterFormat codes
related_codes_placeholder = st.empty()

# Display buttons for each UniFormat code
for index, row in data.iterrows():
    if st.button(f"Select {row['UniFormatCode']}", key=row['UniFormatCode']):
        # This is where you'd fetch and display the related MasterFormat codes
        # Here we're just displaying a placeholder message
        related_codes_placeholder.write(f"Related MasterFormat Codes for {row['UniFormatCode']} would be displayed here.")
