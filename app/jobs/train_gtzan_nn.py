
# https://www.youtube.com/watch?v=_xcFAiufwd0
# https://github.com/musikalkemist/DeepLearningForAudioWithPython/blob/master/13-%20Implementing%20a%20neural%20network%20for%20music%20genre%20classification/code/mlp_genre_classifier.py


import os
import json

import numpy as np
from pandas import DataFrame, Series
from sklearn.model_selection import train_test_split
from category_encoders import OneHotEncoder #, OrdinalEncoder

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

from app import GTZAN_DIRPATH

N_MFCC = int(os.getenv("N_MFCC", default=20))
N_EPOCHS = int(os.getenv("N_EPOCHS", default=50))



def load_gtzan_mfcc(n_mfcc, encode_labels=True):

    print("LOADING DATA...")
    json_filepath = os.path.join(GTZAN_DIRPATH, f"mfcc_{n_mfcc}.json")
    print(os.path.abspath(json_filepath))
    with open(json_filepath, "r") as json_file:
        data = json.load(json_file)

    #> {"genre": "pop", "audio_filename": "pop.00000.wav", "mfcc": [[], [], []]},
    #> {"genre": "pop", "audio_filename": "pop.00001.wav", "mfcc": [[], [], []]},
    #> {"genre": "pop", "audio_filename": "pop.00002.wav", "mfcc": [[], [], []]},

    print("PROCESSING DATA...")
    x, y = [], []
    for record in data:
        x.append(record["mfcc"])
        y.append(record["genre"])
    x, y = np.array(x), np.array(y)
    print("X:", x.shape) #> (989, 1292, 20)
    print("Y:", y.shape) #> (989,)

    if encode_labels:
        print("ENCODING LABELS...")
        y = Series(y, name="genre")
        encoder = OneHotEncoder(handle_unknown="error", use_cat_names=True, return_df=True)
        y_encoded = encoder.fit_transform(y)
        #print(encoder.feature_names_out_) #> ['genre_pop', 'genre_metal', 'genre_disco', 'genre_blues', 'genre_reggae', 'genre_classical', 'genre_rock', 'genre_hiphop', 'genre_country', 'genre_jazz']
        print("Y:", y_encoded.shape)
        print(y_encoded.head())
        y = y_encoded

    return x, y



#def train_model(x_train, y_train, x_val, y_val, x_test, y_test, n_epochs=10, learning_rate=0.0001):
#    """Train using three way split """
#
#    # Define the model
#    model = Sequential([
#        Dense(64, activation="relu", input_shape=(x_train.shape[1],)),
#        Dense(32, activation="relu"),
#        Dense(10, activation="softmax")
#    ])
#
#    # Compile the model
#    # model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#    optimizer = Adam(learning_rate=learning_rate)
#    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
#
#    # Train the model
#    history = model.fit(x_train, y_train, epochs=n_epochs, validation_data=(x_val, y_val))
#
#    # Evaluate the model on the test set
#    test_err, test_acc = model.evaluate(x_test, y_test)
#    print("ACCY TEST:", test_acc)
#    print("ERR TEST:", test_err)
#
#    # Return the trained model and the history object
#    return model, history
#


if __name__ == "__main__":

    x, y = load_gtzan_mfcc(n_mfcc=N_MFCC)
    print("-----------------------")
    print("TRAIN TEST SPLIT...")
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=99)
    print("X TRAIN:", x_train.shape)
    print("Y TRAIN:", y_train.shape)
    print("X TEST:", x_test.shape)
    print("Y TEST:", y_test.shape)

    print("-----------------------")
    print("TRAINING NEURAL NETWORK FOR GENRE CLASSIFICATION...")

    model = Sequential([
        # input layer:
        # ... x shape is (n_tracks, 1292, 20), so we are specifying the shape of the individual mfcc features:
        Flatten(input_shape=(x.shape[1], x.shape[2])),
        # dense layers:
        Dense(512, activation="relu"),
        Dense(256, activation="relu"),
        Dense(64, activation="relu"),
        # output layer:
        Dense(10, activation="softmax")
    ])

    # compile model:
    optimizer = Adam(learning_rate=0.0001)
    model.compile(
        optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    model.summary()

    # train model:
    history = model.fit(x_train, y_train, validation_data=(x_test, y_test), batch_size=32, epochs=N_EPOCHS)

    breakpoint()
