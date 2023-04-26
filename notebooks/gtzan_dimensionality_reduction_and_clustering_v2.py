# -*- coding: utf-8 -*-
"""ML Music - GTZAN - Dimensionality Reduction and Clustering v2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kJqWRHlpiaWeZ_SRnfl_Bw6rgEM6tyWA

## Data Prep

### Import Data
"""

from pandas import read_csv

TRACK_LENGTH = 3 #30 
N_MFCC = 13

# upload the file into colab
#csv_filepath = f"features_{TRACK_LENGTH}s_mfcc_{N_MFCC}_features.csv"
csv_filepath = f"mfcc_{N_MFCC}_features.csv"

df = read_csv(csv_filepath)
df.index = df["audio_filename"]
df

"""### Scale Data"""

labels = df[["genre", "audio_filename"]]
y = df["genre"]

x = df.drop(columns=["genre", "audio_filename", "track_length"])

feature_names = x.columns.tolist()
#print(features)

#print(x.iloc[0])
#x.head()

from sklearn.preprocessing import scale
from pandas import DataFrame

x_scaled = scale(x)
x_scaled = DataFrame(x_scaled, columns=feature_names)
x_scaled.index = x.index
x_scaled

x_scaled.describe()

"""### Feature Correlation"""

import matplotlib.pyplot as plt
import seaborn as sns

mat = x_scaled.corr(method="spearman")

sns.set(rc = {'figure.figsize':(17,17)})
sns.heatmap(mat, 
            square=True, annot=True, fmt=".2f",
            cbar=True, cmap="Blues"
        )

plt.xlabel("Feature Name")
plt.ylabel("Feature Name")
plt.title("Spearman Correlation between Features")

plt.show()

"""## Dimensionality Reduction"""

def plot_embeddings(x_scaled, embeddings, track_length, n_mfcc, n_components, model_type, chart=True):

    component_names = [f"component_{i}" for i in range(1, n_components+1)]
    embeddings_df = DataFrame(embeddings, columns=component_names)
    embeddings_df.index = x_scaled.index
    embeddings_df["audio_filename"] = x_scaled.index
    embeddings_df["genre"] = embeddings_df["audio_filename"].apply(lambda audio_filename: audio_filename.split(".")[0])
    #print(embeddings_df.head())
    #csv_filepath = os.path.join(DATA_DIRPATH, f"gtzan_songs_{TRACK_LENGTH}s_mfcc{N_MFCC}_pca_{n_components}.csv")
    #embeddings_df.to_csv(csv_filepath)
 
    if chart:
        title = f"""GTZAN Genre Classifier - Dimensionality Reduction ({model_type} n_components={n_components})
            <br><sup>Data: {track_length}s tracks, {n_mfcc} MFCCs</sup>
        """
        chart_params = dict(x="component_1", y="component_2", 
                    color="genre", #, hover_data="audio_filename"
                    title=title, height=500,
        )
        if n_components == 2:
            fig = px.scatter(embeddings_df, **chart_params)
            fig.show()

        elif n_components ==3:
            chart_params["z"] = "component_3"
            fig = px.scatter_3d(embeddings_df, **chart_params)
            fig.show()
    
    return embeddings_df

"""### PCA"""

#n_components=2
#
#pca = PCA(n_components=n_components, random_state=99)
#
#embeddings = pca.fit_transform(x_scaled)
#print("EMBEDDINGS:", type(embeddings), embeddings.shape)
#print("EXPLAINED VARIANCE RATIO:", pca.explained_variance_ratio_)
#print("SINGULAR VALS:", pca.singular_values_)

#component_names = [f"component_{i}" for i in range(1, n_components+1)]
#embeddings_df = DataFrame(embeddings, columns=component_names)
#embeddings_df.index = x_scaled.index
#embeddings_df["audio_filename"] = x_scaled.index
#embeddings_df["genre"] = embeddings_df["audio_filename"].apply(lambda audio_filename: audio_filename.split(".")[0])
#
#print(len(embeddings_df))
#print(embeddings_df.head())
##csv_filepath = os.path.join(DATA_DIRPATH, f"profile_tags_{TOP_TAGS_LIMIT}_pca_{n_components}.csv")
##embeddings_df.to_csv(csv_filepath)

#import plotly.express as px
#
#title = "GTZAN Dataset - Song Similarity"
#px.scatter(embeddings_df, x="component_1", y="component_2", title=title,
#           color="genre" #, hover_data="audio_filename"
#)

import os
from pandas import DataFrame
from sklearn.decomposition import PCA
import plotly.express as px


