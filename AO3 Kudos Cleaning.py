# importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Import the scraped data
top_100_kudos = pd.read_csv("ao3_by_kudos_pg1_to_5.csv") 

# Investigating the data
# print(top_100_kudos.head())
# print(top_100_kudos.columns)
# print(top_100_kudos.dtypes)

# Cleaning the data

# Specifying data types
top_100_kudos = top_100_kudos.astype({
    'work_id': 'string', 
    'user_id': 'string', 
    'title': 'string', 
    'username': 'string',
    'fandoms': 'string',
    'rating': 'string',
    'warnings': 'string',
    'slash_categories': 'string',
    'freeforms': 'string',
    'status': 'string', 
    'date_updated': 'string', 
    'relationships': 'string',
    'characters': 'string',
    'summary': 'string', 
    'language': 'string', 
    'chapters': 'string'})

# The ratings column should be categorical based on the increasing restrictions of the ratings
# print(top_100_kudos.rating.unique())
top_100_kudos['rating'] = pd.Categorical(top_100_kudos['rating'], ordered=True, categories=['General Audiences', 'Teen And Up Audiences', 'Mature', 'Explicit', 'Not Rated']) 

# Some of our columns are a currently a list, recognized as a string. 
# We need to clean this up so that we can use aggregate functions on the data.
top_100_kudos['fandoms'] = top_100_kudos.fandoms.apply(eval)
top_100_kudos['freeforms'] = top_100_kudos.freeforms.apply(eval)
top_100_kudos['warnings'] = top_100_kudos.warnings.apply(eval)
top_100_kudos['slash_categories'] = top_100_kudos.slash_categories.apply(eval)
top_100_kudos['relationships'] = top_100_kudos.relationships.apply(eval)
top_100_kudos['characters'] = top_100_kudos.characters.apply(eval)

# The following shows that our lists are in fact now lists.
for i, l in enumerate(top_100_kudos['freeforms']):
    print("list",i,"is",type(l))

