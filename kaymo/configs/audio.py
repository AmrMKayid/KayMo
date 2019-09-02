import os
import warnings
from pathlib import Path
from typing import Tuple

from dataclasses import dataclass, asdict
from fastprogress import progress_bar


@dataclass
class SpectrogramConfig:
    r"""
    Configuration for how Spectrograms are generated
    """
    n_fft: int = 2560  # Size of FFT, creates n_fft // 2 + 1 bins
    win_length: int = None  # Window size. (Default: n_fft)
    hop_length: int = 256  # Length of hop between STFT windows. ( Default: win_length // 2)
    pad: int = 0  # Two sided padding of signal. (Default: 0)

    f_min: int = 0  # Minimum frequency. (Default: 0.)
    f_max: int = 22050  # Maximum frequency. (Default: None)
    n_mels: int = 128  # Number of mel filterbanks. (Default: 128)
    to_db_scale: bool = True
    top_db: int = 100
    n_mfcc: int = 20

    # ws: int = None

    def mel_cfgs(self):
        return {k: v for k, v in asdict(self).items() if k in ["f_min", "f_max", "hop_length", "n_fft",
                                                               "n_mels", "pad", "win_length"]}


@dataclass
class AudioConfig:
    r"""
    Options for pre-processing audio signals
    """
    cache: bool = True
    cache_dir = Path('.cache')
    force_cache = False

    duration: int = None
    max_to_pad: float = None
    pad_mode: str = "zeros"
    remove_silence: str = None
    use_spectro: bool = True
    mfcc: bool = False

    delta: bool = False
    silence_padding: int = 200
    silence_threshold: int = 20
    segment_size: int = None
    resample_to: int = None
    standardize: bool = False
    downmix: bool = False
    _processed = False
    _sample_rate = None
    sg_cfg: SpectrogramConfig = SpectrogramConfig()

    def __setattr__(self, key, value):
        r"""
        Override to warn user if they are mixing seconds and ms
        :param key:
        :param value:
        :return:
        """
        if key in 'duration max_to_pad segment_size'.split():
            if value is not None and value <= 30:
                warnings.warn(f"{key} should be in milliseconds, "
                              f"it looks like you might be trying to use seconds")

        self.__dict__[key] = value

    def clear_cache(self):
        r"""
        Delete the files and empty dirs in the cache folder
        :return:
        """
        num_removed = 0
        parent_dirs = set()
        if not os.path.exists(self.cache_dir / "cache_contents.txt"):
            print("Cache contents not found, try calling again after creating your AudioList")

        with open(self.cache_dir / "cache_contents.txt", 'r') as f:
            pb = progress_bar(f.read().split('\n')[:-1])
            for line in pb:
                if not os.path.exists(line):
                    continue
                else:
                    try:
                        os.remove(line)
                    except Exception as e:
                        print(f"Warning: Failed to remove {line}, due to error {str(e)}...continuing")
                    else:
                        parent = Path(line).parents[0]
                        parent_dirs.add(parent)
                        num_removed += 1
        for parent in parent_dirs:
            if os.path.exists(parent) and len(parent.ls()) == 0:
                try:
                    os.rmdir(str(parent))
                except Exception as e:
                    print(f"Warning: Unable to remove empty dir {parent}, due to error {str(e)}...continuing")
        os.remove(self.cache_dir / "cache_contents.txt")
        print(f"{num_removed} files removed")

    def cache_size(self) -> Tuple:
        r"""
        Check cache size
        :return: a tuple of int in bytes, and string representing MB
        """
        cache_size = 0
        if not os.path.exists(self.cache_dir):
            print("Cache not found, try calling again after creating your AudioList")
            return (None, None)
        for (path, dirs, files) in os.walk(self.cache_dir):
            for file in files:
                cache_size += os.path.getsize(os.path.join(path, file))
        return (cache_size, f"{cache_size // (2 ** 20)} MB")
