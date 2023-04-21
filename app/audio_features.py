
import os

import librosa
from librosa.feature import mfcc, chroma_stft, melspectrogram, spectral_contrast, tonnetz
from librosa.effects import harmonic
import numpy as np
import soundfile as sf


def split_into_batches(my_list, batch_size=10_000):
    """Splits a list into evenly sized batches"""
    # h/t: https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    for i in range(0, len(my_list), batch_size):
        yield my_list[i : i + batch_size]


class AudioFeatures:

    def __init__(self, audio_filepath):
        self.audio_filepath = audio_filepath

        self.audio_filename = self.audio_filepath.split("/")[-1]
        print(self.audio_filename)

        # EXTRACT AUDIO DATA:
        self.audio, self.sample_rate = librosa.load(self.audio_filepath)

    @property
    def sr(self):
        """shorthand alias for the sample rate"""
        return self.sample_rate

    #
    # AUDIO FEATURES
    #

    def mfcc(self, n_mfcc=12, audio_data=None):
        """audio_data (np.array)"""
        # if no data is specified, use the entire audio:
        if not isinstance(audio_data, np.ndarray):
            audio_data = self.audio

        print(f"MFCC ({n_mfcc})...")
        return mfcc(y=audio_data, sr=self.sr, n_mfcc=n_mfcc)

    #def chroma_stft(self):
    #    print("CHROMA STFT...")
    #    return chroma_stft(y=audio_data, sr=self.sr)

    #def melspectrogram(self, audio_data=None):
    #    print("MELSPECTROGRAM...")
    #    return melspectrogram(y=audio_data, sr=self.sr)

    #def spectral_contrast(self, audio_data=None):
    #    print("SPECTRAL CONTRAST...")
    #    return spectral_contrast(y=audio_data, sr=self.sr)

    #def tonnetz(self, audio_data=None):
    #    print("TONNETZ...")
    #    return tonnetz(y=harmonic(audio_data), sr=self.sr)

    #
    # TRACK CUTTING
    #

    def tracks(self, track_length_seconds=30, discard_last=True):
        """Returns equal sized tracks of the given duration.
            Discards the last track, because it will have a different duration.
        """

        track_length = track_length_seconds * self.sr
        #print("TRACK LENGTH:", track_length) #> 661_500 for 30s with a sample rate of 22_050 per second

        all_tracks = list(split_into_batches(self.audio.tolist(), batch_size=track_length))
        #print(f"ALL TRACKS ({len(all_tracks)}):", [len(t) for t in all_tracks])

        if discard_last:
            return all_tracks[0:-1] # not including the last item in the list
        else:
            return all_tracks


    def cut_tracks(self, tracks_dirpath):
        tracks = self.tracks()
        os.makedirs(tracks_dirpath, exist_ok=True)
        for i, track_30s in enumerate(tracks):
            track_name = f"track_{i+1}.mp3"
            track_filepath = os.path.join(tracks_dirpath, track_name)
            # https://pysoundfile.readthedocs.io/en/latest/#soundfile.write
            sf.write(track_filepath, track_30s, samplerate=self.sr)


if __name__ == "__main__":

    CHANNELS_DIRPATH = os.path.join(os.path.dirname(__file__), "..", "content", "youtube")
    channel_names = [fname for fname in os.listdir(CHANNELS_DIRPATH) if fname not in [".DS_Store"]]
    channel_name = channel_names[0]
    print("CHANNEL:", channel_name.upper())

    channel_dirpath = os.path.join(CHANNELS_DIRPATH, channel_name)
    video_ids = [fname for fname in os.listdir(channel_dirpath) if fname not in [".DS_Store"]]
    video_id = video_ids[0]
    print("VIDEO:", video_id)

    video_dirpath = os.path.join(channel_dirpath, video_id)
    audio_filenames = [fname for fname in os.listdir(video_dirpath) if fname.endswith(".mp4")]
    audio_filename = audio_filenames[0]
    audio_filepath = os.path.join(video_dirpath, audio_filename)

    af = AudioFeatures(audio_filepath)
    print(af.audio_filename)

    #print("GENERATING MFCCs...")
    #the_mfcc = af.mfcc()
    #print(the_mfcc.shape)

    print("CUTTING TRACKS...")
    #sf.available_subtypes("MP3")
    #sf.available_formats()

    tracks_dirpath = os.path.join(video_dirpath, "tracks")
    af.cut_tracks(tracks_dirpath)
    print(os.listdir(tracks_dirpath))


    breakpoint()


    track30 = tracks[0]
    len(track30)

    video_mfcc = ytp.mfcc()
    print(type(video_mfcc), video_mfcc.shape)

    track_array = np.array(track30)
    isinstance(track_array, np.ndarray)

    #np.array(track30) or "five"

    track_mfcc = ytp.mfcc(audio_data=np.array(track30))

    print(type(track_mfcc), track_mfcc.shape)

    track_mfcc.shape[0]
