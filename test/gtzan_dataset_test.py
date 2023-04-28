
from app.gtzan_dataset import GenreDataset



def test_genres():

    ds = GenreDataset()

    assert ds.genres == ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

    assert len(ds.audio_filepaths) == 1000
