import os

import numpy as np
from pandas import DataFrame

from app.gtzan_dataset import GenreDataset, GTZAN_DIRPATH, GENRES_DIRPATH
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
            #print(audio_filepath)
            try:
                ap = AudioProcessor(audio_filepath)
                tracks = ap.tracks(track_length_seconds=TRACK_LENGTH)
                for track in tracks:
                    track_info = {"genre": genre, "audio_filename": audio_filename, "track_length": len(track)}
                    track_features = ap.audio_features(n_mfcc=N_MFCC, audio_data=np.array(track))
                    records.append({**track_info, **track_features})

            except Exception as err:
                print("... ERR:", audio_filename, err)

    #
    # FEATURE RESULTS
    #

    results_df = DataFrame(records)
    print("TRACKS:", len(results_df))
    print(results_df.head())

    print("TRACK LENGTHS:")
    print(results_df["track_length"].value_counts())

    # SAVE FEATURE RECORDS

    FEATURES_DIR = os.path.join(GTZAN_DIRPATH, f"features_{TRACK_LENGTH}s")
    os.makedirs(FEATURES_DIR, exist_ok=True)

    csv_filepath = os.path.join(FEATURES_DIR, f"features_mfcc_{N_MFCC}.csv")
    results_df.to_csv(csv_filepath, index=False)
