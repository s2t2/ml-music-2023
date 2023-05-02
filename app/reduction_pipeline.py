



import os
import numpy as np
from functools import cached_property


from pandas import DataFrame
from sklearn.preprocessing import scale #, StandardScaler

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap import UMAP

import plotly.express as px

from app import RESULTS_DIRPATH
from app.youtube_dataset import YoutubeDataset
from app.audio_processor import TRACK_LENGTH, N_MFCC

N_COMPONENTS = int(os.getenv("N_COMPONENTS", default="2"))
X_SCALE = bool(os.getenv("X_SCALE", default="true") == "true")
FIG_SHOW = bool(os.getenv("FIG_SHOW", default="false") == "true")
FIG_SAVE = bool(os.getenv("FIG_SAVE", default="false") == "true")

LABEL_COLS = ["artist_name", "video_id", "audio_filename", "track_number", "track_length"]



class ReductionPipeline:
    def __init__(self, df, label_cols=LABEL_COLS, y_col="artist_name", x_scale=X_SCALE,
                        track_length=TRACK_LENGTH, n_mfcc=N_MFCC,
                        reducer_type="PCA", n_components=N_COMPONENTS):

        self.df = df
        self.labels_df = self.df[label_cols]
        self.x = self.df.drop(columns=label_cols)
        self.y = self.df[y_col]
        print("X:", self.x.shape)
        print("Y:", len(self.y))

        self.x_scale = x_scale
        self.track_length = track_length
        self.n_mfcc = n_mfcc
        self.reducer_type = reducer_type
        self.n_components = n_components

        self.reducer_name = {"PCA": "pca", "T-SNE": "tsne", "UMAP": "umap"}[self.reducer_type]

        self.reducer = None
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

        if self.reducer_type == "PCA":
            self.reducer = PCA(n_components=self.n_components, random_state=99)
        elif self.reducer_type == "T-SNE":
            self.reducer = TSNE(n_components=self.n_components, random_state=99)
        elif self.reducer_type == "UMAP":
            self.reducer = UMAP(n_components=self.n_components, random_state=99)

        self.embeddings = self.reducer.fit_transform(x)
        print("EMBEDDINGS:", type(self.embeddings), self.embeddings.shape)
        self.embeddings_df = DataFrame(self.embeddings, columns=self.component_names)
        self.embeddings_df = self.embeddings_df.merge(self.labels_df, left_index=True, right_index=True)

        # EXPLAINABILITY:
        if self.reducer_type == "PCA":
            print("EXPLAINED VARIANCE RATIO:", self.reducer.explained_variance_ratio_)
            print("SINGULAR VALS:", self.reducer.singular_values_)

            self.loadings = self.reducer.components_.T * np.sqrt(self.reducer.explained_variance_)
            print("LOADINGS...", type(self.loadings), self.loadings.shape)
            self.loadings_df = DataFrame(self.loadings, columns=self.component_names)
            self.loadings_df.index = self.reducer.feature_names_in_

            # these represent the absolute magnitude of importances, not direction up or down
            self.feature_importances = {}
            for component_name in self.component_names:
                top_feature_names = self.loadings_df.abs().sort_values(by=[component_name], ascending=False).head(10)[component_name]
                self.feature_importances[component_name] = top_feature_names.to_dict()

        elif self.reducer_type == "T-SNE":
            print("K-L DIVERGENCE:", self.reducer.kl_divergence_)



    @property
    def results_dirpath(self):
        dirpath = os.path.join(RESULTS_DIRPATH, "youtube", f"length_{self.track_length}_mfcc_{self.n_mfcc}")
        os.makedirs(dirpath, exist_ok=True)
        return dirpath

    @property
    def embeddings_png_filepath(self):
        return os.path.join(self.results_dirpath, f"{self.reducer_name}_{self.n_components}.png")

    @property
    def embeddings_html_filepath(self):
        return os.path.join(self.results_dirpath, f"{self.reducer_name}_{self.n_components}.html")

    @property
    def centroids_png_filepath(self):
        return os.path.join(self.results_dirpath, f"{self.reducer_name}_{self.n_components}_centroids.png")

    @property
    def centroids_html_filepath(self):
        return os.path.join(self.results_dirpath, f"{self.reducer_name}_{self.n_components}_centroids.html")


    def plot_embeddings(self, height=500, fig_show=FIG_SHOW, fig_save=FIG_SAVE):
        title = f"""Youtube Audio - Dimensionality Reduction ({self.reducer_type} n_components={self.n_components})
            <br><sup>Data: {self.track_length} second tracks, {self.n_mfcc} MFCCs</sup>
        """
        chart_params = dict(x="component_1", y="component_2",
            title=title, height=height,
            color="artist_name", hover_data=["audio_filename", "track_number"]
        )

        fig = None
        if self.n_components == 2:
            fig = px.scatter(self.embeddings_df, **chart_params)
        elif self.n_components ==3:
            chart_params["z"] = "component_3"
            fig = px.scatter_3d(self.embeddings_df, **chart_params)

        if fig and fig_show:
            fig.show()

        if fig and fig_save:
            #fig.write_image(self.embeddings_png_filepath)
            fig.write_html(self.embeddings_html_filepath)

        return fig


    def plot_embedding_centroids(self, height=500, fig_show=FIG_SHOW, fig_save=FIG_SAVE):
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

        elif self.n_components ==3:
            chart_params["z"] = "component_3"
            agg_params["component_3"] = "mean"
            artist_centroids = self.embeddings_df.groupby("artist_name").agg(agg_params)
            artist_centroids["artist_name"] = artist_centroids.index
            fig = px.scatter_3d(artist_centroids, **chart_params)

        if fig:
            fig.update_traces(textposition='top center')

        if fig and fig_show:
            fig.show()

        if fig and fig_save:
            fig.write_html(self.centroids_html_filepath)

        return fig




