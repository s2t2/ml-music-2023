
# https://www.youtube.com/watch?v=_xcFAiufwd0
# https://github.com/musikalkemist/DeepLearningForAudioWithPython/blob/master/13-%20Implementing%20a%20neural%20network%20for%20music%20genre%20classification/code/mlp_genre_classifier.py

# todo: tuning
# https://www.tensorflow.org/tensorboard/hyperparameter_tuning_with_hparams

import os
import json

import numpy as np
from pandas import DataFrame, Series
from sklearn.model_selection import train_test_split
from category_encoders import OneHotEncoder #, OrdinalEncoder

#import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping

import plotly.express as px

from app.gtzan_dataset import GTZAN_DIRPATH
from app.audio_processor import TRACK_LENGTH, N_MFCC


VAL_SIZE = float(os.getenv("VAL_SIZE", default=0.15))
TEST_SIZE = float(os.getenv("TEST_SIZE", default=0.10))

# LAYER_SIZES = [int(n) for n in os.getenv("LAYER_SIZES", default="512,256,64").split(",") ]
N_EPOCHS = int(os.getenv("N_EPOCHS", default=150))
LAMBDA = float(os.getenv("LAMBDA", default=0.001))
DROPOUT_RATE = float(os.getenv("DROPOUT_RATE", default=0.15))
LEARNING_RATE = float(os.getenv("LEARNING_RATE", default=0.0001))
PATIENCE = int(os.getenv("PATIENCE", default=10))



def load_gtzan_mfcc(track_length=TRACK_LENGTH, n_mfcc=N_MFCC, encode_labels=True):

    print("LOADING DATA...")
    json_filepath = os.path.join(GTZAN_DIRPATH, f"features_{track_length}s", f"mfcc_{n_mfcc}.json")
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


def train_model(x, y, x_scale=True, val_size=VAL_SIZE, test_size=TEST_SIZE,
                layer_sizes=[512, 256, 64],
                l2_lambda=LAMBDA, dropout_rate=DROPOUT_RATE,
                learning_rate=LEARNING_RATE, n_epochs=N_EPOCHS, patience=PATIENCE
    ):
    """
        Params:

            x (np.array) : training features, with shape like (n_tracks, track_length, n_mfcc)

            y (np.array) : training labels

            l2_lambda (float) : L2 regularization penalty, keras default is 0.01
                        https://www.tensorflow.org/api_docs/python/tf/keras/regularizers/L2#arguments

            learning_rate (float) : Adam learning rate, keras default is 0.001
                        https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam

            dropout_rate (float) :  Float between 0 and 1. Fraction of the input units to drop.
                        https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dropout

            n_epochs (int) : Number of epochs for training.

            patience (int) : Number of epochs to wait before early stopping, if better performance is not achieved.

    """

    if x_scale:
        print("-----------------------")
        print("FEATURE SCALING...")
        # x shape is like (n_tracks, track_length, n_mfcc)
        x = (x - x.mean()) / x.std()
        print("X SCALED - MEAN:", x.mean())
        print("X SCALED - VAR:", x.var())
        print("X SCALED - STD:", x.std())


    print("-----------------------")
    print("THREE WAY SPLIT...")
    # get the ratios right first, remaining goes into training set size
    n_samples = len(x)
    _val_size = int(n_samples * val_size)
    _test_size = int(n_samples * test_size)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=_test_size, shuffle=True, random_state=99)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=_val_size, shuffle=True, random_state=99)
    print("X TRAIN:", x_train.shape)
    print("Y TRAIN:", y_train.shape)
    print("X VAL:", x_val.shape)
    print("Y VAL:", y_val.shape)
    print("X TEST:", x_test.shape)
    print("Y TEST:", y_test.shape)


    print("-----------------------")
    print("MODEL ARCHITECTURE...")
    # x shape is like (n_tracks, track_length, n_mfcc), so we are specifying the shape of the individual mfcc features:
    input_layer = Flatten(input_shape=(x.shape[1], x.shape[2]))
    hidden_layers = []
    for n_units in layer_sizes:
       hidden_layers += [
            Dense(n_units, activation="relu", kernel_regularizer=l2(l2_lambda)),
            Dropout(dropout_rate, seed=99)
       ]
    output_layer = Dense(10, activation="softmax")
    layers = [input_layer] + hidden_layers + [output_layer]
    model = Sequential(layers)

    # compile model:
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy", # use with one-hot encoded labels
        metrics=["accuracy"]
    )
    model.summary()


    print("-----------------------")
    print("MODEL TRAINING...")

    history = model.fit(x_train, y_train, batch_size=32, epochs=n_epochs,
        validation_data=(x_val, y_val),
        callbacks=[EarlyStopping(monitor="loss", patience=patience)]
    )


    print("-----------------------")
    print("MODEL EVALUATION...")

    history_df = DataFrame({
        "train_accy": history.history["accuracy"],
        "val_accy": history.history["val_accuracy"]
    })
    history_df["epoch"] = history_df.index + 1

    test_err, test_accy = model.evaluate(x_test, y_test)
    test_accy = round(test_accy, 4)
    print("ACCY (TEST):", test_accy)

    title = f"""GTZAN Genre Classifier - Neural Net ({TRACK_LENGTH}s tracks, {N_MFCC} MFCCs)
        <br><sup>Test Accy: {test_accy}</sup>
        <br><sup>Splits: {1 - val_size - test_size} / {val_size} / {test_size} | Params: dropout_rate={dropout_rate}, l2_penalty={l2_lambda}, learning_rate={learning_rate}, patience={patience}</sup>
    """

    fig = px.line(history_df, x="epoch", y=["train_accy", "val_accy"], title=title)
    fig.show()



if __name__ == "__main__":

    x, y = load_gtzan_mfcc()

    train_model(x, y)
