import warnings
from pathlib import Path, PosixPath

import numpy as np
import torch
import torchaudio
from IPython.core.display import display
from IPython.lib.display import Audio
from fastai.data_block import ItemBase
from fastai.vision import Image


class AudioItem(ItemBase):

    def __init__(self, data_signal=None, sample_rate=None, path=None, start=None, end=None, spectro=None,
                 max_to_pad=None):

        if isinstance(data_signal, np.ndarray):
            data_signal = torch.from_numpy(data_signal)

        if data_signal is not None:
            if len(data_signal.shape) == 1:
                data_signal = data_signal.unsqueeze(0)

            if data_signal is not None and len(data_signal.shape) > 1 and data_signal.shape[0] > 1:
                warnings.warn(
                    f'''Audio file {path} has {data_signal.shape[0]} channels, 
                    Need to change to mono''')

        self._data_signal, self._sample_rate, self.path = data_signal, sample_rate, path
        self.max_to_pad, self.spectro = max_to_pad, spectro
        self.start, self.end = start, end

    @classmethod
    def open(self, item, **kwargs):

        if isinstance(item, (Path, PosixPath, str)):
            data_signal, sample_rate = torchaudio.load(item)
            return AudioItem(data_signal=data_signal, sample_rate=sample_rate, path=Path(item))
        if isinstance(item, (tuple, np.ndarray)):
            return AudioItem(item)

    def __str__(self):
        return f'{self.__class__.__name__}: ' \
            f'{round(self.duration, 2)} seconds ({self.data_signal.shape[0]} samples @ {self.sample_rate}hz)'

    def __len__(self):
        return self.data.shape[0]

    def _repr_html_(self):
        return f'{self.__str__()}<br />{self.ipy_audio._repr_html_()}'

    def reconstruct(self, t):
        return AudioItem(spectro=t)

    def _reload_signal(self):
        data_signal, sample_rate = torchaudio.load(self.path)
        self._sample_rate = sample_rate
        self._data_signal = data_signal

    def show(self, title: [str] = None, **kwargs):
        print(f"File: {self.path}")
        print(f"Total Length: {round(self.duration, 2)} seconds")
        self.hear(title=title)
        for im in self.get_spec_images():
            display(im)
            print(f"Shape: {im.shape[1]}x{im.shape[2]}")

    def get_spec_images(self):
        sg = self.spectro
        if sg is None: return []
        return [Image(s.unsqueeze(0)) for s in sg]

    def hear(self, title=None):
        if title is not None:
            print("Label:", title)

        if self.start is not None or self.end is not None:
            print(f"{round(self.start / self.sr, 2)}s-{round(self.end / self.sr, 2)}s of original clip")
            start = 0 if self.start is None else self.start
            end = len(self.sig) - 1 if self.end is None else self.end
            display(Audio(data=self.data_signal[start:end], rate=self.sample_rate))
        else:
            display(self.ipy_audio)

    def apply_tfms(self, tfms):
        for tfm in tfms:
            self.data = tfm(self.data)
        return self

    @property
    def shape(self):
        return self.data.shape

    @property
    def data_signal(self):
        if not hasattr(self, '_data_signal') or self._data_signal is None:
            self._reload_signal()
        return self._data_signal.squeeze(0)

    @data_signal.setter
    def data_signal(self, data_signal):
        self._data_signal = data_signal

    @property
    def sample_rate(self):
        if not hasattr(self, '_sample_rate') or self._sample_rate is None:
            # Gets metadata from an audio file without loading the signal.
            si, ei = torchaudio.info(str(self.path))
            self._sample_rate = si.rate
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, sample_rate):
        self._sample_rate = sample_rate

    @property
    def ipy_audio(self):
        return Audio(data=self.data_signal, rate=self.sample_rate)

    @property
    def duration(self):
        if self._sample_rate is not None:
            return len(self.data_signal) / self.sample_rate
        else:
            si, ei = torchaudio.info(str(self.path))
            return si.length / si.rate

    @property
    def data(self):
        return self.spectro if self.spectro is not None else self.data_signal

    @data.setter
    def data(self, x):
        if self.spectro is not None:
            self.spectro = x
        else:
            self.data_signal = x
