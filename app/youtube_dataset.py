

import os
import json
from functools import cached_property
from pandas import read_csv

from app import DATA_DIRPATH


YOUTUBE_DIRPATH = os.path.join(DATA_DIRPATH, "youtube")
YOUTUBE_AUDIO_DIRPATH = os.path.join(YOUTUBE_DIRPATH, "audio")


class AudioFile:

    def __init__(self, audio_filepath):
        self.audio_filepath = audio_filepath

        self.artist_name = self.audio_filepath.split("/")[-3]
        self.video_id = self.audio_filepath.split("/")[-2]
        self.audio_filename = self.audio_filepath.split("/")[-1]

        #self.artist_dirpath = os.path.join(______, self.artist_name)
        #self.video_dirpath = os.path.join(self.artist_dirpath, self.video_id)

    #def exists(self):
    #    return os.path.isfile(self.audio_filepath)


class YoutubeDataset:

    def __init__(self, youtube_dirpath=YOUTUBE_DIRPATH):
        self.youtube_dirpath = youtube_dirpath
        self.youtube_audio_dirpath = os.path.join(self.youtube_dirpath, "audio")

    @property
    def artist_names(self):
        return [fname for fname in os.listdir(YOUTUBE_AUDIO_DIRPATH) if fname not in [".DS_Store"]]

    @cached_property
    def audio_files(self):
        files = []
        for artist_name in self.artist_names:
            artist_dirpath = os.path.join(self.youtube_audio_dirpath, artist_name)
            video_ids = [video_id for video_id in os.listdir(artist_dirpath) if video_id not in [".DS_Store"]]
            for video_id in video_ids:
                video_dirpath = os.path.join(artist_dirpath, video_id)
                audio_filename = [fname for fname in os.listdir(video_dirpath) if fname.endswith(".mp4")][0]
                audio_filepath = os.path.join(video_dirpath, audio_filename)
                files.append(AudioFile(audio_filepath))
        return files

    def features_csv_filepath(self, track_length, n_mfcc):
        features_dirpath = os.path.join(self.youtube_dirpath, "features")
        os.makedirs(features_dirpath, exist_ok=True)
        return os.path.join(features_dirpath, f"length_{track_length}_mfcc_{n_mfcc}_features.csv")

    def read_features_csv(self, track_length, n_mfcc):
        csv_filepath = self.features_csv_filepath(track_length, n_mfcc)
        return read_csv(csv_filepath)












    # TODO: deprecate these methods

    def video_dirpaths(self, artist_name=None):
        if artist_name:
            artist_names = [artist_name]
        else:
            artist_names = self.artist_names

        dirpaths = []
        for artist_name in artist_names:
            artist_dirpath = os.path.join(YOUTUBE_AUDIO_DIRPATH, artist_name)
            video_ids = [fname for fname in os.listdir(artist_dirpath) if fname not in [".DS_Store"]]

            for video_id in video_ids:
                dirpath = os.path.join(artist_dirpath, video_id)
                dirpaths.append(dirpath)

        return sorted(dirpaths)

    def take_audio_filepath(self, artist_name=None):
        video_dirpath = self.video_dirpaths(artist_name)[0]
        audio_filenames = [fname for fname in os.listdir(video_dirpath) if fname.endswith(".mp4")]
        audio_filename = audio_filenames[0]
        audio_filepath = os.path.join(video_dirpath, audio_filename)

        return audio_filepath



# TODO: move me
def load_mfcc_json(track_length, n_mfcc):
    print("LOADING DATA...")
    json_filepath = os.path.join(YOUTUBE_DIRPATH, f"features_{track_length}s", f"mfcc_{n_mfcc}.json")
    print(os.path.abspath(json_filepath))
    with open(json_filepath, "r") as json_file:
        return json.load(json_file)
