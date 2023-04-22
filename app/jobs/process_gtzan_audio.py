import os
import json

import librosa
import numpy as np
from pandas import DataFrame

from app import GTZAN_DIRPATH
from app.audio_features import AudioFeatures as AudioProcessor

GENRES_DIRPATH = os.path.join(GTZAN_DIRPATH, "genres_original")

N_MFCC = os.getenv("N_MFCC", default=20)


if __name__ == "__main__":

    GENRES = [genre for genre in os.listdir(GENRES_DIRPATH) if genre not in [".DS_Store"]]
    print("GENRES:", GENRES)

    results = []
    for genre in GENRES:
        genre_dirpath = os.path.join(GENRES_DIRPATH, genre)
        #audio_filenames = sorted(os.listdir(genre_dirpath))
        audio_filenames = sorted([fname for fname in os.listdir(genre_dirpath) if fname.endswith(".wav")])
        print(genre, len(audio_filenames))

        for audio_filename in audio_filenames:
            audio_filepath = os.path.join(genre_dirpath, audio_filename)
            try:
                ap = AudioProcessor(audio_filepath)

                #track = ap.audio
                tracks = ap.tracks()
                track = np.array(tracks[0]) # trim longer songs at 30 seconds!

                mfcc = ap.mfcc(n_mfcc=N_MFCC, audio_data=track)
                mfcc = mfcc.T

                #print(audio_filename, track.shape, mfcc.shape)
                results.append({
                    "genre": genre,
                    "audio_filename": audio_filename,
                    "track_length": len(track),
                    "mfcc_rows": mfcc.shape[0], # related to the track length
                    "mfcc_cols": mfcc.shape[1], # should equal n_mfcc
                    "mfcc": mfcc
                })

                #ap.save_mfcc(genre, audio_filename, mfcc)
            except Exception as err:
                print("... ERR:", audio_filename, err)


    results_df = DataFrame(results)
    results_df.drop(columns=["mfcc"], inplace=True) # drop column with nested data
    print(results_df.head())

    print("TRACK LENGTHS:")
    print(results_df["track_length"].value_counts())

    print(results_df["mfcc_rows"].value_counts())
    # DISTRIBUTION OF ORIGINAL WAV FILE LENGTHS:
    # 1293    944
    # 1320     10
    # 1292      9
    # 1308      7
    # 1305      6
    # 1296      5
    # 1300      3
    # 1298, 1303      2
    # 1313, 1301, 1297, 1307, 1314, 1290, 1310, 1309, 1299, 1302,1304     1

    print("N MFCC:")
    print(results_df["mfcc_cols"].value_counts())

    results_df.to_csv(os.path.join(GTZAN_DIRPATH, "mfcc_summary.csv"), index=False)



    # todo: all mfccs as JSON

    breakpoint()
