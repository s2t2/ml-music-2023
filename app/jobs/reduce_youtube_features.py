



import os
import json
import numpy as np
from functools import cached_property


from sklearn.preprocessing import scale
from pandas import DataFrame
from sklearn.decomposition import PCA
import plotly.express as px


from app.youtube_dataset import YoutubeDataset
from app.audio_processor import TRACK_LENGTH, N_MFCC

N_COMPONENTS = int(os.getenv("N_COMPONENTS", default="2"))
X_SCALE = bool(os.getenv("X_SCALE", default="true") == "true")

LABEL_COLS = ["artist_name", "video_id", "audio_filename", "track_number", "track_length"]



class ReductionPipeline:
    def __init__(self, df, label_cols=LABEL_COLS, y_col="artist_name", x_scale=X_SCALE,
                        n_components=N_COMPONENTS, track_length=TRACK_LENGTH, n_mfcc=N_MFCC,
                        chart=True):

        self.df = df
        self.labels_df = self.df[label_cols]
        self.x = self.df.drop(columns=label_cols)
        self.y = self.df[y_col]
        print("X:", self.x.shape)
        print("Y:", len(self.y))

        self.x_scale = x_scale

        self.model_type = "PCA"
        self.n_components = n_components

        self.chart = chart
        self.track_length = track_length
        self.n_mfcc = n_mfcc

        self.embeddings = None
        self.embeddings_df = None
        self.loadings = None
        self.loadings_df = None

    @cached_property
    def feature_names(self):
        return self.x.columns.tolist()

    @cached_property
    def component_names(self):
        return [f"component_{i}" for i in range(1, self.n_components+1)]

    @cached_property
    def x_scaled(self):
        x = scale(self.x)
        df = DataFrame(x, columns=self.feature_names)
        df.index = self.x.index
        return df

    def perform(self):
        if self.x_scale:
            x = self.x_scaled
        else:
            x = self.x

        self.pca = PCA(n_components=self.n_components, random_state=99)

        self.embeddings = self.pca.fit_transform(x)
        print("EMBEDDINGS:", type(self.embeddings), self.embeddings.shape)
        print("EXPLAINED VARIANCE RATIO:", self.pca.explained_variance_ratio_)
        print("SINGULAR VALS:", self.pca.singular_values_)

        self.embeddings_df = DataFrame(self.embeddings, columns=self.component_names)
        self.embeddings_df = self.embeddings_df.merge(self.labels_df, left_index=True, right_index=True)

        self.loadings = self.pca.components_.T * np.sqrt(self.pca.explained_variance_)
        self.loadings_df = DataFrame(self.loadings)

        if self.chart:
            self.plot_embeddings()

    def plot_embeddings(self, height=500):
        title = f"""GTZAN Genre Classifier - Dimensionality Reduction ({self.model_type} n_components={self.n_components})
            <br><sup>Data: {self.track_length}s tracks, {self.n_mfcc} MFCCs</sup>
        """
        chart_params = dict(x="component_1", y="component_2", title=title, height=height,
            color="artist_name", #, hover_data="audio_filename"
        )

        if self.n_components == 2:
            fig = px.scatter(self.embeddings_df, **chart_params)
            fig.show()
        elif self.n_components ==3:
            chart_params["z"] = "component_3"
            fig = px.scatter_3d(self.embeddings_df, **chart_params)
            fig.show()







#def plot_explained_variance(pca_results):
#    pca_results_df = DataFrame(pca_results)
#
#    title = f"""Total Explained Variance by Number of Components (PCA)
#    <br><sup>Data: {TRACK_LENGTH}s tracks, {N_MFCC} MFCCs</sup>
#    """
#    fig = px.line(pca_results_df, x="n_components", y="explained_variance",
#            title=title,
#            markers="line+point", color_discrete_sequence=["steelblue"]
#    )
#    fig.show()


#def plot_scree(pca_results_df):
#    eigenvals = pca_results_df.sort_values(by=["n_components"], ascending=False).iloc[0]["eigenvals"]
#    print("EIGENVALS:", eigenvals)
#
#    component_numbers = list(range(1, len(pca_results_df)+1))
#    print("COMPONENT NUMBERS:", component_numbers)
#
#    title=f"""Scree Plot of Eigenvalues by Component (PCA)
#    <br><sup>Data: {TRACK_LENGTH}s tracks, {N_MFCC} MFCCs</sup>
#    """
#    fig = px.line(x=component_numbers, y=eigenvals,
#            title=title,
#            labels={"x": "Component Number", "y": "Eigenvalue"},
#            markers="line+point", color_discrete_sequence=["steelblue"]
#    )
#    fig.show()






if __name__ == "__main__":

    #
    # LOAD DATA
    #

    ds = YoutubeDataset()
    print(ds.artist_names)

    df = ds.read_features_csv(track_length=TRACK_LENGTH, n_mfcc=N_MFCC)
    #df.index = df["artist_name"] + "  " + df["audio_filename"] + "  " + df["track_number"].astype(str)
    #df.index = df["audio_filename"] + "--" + df["track_number"].astype(str)
    print(len(df))

    #
    # REDUCE DATA
    #

    pca_pipeline = ReductionPipeline(df)
    pca_pipeline.perform()

    #print(embeddings_df.head())
    #csv_filepath = os.path.join(DATA_DIRPATH, f"gtzan_songs_{TRACK_LENGTH}s_mfcc{N_MFCC}_pca_{n_components}.csv")
    #embeddings_df.to_csv(csv_filepath)
