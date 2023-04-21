from pytube import YouTube as Video

from app.video_service import VideoService, split_into_batches


#assert parse_audio_filename("/content/Maggie Rogers - The Knife (Live On Austin City Limits).mp4") == "Maggie Rogers - The Knife (Live On Austin City Limits).mp4"
#assert parse_video_id("https://www.youtube.com/watch?v=0dzZXpf7sSQ") == "0dzZXpf7sSQ"

def test_split_into_batches():
    result = list(split_into_batches([1,2,3,4,5,6,7], batch_size=3))
    print(result)
    assert result == [[1,2,3], [4,5,6], [7]]


def test_video_service():

    yt = VideoService()

    # VIDEO:

    video = yt.video
    assert isinstance(video, Video)
