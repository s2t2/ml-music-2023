import os

import numpy as np
from pandas import DataFrame

from app import download_json
from app.gtzan_dataset import GenreDataset, GTZAN_DIRPATH, GENRES_DIRPATH #, GenresDataset
from app.audio_processor import AudioProcessor, TRACK_LENGTH, N_MFCC


if __name__ == "__main__":

    ds = GenreDataset()
    genres = ds.genres
    print("GENRES:", genres)

    records = []
    for genre in genres:
        genre_dirpath = os.path.join(GENRES_DIRPATH, genre)
        #audio_filenames = sorted(os.listdir(genre_dirpath))
        audio_filenames = sorted([fname for fname in os.listdir(genre_dirpath) if fname.endswith(".wav")])
        print(genre, len(audio_filenames))

        for audio_filename in audio_filenames:
            audio_filepath = os.path.join(genre_dirpath, audio_filename)
            try:
                ap = AudioProcessor(audio_filepath)

                #track = ap.audio
                tracks = ap.tracks(track_length_seconds=TRACK_LENGTH)
                for track in tracks:
                    track = np.array(track)

                    mfcc = ap.mfcc(n_mfcc=N_MFCC, audio_data=track)
                    mfcc = mfcc.T

                    #print(audio_filename, track.shape, mfcc.shape)
                    records.append({
                        "genre": genre,
                        "audio_filename": audio_filename,
                        "track_length": len(track),
                        "mfcc_rows": mfcc.shape[0], # related to the track length
                        "mfcc_cols": mfcc.shape[1], # should equal n_mfcc
                        "mfcc": mfcc
                    })


            except Exception as err:
                print("... ERR:", audio_filename, err)

    #
    # MFCC RESULTS
    #

    results_df = DataFrame(records)
    results_df.drop(columns=["mfcc"], inplace=True) # drop column with nested data
    print("TRACKS:", len(results_df))
    print(results_df.head())

    print("TRACK LENGTHS:")
    print(results_df["track_length"].value_counts())
    print(results_df["mfcc_rows"].value_counts())
    print("N MFCC:")
    print(results_df["mfcc_cols"].value_counts())

    #
    # SAVE MFCC RECORDS
    #

    FEATURES_DIR = os.path.join(GTZAN_DIRPATH, f"features_{TRACK_LENGTH}s")
    os.makedirs(FEATURES_DIR, exist_ok=True)

    #csv_filepath = os.path.join(FEATURES_DIR, f"mfcc_{N_MFCC}_summary.csv")
    #results_df.to_csv(csv_filepath, index=False)

    json_filepath = os.path.join(FEATURES_DIR, f"mfcc_{N_MFCC}.json")
    for row in results_df:
        row["mfcc"] = row["mfcc"].tolist() # numpy not serializable
        del row["track_length"]
        del row["mfcc_rows"]
        del row["mfcc_cols"]
    download_json(results_df, json_filepath)
