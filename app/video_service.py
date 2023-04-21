


import os
from functools import cached_property
from pprint import pprint







from pytube import YouTube as Video
from pytube.exceptions import PytubeError

#import numpy as np
from IPython.display import display, Audio, Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image as PilImage



#import warnings
#warnings.filterwarnings("ignore")

from app.video_decorators import video_metadata

# you might need to update the path below, or create a shortcut to the path below
#DATASET_PATH = '/content/drive/MyDrive/Research/DS Research Shared 2023/data/ml_music_2023'
#print(DATASET_PATH)
#assert os.path.isdir(DATASET_PATH)

#CHANNELS_DIRPATH = os.path.join(DATASET_PATH, "youtube_channels")
#print(os.listdir(CHANNELS_DIRPATH))





def parse_video_id(video_url):
    """assumes all video urls are cleanly formatted like https://www.youtube.com/watch?v=ABC123"""
    return video_url.split("?v=")[-1]

def parse_audio_filename(audio_filepath):
    """
    Param audio_filepath like: "/content/Maggie Rogers - The Knife (Live On Austin City Limits).mp4"
    """
    return audio_filepath.split("/content/")[-1]

def split_into_batches(my_list, batch_size=10_000):
    """Splits a list into evenly sized batches"""
    # h/t: https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    for i in range(0, len(my_list), batch_size):
        yield my_list[i : i + batch_size]




class VideoService:

    def __init__(self, video_url="https://www.youtube.com/watch?v=q6HiZIQoLSU", audio_filepath=None):
        self.video_url = video_url
        self.audio_filepath = audio_filepath

    @cached_property
    def video(self, max_attempts=5):
        """returns the video or none?"""
        n_attempts = 0
        while n_attempts < max_attempts:
            n_attempts+=1
            print(f"FETCHING YOUTUBE VIDEO (ATTEMPT #{n_attempts})...")
            try:
                v = Video(self.video_url)
                v.title
                return v
                #raise PytubeError("OOPS")
            except (PytubeError, KeyError) as err:
                print("ERROR:", err)


    def display_thumbnail(self, height=250, notebook=False):
        if notebook:
            display(Image(url=self.video.thumbnail_url, height=height))
        else:
            response = requests.get(self.video.thumbnail_url)
            image = PilImage.open(BytesIO(response.content))
            plt.imshow(image)
            plt.show()




    #def download_audio(self)
    #    self.audio_streams = self.video.streams.filter(only_audio=True, file_extension='mp4').order_by("abr").asc()
    #    download_params = {"skip_existing": True}
    #    if audio_filepath:
    #        download_params["output_path"] = audio_filepath
    #    self.audio_filepath = self.audio_streams.first().download(**download_params)
    #    #print("AUDIO FILEPATH:", self.audio_filepath) # "/content/Maggie Rogers - Say It (Live On The Tonight Show Starring Jimmy Fallon  2019).mp4"

    #def play_in_colab(self, audio_data=None, image=True):
    #    audio_data = audio_data or self.audio_filepath
    #    if image:
    #        display(Image(url=self.video.thumbnail_url, height=250))
    #    display(Audio(audio_data, autoplay=False, rate=self.sr)) # rate only necessary when passing custom audio data

    #def play_local(self, audio_data=None, image=True):
    #    #self.play_in_colab(audio_data, image)



if __name__ == "__main__":


    vs = VideoService()

    video = vs.video
    if video:
        print("VIDEO ID:", video.video_id)
        print("TITLE:", video.title)
        print("AUTHOR:", video.author)
        print("URL:", video.watch_url)
        print("LENGTH:", video.length)
        #print("PUBLISHED:", video.publish_date)
        #print(video_metadata(video))

        vs.display_thumbnail()
