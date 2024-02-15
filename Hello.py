import streamlit as st

# Define the main app function
def main():
    """BIM QTO Tools Landing Page"""
    
    # App title and description
    st.title('Welcome to BIM QTO Tools')
    st.markdown('''
        BIM QTO Tools is a suite of utilities designed to assist professionals in the Building Information Modeling (BIM) 
        and Quantity Take-Off (QTO) processes. This platform offers tools like Code Mapper and other resources to streamline 
        your workflow and enhance productivity.
        
        **Features include:**
        
        - **Code Mapper**: Easily map UniFormat codes to MasterFormat codes.
        - **QTO Calculator**: Quickly calculate quantities based on BIM models.
        - **... and more!**

        Get started by selecting a tool from the left sidebar.
    ''')

    # Sidebar navigation
    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Select a page:', ['Home', 'Code Mapper', 'QTO Calculator', 'About'])

    # Page routing
    if page == 'Home':
        st.sidebar.write('You are on the Home page.')
        # Further home page content goes here
    elif page == 'Code Mapper':
        st.sidebar.write('Navigate to the Code Mapper tool.')
        # Code to display the Code Mapper tool goes here
    elif page == 'QTO Calculator':
        st.sidebar.write('Navigate to the QTO Calculator tool.')
        # Code to display the QTO Calculator goes here
    elif page == 'About':
        st.sidebar.write('Learn more about BIM QTO Tools.')
        # Code to display information about the app goes here

if __name__ == "__main__":
    main()
