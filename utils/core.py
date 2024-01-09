
from lightfm import LightFM
from lightfm.data import Dataset
import multiprocessing
import pickle
import pandas as pd

smartlink_prefix = 'https://grf.argoflow.io/fh4018-pdf.sl?sl='
'''
In this example, we will focus on the smartlink to recommend. Top 5
'''

number_of_recommendations = 5


def save_model_and_dataset(_df,_model,_dataset,_name):
    with open(_name+'.pkl', 'wb') as f:
        pickle.dump((_df,_model,_dataset), f)


def load_model_and_dataset(_name):
    try:
        with open(_name+'.pkl', 'rb') as f:
            (_df,_model,_dataset) = pickle.load(f)
        return (_df,_model,_dataset)
    except:
        return (None,None,None)

def load_pd_data(url):
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
    #csv = df_grouped.to_csv("small2.csv",index=False)
    return df_grouped

def build_recommender(df):
    print("build_recommender")
    num_threads = multiprocessing.cpu_count() -1
    print("num_threads=",num_threads)
    _dataset = Dataset()
    _dataset.fit((x for x in df['visitor']), (x for x in df['smartlink_id']))

    # Building the interactions matrix
    (interactions, weights) = _dataset.build_interactions(((row['visitor'], row['smartlink_id']) for index, row in df.iterrows()))

    _model = LightFM(loss='warp')
    _model.fit(interactions, epochs=30, num_threads=num_threads)

    return _model, _dataset

# Function to make recommendations for a selected visitor
def make_recommendations(_model, dataset, visitor):
    print("make_recommendations")
    visitor_index = dataset.mapping()[0][visitor]
    n_users, n_items = dataset.interactions_shape()

    # Predict scores for all items
    scores = _model.predict(visitor_index, list(range(n_items)))
    # Get top item indices
    top_items_indices = scores.argsort()[-number_of_recommendations:][::-1]

    # Map back to item ids and include scores
    item_ids = list(dataset.mapping()[2].keys())
    #return links liks https://grf.argoflow.io/fh4018-pdf.sl?sl=64a3e7738309e30012afd726
    recommendations = [(smartlink_prefix + item_ids[x], scores[x]) for x in top_items_indices]
    print("make_recommendations done")
    return recommendations
