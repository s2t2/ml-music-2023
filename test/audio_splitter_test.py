from pytest import fixture

from conftest import TEST_AUDIO_FILEPATH

from app.audio_splitter import AudioSplitter


@fixture
def spl():
    return AudioSplitter(audio_filepath=TEST_AUDIO_FILEPATH)


def test_splits(spl):

    splits = spl.split(n_stems=2)
    assert list(splits.keys()) == ["vocals", "accompaniment"]
    assert splits["vocals"].shape == (661504, 2)
    assert splits["accompaniment"].shape == (661504, 2)

    #splits = spl.split(n_stems=3)
    #>  spleeter.SpleeterError: No embedded configuration 3stems found

    splits = spl.split(n_stems=4)
    assert list(splits.keys()) == ['vocals', 'drums', 'bass', 'other']
    assert splits["vocals"].shape == (661504, 2)
    assert splits["drums"].shape == (661504, 2)
    assert splits["bass"].shape == (661504, 2)
    assert splits["other"].shape == (661504, 2)

    splits = spl.split(n_stems=5)
    assert list(splits.keys()) == ['vocals', 'piano', 'drums', 'bass', 'other']
    assert splits["vocals"].shape == (661504, 2)
    assert splits["piano"].shape == (661504, 2)
    assert splits["drums"].shape == (661504, 2)
    assert splits["bass"].shape == (661504, 2)
    assert splits["other"].shape == (661504, 2)
