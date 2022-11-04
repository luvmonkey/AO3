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
    'rating': 'string',
    'freeforms': 'string',
    'status': 'string', 
    'date_updated': 'string', 
    'summary': 'string', 
    'language': 'string', 
    'chapters': 'string'})

# The ratings column should be categorical based on the increasing restrictions of the ratings
# print(top_100_kudos.rating.unique())
top_100_kudos['rating'] = pd.Categorical(top_100_kudos['rating'], ordered=True, categories=['General Audiences', 'Teen And Up Audiences', 'Mature', 'Explicit', 'Not Rated']) 


# The freeform tags are a currently a list, recognized as a string. 
# We need to clean this up so that we can use aggregate functions on the data.
top_100_kudos['freeforms'] = top_100_kudos.freeforms.apply(eval)

# The following shows that our lists are in fact now lists.
for i, l in enumerate(top_100_kudos['freeforms']):
    print("list",i,"is",type(l))

