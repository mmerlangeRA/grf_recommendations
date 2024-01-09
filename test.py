from lightfm import LightFM
from lightfm.evaluation import precision_at_k, recall_at_k, auc_score
import pandas as pd
from utils.core import load_model_and_dataset, save_model_and_dataset, build_recommender, make_recommendations,load_pd_data_article
import numpy as np
from lightfm.data import Dataset
from lightfm.cross_validation import random_train_test_split
import multiprocessing
import pickle

data_url = "https://nemato-data.fr/public/output.csv"

#tags
df_details = pd.read_csv('article_details.csv',on_bad_lines="warn")
columns_to_drop=["magazine_code","magazine_issue_code","page"]
df_details.drop(columns_to_drop,axis=1,inplace=True)

unique_tags = df_details['theme_name'].unique()

print(unique_tags)

df_details = df_details.groupby('asset_name').agg({
    'asset_title': 'first',  # Same as above
    'theme_name': ', '.join  # Join the 'theme_name' values
}).reset_index() 

item_to_tags = df_details.groupby('asset_name')['theme_name'].apply(list).to_dict()

article_features = {item: ','.join(tags) for item, tags in item_to_tags.items()}
print(article_features)


df = load_pd_data_article(data_url)
num_threads = multiprocessing.cpu_count() -1
print("num_threads=",num_threads)
dataset = Dataset()
print(df.columns)
visitor_ids = (x for x in df['visitor'])
article_ids =  (x for x in df['article_name'])

dataset.fit(visitor_ids,article_ids,item_features=unique_tags)

item_features = dataset.build_item_features(
    (x, article_features[x]) for x in article_ids)

# Building the interactions matrix
(interactions, weights) = dataset.build_interactions(((row['visitor'], row['article_name']) for index, row in df.iterrows()))

# Split the data into training and testing sets
# Test set will be 20% of the interactions
train_data, test_data = random_train_test_split(interactions, test_percentage=0.2)

# model fiiting
model = LightFM(loss='warp')
model.fit(train_data, epochs=30, num_threads=num_threads,item_features=item_features)


# Evaluate the trained model
"""  no item_features
test_precision = precision_at_k(model, test_data, k=5).mean()
test_recall = recall_at_k(model, test_data, k=5).mean()
test_auc = auc_score(model, test_data).mean() 
"""

test_precision = precision_at_k(model, test_interactions=test_data, item_features=item_features, k=5).mean()
test_recall = recall_at_k(model, test_interactions=test_data, item_features=item_features, k=5).mean()
test_auc = auc_score(model, test_interactions=test_data, item_features=item_features).mean()

print(f'Precision@5: {test_precision}')
print(f'Recall@5: {test_recall}')
print(f'AUC: {test_auc}')

''' default, item_features, on smartlink id 
Precision@5: 0.038979191333055496
Recall@5: 0.11866372869430221
AUC: 0.7090743780136108
'''

'''article name
Precision@5: 0.08251718431711197
Recall@5: 0.15909435393500326
AUC: 0.9121911525726318
'''

''' article name with item_features
Precision@5: 0.0786394253373146
Recall@5: 0.1518669951924829
AUC: 0.9087110757827759
'''