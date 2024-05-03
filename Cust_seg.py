import streamlit as st
import pandas as pd
import feat_eng
import pickle
import sklearn
import os
import streamlit as st
from PIL import Image
from feat_eng import feature_eng
import time
def list_images(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            images.append(os.path.join(folder_path, filename))
    return images

def main():
    st.title("Welcome to our Customer Segmentation App")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        customer_data = feat_eng.feature_eng(df)
        customer_data.drop('InvoiceDate', axis=1, inplace=True)
        st.write("### Uploaded CSV file is as follows:")
        st.write(df)
        # Display the uploaded file
        st.write("### The Recency, Frequency and Monetary Parameters for this customer are : ")
        st.write(customer_data)
        customer_data.drop('CustomerID', axis=1, inplace=True)
        pickle_in= open(r'random_forest_model.pkl', 'rb')
        button_clicked = st.button("Recommend Items")
        

        if button_clicked:
            model = pickle.load(pickle_in)
            pickle_top= open(r'top_5_items.pkl', 'rb')
            dict_1 = pickle.load(pickle_top)
            with st.spinner('### Loading Recommended Products for the customer...'):
    # Simulate some time-consuming operation
                time.sleep(3)
            

    # Use the model for making predictions
            prediction = model.predict(customer_data)
            prediction = int(prediction)
            st.write("### Recommended Products are-")
            images = list_images(f"images/Class_{prediction}")
            col1, col2,col3 = st.columns(3)
            with col1:
                    for img_path in images[:2]:
                        img_name = os.path.basename(img_path)
                        st.image(img_path, caption=f"{os.path.splitext(img_name)[0]}", use_column_width=True,output_format="HTML")
            with col2:
                    for img_path in images[2:4]:
                        img_name = os.path.basename(img_path)
                        st.image(img_path, caption=f"{os.path.splitext(img_name)[0]}", use_column_width=True,output_format="HTML")
            with col3:
                    for img_path in images[4:6]:
                        img_name = os.path.basename(img_path)
                        st.image(img_path, caption=f"{os.path.splitext(img_name)[0]}", use_column_width=True,output_format="HTML")
if __name__ == "__main__":
    main()