
import os

from app.gtzan_dataset import GenreDataset
from app.audio_processor import AudioProcessor, TRACK_LENGTH, N_MFCC


N_COMPONENTS = int(os.getenv("N_COMPONENTS", default="3"))



#def pca_pipeline():




if __name__ == "__main__":


    ds = GenreDataset()

    df = ds.read_features_csv(track_length=TRACK_LENGTH, n_mfcc=N_MFCC)

    breakpoint()

    #x_scale = True
    #if x_scale:
    #    x = (x - x.mean()) / x.std()
    #    print("X SCALED - MEAN:", x.mean())
    #    print("X SCALED - STD:", x.std())