class PCATuner:

    def __init__(self, features_df, track_length=TRACK_LENGTH, n_mfcc=N_MFCC, label_cols=LABEL_COLS):
        self.features_df = features_df
        self.track_length = track_length
        self.n_mfcc = n_mfcc

        self.label_cols = label_cols # todo: get this more dynamically
        self.feature_names = self.features_df.drop(columns=self.label_cols).columns.tolist()

        self.results = None
        self.results_df = None


    def perform(self):
        self.results = []

        for n_components in range(1, len(self.feature_names)+1):
            pipeline = ReductionPipeline(self.features_df, reducer_type="PCA", n_components=n_components)
            pipeline.perform()

            pca = pipeline.reducer
            self.results.append({
                "n_components": n_components,
                "explained_variance": pca.explained_variance_ratio_.sum(),
                "eigenvals": pca.explained_variance_, # number of vals depend on n components
                #"loadings": loadings,
                #"embeddings": embeddings
            })
        self.results_df = DataFrame(self.results)
        print(self.results_df[["n_components", "explained_variance"]].head())





    @property
    def results_dirpath(self):
        dirpath = os.path.join(RESULTS_DIRPATH, "youtube", f"length_{self.track_length}_mfcc_{self.n_mfcc}")
        os.makedirs(dirpath, exist_ok=True)
        return dirpath


    def plot_explained_variance(self, height=500, fig_show=FIG_SHOW, fig_save=FIG_SAVE):
        title = f"""Total Explained Variance by Number of Components (PCA)
        <br><sup>Data: {self.track_length}s tracks, {self.n_mfcc} MFCCs</sup>
        """
        fig = px.line(self.results_df, x="n_components", y="explained_variance",
                title=title, height=height,
                markers="line+point", color_discrete_sequence=["steelblue"]
        )
        if fig_show:
            fig.show()

        if fig_save:
            image_filepath = os.path.join(self.results_dirpath, "pca-explained-variance.png")
            fig.write_image(image_filepath)
        #return fig


    def plot_scree(self, height=500, fig_show=FIG_SHOW, fig_save=FIG_SAVE):
        eigenvals = self.results_df.sort_values(by=["n_components"], ascending=False).iloc[0]["eigenvals"]
        print("EIGENVALS:", eigenvals)

        component_numbers = list(range(1, len(self.results_df)+1))
        print("COMPONENT NUMBERS:", component_numbers)

        title=f"""Scree Plot of Eigenvalues by Component (PCA)
        <br><sup>Data: {self.track_length}s tracks, {self.n_mfcc} MFCCs</sup>
        """
        fig = px.line(x=component_numbers, y=eigenvals,
                title=title, height=height,
                labels={"x": "Component Number", "y": "Eigenvalue"},
                markers="line+point", color_discrete_sequence=["steelblue"]
        )
        if fig_show:
            fig.show()

        if fig_save:
            image_filepath = os.path.join(self.results_dirpath, "pca-scree.png")
            fig.write_image(image_filepath)
        #return fig



if __name__ == "__main__":


    ds = YoutubeDataset()

    for track_length in [3,30]:
        df = ds.read_features_csv(track_length=track_length, n_mfcc=N_MFCC)

        tuner = PCATuner(df, track_length=track_length, n_mfcc=N_MFCC)
        tuner.perform()
        tuner.plot_explained_variance()
        tuner.plot_scree()
