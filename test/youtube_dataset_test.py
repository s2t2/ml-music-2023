
from app.youtube_dataset import YoutubeDataset



def test_youtube_ds():

    ds = YoutubeDataset()

    assert isinstance(ds.artist_names, list)

    assert isinstance(ds.audio_files, list)
