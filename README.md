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

GTZAN:

  1. Download the ["gtzan-dataset-music-genre-classification" dataset](https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification) from Kaggle. And unzip, as necessary.
  2. Rename the folder as "gtzan" and move it into the "data" directory.


## Usage

Download audio files:

```sh
python -m app.jobs.download_audio
```

Compile audio features:

```sh
python -m app.jobs.process_audio
```

Train and save genre classifier models:

```sh
python -m app.jobs.train_models
```
