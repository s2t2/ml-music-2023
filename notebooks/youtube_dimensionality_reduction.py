# -*- coding: utf-8 -*-
"""ML Music - YouTube - Dimensionality Reduction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t1E6ELeept8EswpP3elJ5bNbDqwA3QyM

## Setup

### Google Drive
"""

from google.colab import drive

drive.mount('/content/drive')

import os

# you might need to update the path below, or create a shortcut to the path below
DATASET_PATH = '/content/drive/MyDrive/Research/DS Research Shared 2023/data/ml_music_2023'

print(DATASET_PATH)
assert os.path.isdir(DATASET_PATH)

"""## Load Youtube Audio Features"""

from pandas import read_csv

csv_filepath = os.path.join(DATASET_PATH, "30s_features_mfcc_2.csv")

mfcc_df = read_csv(csv_filepath)
mfcc_df.drop(columns="Unnamed: 0", inplace=True)
mfcc_df.head()

import plotly.express as px

px.scatter(mfcc_df, x="mfcc_1_mean", y="mfcc_2_mean", color="channel_name")

from pandas import read_csv

csv_filepath = os.path.join(DATASET_PATH, "30s_features_mfcc_3.csv")

mfcc_df = read_csv(csv_filepath)
mfcc_df.drop(columns="Unnamed: 0", inplace=True)
mfcc_df.head()

import plotly.express as px

fig = px.scatter(mfcc_df, x="mfcc_1_mean", y="mfcc_2_mean", color="channel_name")
fig.show()


fig = px.scatter(mfcc_df, x="mfcc_1_mean", y="mfcc_3_mean", color="channel_name")
fig.show()


fig = px.scatter(mfcc_df, x="mfcc_2_mean", y="mfcc_3_mean", color="channel_name")
fig.show()

from pandas import read_csv

csv_filepath = os.path.join(DATASET_PATH, "30s_features_mfcc_20.csv")

mfcc_df = read_csv(csv_filepath)
mfcc_df.drop(columns="Unnamed: 0", inplace=True)
mfcc_df.head()

"""## Dimensionality Reduction

### PCA
"""

from sklearn.decomposition import PCA

"""### TSNE"""

from sklearn.manifold import TSNE

"""### UMAP"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install umap-learn[plot]

from umap import UMAP

def umapper(df_onehot=df_onehot, n_components=2):

    reducer = UMAP(n_components=n_components, random_state=99)
    embedding = reducer.fit_transform(df_onehot)

    embed_df = DataFrame(embedding, columns=component_names(n_components))
    #embed_df.index = df_onehot.index
    embed_df["tag"] = df_onehot.index
    #embed_df.head()
    csv_filepath = os.path.join(DATA_DIRPATH, f"profile_tags_{TOP_TAGS_LIMIT}_umap_{n_components}.csv")
    embed_df.to_csv(csv_filepath)

    #
    # PLOTTING
    #

    chart_df = embed_df.copy()
    chart_df["tag"] = df_onehot.index
    chart_df = chart_df.merge(tags_df, left_on="tag", right_on="tag")

    title = f"UMAP Dimension Reduction of Top {TOP_TAGS_LIMIT} Tags in User Profiles"
    if n_components == 1:
        chart_df["color"] = chart_df["component_a"]
        
        fig = px.scatter(chart_df, title=title, text="tag", size="user_count",
            x="component_a",            
            labels={"component_a":""},
            #color="color", color_continuous_scale=px.colors.colorbrewer.RdBu
        )
    elif n_components == 2:
        chart_df["color"] = chart_df["component_a"] * chart_df["component_b"]
        if TOP_TAGS_LIMIT == 25:
            chart_df["color"] = chart_df["component_a"] #* chart_df["component_b"] * chart_df["component_c"]

        fig = px.scatter(chart_df, title=title, text="tag", size="user_count",
            x="component_a", y="component_b",        
            labels={"component_a":"", "component_b":""},
            color="color", color_continuous_scale=px.colors.colorbrewer.RdBu
        )
    elif n_components == 3:
        chart_df["color"] = chart_df["component_a"] * chart_df["component_b"] * chart_df["component_c"]
        scale = px.colors.colorbrewer.RdBu_r
        if TOP_TAGS_LIMIT == 25:
            chart_df["color"] = chart_df["component_a"] * chart_df["component_b"] # * chart_df["component_c"]
            scale = px.colors.colorbrewer.RdBu

        # https://plotly.com/python-api-reference/generated/plotly.express.scatter_3d.html
        fig = px.scatter_3d(chart_df, title=title, text="tag", #size="user_count",
            x="component_a", y="component_b", z="component_c", 
            labels={"component_a":"", "component_b":"", "component_c":""},
            color="color", color_continuous_scale=scale
        )
    
    fig.show()
    image_filepath = os.path.join(FIGURES_DIRPATH, f"profile_tags_{TOP_TAGS_LIMIT}_umap_{n_components}.png")
    fig.write_image(image_filepath)
    if n_components in [2,3]:
        html_filepath = os.path.join(FIGURES_DIRPATH, f"profile_tags_{TOP_TAGS_LIMIT}_umap_{n_components}.html")
        fig.write_html(html_filepath)

"""## Clustering"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install hdbscan

from hdbscan import HDBSCAN