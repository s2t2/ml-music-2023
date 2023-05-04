
import pytest

from app.youtube_dataset import YoutubeDataset

from conftest import CI_ENV


@pytest.mark.skipif(CI_ENV, reason="avoid issuing HTTP requests on the CI server")
def test_youtube_ds():

    ds = YoutubeDataset()

    assert isinstance(ds.artist_names, list)

    assert isinstance(ds.audio_files, list)
