#import os
#
#import numpy as np
#from pandas import DataFrame
#
#from app.gtzan_dataset import GenreDataset
#from app.audio_processor import AudioProcessor, TRACK_LENGTH, N_MFCC
#
#
#if __name__ == "__main__":
#
#    ds = GenreDataset()
#    genres = ds.genres
#    print("GENRES:", genres)
#
#    records = []
#    for audio_file in ds.audio_files:
#        try:
#            ap = AudioProcessor(audio_file.audio_filepath)
#            tracks = ap.tracks(track_length_seconds=TRACK_LENGTH)
#            for track in tracks:
#                track_info = {"genre": audio_file.genre, "audio_filename": audio_file.audio_filename, "track_length": len(track)}
#                track_features = ap.audio_features(n_mfcc=N_MFCC, audio_data=np.array(track))
#                records.append({**track_info, **track_features})
#
#        except Exception as err:
#            print("... ERR:", audio_file.audio_filename, err)
#
#    #
#    # FEATURE RESULTS
#    #
#
#    results_df = DataFrame(records)
#    print("TRACKS:", len(results_df))
#    print(results_df.head())
#
#    print("TRACK LENGTHS:")
#    print(results_df["track_length"].value_counts())
#
#    # SAVE FEATURE RECORDS
#
#    csv_filepath = ds.features_csv_filepath(track_length=TRACK_LENGTH, n_mfcc=N_MFCC)
#    results_df.to_csv(csv_filepath, index=False)
#
