import os
from tqdm import tqdm

import librosa

from kaymo import ROOTDIR
import pandas as pd

KAYMODB_PATH = f'{ROOTDIR}/datasets/kaymodb/'


def create_kaymodb_csv():
    df = {'dataset': [], 'filename': [], 'emotion': [], 'length': [], 'path': []}
    emotions = os.listdir(KAYMODB_PATH)
    print(emotions)
    for emotion in emotions:
        wav_files = os.listdir(f'{KAYMODB_PATH}{emotion}')
        print('Emotion: ', emotion)
        for wav in tqdm(wav_files):
            wav_info = wav.split('_')
            dataset, emotion, path = wav_info[1], wav_info[2], f'{KAYMODB_PATH}{emotion}/{wav}'
            # print(dataset, emotion, path)
            df['dataset'].append(dataset)
            df['filename'].append(wav)
            df['emotion'].append(emotion)
            y, sr = librosa.load(f'{KAYMODB_PATH}{emotion}/{wav}')
            df['length'].append(y.shape[0] / sr)
            df['path'].append(path)

    df = pd.DataFrame(df)
    print(df.head())
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_csv(f'{ROOTDIR}/kaymodb.csv', index=None, header=True)


if __name__ == '__main__':
    create_kaymodb_csv()
