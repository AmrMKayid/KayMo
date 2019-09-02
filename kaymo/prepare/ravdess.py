import os
import shutil
from collections import defaultdict, Counter

from kaymo import ROOTDIR

KAYMODB_PATH = f'{ROOTDIR}/datasets/kaymodb/'


def prepare_ravdess():
    ravdess_path = f'{ROOTDIR}/datasets/ravdess'
    wav_songs_data_path = f'{ravdess_path}/songs'
    wav_speech_data_path = f'{ravdess_path}/speech'

    EMOTIONS = {
        '01': 'neutral',
        '02': 'calm',  # New
        '03': 'happy',
        '04': 'sad',
        '05': 'angry',
        '06': 'fearful',
        '07': 'disgust',
        '08': 'surprised'  # New
    }
    emotion_count = Counter(EMOTIONS.values())
    print(emotion_count)

    # ravdees(wav_songs_data_path, EMOTIONS)
    wav_data = os.listdir(wav_songs_data_path)

    wav_file_path = []

    for folder in wav_data:
        if not folder.startswith('Actor'):
            continue

        actor_path = f'{wav_songs_data_path}/{folder}/'
        # print(actor_path)
        actor = os.listdir(actor_path)
        # print('###########################################', actor, len(actor))
        for wav_file in actor:
            if not wav_file.endswith('wav'):
                continue
            wav_info, ext = wav_file.split('.')
            emotion = wav_info.split('-')[2]
            # print(EMOTIONS[emotion])

            emotion_path = KAYMODB_PATH + EMOTIONS[emotion]
            # print(emotion_path)
            os.makedirs(emotion_path, exist_ok=True)

            # print(actor_path + wav_file,
            #       emotion_path + f'/01_1_ravdees_songs__{EMOTIONS[emotion]}_{emotion_count[EMOTIONS[emotion]]}.wav')
            shutil.copy(actor_path + wav_file,
                        emotion_path + f'/01-1-songs_ravdees_{EMOTIONS[emotion]}_{emotion_count[EMOTIONS[emotion]]}.wav')
            emotion_count[EMOTIONS[emotion]] += 1

    print(emotion_count)

    # ravdees(wav_speech_data_path, EMOTIONS)
    emotion_count = Counter(EMOTIONS.values())
    print(emotion_count)

    wav_data = os.listdir(wav_speech_data_path)

    wav_file_path = []

    for folder in wav_data:
        if not folder.startswith('Actor'):
            continue

        actor_path = f'{wav_speech_data_path}/{folder}/'
        # print(actor_path)
        actor = os.listdir(actor_path)
        # print('###########################################', actor, len(actor))
        for wav_file in actor:
            if not wav_file.endswith('wav'):
                continue
            wav_info, ext = wav_file.split('.')
            emotion = wav_info.split('-')[2]
            # print(EMOTIONS[emotion])

            emotion_path = KAYMODB_PATH + EMOTIONS[emotion]
            # print(emotion_path)
            os.makedirs(emotion_path, exist_ok=True)

            # print(actor_path + wav_file,
            #       emotion_path + f'/01_2_ravdees_speech__{EMOTIONS[emotion]}_{emotion_count[EMOTIONS[emotion]]}.wav')
            shutil.copy(actor_path + wav_file,
                        emotion_path + f'/01-2-speech_ravdees_{EMOTIONS[emotion]}_{emotion_count[EMOTIONS[emotion]]}.wav')
            emotion_count[EMOTIONS[emotion]] += 1

    print(emotion_count)


if __name__ == '__main__':
    prepare_ravdess()
