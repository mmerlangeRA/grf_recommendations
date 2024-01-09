import streamlit as st
import pandas as pd
from utils.core import get_article_details, load_model_and_dataset, save_model_and_dataset, build_recommender_article, make_recommendations_article,load_pd_data_article

smartlink_prefix = 'https://grf.argoflow.io/fh4018-pdf.sl?sl='

# Function to load data from URL
@st.cache_data
def load_data(url):
    return load_pd_data_article(url)


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
            model, dataset = build_recommender_article(df)
            save_model_and_dataset(df, model,dataset,_name=name)
            st.write("Recommender System Built Successfully!")

        # Select a visitor
        visitor = st.selectbox("Select a Visitor", df['visitor'].unique())

        if visitor:
            # Get recommendations
            recommended_article_ids = make_recommendations_article(model, dataset, visitor)
            recommendations= [get_article_details(article_id) for article_id in recommended_article_ids]
            # Display recommendations
            st.write("Top recommendations for Visitor:", visitor)
            for title, smartlink_id, page in recommendations:
                link = smartlink_prefix + smartlink_id+"#page="+str(page)
                st.markdown(f"[{title}]({link})", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
