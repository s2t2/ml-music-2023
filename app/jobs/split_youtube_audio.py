
import warnings
warnings.filterwarnings("ignore")


from app.youtube_dataset import YoutubeDataset #, AudioFile as YoutubeAudioFile

from app.audio_processor import TRACK_LENGTH
from app.audio_splitter import AudioSplitter, N_STEMS, STEMS_MAP

import numpy as np
from pandas import DataFrame


if __name__ == "__main__":

    print("-----------")
    ds = YoutubeDataset()
    print(f"YOUTUBE AUDIO FILES ({len(ds.audio_files)})...")
    print(f"ARTISTS ({len(ds.artist_names)}):", sorted(ds.artist_names))

    print("-----------")
    print(f"STEMS ({N_STEMS}):", STEMS_MAP[N_STEMS])

    results = []
    for audio_file in ds.audio_files[0:1]:
        print(audio_file.audio_filename)

        ap = AudioSplitter(audio_file.audio_filepath)
        tracks = ap.tracks(track_length_seconds=TRACK_LENGTH)
        for i, track in enumerate(tracks):
            track = np.array(track)
            print("TRACK", i, track.shape)

            #mfcc = ap.mfcc(n_mfcc=N_MFCC, audio_data=track)
            #mfcc = mfcc.T
            ##print(audio_filename, track.shape, mfcc.shape)

            result = {
                "audio_filename": audio_file.audio_filename,
                "track_number": i+1,
                "track_length": len(track),
                #"mfcc_rows": mfcc.shape[0], # related to the track length
                #"mfcc_cols": mfcc.shape[1], # should equal n_mfcc
                #"mfcc": mfcc,
            }

            print("SPLITTING...")
            splits = ap.split(n_stems=N_STEMS, audio_data=track)
            for stem_name, stem_vals in splits.items():
                # https://github.com/deezer/spleeter/issues/849
                # https://github.com/deezer/spleeter/wiki/4.-API-Reference#raw-waveform-based-separation
                # each stem has two columns, which have similar values
                # could take the first or the second, or average
                # to represent each stem as a single column
                result[stem_name] = stem_vals.mean(axis=1)

            results.append(result)






        #vocals_df = DataFrame(results)

        breakpoint()
        #
        # RUNNING INTO ERROR:
        #
        # self.pid = util.spawnv_passfds(spawn.get_executable(),
        # File "/opt/anaconda3/envs/ml-music/lib/python3.10/multiprocessing/util.py", line 450, in spawnv_passfds
        #     errpipe_read, errpipe_write = os.pipe()
        #
