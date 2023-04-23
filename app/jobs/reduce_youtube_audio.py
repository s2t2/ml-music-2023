




from app.youtube_dataset import YoutubeDataset
from app.audio_processor import AudioProcessor



if __name__ == "__main__":

    ds = YoutubeDataset()
    audio_filepath = ds.take_audio_filepath()

    ap = AudioProcessor(audio_filepath)

    mfcc = ap.mfcc_df()
