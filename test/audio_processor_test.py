
import numpy as np

from app.audio_processor import AudioProcessor, split_into_batches


def test_split_into_batches():
    result = list(split_into_batches([1,2,3,4,5,6,7], batch_size=3))
    print(result)
    assert result == [[1,2,3], [4,5,6], [7]]


def test_audio_processor(ap):
    assert isinstance(ap, AudioProcessor)

    assert ap.sample_rate == 22050
    assert ap.sr == 22050

    # MFCC

    mfcc_df = ap.mfcc_df(n_mfcc=13)
    assert mfcc_df.columns.tolist() == ['mfcc_1', 'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5', 'mfcc_6', 'mfcc_7', 'mfcc_8', 'mfcc_9', 'mfcc_10', 'mfcc_11', 'mfcc_12', 'mfcc_13']

    # TRACKS

    # ... by default cuts 30 second tracks:
    tracks_30 = ap.tracks()
    expected_length = 30 * ap.sr
    assert expected_length == 661500
    assert np.array(tracks_30).shape == (1, expected_length) # one long track

    # ... can customize track length:
    tracks_3 = ap.tracks(track_length_seconds=3)
    expected_length = 3 * ap.sr
    assert expected_length == 66150
    assert np.array(tracks_3).shape == (10, expected_length) # ten shorter tracks
