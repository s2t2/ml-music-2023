import os


from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
import numpy as np

from app.audio_processor import AudioProcessor


N_STEMS = int(os.getenv("N_STEMS", default="2"))


class AudioSplitter(AudioProcessor):
    def __init__(self, audio_filepath, #, output_filepath=None,
                 #n_stems=N_STEMS
                ):
        """
        Params :

            audio_filepath (str) : path to the audio

        """
        super().__init__(audio_filepath=audio_filepath)

        #self.n_stems = n_stems
        #self.model_name = f"spleeter:{self.n_stems}stems"
        #self.sep = Separator(self.model_name)

    def split(self, n_stems=N_STEMS, audio_data=None):
        """Params :

            n_stems (int) :
                2 stems: [vocals, other]
                4 stems: [vocals, drums, bass, other]
                5 stems: [vocals, piano, drums, bass, other]

            audio_data (np.array)
        """
        if not isinstance(audio_data, np.ndarray):
            audio_data = self.audio

        model_name = f"spleeter:{n_stems}stems"
        sep = Separator(model_name)
        return sep.separate(audio_data.reshape(-1, 1))
