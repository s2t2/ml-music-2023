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

> FYI provided GTZAN features CSV file is based on 20 MFCCs

#### Summary Features

There is a CSV file of provided audio features. This data can be used for normal machine learning models. We can optionally recreate our own (mostly similar) versions of the provided data, specifying different track lengths and number of MFCCs:

```sh
TRACK_LENGTH=3 N_MFCC=8   MAX_THREADS=10 python -m app.jobs.process_gtzan_features_async
TRACK_LENGTH=3 N_MFCC=13  MAX_THREADS=10 python -m app.jobs.process_gtzan_features_async
TRACK_LENGTH=3 N_MFCC=20  MAX_THREADS=10 python -m app.jobs.process_gtzan_features_async

TRACK_LENGTH=30 N_MFCC=8  MAX_THREADS=10 python -m app.jobs.process_gtzan_features_async
TRACK_LENGTH=30 N_MFCC=13 MAX_THREADS=10 python -m app.jobs.process_gtzan_features_async
TRACK_LENGTH=30 N_MFCC=20 MAX_THREADS=10 python -m app.jobs.process_gtzan_features_async
```


Dimensionality reduction on summary features:

```sh
TRACK_LENGTH=3 N_MFCC=8   N_COMPONENTS=2 python -m app.jobs.reduce_gtzan_features
TRACK_LENGTH=3 N_MFCC=13  N_COMPONENTS=2 python -m app.jobs.reduce_gtzan_features
TRACK_LENGTH=3 N_MFCC=20  N_COMPONENTS=2 python -m app.jobs.reduce_gtzan_features
```



#### Raw MFCC Features

Generate MFCCs from the raw audio files, optionally specifying the track length in seconds, and the number of MFCCs:

```sh
TRACK_LENGTH=3 N_MFCC=8   python -m app.jobs.process_gtzan_mfcc
TRACK_LENGTH=3 N_MFCC=13  python -m app.jobs.process_gtzan_mfcc
TRACK_LENGTH=3 N_MFCC=20  python -m app.jobs.process_gtzan_mfcc

TRACK_LENGTH=30 N_MFCC=8  python -m app.jobs.process_gtzan_mfcc
TRACK_LENGTH=30 N_MFCC=13 python -m app.jobs.process_gtzan_mfcc
TRACK_LENGTH=30 N_MFCC=20 python -m app.jobs.process_gtzan_mfcc
```

Train a neural network on the raw MFCC data:

```sh
TRACK_LENGTH=3 N_MFCC=13 python -m app.jobs.train_gtzan_nn
TRACK_LENGTH=30 N_MFCC=13 python -m app.jobs.train_gtzan_nn
```







### YouTube

Test the YouTube service on one video:

```sh
python -m app.youtube_video_service
# VIDEO_URL="" python -m app.youtube_video_service
```


Download audio file for all the videos:


```sh
python -m app.jobs.download_youtube_audio
```


Generate audio features based on MFCCs from the raw audio files, optionally specifying the track length in seconds (e.g. 3, 30), as well as the number of MFCCs:

```sh
TRACK_LENGTH=3 N_MFCC=2   python -m app.jobs.process_youtube_audio
TRACK_LENGTH=3 N_MFCC=3   python -m app.jobs.process_youtube_audio
TRACK_LENGTH=3 N_MFCC=8   python -m app.jobs.process_youtube_audio
TRACK_LENGTH=3 N_MFCC=10  python -m app.jobs.process_youtube_audio
TRACK_LENGTH=3 N_MFCC=13  python -m app.jobs.process_youtube_audio
TRACK_LENGTH=3 N_MFCC=20  python -m app.jobs.process_youtube_audio

TRACK_LENGTH=30 N_MFCC=2  python -m app.jobs.process_youtube_audio
TRACK_LENGTH=30 N_MFCC=3  python -m app.jobs.process_youtube_audio
TRACK_LENGTH=30 N_MFCC=8  python -m app.jobs.process_youtube_audio
TRACK_LENGTH=30 N_MFCC=10 python -m app.jobs.process_youtube_audio
TRACK_LENGTH=30 N_MFCC=13 python -m app.jobs.process_youtube_audio
TRACK_LENGTH=30 N_MFCC=20 python -m app.jobs.process_youtube_audio
```

Use GTZAN classifier to classify the genre of these these audio features:

```sh
TRACK_LENGTH=30 N_MFCC=20 python -m app.jobs.classify_youtube_audio
```


Analyze the similarity of the audio features:

```sh
TRACK_LENGTH=30 N_MFCC=20 python -m app.jobs.reduce_youtube_audio
```


Cluster the audio features, by artist:

```sh
TRACK_LENGTH=30 N_MFCC=20 python -m app.jobs.cluster_youtube_audio
```

## Testing

```sh
pytest
```
