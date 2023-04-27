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

There is a CSV file of provided audio features (based on 20 MFCCs). We can optionally recreate our own (mostly similar) versions of the provided data, specifying different track lengths and number of MFCCs:

```sh
TRACK_LENGTH=3 N_MFCC=8   MAX_THREADS=10 python -m app.jobs.process_gtzan_audio_async
TRACK_LENGTH=3 N_MFCC=13  MAX_THREADS=10 python -m app.jobs.process_gtzan_audio_async
TRACK_LENGTH=3 N_MFCC=20  MAX_THREADS=10 python -m app.jobs.process_gtzan_audio_async

TRACK_LENGTH=30 N_MFCC=8  MAX_THREADS=10 python -m app.jobs.process_gtzan_audio_async
TRACK_LENGTH=30 N_MFCC=13 MAX_THREADS=10 python -m app.jobs.process_gtzan_audio_async
TRACK_LENGTH=30 N_MFCC=20 MAX_THREADS=10 python -m app.jobs.process_gtzan_audio_async
```


Generate raw MFCC data from the raw audio files, optionally specifying the track length in seconds, and the number of MFCCs:

```sh
TRACK_LENGTH=3 N_MFCC=8   python -m app.jobs.process_gtzan_mfcc
TRACK_LENGTH=3 N_MFCC=13  python -m app.jobs.process_gtzan_mfcc
TRACK_LENGTH=3 N_MFCC=20  python -m app.jobs.process_gtzan_mfcc

TRACK_LENGTH=30 N_MFCC=8  python -m app.jobs.process_gtzan_mfcc
TRACK_LENGTH=30 N_MFCC=13 python -m app.jobs.process_gtzan_mfcc
TRACK_LENGTH=30 N_MFCC=20 python -m app.jobs.process_gtzan_mfcc
```

Train a neural network genre classifier on the raw MFCC data:

```sh
TRACK_LENGTH=3 N_MFCC=13 python -m app.jobs.train_gtzan_nn
TRACK_LENGTH=30 N_MFCC=13 python -m app.jobs.train_gtzan_nn
```







### YouTube

Test the YouTube service on one video:

```sh
VIDEO_URL="________" python -m app.youtube_video_service
```

Download audio files for the specified YouTube video URLs:

```sh
ARTIST_NAME="________" MAX_RETRIES=50 python -m app.jobs.download_youtube_audio
```


Generate audio features data from the raw audio files, specifying the track length in seconds, as well as the number of MFCCs:

```sh
TRACK_LENGTH=3 N_MFCC=8   MAX_THREADS=10 python -m app.jobs.process_youtube_audio_async
TRACK_LENGTH=3 N_MFCC=13  MAX_THREADS=10 python -m app.jobs.process_youtube_audio_async
TRACK_LENGTH=3 N_MFCC=20  MAX_THREADS=10 python -m app.jobs.process_youtube_audio_async

TRACK_LENGTH=30 N_MFCC=8  MAX_THREADS=10 python -m app.jobs.process_youtube_audio_async
TRACK_LENGTH=30 N_MFCC=13 MAX_THREADS=10 python -m app.jobs.process_youtube_audio_async
TRACK_LENGTH=30 N_MFCC=20 MAX_THREADS=10 python -m app.jobs.process_youtube_audio_async
```


Perform dimensionality reduction on the audio features to obtain song embeddings, and plot them in two or three dimensions:

```sh
python -m app.jobs.reduce_youtube_features
```



## Testing

```sh
pytest
```
