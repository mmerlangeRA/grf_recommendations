
from lightfm import LightFM
from lightfm.data import Dataset
import multiprocessing
import pickle
import pandas as pd

smartlink_prefix = 'https://grf.argoflow.io/fh4018-pdf.sl?sl='
number_of_recommendations = 5

def get_article_detail_dictionary():
    path = 'article_ref.pkl'
    try:
        result_dict = pickle.load(path)
    except:
        result_dict = None
    
    if result_dict is None:
        print("building article_detail_dictionary")
        df_details = pd.read_csv('article_details.csv',on_bad_lines="warn")
        columns_to_drop=["magazine_code","magazine_issue_code","theme_name","theme_name_2"]
        df_details.drop(columns_to_drop,axis=1,inplace=True)
        df_details.drop_duplicates()

        df_fat_data = pd.read_csv('https://nemato-data.fr/public/output.csv',on_bad_lines="warn")
        columns_to_drop=["visitor","view_seconds","rating","smartlink_name"]
        df_fat_data.drop(columns_to_drop,axis=1,inplace=True)
        df_fat_data.drop_duplicates()

        merged_df = pd.merge(df_details, df_fat_data, left_on='asset_name', right_on='article_name')

        # Create the dictionary
        result_dict = dict(zip(merged_df['asset_name'], zip(merged_df['asset_title'],merged_df['smartlink_id'], merged_df['page_x'])))
        pickle.dump(result_dict, open(path, 'wb'))
        print("built article_detail_dictionary")
    return result_dict

result_dict = get_article_detail_dictionary()


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

def load_data(url):
    print("load_data "+url)
    df = pd.read_csv(url,on_bad_lines="warn")
    columns_to_drop=["smartlink_name","article_name","rating"]
    df.drop(columns_to_drop,axis=1,inplace=True)
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
    df_grouped['rating']= df_grouped['view_seconds']/1800*5
    return df_grouped


def load_pd_data_article(url):
    print("load_pd_data_article "+url)
    df = pd.read_csv(url,on_bad_lines="warn")
    columns_to_drop=["smartlink_name","rating"]
    df.drop(columns_to_drop,axis=1,inplace=True)
    # manage duplicates
    duplicates = df.duplicated(keep=False)  # keep=False marks all duplicates as True
    num_duplicates = duplicates.sum()
    df_cleaned = df.drop_duplicates()

    #filter where<30s
    df_cleaned = df_cleaned[df_cleaned['view_seconds'] >= 30]
    #cap max duration
    df_cleaned['view_seconds'] = df_cleaned['view_seconds'].clip(upper=1800)

    #calculate rating
    df_grouped = df_cleaned.groupby(['article_name', 'visitor'])['view_seconds'].sum().reset_index()
    df_grouped['rating']= df_grouped['view_seconds']/1800*5
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

def build_recommender_article(df):
    print("build_recommender")
    num_threads = multiprocessing.cpu_count() -1
    print("num_threads=",num_threads)
    _dataset = Dataset()
    _dataset.fit((x for x in df['visitor']), (x for x in df['article_name']))

    # Building the interactions matrix
    (interactions, weights) = _dataset.build_interactions(((row['visitor'], row['article_name']) for index, row in df.iterrows()))

    _model = LightFM(loss='warp')
    _model.fit(interactions, epochs=30, num_threads=num_threads)

    return _model, _dataset

# Function to make recommendations for a selected visitor
def make_recommendations(_model, dataset, visitor):
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
    return recommendations

def make_recommendations_article(_model, dataset, visitor):
    visitor_index = dataset.mapping()[0][visitor]
    n_users, n_items = dataset.interactions_shape()

    # Predict scores for all items
    scores = _model.predict(visitor_index, list(range(n_items)))
    # Get top item indices
    top_items_indices = scores.argsort()[-number_of_recommendations:][::-1]
    
    # Map back to item ids and include scores
    article_ids = list(dataset.mapping()[2].keys())
    recommendations = [article_ids[x] for x in top_items_indices]
    return recommendations


def get_article_details(article_id):
    return result_dict[article_id]