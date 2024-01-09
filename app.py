import streamlit as st
import pandas as pd
from utils.core import load_model_and_dataset, save_model_and_dataset, build_recommender, make_recommendations,load_pd_data




# Function to load data from URL
@st.cache_data
def load_data(url):
    return load_pd_data(url)


# Streamlit app
def main():

    print("main loaded")
    
    st.title("GRF Smartlink Recommendation System")

    # User inputs the URL
    url = st.text_input("Enter the URL of the dataset")

    if url:
        name_csv = url.split('/')[-1]
        name = name_csv.split('.')[0]
        #try to load corresponding model and dataset
        df,model,dataset = load_model_and_dataset(name)
        if model is None:
            df = load_data(url)
        st.write("Data Loaded Successfully!")
        # Build the recommender system
        if model is None:
            st.write("Building Recommender System...")
            model, dataset = build_recommender(df)
            save_model_and_dataset(df, model,dataset,_name=name)
            st.write("Recommender System Built Successfully!")

        # Select a visitor
        visitor = st.selectbox("Select a Visitor", df['visitor'].unique())

        if visitor:
            # Get recommendations
            recommendations = make_recommendations(model, dataset, visitor)

            # Display recommendations
            st.write("Top recommendations for Visitor:", visitor)
            for link, score in recommendations:
                st.markdown(f"[{link}]({link})", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
