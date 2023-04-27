



import os
import json
import numpy as np
from functools import cached_property


from sklearn.preprocessing import scale
from pandas import DataFrame
from sklearn.decomposition import PCA
import plotly.express as px

from app import RESULTS_DIRPATH
from app.youtube_dataset import YoutubeDataset
from app.audio_processor import TRACK_LENGTH, N_MFCC

N_COMPONENTS = int(os.getenv("N_COMPONENTS", default="2"))
X_SCALE = bool(os.getenv("X_SCALE", default="true") == "true")
FIG_SHOW = bool(os.getenv("FIG_SHOW", default="false") == "true")

LABEL_COLS = ["artist_name", "video_id", "audio_filename", "track_number", "track_length"]



class ReductionPipeline:
    def __init__(self, df, label_cols=LABEL_COLS, y_col="artist_name", x_scale=X_SCALE,
                        reducer_type="PCA", n_components=N_COMPONENTS,
                        track_length=TRACK_LENGTH, n_mfcc=N_MFCC,
                        fig_show=FIG_SHOW #, fig_save=True
                        ):

        self.df = df
        self.labels_df = self.df[label_cols]
        self.x = self.df.drop(columns=label_cols)
        self.y = self.df[y_col]
        print("X:", self.x.shape)
        print("Y:", len(self.y))

        self.x_scale = x_scale

        self.reducer_type = reducer_type
        self.n_components = n_components

        self.fig_show = fig_show
        #self.fig_save = fig_save
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

        self.plot_embeddings()
        self.plot_embedding_centroids()

    @property
    def results_dirpath(self):
        dirpath = os.path.join(RESULTS_DIRPATH, "youtube", f"length_{self.track_length}_mfcc_{self.n_mfcc}")
        os.makedirs(dirpath, exist_ok=True)
        return dirpath

    @property
    def embeddings_png_filepath(self):
        return os.path.join(self.results_dirpath, f"pca_{self.n_components}.png")

    @property
    def embeddings_html_filepath(self):
        return os.path.join(self.results_dirpath, f"pca_{self.n_components}.html")

    @property
    def centroids_png_filepath(self):
        return os.path.join(self.results_dirpath, f"pca_{self.n_components}_centroids.png")

    @property
    def centroids_html_filepath(self):
        return os.path.join(self.results_dirpath, f"pca_{self.n_components}_centroids.html")


    def plot_embeddings(self, height=500):
        title = f"""Youtube Audio - Dimensionality Reduction ({self.reducer_type} n_components={self.n_components})
            <br><sup>Data: {self.track_length} second tracks, {self.n_mfcc} MFCCs</sup>
        """
        chart_params = dict(x="component_1", y="component_2",
            title=title, height=height,
            color="artist_name", hover_data=["audio_filename", "track_number"]
        )

        if self.n_components == 2:
            fig = px.scatter(self.embeddings_df, **chart_params)
            if self.show:
                fig.show()
            #fig.write_image(self.embeddings_png_filepath)
            fig.write_html(self.embeddings_html_filepath)
        elif self.n_components ==3:
            chart_params["z"] = "component_3"
            fig = px.scatter_3d(self.embeddings_df, **chart_params)
            if self.show:
                fig.show()
            fig.write_html(self.embeddings_html_filepath)


    def plot_embedding_centroids(self, height=500):
        title = f"""Youtube Audio - Dimensionality Reduction ({self.reducer_type} n_components={self.n_components}) Artist Centroids
            <br><sup>Data: {self.track_length} second tracks, {self.n_mfcc} MFCCs</sup>
        """
        chart_params = dict(x="component_1", y="component_2",
            title=title, height=height,
            color="artist_name", # hover_data=["audio_filename", "track_number"]
            text="artist_name"

        )
        agg_params = {"component_1": "mean", "component_2": "mean"}

        fig = None
        if self.n_components == 2:
            artist_centroids = self.embeddings_df.groupby("artist_name").agg(agg_params)
            artist_centroids["artist_name"] = artist_centroids.index
            fig = px.scatter(artist_centroids, **chart_params)
            fig.update_traces(textposition='top center')
            if self.show:
                fig.show()
            fig.write_image(self.centroids_png_filepath)
            fig.write_html(self.centroids_html_filepath)

        elif self.n_components ==3:
            chart_params["z"] = "component_3"
            agg_params["component_3"] = "mean"
            artist_centroids = self.embeddings_df.groupby("artist_name").agg(agg_params)
            artist_centroids["artist_name"] = artist_centroids.index
            fig = px.scatter_3d(artist_centroids, **chart_params)
            fig.update_traces(textposition='top center')
            if self.show:
                fig.show()
            fig.write_html(self.centroids_html_filepath)







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

    ds = YoutubeDataset()

    component_nums = [2 , 3
    ]
    params_grid = [
        # (track_length, n_mfcc)
        (3, 8), (3,13), (3,20),
        #(10, 8), (10,13), (10,20),
        #(15, 8), (15,13), (15,20),
        #(20, 8), (20,13), (20,20),
        (30, 8), (30,13), (30,20)
    ]
    #params_grid = [
    #    # (track_length, n_mfcc)
    #    (3,13), (3,20),
    #    (30,13), (30,20)
    #]
    for track_length, n_mfcc in params_grid:

        try:
            print("----------------------")
            print("LENGTH:", track_length, "N_MFCC:", n_mfcc)

            df = ds.read_features_csv(track_length=track_length, n_mfcc=n_mfcc)
            print("TRACKS:", len(df))

            print("ARTIST NAMES:")
            print(sorted(df["artist_name"].unique()))

            print("FEATURES:")
            print(df.columns.tolist())

            for n_components in component_nums:
                pca_pipeline = ReductionPipeline(df,
                    track_length=track_length,
                    n_mfcc=n_mfcc,
                    n_components=n_components
                )
                pca_pipeline.perform()
        except Exception as err:
            print("OOPS:", err)


    exit()




    #
    # LOAD DATA
    #

    ds = YoutubeDataset()

    df = ds.read_features_csv(track_length=TRACK_LENGTH, n_mfcc=N_MFCC)
    print("TRACKS:", len(df))

    print("ARTIST NAMES:")
    print(sorted(df["artist_name"].unique()))

    print("FEATURES:")
    print(df.columns.tolist())

    #
    # REDUCE DATA
    #

    pca_pipeline = ReductionPipeline(df)
    pca_pipeline.perform()
