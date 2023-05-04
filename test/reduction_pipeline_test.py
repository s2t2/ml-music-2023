


from pandas import read_csv
from pytest import fixture


from app.reduction_pipeline import ReductionPipeline, PCATuner


TRACK_LENGTH = 30
N_MFCC = 13

@fixture
def audio_features_df():
    csv_filepath = f"https://github.com/s2t2/ml-music-2023/raw/main/data/youtube/features_v1/length_{TRACK_LENGTH}_mfcc_{N_MFCC}_features.csv"
    return read_csv(csv_filepath)


def verify_embeddings(pipeline):
    embeddings = pipeline.embeddings
    assert embeddings.shape == (1818, 2)
    embeddings_df = pipeline.embeddings_df
    assert embeddings_df.columns.tolist() == ['component_1', 'component_2', 'artist_name', 'video_id', 'audio_filename', 'track_number', 'track_length']



def test_pca_pipeline(audio_features_df):
    feature_names = ['tempo', 'chroma_stft_mean', 'chroma_stft_var', 'rms_mean', 'rms_var', 'spectral_centroid_mean', 'spectral_centroid_var', 'spectral_bandwidth_mean', 'spectral_bandwidth_var', 'spectral_rolloff_mean', 'spectral_rolloff_var', 'zero_crossing_rate_mean', 'zero_crossing_rate_var', 'tonnetz_mean', 'tonnetz_var', 'mfcc_1_mean', 'mfcc_1_var', 'mfcc_2_mean', 'mfcc_2_var', 'mfcc_3_mean', 'mfcc_3_var', 'mfcc_4_mean', 'mfcc_4_var', 'mfcc_5_mean', 'mfcc_5_var', 'mfcc_6_mean', 'mfcc_6_var', 'mfcc_7_mean', 'mfcc_7_var', 'mfcc_8_mean', 'mfcc_8_var', 'mfcc_9_mean', 'mfcc_9_var', 'mfcc_10_mean', 'mfcc_10_var', 'mfcc_11_mean', 'mfcc_11_var', 'mfcc_12_mean', 'mfcc_12_var', 'mfcc_13_mean', 'mfcc_13_var']

    pipeline = ReductionPipeline(audio_features_df,
        track_length=TRACK_LENGTH, n_mfcc=N_MFCC,
        reducer_type="PCA", n_components=2,
    )
    pipeline.perform()
    verify_embeddings(pipeline)

    pca = pipeline.reducer
    assert pca.explained_variance_.tolist() == [8.980046729035566, 7.014918995282904]
    assert pca.explained_variance_ratio_.tolist() == [0.21890505388738124, 0.17100147326771628]
    assert pca.singular_values_.tolist() == [127.73701463028492, 112.89866170344553]
    assert pca.feature_names_in_.tolist() == feature_names

    loadings = pipeline.loadings
    assert loadings.shape == (41, 2)
    assert loadings.min() > -1
    assert loadings.max() < 1
    loadings_df = pipeline.loadings_df
    assert loadings_df.columns.tolist() == ["component_1", "component_2"]
    assert loadings_df.index.tolist() == feature_names

    # these represent the absolute magnitude of importances, not direction up or down
    feature_importances = pipeline.feature_importances
    assert feature_importances["component_1"] == {
        'mfcc_8_var': 0.805443354102087,
        'mfcc_7_var': 0.7973620573318918,
        'mfcc_6_var': 0.79285956726038,
        'mfcc_9_var': 0.7860296338757697,
        'mfcc_10_var': 0.7663541218866315,
        'mfcc_4_var': 0.756703823949484,
        'mfcc_5_var': 0.7230504963967018,
        'spectral_centroid_var': 0.7110909325450872,
        'mfcc_11_var': 0.6849105101981539,
        'mfcc_2_var': 0.6737980228824214
    }
    assert feature_importances["component_2"] == {
        'spectral_bandwidth_mean': 0.8539164806642479,
        'spectral_rolloff_mean': 0.8464210286829734,
        'spectral_centroid_mean': 0.8184160145817183,
        'mfcc_2_mean': 0.8120671323088787,
        'chroma_stft_mean': 0.743604778175382,
        'mfcc_1_mean': 0.6886499046288507,
        'tonnetz_var': 0.642432984513275,
        'mfcc_8_mean': 0.5722250679251756,
        'mfcc_10_mean': 0.5581507671324493,
        'zero_crossing_rate_mean': 0.5227770916583789
    }


def test_tsne_pipeline(audio_features_df):
    pipeline = ReductionPipeline(audio_features_df,
        track_length=TRACK_LENGTH, n_mfcc=N_MFCC,
        reducer_type="T-SNE", n_components=2
    )
    pipeline.perform()
    verify_embeddings(pipeline)


def test_umap_pipeline(audio_features_df):
    pipeline = ReductionPipeline(audio_features_df,
        track_length=TRACK_LENGTH, n_mfcc=N_MFCC,
        reducer_type="UMAP", n_components=2,
    )
    pipeline.perform()
    verify_embeddings(pipeline)






def test_pca_tuner(audio_features_df):

    tuner = PCATuner(audio_features_df, track_length=TRACK_LENGTH, n_mfcc=N_MFCC)

    assert "perform" in dir(tuner)
    assert "plot_explained_variance" in dir(tuner)
    assert "plot_scree" in dir(tuner)
