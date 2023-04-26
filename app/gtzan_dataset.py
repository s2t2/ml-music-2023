

import os
from functools import cached_property

from pandas import read_csv

from app import DATA_DIRPATH


GTZAN_DIRPATH = os.path.join(DATA_DIRPATH, "gtzan")
GENRES_DIRPATH = os.path.join(GTZAN_DIRPATH, "genres_original")


class AudioFile:

    def __init__(self, audio_filepath):
        self.audio_filepath = audio_filepath

        self.genre = audio_filepath.split("/")[-2]
        self.audio_filename = audio_filepath.split("/")[-1]

        self.genre_dirpath = os.path.join(GENRES_DIRPATH, self.genre)


class GenreDataset:

    @cached_property
    def genres(self):
        return sorted([genre for genre in os.listdir(GENRES_DIRPATH) if genre not in [".DS_Store"]])

    #@cached_property
    #def audio_filepaths(self):
    #    filepaths = []
    #    for genre in self.genres:
    #        genre_dirpath = os.path.join(GENRES_DIRPATH, genre)
    #        audio_filenames = sorted([fname for fname in os.listdir(genre_dirpath) if fname.endswith(".wav")])
    #        #print(genre, len(audio_filenames))
    #        for audio_filename in audio_filenames:
    #            audio_filepath = os.path.join(genre_dirpath, audio_filename)
    #            filepaths.append(audio_filepath)
    #    return filepaths

    @cached_property
    def audio_files(self):
        files = []
        for genre in self.genres:
            genre_dirpath = os.path.join(GENRES_DIRPATH, genre)
            audio_filenames = sorted([fname for fname in os.listdir(genre_dirpath) if fname.endswith(".wav")])
            #print(genre, len(audio_filenames))

            for audio_filename in audio_filenames:
                audio_filepath = os.path.join(genre_dirpath, audio_filename)
                files.append(AudioFile(audio_filepath))

        return files


    def features_csv_filepath(self, track_length, n_mfcc):
        features_dirpath = os.path.join(GTZAN_DIRPATH, f"features_{track_length}s")
        os.makedirs(features_dirpath, exist_ok=True)
        return os.path.join(features_dirpath, f"mfcc_{n_mfcc}_features.csv")

    def read_features_csv(self, track_length, n_mfcc):
        csv_filepath = self.features_csv_filepath(track_length, n_mfcc)
        return read_csv(csv_filepath)
