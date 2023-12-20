import streamlit as st
import pandas as pd
from lightfm import LightFM
from lightfm.data import Dataset
import multiprocessing

# Function to load data from URL
@st.cache_data
def load_data(url):
    print("load_data "+url)
    df = pd.read_csv(url,on_bad_lines="warn")
    columns_to_drop=["smartlink_name","article_name","rating"]
    df.drop(columns_to_drop,axis=1,inplace=True)
    print(df.shape)
    # manage duplicates
    duplicates = df.duplicated(keep=False)  # keep=False marks all duplicates as True
    num_duplicates = duplicates.sum()
    print(f"Number of duplicate rows: {num_duplicates}")
    df_cleaned = df.drop_duplicates()

    #filter where<30s
    df_cleaned = df_cleaned[df_cleaned['view_seconds'] >= 30]
    #cap max duration
    df_cleaned['view_seconds'] = df_cleaned['view_seconds'].clip(upper=1800)

    #calculate rating
    df_grouped = df_cleaned.groupby(['smartlink_id', 'visitor'])['view_seconds'].sum().reset_index()
    #csv = df_grouped.to_csv("small2.csv",index=False)
    df_grouped['rating']= df_grouped['view_seconds']/1800*5
    csv = df_grouped.to_csv("small2.csv",index=False)
    return df_grouped

# Function to build the recommendation system
@st.cache_resource
def build_recommender(df):
    print("build_recommender")
    num_threads = multiprocessing.cpu_count() -1
    print("num_threads=",num_threads)
    dataset = Dataset()
    dataset.fit((x for x in df['visitor']), (x for x in df['smartlink_id']))

    # Building the interactions matrix
    (interactions, weights) = dataset.build_interactions(((row['visitor'], row['smartlink_id']) for index, row in df.iterrows()))

    model = LightFM(loss='warp')
    model.fit(interactions, epochs=30, num_threads=num_threads)

    return model, dataset

# Function to make recommendations for a selected visitor

def make_recommendations(_model, dataset, visitor):
    print("make_recommendations")
    visitor_index = dataset.mapping()[0][visitor]
    n_users, n_items = dataset.interactions_shape()

    # Predict scores for all items
    scores = _model.predict(visitor_index, list(range(n_items)))
    # Get top item indices
    top_items_indices = scores.argsort()[-5:][::-1]

    # Map back to item ids and include scores
    item_ids = list(dataset.mapping()[2].keys())
    recommendations = [(item_ids[x], scores[x]) for x in top_items_indices]
    print("make_recommendations done")
    return recommendations

# Streamlit app
def main():
    st.title("Smartlink Recommendation System")

    # User inputs the URL
    url = st.text_input("Enter the URL of the dataset")

    if url:
        df = load_data(url)
        st.write("Data Loaded Successfully!")
        # Build the recommender system
        model, dataset = build_recommender(df)
        st.write("Recommender System Built Successfully!")

        # Select a visitor
        visitor = st.selectbox("Select a Visitor", df['visitor'].unique())

        if visitor:
            # Get recommendations
            recommendations = make_recommendations(model, dataset, visitor)

            # Display recommendations
            st.write("Recommendations for Visitor:", visitor)
            st.write(recommendations)

if __name__ == "__main__":
    main()
