import os
from threading import current_thread #, BoundedSemaphore
from concurrent.futures import ThreadPoolExecutor, as_completed # see: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor

import numpy as np
from pandas import DataFrame

from app.gtzan_dataset import GenreDataset, AudioFile
from app.audio_processor import AudioProcessor, TRACK_LENGTH, N_MFCC #, split_into_batches


MAX_THREADS = int(os.getenv("MAX_THREADS", default=5)) # the max number of threads to use, for concurrent processing


def process_audio_async(audio_file:AudioFile):
    audio_filename = audio_file.audio_filename #audio_filepath.split("/")[-1]
    print(f"{current_thread().name} PROCESSING AUDIO -- {audio_filename}")

    records = []
    try:
        ap = AudioProcessor(audio_file.audio_filepath)
        tracks = ap.tracks(track_length_seconds=TRACK_LENGTH)
        for track in tracks:
            track_info = {"genre": audio_file.genre, "audio_filename": audio_filename, "track_length": len(track)}
            #records.append(track_info)
            track_features = ap.audio_features(n_mfcc=N_MFCC, audio_data=np.array(track))
            records.append({**track_info, **track_features})

    except Exception as err:
        print("... ERR:", audio_filename, err)

    return records








if __name__ == "__main__":

    ds = GenreDataset()
    genres = ds.genres
    print("GENRES:", genres)

    records = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS, thread_name_prefix="THREAD") as executor:

        futures = [executor.submit(process_audio_async, audio_file) for audio_file in ds.audio_files]
        print("AUDIO FILES TO BE PROCESSED:", len(futures))
        for future in as_completed(futures):
            records += future.result()

    print("----------------")
    print("ASYNC PERFORMANCE COMPLETE...")

    #
    # FEATURE RESULTS
    #

    results_df = DataFrame(records)
    print("TRACKS:", len(results_df))
    print(results_df.head())

    print("TRACK LENGTHS:")
    print(results_df["track_length"].value_counts())
    #assert len(results_df["track_length"].unique()) == 1

    # SAVE FEATURE RECORDS

    csv_filepath = ds.features_csv_filepath(track_length=TRACK_LENGTH, n_mfcc=N_MFCC)
    results_df.to_csv(csv_filepath, index=False)
