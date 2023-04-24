

import os
import json

from app import DATA_DIRPATH


YOUTUBE_DIRPATH = os.path.join(DATA_DIRPATH, "youtube")
YOUTUBE_AUDIO_DIRPATH = os.path.join(YOUTUBE_DIRPATH, "audio")



def load_mfcc_json(track_length, n_mfcc):
    print("LOADING DATA...")
    json_filepath = os.path.join(YOUTUBE_DIRPATH, f"features_{track_length}s", f"mfcc_{n_mfcc}.json")
    print(os.path.abspath(json_filepath))
    with open(json_filepath, "r") as json_file:
        return json.load(json_file)




class YoutubeDataset:

    @property
    def artist_names(self):
        return [fname for fname in os.listdir(YOUTUBE_AUDIO_DIRPATH) if fname not in [".DS_Store"]]


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
