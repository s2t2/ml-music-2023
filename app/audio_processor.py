
import os
#import json

import numpy as np
from pandas import DataFrame

import librosa
import librosa.feature as lf
import soundfile as sf

import warnings
warnings.filterwarnings("ignore")


TRACK_LENGTH = int(os.getenv("TRACK_LENGTH", default=30)) # in seconds

N_MFCC = int(os.getenv("N_MFCC", default=13))


def split_into_batches(my_list, batch_size=10_000):
    """Splits a list into evenly sized batches"""
    # h/t: https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    for i in range(0, len(my_list), batch_size):
        yield my_list[i : i + batch_size]


class AudioProcessor:

    def __init__(self, audio_filepath):
        self.audio_filepath = audio_filepath

        self.audio_filename = self.audio_filepath.split("/")[-1]

        # EXTRACT AUDIO DATA:
        self.audio, self.sample_rate = librosa.load(self.audio_filepath)
        #self.audio, self.sample_rate = librosa.__audioread_load(self.audio_filepath)

        self._tracks = None
        self._track_names = None

    @property
    def sr(self):
        """shorthand alias for the sample rate"""
        return self.sample_rate

    #
    # AUDIO FEATURES
    #

    def mfcc(self, n_mfcc=N_MFCC, audio_data=None):
        """Params :

            n_mfcc (int) : number of MFCCs

            audio_data (np.array) : the audio signal from librosa.read.
                If no data is specified, uses the entire audio file.
        """
        if not isinstance(audio_data, np.ndarray):
            audio_data = self.audio

        #print(f"MFCC ({n_mfcc})...")
        return lf.mfcc(y=audio_data, sr=self.sr, n_mfcc=n_mfcc)

    def mfcc_df(self, n_mfcc=N_MFCC, audio_data=None):
        the_mfcc = self.mfcc(n_mfcc, audio_data)
        #n_mfcc = the_mfcc.shape[0]
        mfcc_cols = [f"mfcc_{i}" for i in range(1, n_mfcc+1)]
        return DataFrame(the_mfcc.T, columns=mfcc_cols)

    def audio_features(self, n_mfcc=N_MFCC, n_chroma=1, audio_data=None):
        audio_data = audio_data or self.audio

        features = {}

        #
        # SINGLE COLUMN
        #

        features["tempo"] = lf.tempo(y=audio_data, sr=self.sr)[0]

        #
        # MEAN AND VAR COLUMNS
        # ... (the GTZAN dataset summarizes these with a single col for the mean and variance)
        #

        n_chroma=12
        chroma_stft = lf.chroma_stft(y=audio_data, sr=self.sr, n_chroma=n_chroma) # there are n_chroma cols
        features["chroma_stft_mean"] = chroma_stft.mean()
        features["chroma_stft_var"] = chroma_stft.var()

        rms = lf.rms(y=audio_data)
        features["rms_mean"] = rms.mean()
        features["rms_var"] = rms.var()

        spectral_centroid = lf.spectral_centroid(y=audio_data, sr=self.sr)
        features["spectral_centroid_mean"] = spectral_centroid.mean()
        features["spectral_centroid_var"] = spectral_centroid.var()

        spectral_bandwidth = lf.spectral_bandwidth(y=audio_data, sr=self.sr)
        features["spectral_bandwidth_mean"] = spectral_bandwidth.mean()
        features["spectral_bandwidth_var"] = spectral_bandwidth.var()

        spectral_rolloff = lf.spectral_rolloff(y=audio_data, sr=self.sr)
        features["spectral_rolloff_mean"] = spectral_rolloff.mean()
        features["spectral_rolloff_var"] = spectral_rolloff.var()

        zero_crossing = lf.zero_crossing_rate(y=audio_data)
        features["zero_crossing_rate_mean"] = zero_crossing.mean()
        features["zero_crossing_rate_var"] = zero_crossing.var()

        # is this the harmony feature from GTZAN?
        #harmony = librosa.effects.harmonic(audio_data, margin=3.0)
        #features["harmony_mean"] = harmony.mean()
        #features["harmony_var"] = harmony.var()

        # not sure where the perceptr features are

        # new feature not in GTZAN
        tonnetz = lf.tonnetz(y=audio_data, sr=self.sr) # there are six cols
        features["tonnetz_mean"] = tonnetz.mean()
        features["tonnetz_var"] = tonnetz.var()

        #
        # MEAN AND VAR COLUMNS FOR EACH MFCC
        #

        mfcc = lf.mfcc(y=audio_data, sr=self.sr, n_mfcc=n_mfcc)
        #mfcc_mean = np.mean(mfcc, axis=1)
        #mfcc_var = np.var(mfcc, axis=1)
        for i in range(0, n_mfcc):
            features[f"mfcc_{i+1}_mean"] = mfcc[i].mean().tolist()
            features[f"mfcc_{i+1}_var"] = mfcc[i].var().tolist()

        #features = dict(zip(feature_names, feature_vals))
        return features


    #
    # TRACK CUTTING
    #

    def tracks(self, track_length_seconds=TRACK_LENGTH, discard_last=True):
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

    def cut_tracks(self, tracks_dirpath, tracks_params=None):
        tracks = self.tracks(**tracks_params)
        track_names = []
        os.makedirs(tracks_dirpath, exist_ok=True)
        for i, track_30s in enumerate(tracks):
            track_name = f"track_{i+1}.mp3"
            track_filepath = os.path.join(tracks_dirpath, track_name)
            # https://pysoundfile.readthedocs.io/en/latest/#soundfile.write
            sf.write(track_filepath, track_30s, samplerate=self.sr)

            track_names.append(track_name)

        self._tracks, self._track_names = tracks, track_names
        return tracks, track_names

    #
    # SAVE MFCCS
    #

    #def save_json(self, json_filepath, data):
    #    with open(json_filepath, "w") as json_file:
    #        json.dump(data, json_file)


    #def save_mfcc(self, video_dirpath, n_mfcc):
    #    mfcc_dirpath = os.path.join(video_dirpath, f"mfcc_{n_mfcc}")
    #    os.makedirs(mfcc_dirpath, exist_ok=True)
    #
    #    df = self.mfcc_df(n_mfcc=n_mfcc)
    #    csv_filepath = os.path.join(mfcc_dirpath, "full_length.csv")
    #    df.to_csv(csv_filepath)


    #def save_track_mfcc(self, video_dirpath, n_mfcc):
    #    """cut tracks first"""
    #    mfcc_dirpath = os.path.join(video_dirpath, f"mfcc_{n_mfcc}")
    #    os.makedirs(mfcc_dirpath, exist_ok=True)
    #
    #    for track, track_name in zip(self._tracks, self._track_names):
    #        csv_filename = track_name.replace(".mp3", ".csv")
    #
    #        df = self.mfcc_df(n_mfcc=n_mfcc, audio_data=np.array(track))
    #        csv_filepath = os.path.join(mfcc_dirpath, csv_filename)
    #        df.to_csv(csv_filepath)



