

import pytest

from app.gtzan_dataset import GenreDataset

from conftest import CI_ENV


@pytest.mark.skipif(CI_ENV, reason="avoid issuing HTTP requests on the CI server")
def test_genres():

    ds = GenreDataset()

    assert ds.genres == ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

    assert len(ds.audio_files) == 1000
