
# https://www.youtube.com/watch?v=_xcFAiufwd0

import os
import json

import numpy as np
from pandas import DataFrame
from sklearn.model_selection import train_test_split
#from tensorflow.keras.layers import Sequential, Dense

from app import GTZAN_DIRPATH

N_MFCC = int(os.getenv("N_MFCC", default=20))


if __name__ == "__main__":

    print("LOADING DATA...")
    json_filepath = os.path.join(GTZAN_DIRPATH, f"mfcc_{N_MFCC}.json")
    print(os.path.abspath(json_filepath))
    with open(json_filepath, "r") as json_file:
        data = json.load(json_file)

    #> {"genre": "pop", "audio_filename": "pop.00000.wav", "mfcc": [[], [], []]},
    #> {"genre": "pop", "audio_filename": "pop.00001.wav", "mfcc": [[], [], []]},
    #> {"genre": "pop", "audio_filename": "pop.00002.wav", "mfcc": [[], [], []]},

    #df = DataFrame(data)
    #df["mfcc"] = df["mfcc"].apply(lambda val: np.array(val))
    #x = df["mfcc"]
    #y = df["genre"]

    print("PROCESSING DATA...")
    x, y = [], []
    for record in data:
        x.append(record["mfcc"])
        y.append(record["genre"])
    x, y = np.array(x), np.array(y)
    print("X:", x.shape)
    print("Y:", y.shape)

    print("-----------------------")
    print("TRAIN TEST SPLIT...")
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=99)
    print("X TRAIN:", x_train.shape)
    print("Y TRAIN:", y_train.shape)
    print("X TEST:", x_test.shape)
    print("Y TEST:", y_test.shape)

    print("-----------------------")
    print("TRAINING NEURAL NETWORK FOR GENRE CLASSIFICATION...")
