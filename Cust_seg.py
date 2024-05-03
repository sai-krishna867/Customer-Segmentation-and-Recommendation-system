import streamlit as st
import pandas as pd
import feat_eng
import pickle
import sklearn
from feat_eng import feature_eng
def main():
    st.title("Customer Segmentation")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        customer_data = feat_eng.feature_eng(df)
        customer_data.drop('InvoiceDate', axis=1, inplace=True)
        
        # Display the uploaded file
        st.write(sklearn.__version__)

        st.write(customer_data)
        customer_data.drop('CustomerID', axis=1, inplace=True)
        st.write("### Uploaded CSV file:")
        
        st.write(df)
      
        pickle_in= open(r'random_forest_model.pkl', 'rb')
    
        model = pickle.load(pickle_in)
        pickle_top= open(r'top_5_items.pkl', 'rb')
        dict_1 = pickle.load(pickle_top)
        

# Use the model for making predictions
        prediction = model.predict(customer_data)
        prediction = int(prediction)
        st.write((prediction))
        st.write((dict_1[prediction]))

    st.write("""
    ## Welcome to our Customer Segmentation App
    Here, you can explore different customer segments based on various features.
    by
    """)

    # Add your Streamlit widgets and code for customer segmentation here

if __name__ == "__main__":
    main()
