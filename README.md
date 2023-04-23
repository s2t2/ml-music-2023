# ml-music

Machine Learning for Music


## Setup

```sh
conda create -n ml-music python=3.10
conda activate
```

```sh
pip install -r requirements.txt
```

## Datasets

### GTZAN

Download the ["gtzan-dataset-music-genre-classification" dataset](https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification) from Kaggle. Unzip, as necessary. Rename the unzipped folder as "gtzan" and move it into the "data" directory.

Generate MFCCs from the raw audio files, optionally specifying the track length in seconds (e.g. 3, 30), and the number of MFCCs (uses 20 by default, to match provided GTZAN CSV file):

```sh
TRACK_LENGTH=3 N_MFCC=2 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=3 N_MFCC=3 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=3 N_MFCC=13 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=3 N_MFCC=20 python -m app.jobs.process_gtzan_audio

TRACK_LENGTH=30 N_MFCC=2 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=30 N_MFCC=3 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=30 N_MFCC=13 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=30 N_MFCC=20 python -m app.jobs.process_gtzan_audio
```

This will create a corresponding JSON file in the "gtzan" directory, with a record per track, and the mfcc dimensions for each track will be 1292 rows by N_MFCC cols:


```json
[
  {"genre": "pop", "audio_filename": "pop.00000.wav", "mfcc": [[], [], []]},
  {"genre": "pop", "audio_filename": "pop.00001.wav", "mfcc": [[], [], []]},
  {"genre": "pop", "audio_filename": "pop.00002.wav", "mfcc": [[], [], []]},
  // ...
]
```

Train a neural network on this data:

```sh
TRACK_LENGTH=3 N_MFCC=13 python -m app.jobs.train_gtzan_nn
```

### YouTube

```sh
python -m app.youtube_video_service
```

## Generic Utilities

## Testing

```sh
pytest
```
