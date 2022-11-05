# importing necessary libraries
import pandas as pd
import numpy as np
import os

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
# for i, l in enumerate(top_100_kudos['characters']):
#     print("list",i,"is",type(l))

#Create a list of unique items for every column
#Fandoms
unique_fandoms = []
for row in top_100_kudos['fandoms']:
    for item in row:
        if item in unique_fandoms:
            None
        else:
            unique_fandoms.append(item)

#Freeforms
unique_freeforms = []
for row in top_100_kudos['freeforms']:
    for item in row:
        if item in unique_freeforms:
            None
        else:
            unique_freeforms.append(item)

#Warnings
unique_warnings = []
for row in top_100_kudos['warnings']:
    for item in row:
        if item in unique_warnings:
            None
        else:
            unique_warnings.append(item)

#Slash Categories
unique_slash_categories = []
for row in top_100_kudos['slash_categories']:
    for item in row:
        if item in unique_slash_categories:
            None
        else:
            unique_slash_categories.append(item)

#Relationships
unique_relationships = []
for row in top_100_kudos['relationships']:
    for item in row:
        if item in unique_relationships:
            None
        else:
            unique_relationships.append(item)

#Characters
unique_characters = []
for row in top_100_kudos['characters']:
    for item in row:
        if item in unique_characters:
            None
        else:
            unique_characters.append(item)


# Function to create a boolean dataframe for each listed column
def boolean_df(col_name, unique_items):
# Create empty dict to hold all the data
    bool_dict = {} 
    for item in unique_items:
        # Create an empty dict to hold the data unique to that item
        item_dict = {}
        #Iterating through 100 rows of data
        for i in range(0,100):
            work_id = top_100_kudos['work_id'].iloc[i]
            if item in top_100_kudos[col_name].iloc[i]:
                # True if that item is in the list for that work
                item_dict[work_id] = True
            else:
                item_dict[work_id] = False
        # Add boolean dictionary for specific item to larger dict
        bool_dict[item] = item_dict
    return pd.DataFrame(bool_dict)

# Create a separate dataframe for each listed column
fandoms_bool = boolean_df('fandoms', unique_fandoms)
freeforms_bool = boolean_df('freeforms', unique_freeforms)
warnings_bool = boolean_df('warnings', unique_warnings)
slash_categories_bool = boolean_df('slash_categories', unique_slash_categories)
relationships_bool = boolean_df('relationships', unique_relationships)
characters_bool = boolean_df('characters', unique_characters)

# Creating a boolean column based on status
status_map = {'Complete Work': True, 'Work in Progress': False}
top_100_kudos['completed'] = top_100_kudos['status'].map(status_map)


# Separating out the chapters column into two new columns
top_100_kudos['chapters_written'] = top_100_kudos['chapters'].apply(lambda x: x.split('/')[0])
top_100_kudos['chapters_total'] = top_100_kudos['chapters'].apply(lambda x: x.split('/')[1])
# 
top_100_kudos['chapters_total'] = top_100_kudos.chapters_total.replace('?', np.NaN)

# Changing the datatype of the chapters columns so aggregate functions can be used. (Cannot use int64 due to NaN)
top_100_kudos = top_100_kudos.astype({
    'chapters_written': 'int64', 
    'chapters_total': 'float64'})

# Saving clean versions of the data
top_100_kudos.to_csv('top_100_kudos_clean.csv')
fandoms_bool.to_csv('top_100_kudos_fandoms_bool.csv')
freeforms_bool.to_csv('top_100_kudos_freeforms_bool.csv')
warnings_bool.to_csv('top_100_kudos_warnings_bool.csv')
slash_categories_bool.to_csv('top_100_kudos_slash_categories_bool.csv')
relationships_bool.to_csv('top_100_kudos_relationships_bool.csv')
characters_bool.to_csv('top_100_kudos_characters_bool.csv')