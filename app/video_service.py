


import os
from functools import cached_property
from pprint import pprint

from pytube import YouTube as Video, Channel
from pytube.exceptions import PytubeError

from app.video_decorators import video_metadata
from app.image_service import ImageService


class VideoService:

    def __init__(self, video_url="https://www.youtube.com/watch?v=q6HiZIQoLSU"):
        self.video_url = video_url

        self.audio_filepath = None

        #self.download_audio()


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

    @cached_property
    def audio_streams(self):
        return self.video.streams.filter(only_audio=True, file_extension='mp4').order_by("abr").asc()

    def download_audio(self, audio_filepath=None):
        download_params = {"skip_existing": True}
        if audio_filepath:
            download_params["output_path"] = audio_filepath
        self.audio_filepath = self.audio_streams.first().download(**download_params)
        print("AUDIO FILEPATH:", self.audio_filepath) #> "/content/Maggie Rogers - Say It (Live On The Tonight Show Starring Jimmy Fallon  2019).mp4"



    def display_thumbnail_notebook(self, height=250):
        ImageService(url=self.video.thumbnail_url).display_notebook(height=height)

    def display_thumbnail_local(self):
        ImageService(url=self.video.thumbnail_url).display_local()

    #def play_in_colab(self, audio_data=None, image=True):
    #    audio_data = audio_data or self.audio_filepath
    #    if image:
    #        display(Image(url=self.video.thumbnail_url, height=250))
    #    display(Audio(audio_data, autoplay=False, rate=self.sr)) # rate only necessary when passing custom audio data

    #def play_local(self, audio_data=None, image=True):
    #    #self.play_in_colab(audio_data, image)

    #@cached_property
    #def channel(self):
    #    return Channel(self.video.channel_url)

if __name__ == "__main__":


    VIDEOS_DIRPATH = os.path.join(os.path.dirname(__file__), "..", "content", "videos")

    yt = VideoService()

    video = yt.video
    if video:
        print("VIDEO ID:", video.video_id)
        print("TITLE:", video.title)
        print("AUTHOR:", video.author)
        print("URL:", video.watch_url)
        print("LENGTH:", video.length)
        #print("PUBLISHED:", video.publish_date)
        #print(video_metadata(video))

        yt.display_thumbnail_local()

        breakpoint()
        audio_filepath = os.path.join(VIDEOS_DIRPATH, video.author.lower(), video.video_id)
        yt.download_audio(audio_filepath=audio_filepath)