def pca_pipeline(x_scaled=x_scaled, n_components=2, track_length=TRACK_LENGTH, n_mfcc=N_MFCC):

    pca = PCA(n_components=n_components, random_state=99)

    embeddings = pca.fit_transform(x_scaled)
    print("EMBEDDINGS:", type(embeddings), embeddings.shape)
    print("EXPLAINED VARIANCE RATIO:", pca.explained_variance_ratio_)
    print("SINGULAR VALS:", pca.singular_values_)

    embeds_df = plot_embeddings(x_scaled, embeddings, track_length, n_mfcc, n_components, "PCA")
    return pca, embeds_df 


pca_pipeline(n_components=2)

pca_pipeline(n_components=3)

"""#### PCA Tuning"""

import numpy as np

pca_results = []
for n_components in range(1, len(x_scaled.columns)+1):

    pca = PCA(n_components=n_components, random_state=99)

    embeddings = pca.fit_transform(x_scaled)
    #print("COMPONENTS:", pca.components_.shape) # EIGEN VECTORS #> (2, 10)
    #print("FEATURE NAMES:", pca.feature_names_in_)
    #print("EMBEDDINGS:", embeddings.shape) #> (28, 2)
    #print("EXPLAINED VARIANCE:", pca.explained_variance_.shape) #> (2,)
    #print("EXPLAINED VARIANCE RATIO:", pca.explained_variance_ratio_.shape) #> (2,)
    #print("SINGULAR VALS:", pca.singular_values_.shape) #> (2,)

    # https://stackoverflow.com/a/44728692/670433
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    # print("LOADINGS:", loadings.shape) #> (10, 2)

    #print("EIGENVAL:")
    pca_results.append({
        "n_components": n_components,
        "explained_variance": pca.explained_variance_ratio_.sum(),
        "eigenvals": pca.explained_variance_, # number of vals depend on n components
        "loadings": loadings,
        "embeddings": embeddings
    })


pca_results_df = DataFrame(pca_results)
pca_results_df[["n_components", "explained_variance"]].head()

title = f"""Total Explained Variance by Number of Components (PCA)
<br><sup>Data: {TRACK_LENGTH}s tracks, {N_MFCC} MFCCs</sup>
"""
fig = px.line(pca_results_df, x="n_components", y="explained_variance", 
        title=title,
        markers="line+point", color_discrete_sequence=["steelblue"]
)
fig.show()

"""Looks like around 90% of the variance is explained with 9 features, 90% of the variance is explained with 12."""

eigenvals = pca_results_df.sort_values(by=["n_components"], ascending=False).iloc[0]["eigenvals"]
print("EIGENVALS:", eigenvals)

component_numbers = list(range(1, len(pca_results_df)+1))
print("COMPONENT NUMBERS:", component_numbers)

title=f"""Scree Plot of Eigenvalues by Component (PCA)
<br><sup>Data: {TRACK_LENGTH}s tracks, {N_MFCC} MFCCs</sup>
"""
fig = px.line(x=component_numbers, y=eigenvals, 
        title=title,
        labels={"x": "Component Number", "y": "Eigenvalue"},
        markers="line+point", color_discrete_sequence=["steelblue"]
)
fig.show()
# RETAIN ALL BEFORE THE ELBOW

"""For 30 second tracks and 13 MFCCs, looks like we could keep six to nine components.

### T-SNE

T-SNE is slow.
"""

import os
from pandas import DataFrame
from sklearn.manifold import TSNE
import plotly.express as px


def tsne_pipeline(x_scaled=x_scaled, n_components=2, track_length=TRACK_LENGTH, n_mfcc=N_MFCC):

    tsne = TSNE(n_components=n_components, random_state=99)

    embeddings = tsne.fit_transform(x_scaled)
    print("EMBEDDINGS:", type(embeddings), embeddings.shape)
    print("K-L DIVERGENCE:", tsne.kl_divergence_)

    plot_embeddings(x_scaled, embeddings, track_length, n_mfcc, n_components, "T-SNE")



tsne_pipeline(n_components=2)

#tsne_pipeline(n_components=3)

"""### UMAP"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install umap-learn[plot]

from umap import UMAP


def umapper(x_scaled=x_scaled, n_components=2, track_length=TRACK_LENGTH, n_mfcc=N_MFCC):

    reducer = UMAP(n_components=n_components, random_state=99)
    embeddings = reducer.fit_transform(x_scaled)

    embeds_df = plot_embeddings(x_scaled, embeddings, track_length, n_mfcc, n_components, "UMAP")

    return reducer, embeds_df


umapper(n_components=2)

umapper(n_components=3)

"""## Clustering

https://scikit-learn.org/stable/modules/clustering.html

