
import os

from app import YOUTUBE_DIRPATH
from app.youtube_video_service import YoutubeVideoService


VIDEO_URLS = {
    "maggie_rogers":[
        "https://www.youtube.com/watch?v=0dzZXpf7sSQ", # say it
        "https://www.youtube.com/watch?v=q6HiZIQoLSU", # knife
        "https://www.youtube.com/watch?v=bR1d8l92Q8Q", # fallingwater
        "https://www.youtube.com/watch?v=gigJjgPThYA", # overdrive
        "https://www.youtube.com/watch?v=MSFjYe54uv4", # light on
        "https://www.youtube.com/watch?v=yaXAMuhIe7Y", # give a little
        "https://www.youtube.com/watch?v=iKYxMnW7bgs", # love you for a long time
        "https://www.youtube.com/watch?v=IHi5jq2P_Zk", # split stones
        "https://www.youtube.com/watch?v=19ItfuE585w", # alaska (acoustic)
    ],
    "john_mayer": [
        # BATTLE STUDIES
        "https://www.youtube.com/watch?v=GeCClzNCfcA", # John Mayer - Heartbreak Warfare (Official Music Video)
        "https://www.youtube.com/watch?v=FgK7vTaJCEM", # All We Ever Do Is Say Goodbye
        "https://www.youtube.com/watch?v=zr6lp-45bOQ", # Half of My Heart
        "https://www.youtube.com/watch?v=KoLc_6BmyTc", # John Mayer - Perfectly Lonely (Official Audio)
        "https://www.youtube.com/watch?v=VDrZww-uHZU", # Assassin
        "https://www.youtube.com/watch?v=5zqRVADxYpM", # Crossroads
        "https://www.youtube.com/watch?v=E3ZAc6WlPYg", # War of My Life
        "https://www.youtube.com/watch?v=Nt-jb5JHWB8", # Edge of Desire
        "https://www.youtube.com/watch?v=cZVT8Zg0YwE", # Do You Know Me
        "https://www.youtube.com/watch?v=LaG0keIFX6o", # Friends, Lovers or Nothing
        # CONTINUUM
    ],
    "chris_stapleton":[
        # VOL 2
        "https://www.youtube.com/watch?v=sI0TeFf6uD8", # Chris Stapleton - Broken Halos (Official Audio)
        "https://www.youtube.com/watch?v=7IhQrVeXn2M", # Chris Stapleton - I Was Wrong (Official Audio)
        "https://www.youtube.com/watch?v=k4oGoiN4JtM", # Chris Stapleton - Without Your Love (Official Audio)
        "https://www.youtube.com/watch?v=m_TsUb0T95E", # Chris Stapleton - Death Row (Official Audio)
        # VOL 1
        "https://www.youtube.com/watch?v=MPoN-FNB2V8", # Chris Stapleton - Millionaire (Official Audio)
        # STARTING OVER
        "https://www.youtube.com/watch?v=wilhfxYfqfc", # You Should Probably Leave
        "https://www.youtube.com/watch?v=UIAo_Awfs-E", # Cold
        "https://www.youtube.com/watch?v=A3svABDnmio", # Chris Stapleton - Starting Over (Official Music Video)
        "https://www.youtube.com/watch?v=WbBt5qDoCAs", # Chris Stapleton - Devil Always Made Me Think Twice (Official Audio)
        "https://www.youtube.com/watch?v=jsE_zp_4vyo", # Chris Stapleton - Joy Of My Life (Official Audio)
        "https://www.youtube.com/watch?v=EzqskyzdWJw", # Chris Stapleton - Hillbilly Blood (Official Audio)
        # TRAVELER
        "https://www.youtube.com/watch?v=l6_w3887Rwo", # Tennessee Whiskey
    ],


}



if __name__ == "__main__":

    print("DOWNLOADING AUDIO FROM YOUTUBE...")

    for artist_name, video_urls in VIDEO_URLS.items():
        for video_url in video_urls:
            print(video_url)

            yt = YoutubeVideoService(video_url, artist_name=artist_name)
            video = yt.video
            if video:
                print("... VIDEO:", video.video_id, video.author, video.title)
                yt.download_metadata()
                yt.download_audio()
            else:
                print("... OOPS, SKIPPING...")
