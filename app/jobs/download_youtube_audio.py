
import os

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
    "tupac": [
        "https://www.youtube.com/watch?v=xg3J5slvB-k", # changes
        "https://www.youtube.com/watch?v=Mb1ZvUDvLDY", # dear mama
        "https://www.youtube.com/watch?v=Do5MMmEygsY", # ghetto gospel
        "https://www.youtube.com/watch?v=mwgZalAFNhM", # california love
    ],
    "jay_z": [
        "https://www.youtube.com/watch?v=vk6014HuxcE", # empire state of mind w/ alicia keys
        "https://www.youtube.com/watch?v=Cgoqrgc_0cM", # big pimpin
        "https://www.youtube.com/watch?v=Oz_-VaTHpc8", # dirt off your shoulder
        "https://www.youtube.com/watch?v=MaQZF0msXxE", # encore
        "https://www.youtube.com/watch?v=GRKmpn3SBdw", # izzo
        "https://www.youtube.com/watch?v=Kzq15y2J4UM", # young forever
        "https://www.youtube.com/watch?v=MzTLMp-vh9s", # 99 problems (clean)
    ],
    "adele": [
        "https://www.youtube.com/watch?v=rYEDA3JcQqw", # rolling in the deep
        "https://www.youtube.com/watch?v=uJdu4Lfy8aI", # set fire to the rain
        "https://www.youtube.com/watch?v=hLQl3WQQoQ0", # someone like you
        "https://www.youtube.com/watch?v=U3ASj1L6_sY", # easy on me
        "https://www.youtube.com/watch?v=oytOOA9sOiE", # love in the dark
        "https://www.youtube.com/watch?v=YQHsXMglC9A", # hello
    ],
    "taylor_swift": [
        "https://www.youtube.com/watch?v=e-ORhEE9VVg", # blank space
        "https://www.youtube.com/watch?v=b1kbLwvqugk", # anti hero
        "https://www.youtube.com/watch?v=nfWlot6h_JM", # shake it off
        "https://www.youtube.com/watch?v=-CmadmM5cOk", # style
        "https://www.youtube.com/watch?v=K-a8s8OLBSE", # cardigan
        "https://www.youtube.com/watch?v=-BjZmE2gtdo", # lover
        "https://www.youtube.com/watch?v=QcIy9NiNbmo", # bad blood
    ],
    "phantogram": [
        "https://www.youtube.com/watch?v=a0ul-BghOAs", # black out days
        "https://www.youtube.com/watch?v=pmb1dDB2tak", # cruel world
        "https://www.youtube.com/watch?v=ZvSgLHWR16o", # mouth full of diamonds
        "https://www.youtube.com/watch?v=Ur17pfjIRVo", # don't move
    ],
    "ariana_grande": [
        "https://www.youtube.com/watch?v=SXiSVQZLje8", # side to side
        "https://www.youtube.com/watch?v=gl1aHhXnN1k", # thank u next
        "https://www.youtube.com/watch?v=pE49WK-oNjU", # stuck with you
        "https://www.youtube.com/watch?v=g5qU7p7yOY8", # love me harder
        "https://www.youtube.com/watch?v=BPgEgaPk62M", # one last time
        "https://www.youtube.com/watch?v=B6_iQvaIjXw", # 34+35
        "https://www.youtube.com/watch?v=tcYodQoapMg", # positions
        "https://www.youtube.com/watch?v=kHLHSlExFis", # god is a woman
        "https://www.youtube.com/watch?v=uKqRAC-JNOM", # bloodline
        "https://www.youtube.com/watch?v=m7XHduHsBvk", # bad idea
        "https://www.youtube.com/watch?v=Z1pmpDRrQhU", # ghostin
        "https://www.youtube.com/watch?v=LH4Y1ZUUx2g", # break up w your gf
    ]

    # "_______", #
    # "_______", #
    # "_______", #
    # "_______", #

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
