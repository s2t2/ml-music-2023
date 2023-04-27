


import os
from functools import cached_property
from time import sleep
from pprint import pprint
import json

from pytube import YouTube as Video, Channel
from pytube.exceptions import PytubeError
from IPython.display import display, Audio, Image
#from simpleaudio import WaveObject

from app import download_json
from app.youtube_dataset import YOUTUBE_AUDIO_DIRPATH
from app.video_decorators import video_metadata
from app.image_service import ImageService


VIDEO_URL = os.getenv("VIDEO_URL", default="https://www.youtube.com/watch?v=q6HiZIQoLSU")
MAX_ATTEMPTS = int(os.getenv("MAX_ATTEMPTS", default=15))
VERBOSE = bool(os.getenv("VERBOSE", default="false") == "true")

class YoutubeVideoService():

    def __init__(self, video_url=VIDEO_URL, artist_name=None):
        self.video_url = video_url
        self.artist_name = artist_name
        #self.max_attempts = max_attempts
        self.audio_filepath = None

    @cached_property
    def video(self, max_attempts=MAX_ATTEMPTS):
        """returns the video or none?"""
        n_attempts = 0
        while n_attempts < max_attempts:
            n_attempts+=1
            #print(f"FETCHING YOUTUBE VIDEO (ATTEMPT #{n_attempts})...")
            #print("...")
            try:
                #raise PytubeError("OOPS")
                v = Video(self.video_url)
                # https://github.com/pytube/pytube/issues/1473
                # https://github.com/pytube/pytube/issues/1545
                v.title
                return v
            except (PytubeError, KeyError) as err:
                if VERBOSE:
                    print("... ERROR:", err)
                sleep(1)

    @cached_property
    def channel(self):
        return Channel(self.video.channel_url)

    @cached_property
    def audio_streams(self):
        return self.video.streams.filter(only_audio=True, file_extension='mp4').order_by("abr").asc()

    @cached_property
    def video_dirpath(self):
        if not self.artist_name:
            default_artist_name = self.video.author.lower()
            self.artist_name = input(f"What is the artist name you would like to save this video under ({default_artist_name})? ") or default_artist_name

        dirpath = os.path.join(YOUTUBE_AUDIO_DIRPATH, self.artist_name, self.video.video_id)
        os.makedirs(dirpath, exist_ok=True)
        return dirpath

    def download_metadata(self, download_dirpath=None):
        download_dirpath = download_dirpath or self.video_dirpath
        metadata_filepath = os.path.join(self.video_dirpath, "video.json")
        download_json(data=video_metadata(self.video, as_json=True), json_filepath=metadata_filepath)

    def download_audio(self, download_dirpath=None):
        download_dirpath = download_dirpath or self.video_dirpath
        download_params = {"skip_existing": True, "output_path": download_dirpath}
        self.audio_filepath = self.audio_streams.first().download(**download_params)
        #print("AUDIO FILEPATH:", self.audio_filepath) #> "/content/Maggie Rogers - Say It (Live On The Tonight Show Starring Jimmy Fallon  2019).mp4"


    #def display_thumbnail_in_colab(self, height=250):
    #    ImageService(url=self.video.thumbnail_url).display_notebook(height=height)

    def display_thumbnail(self):
        ImageService(url=self.video.thumbnail_url).display()

    #def play_audio_in_colab(self, audio_data=None, image=True):
    #    audio_data = audio_data or self.audio_filepath
    #    display(Audio(audio_data, autoplay=False, rate=self.sr)) # rate only necessary when passing custom audio data

    #def play_audio(self, audio_filepath=None):
    #    #playsound(audio_data)
    #    wave_obj = WaveObject.from_wave_file(audio_filepath or self.audio_filepath)
    #    play_obj = wave_obj.play()
    #    play_obj.wait_done()


if __name__ == "__main__":

    yt = YoutubeVideoService()

    video = yt.video
    if video:
        print("VIDEO:", video.video_id, video.watch_url)
        print("AUTHOR:", video.author)
        print("TITLE:", video.title)
        print("LENGTH:", video.length)
        print("VIEWS:", video.views)

        yt.display_thumbnail()

        print("DOWNLOADING METADATA...")
        yt.download_metadata()

        print("DOWNLOADING AUDIO...")
        yt.download_audio()

        #yt.play_audio()