if __name__ == "__main__":

    pass

    #from conftest import TEST_AUDIO_FILEPATH
#
    #ap = AudioProcessor(TEST_AUDIO_FILEPATH)
#
    #ap.all_audio_features()







    #from app.gtzan_dataset import GTZAN_DIRPATH
    #from app.youtube_dataset import YoutubeDataset
    #
    #print("Let's grab an example audio file to process...")
    #dataset_name = input("Please choose a dataset ('gtzan', 'youtube'): ") or "gtzan"
    #print("DATASET:", dataset_name)
    #if dataset_name == "gtzan":
    #    audio_filepath = os.path.join(GTZAN_DIRPATH, "genres_original", "pop", "pop.00000.wav")
    #elif dataset_name == "youtube":
    #    ds = YoutubeDataset()
    #    artist_name = input("Choose an artist name: ") or None
    #    audio_filepath = ds.take_audio_filepath(artist_name)
    #
    #ap = AudioProcessor(audio_filepath)
    #print("AUDIO:", ap.audio_filename)
    #
    #TRACK_LENGTHS = [3, 10, 30]
    #NUMS_MFCC = [2, 3, 7, 13, 20]
    #
    #for track_length in TRACK_LENGTHS:
    #    print("------------------------")
    #    print(f"TRACKS ({track_length} SECOND)...")
    #
    #    tracks = ap.tracks(track_length_seconds=track_length)
    #    for i, track in enumerate(tracks):
    #        track = np.array(track)
    #        print("TRACK:", i, track.shape)
    #
    #        for n_mfcc in NUMS_MFCC:
    #            mfcc_df = ap.mfcc_df(audio_data=track, n_mfcc=n_mfcc)
    #            print("...", mfcc_df.shape)
    #            #ap.save_track_mfcc(video_dirpath=video_dirpath, n_mfcc=n_mfcc)



    #print("CUTTING TRACKS...")
    #tracks_dirpath = os.path.join(video_dirpath, "tracks")
    #tracks, track_names = af.cut_tracks(tracks_dirpath)
    ##track_names = sorted([fname for fname in os.listdir(tracks_dirpath) if fname.endswith(".mp3")])
    #print(track_names)

    #print("GENERATING MFCCs...")

    #for n_mfcc in [2, 3, 12, 20]:
    #    af.save_track_mfcc(video_dirpath=video_dirpath, n_mfcc=n_mfcc)
