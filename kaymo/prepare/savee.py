import os
import shutil
from collections import defaultdict, Counter

from kaymo import ROOTDIR

KAYMODB_PATH = f'{ROOTDIR}/datasets/kaymodb/'


def prepare_savee():
    savee_path = f'{ROOTDIR}/datasets/savee/'
    wav_data = os.listdir(savee_path)

    EMOTIONS = {
        'a': 'angry',
        'd': 'disgust',
        'f': 'fearful',
        'h': 'happy',
        'n': 'neutral',
        'sa': 'sad',
        'su': 'surprised'
    }
    emotion_count = Counter(EMOTIONS.values())
    print(emotion_count)

    for folder in wav_data:
        if not folder.startswith('Actor'):
            continue

        actor_path = f'{savee_path}{folder}'
        actor = os.listdir(actor_path)
        # print('###########################################', len(actor))
        for wav_file in actor:
            if not wav_file.endswith('wav'):
                continue
            wav_info, ext = wav_file.split('.')
            emotion = wav_info[:2]
            if not emotion.startswith('s'):
                emotion = emotion[0]

            emotion_path = KAYMODB_PATH + EMOTIONS[emotion]
            # print(emotion_path)
            os.makedirs(emotion_path, exist_ok=True)

            # print(actor_path + '/' + wav_file,
            #       emotion_path + f'/02_savee_{EMOTIONS[emotion]}_{emotion_count[EMOTIONS[emotion]]}.wav')
            shutil.copy(actor_path + '/' + wav_file,
                        emotion_path + f'/02_savee_{EMOTIONS[emotion]}_{emotion_count[EMOTIONS[emotion]]}.wav')
            emotion_count[EMOTIONS[emotion]] += 1

    print(emotion_count)


if __name__ == '__main__':
    prepare_savee()
