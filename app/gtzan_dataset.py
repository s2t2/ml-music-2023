

import os
from functools import cached_property

from app import DATA_DIRPATH


GTZAN_DIRPATH = os.path.join(DATA_DIRPATH, "gtzan")
GENRES_DIRPATH = os.path.join(GTZAN_DIRPATH, "genres_original")


class GenreDataset:

    @cached_property
    def genres(self):
        return sorted([genre for genre in os.listdir(GENRES_DIRPATH) if genre not in [".DS_Store"]])

    @cached_property
    def audio_filepaths(self):
        filepaths = []
        for genre in self.genres:
            genre_dirpath = os.path.join(GENRES_DIRPATH, genre)
            audio_filenames = sorted([fname for fname in os.listdir(genre_dirpath) if fname.endswith(".wav")])
            #print(genre, len(audio_filenames))

            for audio_filename in audio_filenames:
                audio_filepath = os.path.join(genre_dirpath, audio_filename)
                filepaths.append(audio_filepath)

        return filepaths
