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
