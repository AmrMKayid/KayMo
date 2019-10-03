import os

import librosa
import numpy as np
import pandas as pd
from tqdm import tqdm

from kaymo import ROOTDIR

KAYMODB_PATH = f'{ROOTDIR}/datasets/kaymodb/'


def extract_audio_feature(path, mono=True, sr=16000):
    y, sr = librosa.load(path, mono=mono, sr=sr)
    length = y.shape[0] / sr
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    features = f'{np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} ' \
        f'{np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
    for e in mfcc:
        features += f' {np.mean(e)}'
    return features, length


def create_kaymodb_csv(mono=True, sr=16000):
    df = {'dataset': [], 'filename': [], 'emotion': [], 'length': [], 'path': [], 'features': []}
    emotions = os.listdir(KAYMODB_PATH)
    emotions.remove('.DS_Store')
    print(emotions)
    for emotion in emotions:
        wav_files = os.listdir(f'{KAYMODB_PATH}{emotion}')
        print(f'\nEmotion: {emotion}\n')
        for wav in tqdm(wav_files):
            wav_info = wav.split('_')
            dataset, emotion, path = wav_info[1], wav_info[2], f'{KAYMODB_PATH}{emotion}/{wav}'
            # print(dataset, emotion, path)
            df['dataset'].append(dataset)
            df['filename'].append(wav)
            df['emotion'].append(emotion)
            df['path'].append(path)
            features, length = extract_audio_feature(path)
            df['length'].append(length)
            df['features'].append(features.split())


    df = pd.DataFrame(df)
    df = df.sample(frac=1).reset_index(drop=True)
    features = df['features'].apply(pd.Series)  # expand df.features into its own dataframe
    features = features.rename(columns=lambda x: 'features_' + str(x))  # rename each variable is tags
    # print(features)
    df = pd.concat([df[:], features[:]], axis=1)  # join the features dataframe back to the original dataframe
    df.drop(columns=['features'], axis=1, inplace=True)
    print(df.head())
    df.to_csv(f'{ROOTDIR}/kaymodb.csv', index=None, header=True)


if __name__ == '__main__':
    create_kaymodb_csv()
