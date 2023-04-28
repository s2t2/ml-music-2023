import os
from pytest import fixture


from app.audio_processor import AudioProcessor


TEST_AUDIO_FILEPATH = os.path.join(os.path.dirname(__file__), "test", "audio", "pop.00032.wav")


@fixture
def ap():
    return AudioProcessor(audio_filepath=TEST_AUDIO_FILEPATH)