Let's use a higher dimension dataset, like the original scaled data, or a reduced version with the optimal number of components we saw from the PCA tuning.
"""

N_COMPONENTS = 7

pca, embeds_df = pca_pipeline(n_components=N_COMPONENTS)
embeds_df.head()

#umap, embeds_df = umapper(n_components=N_COMPONENTS)
#embeds_df

from sklearn.model_selection import train_test_split

# use original data:
#x_cluster = x_scaled
#y_cluster = y

# use reduced data:
x_cluster = embeds_df.drop(columns=["genre", "audio_filename"])
y_cluster = embeds_df["genre"]

x_train, x_test, y_train, y_test = train_test_split(x_cluster, y_cluster, shuffle=True, random_state=99)
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

x_test.columns

"""### KMeans

https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans
"""

from sklearn.cluster import KMeans
import numpy as np

N_CLUSTERS = 10

kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=99, n_init="auto")
kmeans.fit(x_train)
cluster_labels = kmeans.labels_
cluster_centers = kmeans.cluster_centers_

y_pred = kmeans.predict(x_test)
print("TRUE:", y_test.values[0:10])
print("PRED:", y_pred[0:10])

#feature_names = kmeans.get_feature_names_out()
#feature_names

preds_df = DataFrame()
preds_df["audio_filename"] = y_test.index
preds_df["genre"] = y_test.values
preds_df["kmeans_cluster_id"] = ["cluster_" + str(cluster_id) for cluster_id in y_pred]
preds_df.head()

for genre in preds_df["genre"].unique().tolist():
    print("---------------")
    preds = preds_df[preds_df["genre"] == genre]
    print(f"GENRE {genre} .... ({len(preds)} members):")
    print(preds["kmeans_cluster_id"].value_counts())

for cluster_id in range(1, N_CLUSTERS+1):
    print("---------------")
    preds = preds_df[preds_df["kmeans_cluster_id"] == f"cluster_{cluster_id}"]
    print(f"CLUSTER ID {cluster_id} .... ({len(preds)} members):")
    print(preds["genre"].value_counts())

"""### Spectral Clustering

https://scikit-learn.org/stable/modules/generated/sklearn.cluster.SpectralClustering.html#sklearn.cluster.SpectralClustering
"""

from sklearn.cluster import SpectralClustering

N_CLUSTERS = 10

sc = SpectralClustering(n_clusters=N_CLUSTERS, assign_labels='discretize', random_state=0)
sc.fit(x_train)
#print(sc.labels_)
print(sc.n_features_in_)
print(sc.feature_names_in_)

#y_pred = sc.predict(x_test)
#print("TRUE:", y_test.values[0:10])
#print("PRED:", y_pred[0:10])

"""### DBSCAN

https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html#sklearn.cluster.DBSCAN
"""

from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=3, min_samples=2)
dbscan.fit(x_train)
cluster_labels = dbscan.labels_

#y_pred = dbscan.predict(x_test)
#print("TRUE:", y_test.values[0:10])
#print("PRED:", y_pred[0:10])

preds_df = DataFrame()
preds_df["audio_filename"] = y_train.index
preds_df["genre"] = y_train.values
preds_df["dbscan_cluster_id"] = cluster_labels # ["cluster_" + str(cluster_id) for cluster_id in cluster_labels]
preds_df.head()

#for genre in preds_df["genre"].unique().tolist():
#    print("---------------")
#    preds = preds_df[preds_df["genre"] == genre]
#    print(f"GENRE {genre} .... ({len(preds)} members):")
#    print(preds["dbscan_cluster_id"].value_counts())

for cluster_id in sorted(preds_df["dbscan_cluster_id"].unique()):
    print("---------------")
    preds = preds_df[preds_df["dbscan_cluster_id"] == cluster_id] # f"cluster_{cluster_id}"
    print(f"CLUSTER {cluster_id}...") # ({len(preds)} members):
    print(preds["genre"].value_counts())

"""### HDBSCAN"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install hdbscan

from hdbscan import HDBSCAN

hdbscan = HDBSCAN()
hdbscan.fit(x_train)
#print(hdbscan.labels_)

preds_df = DataFrame()
preds_df["audio_filename"] = y_train.index
preds_df["genre"] = y_train.values
preds_df["hdbscan_label"] = hdbscan.labels_
preds_df["hdbscan_probability"] = hdbscan.probabilities_
preds_df.sort_values(by=["hdbscan_label"], inplace=True)
preds_df.head()

preds_df["hdbscan_label"].unique()

preds_df[preds_df["hdbscan_label"] == -1].sort_values(by="hdbscan_probability", ascending=False)

