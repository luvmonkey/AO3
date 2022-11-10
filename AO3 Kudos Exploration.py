#Import Libraries
import pandas as pd
import matplotlib.pyplot as plt

# Import Data
top_100_kudos = pd.read_csv('top_100_kudos_clean.csv')
fandoms_bool = pd.read_csv('top_100_kudos_fandoms_bool.csv')
freeforms_bool = pd.read_csv('top_100_kudos_freeforms_bool.csv')
warnings_bool = pd.read_csv('top_100_kudos_warnings_bool.csv')
slash_categories_bool = pd.read_csv('top_100_kudos_slash_categories_bool.csv')
relationships_bool = pd.read_csv('top_100_kudos_relationships_bool.csv')
characters_bool = pd.read_csv('top_100_kudos_characters_bool.csv')

# Initial exploration
slash_categories_bool = slash_categories_bool.set_index('Unnamed: 0')
print(slash_categories_bool.columns)

print(slash_categories_bool.head())

# for col in slash_categories_bool.columns:
#     print(col, ' ', slash_categories_bool[col].sum)