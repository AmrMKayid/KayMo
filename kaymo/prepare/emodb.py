import os
import shutil
from collections import defaultdict, Counter

from kaymo import ROOTDIR

# PATH = os.path.dirname(os.path.abspath(__file__))
KAYMODB_PATH = f'{ROOTDIR}/datasets/kaymodb/'


def prepare_emodb():
    emodb_path = f'{ROOTDIR}/datasets/emodb/wav/'
    wav_data = os.listdir(emodb_path)

    EMOTIONS = {
        'W': 'angry',
        'L': 'bored',
        'E': 'disgust',
        'A': 'fearful',
        'F': 'happy',
        'T': 'sad',
        'N': 'neutral',
    }
    emotion_count = Counter(EMOTIONS.values())
    print(emotion_count)

    wav_file_path = []

    for wav_file in wav_data:
        if not wav_file.endswith('wav'):
            continue
        wav_info, ext = wav_file.split('.')
        # print(wav_info)
        speaker_num, text, emotion, extra = wav_info[:2], wav_info[2:5], wav_info[5], wav_info[6]
        # print(speaker_num, text, emotion, extra)
        emotion_path = KAYMODB_PATH + EMOTIONS[emotion]
        # print(emotion_path)
        os.makedirs(emotion_path, exist_ok=True)

        # print(emodb_path + wav_file, emotion_path + f'/0_emodb_{EMOTIONS[emotion]}
        # _{emotion_count[EMOTIONS[emotion]]}.wav')
        shutil.copy(emodb_path + wav_file,
                    emotion_path + f'/0_emodb_{EMOTIONS[emotion]}_{emotion_count[EMOTIONS[emotion]]}.wav')
        emotion_count[EMOTIONS[emotion]] += 1

    print(emotion_count)


if __name__ == '__main__':
    prepare_emodb()
