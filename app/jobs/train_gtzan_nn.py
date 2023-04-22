
# https://www.youtube.com/watch?v=_xcFAiufwd0
# https://github.com/musikalkemist/DeepLearningForAudioWithPython/blob/master/13-%20Implementing%20a%20neural%20network%20for%20music%20genre%20classification/code/mlp_genre_classifier.py


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
#from tensorflow.keras.callbacks import EarlyStopping

import plotly.express as px

from app import GTZAN_DIRPATH


N_MFCC = int(os.getenv("N_MFCC", default=13))

VAL_SIZE = float(os.getenv("VAL_SIZE", default=0.15))
TEST_SIZE = float(os.getenv("TEST_SIZE", default=0.10))

# TODO: customize LAYER_SIZES "512,256,64"
# os.getenv("N_EPOCHS", default=50))
N_EPOCHS = int(os.getenv("N_EPOCHS", default=50))
LAMBDA = float(os.getenv("LAMBDA", default=0.001))
DROPOUT_RATE = float(os.getenv("DROPOUT_RATE", default=0.15))
LEARNING_RATE = float(os.getenv("LEARNING_RATE", default=0.0001))



def load_gtzan_mfcc(n_mfcc=N_MFCC, encode_labels=True):

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


def train_model(x, y, val_size=VAL_SIZE, test_size=TEST_SIZE,
                layer_sizes=[512, 256, 64],
                l2_lambda=LAMBDA, dropout_rate=DROPOUT_RATE,
                learning_rate=LEARNING_RATE, n_epochs=N_EPOCHS
    ):

    print("-----------------------")
    print("THREE WAY SPLIT...")
    # roll your own three way split, get the ratios right first, remaining goes into training set size
    n_samples = len(x)
    val_size = int(n_samples * val_size)
    test_size = int(n_samples * test_size)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=99)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=val_size, random_state=99)
    print("X TRAIN:", x_train.shape)
    print("Y TRAIN:", y_train.shape)
    print("X VAL:", x_val.shape)
    print("Y VAL:", y_val.shape)
    print("X TEST:", x_test.shape)
    print("Y TEST:", y_test.shape)


    print("-----------------------")
    print("MODEL ARCHITECTURE...")
    # x shape is (n_tracks, 1292, 20), so we are specifying the shape of the individual mfcc features:
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
        #callbacks=[EarlyStopping(monitor="loss", patience=10)]
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

    title = f"""GTZAN Genre Classifier - Neural Net (30s tracks, {N_MFCC} MFCCs)
        <br><sup>Splits: val_size={val_size}, test_size={test_size}</sup>
        <br><sup>Params: dropout_rate={dropout_rate}, l2_lambda={l2_lambda}, learning_rate={learning_rate}</sup>
        <br><sup>Test Accy: {test_accy}</sup>
    """
    fig = px.line(history_df, x="epoch", y=["train_accy", "val_accy"], title=title)
    fig.show()



if __name__ == "__main__":

    x, y = load_gtzan_mfcc()

    train_model(x, y)
