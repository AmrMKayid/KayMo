import os
import shutil
from collections import defaultdict, Counter

from kaymo import ROOTDIR

KAYMODB_PATH = f'{ROOTDIR}/datasets/kaymodb/'


def prepare_tess():
    tess_path = f'{ROOTDIR}/datasets/tess/'
    wav_data = os.listdir(tess_path)

    EMOTIONS = {
        'angry': 'angry',
        'ps': 'surprised',
        'disgust': 'disgust',
        'fear': 'fearful',
        'happy': 'happy',
        'sad': 'sad',
        'neutral': 'neutral',
    }
    emotion_count = Counter(EMOTIONS.values())
    print(emotion_count)

    for wav_file in wav_data:
        if not wav_file.endswith('wav'):
            continue
        wav_info, ext = wav_file.split('.')
        # print(wav_info)
        _, _, emotion = wav_info.split('_')

        emotion_path = KAYMODB_PATH + EMOTIONS[emotion]
        # print(emotion_path)
        os.makedirs(emotion_path, exist_ok=True)

        # print(tess_path + wav_file,
        #       emotion_path + f'/03_tess_{EMOTIONS[emotion]}_{emotion_count[EMOTIONS[emotion]]}.wav')
        shutil.copy(tess_path + wav_file,
                    emotion_path + f'/03_tess_{EMOTIONS[emotion]}_{emotion_count[EMOTIONS[emotion]]}.wav')
        emotion_count[EMOTIONS[emotion]] += 1

    print(emotion_count)


if __name__ == '__main__':
    prepare_tess()
