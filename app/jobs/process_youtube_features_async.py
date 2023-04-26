import os
from threading import current_thread #, BoundedSemaphore
from concurrent.futures import ThreadPoolExecutor, as_completed # see: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor

import numpy as np
from pandas import DataFrame

from app.youtube_dataset import YoutubeDataset, AudioFile as YoutubeAudioFile
from app.audio_processor import AudioProcessor, TRACK_LENGTH, N_MFCC #, split_into_batches


MAX_THREADS = int(os.getenv("MAX_THREADS", default=5)) # the max number of threads to use, for concurrent processing


# todo: consider refactoring into the FeatureMakerAsync class, or assigning to a class method
def process_youtube_audio_async(audio_file:YoutubeAudioFile, track_length=TRACK_LENGTH, n_mfcc=N_MFCC):
    audio_filename = audio_file.audio_filename #audio_filepath.split("/")[-1]
    print(f"{current_thread().name} PROCESSING AUDIO -- {audio_filename}")

    records = []
    try:
        ap = AudioProcessor(audio_file.audio_filepath)
        tracks = ap.tracks(track_length_seconds=track_length)
        for i, track in enumerate(tracks):
            track_info = {
                "artist_name": audio_file.artist_name,
                "video_id": audio_file.video_id,
                "audio_filename": audio_filename,
                "track_number": i+1,
                "track_length": len(track)
            }
            #records.append(track_info)
            track_features = ap.audio_features(n_mfcc=n_mfcc, audio_data=np.array(track))
            records.append({**track_info, **track_features})

    except Exception as err:
        print("... ERR:", audio_filename, err)

    return records


class FeatureMaker:
    def __init__(self, ds, track_length=TRACK_LENGTH, n_mfcc=N_MFCC):
        """Pass one of the dataset classes GenreDataset or YoutubeDataset"""
        self.ds = ds
        self.track_length = track_length
        self.n_mfcc = n_mfcc


    def perform_async(self, max_threads=MAX_THREADS):
        artist_names = ds.artist_names
        print("ARTISTS:", artist_names)

        records = []
        with ThreadPoolExecutor(max_workers=max_threads, thread_name_prefix="THREAD") as executor:

            futures = [executor.submit(process_youtube_audio_async, audio_file) for audio_file in ds.audio_files]
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

        csv_filepath = ds.features_csv_filepath(track_length=self.track_length, n_mfcc=self.n_mfcc)
        results_df.to_csv(csv_filepath, index=False)



if __name__ == "__main__":

    ds = YoutubeDataset()

    job = FeatureMaker(ds=ds) # audio_filetype = YoutubeAudioFile

    job.perform_async()
