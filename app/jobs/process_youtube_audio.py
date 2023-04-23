import os

import numpy as np
from pandas import DataFrame

from app import download_json
from app.youtube_dataset import YoutubeDataset, YOUTUBE_DIRPATH #YOUTUBE_AUDIO_DIRPATH
from app.audio_processor import AudioProcessor, TRACK_LENGTH


N_MFCC = int(os.getenv("N_MFCC", default=13))


if __name__ == "__main__":

    ds = YoutubeDataset()
    video_dirpaths = ds.video_dirpaths()
    print(f"VIDEOS ({len(video_dirpaths)})")

    results = []
    for video_dirpath in video_dirpaths:
        # each video directory has one .mp4 audio file
        audio_filenames = sorted([fname for fname in os.listdir(video_dirpath) if fname.endswith(".mp4")])
        audio_filename = audio_filenames[0]
        audio_filepath = os.path.join(video_dirpath, audio_filename)
        print(os.path.abspath(audio_filepath))

        try:
            ap = AudioProcessor(audio_filepath)

            tracks = ap.tracks(track_length_seconds=TRACK_LENGTH)
            for i, track in enumerate(tracks):
                track = np.array(track)

                mfcc = ap.mfcc(n_mfcc=N_MFCC, audio_data=track)
                mfcc = mfcc.T

                #print(audio_filename, track.shape, mfcc.shape)
                results.append({
                    #"artist_name": artist_name,
                    "audio_filename": audio_filename,
                    "track_number": i+1,
                    "track_length": len(track),
                    "mfcc_rows": mfcc.shape[0], # related to the track length
                    "mfcc_cols": mfcc.shape[1], # should equal n_mfcc
                    "mfcc": mfcc
                })

        except Exception as err:
            print("... ERR:", audio_filename, err)

    results_df = DataFrame(results)
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

    FEATURES_DIR = os.path.join(YOUTUBE_DIRPATH, f"features_{TRACK_LENGTH}s")
    os.makedirs(FEATURES_DIR, exist_ok=True)

    csv_filepath = os.path.join(FEATURES_DIR, f"mfcc_{N_MFCC}_details.csv")
    results_df.to_csv(csv_filepath, index=False)

    json_filepath = os.path.join(FEATURES_DIR, f"mfcc_{N_MFCC}.json")
    for row in results:
        row["mfcc"] = row["mfcc"].tolist() # numpy not serializable
        del row["track_length"]
        del row["mfcc_rows"]
        del row["mfcc_cols"]
    download_json(results, json_filepath)
