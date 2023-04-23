from pytube import YouTube as Video

from app.youtube_video_service import YoutubeVideoService #, split_into_batches

def test_video_service():

    yt = YoutubeVideoService()

    video = yt.video
    assert isinstance(video, Video)











#def parse_video_id(video_url):
#    """assumes all video urls are cleanly formatted like https://www.youtube.com/watch?v=ABC123"""
#    return video_url.split("?v=")[-1]

#def parse_audio_filename(audio_filepath):
#    """
#    Param audio_filepath like: "/content/Maggie Rogers - The Knife (Live On Austin City Limits).mp4"
#    """
#    return audio_filepath.split("/content/")[-1]




#assert parse_audio_filename("/content/Maggie Rogers - The Knife (Live On Austin City Limits).mp4") == "Maggie Rogers - The Knife (Live On Austin City Limits).mp4"
#assert parse_video_id("https://www.youtube.com/watch?v=0dzZXpf7sSQ") == "0dzZXpf7sSQ"
