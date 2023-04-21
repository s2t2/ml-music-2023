from pytube import YouTube as Video

from app.video_service import VideoService #, split_into_batches

def test_video_service():

    yt = VideoService()

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

#def split_into_batches(my_list, batch_size=10_000):
#    """Splits a list into evenly sized batches"""
#    # h/t: https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
#    for i in range(0, len(my_list), batch_size):
#        yield my_list[i : i + batch_size]



#assert parse_audio_filename("/content/Maggie Rogers - The Knife (Live On Austin City Limits).mp4") == "Maggie Rogers - The Knife (Live On Austin City Limits).mp4"
#assert parse_video_id("https://www.youtube.com/watch?v=0dzZXpf7sSQ") == "0dzZXpf7sSQ"

#def test_split_into_batches():
#    result = list(split_into_batches([1,2,3,4,5,6,7], batch_size=3))
#    print(result)
#    assert result == [[1,2,3], [4,5,6], [7]]