preds_df[preds_df["hdbscan_label"] == 0].sort_values(by="hdbscan_probability", ascending=False)

preds_df[preds_df["hdbscan_label"] == 1].sort_values(by="hdbscan_probability", ascending=False)

preds_df[preds_df["hdbscan_label"] == 2].sort_values(by="hdbscan_probability", ascending=False)

preds_df[preds_df["hdbscan_label"] == 3].sort_values(by="hdbscan_probability", ascending=False)

"""#### HDBSCAN Eval"""

#def cluster_eval(X_df=df_onehot, embed_df=embed_df, metric="euclidean"): 
#    print("-------------")
#    print("METRIC:", metric)
#
#    hdbscan = HDBSCAN(metric=metric)
#
#    hdbscan.fit(embed_df)
#    #print(hdbscan.labels_[0:25])
#    #print(hdbscan.probabilities_[0:25])
#
#    # EXPORT RESULTS TO CSV...
#    labels_df = embed_df.copy()
#    labels_df["hdbscan_label"] = hdbscan.labels_
#    labels_df["hdbscan_probability"] = hdbscan.probabilities_
#    labels_df.sort_values(by=["hdbscan_label"], inplace=True)
#    #print(labels_df.head())
#    print(labels_df["hdbscan_label"].value_counts())
#    #csv_filepath = os.path.join(DATA_DIRPATH, f"tags_users_onehot_{CLUSTERING_TAGS_LIMIT}_umap_{CLUSTERING_N_COMPONENTS}_cluster_hdbscan_{metric}.csv")
#    #labels_df.to_csv(csv_filepath)
#
#    # EVALUATION
#
#    labels = hdbscan.labels_
#
#    sh_score = metrics.silhouette_score(X_df, labels, metric='euclidean')
#    #print("SH SCORE:", sh_score) #> 0.0567
#
#    ch_score = metrics.calinski_harabasz_score(X_df, labels)
#    #print("CH SCORE:", ch_score) #> 2.5839
#
#    db_score = metrics.davies_bouldin_score(X_df, labels)
#    #print("DB SCORE:", db_score) #> 3.5719
#
#    # REPORT ON THE SCORES:
#    return {
#        "metric": metric,
#        "sh_score": sh_score,
#        "ch_score": ch_score,
#        "db_score": db_score
#    }
#     
#
DISTINCT_METRICS = [
 'braycurtis',       #: hdbscan.dist_metrics.BrayCurtisDistance,
 'canberra'       , #  : hdbscan.dist_metrics.CanberraDistance,
 'chebyshev'      , #  : hdbscan.dist_metrics.ChebyshevDistance,
 'dice'           , #  : hdbscan.dist_metrics.DiceDistance,
 'euclidean'      , #  : hdbscan.dist_metrics.EuclideanDistance,
 'hamming'        , #  : hdbscan.dist_metrics.HammingDistance,
 'haversine'      , #  : hdbscan.dist_metrics.HaversineDistance,
 'jaccard'        , #  : hdbscan.dist_metrics.JaccardDistance,
 'kulsinski'      , #  : hdbscan.dist_metrics.KulsinskiDistance,
 'mahalanobis'    , #  : hdbscan.dist_metrics.MahalanobisDistance,
 'manhattan'      , #  : hdbscan.dist_metrics.ManhattanDistance,
 'matching'       , #  : hdbscan.dist_metrics.MatchingDistance,
 'minkowski'      , #  : hdbscan.dist_metrics.MinkowskiDistance,
 'pyfunc'         , #  : hdbscan.dist_metrics.PyFuncDistance,
 'rogerstanimoto' , #  : hdbscan.dist_metrics.RogersTanimotoDistance,
 'russellrao'     , #  : hdbscan.dist_metrics.RussellRaoDistance,
 'seuclidean'     , #  : hdbscan.dist_metrics.SEuclideanDistance,
 'sokalmichener'  , #  : hdbscan.dist_metrics.SokalMichenerDistance,
 'sokalsneath'    , #  : hdbscan.dist_metrics.SokalSneathDistance,
 'wminkowski'     , #  : hdbscan.dist_metrics.WMinkowskiDistance}
]
#
#     
#
#
#eval_results = []
#for metric in DISTINCT_METRICS:
#
#    try:
#        result = cluster_eval(metric=metric)
#        eval_results.append(result)
#    except Exception as err:
#        #print("OOPS, ERROR...", err)
#        result = {"metric": metric, "err": err}
#        eval_results.append(result)
#
#eval_results_df = DataFrame(eval_results)
#eval_results_df

"""## Results and Interpretation

Doesn't look like we are getting good results for dimensionality reduction or clustering.
"""