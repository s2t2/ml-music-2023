



import os



from app.youtube_dataset import YoutubeDataset
from app.audio_processor import TRACK_LENGTH, N_MFCC
from app.reduction_pipeline import ReductionPipeline #, N_COMPONENTS, X_SCALE, FIG_SHOW, LABEL_COLS







if __name__ == "__main__":

    ds = YoutubeDataset()

    component_nums = [2 , 3]
    #params_grid = [
    #    # (track_length, n_mfcc)
    #    (3, 8), (3,13), (3,20),
    #    #(10, 8), (10,13), (10,20),
    #    #(15, 8), (15,13), (15,20),
    #    #(20, 8), (20,13), (20,20),
    #    (30, 8), (30,13), (30,20)
    #]
    params_grid = [
        # (track_length, n_mfcc)
        (3,13), #(3,20),
        (30,13), # (30,20)
    ]
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
                pca_pipeline.plot_embeddings()
                pca_pipeline.plot_embedding_centroids()
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
