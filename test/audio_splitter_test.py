import numpy as np

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



def test_split_track(spl):
    ap = spl

    tracks = ap.tracks(track_length_seconds=3)
    track = tracks[0]
    track = np.array(track)
    assert len(track) == 66150

    splits = ap.split(n_stems=5, audio_data=track)
    assert len(splits["vocals"]) == 66150
    assert len(splits["piano"]) == 66150
    assert len(splits["drums"]) == 66150
    assert len(splits["bass"]) == 66150
    assert len(splits["other"]) == 66150

    #breakpoint()

    #vocals = splits["vocals"]

    #vocals = splits["vocals"]
    #vocals_0 = vocals[:,0]
    #vocals_1 = vocals[:,1]

    #vocals_df = DataFrame(vocals, columns=["vocals_0", "vocals_1"])

    # take the average of the two columns, convert into a single column
    #result["vocals"] = splits["vocals"].mean(axis=1)
