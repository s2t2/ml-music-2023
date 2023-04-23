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

Generate MFCCs from the raw audio files, optionally specifying the track length in seconds (e.g. 3, 30), and the number of MFCCs (FYI provided GTZAN features CSV file is based on 20 MFCCs):

```sh
TRACK_LENGTH=3 N_MFCC=2 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=3 N_MFCC=3 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=3 N_MFCC=8 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=3 N_MFCC=13 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=3 N_MFCC=20 python -m app.jobs.process_gtzan_audio

TRACK_LENGTH=30 N_MFCC=2 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=30 N_MFCC=3 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=30 N_MFCC=8 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=30 N_MFCC=13 python -m app.jobs.process_gtzan_audio
TRACK_LENGTH=30 N_MFCC=20 python -m app.jobs.process_gtzan_audio
```

Train a neural network on this data:

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


Extract all the videos:


```sh
python -m app.jobs.download_youtube_audio
```


Generate MFCCs from the raw audio files, optionally specifying the track length in seconds (e.g. 3, 30), and the number of MFCCs:

```sh
TRACK_LENGTH=3 N_MFCC=2   python -m app.jobs.process_youtube_audio
TRACK_LENGTH=3 N_MFCC=3   python -m app.jobs.process_youtube_audio
TRACK_LENGTH=3 N_MFCC=8   python -m app.jobs.process_youtube_audio
TRACK_LENGTH=3 N_MFCC=13  python -m app.jobs.process_youtube_audio
TRACK_LENGTH=3 N_MFCC=20  python -m app.jobs.process_youtube_audio

TRACK_LENGTH=30 N_MFCC=2  python -m app.jobs.process_youtube_audio
TRACK_LENGTH=30 N_MFCC=3  python -m app.jobs.process_youtube_audio
TRACK_LENGTH=30 N_MFCC=8  python -m app.jobs.process_youtube_audio
TRACK_LENGTH=30 N_MFCC=13 python -m app.jobs.process_youtube_audio
TRACK_LENGTH=30 N_MFCC=20 python -m app.jobs.process_youtube_audio
```


## Testing

```sh
pytest
```
