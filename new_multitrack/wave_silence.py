"""Routines to test the 'emptiness' of a wave file."""

import struct
import wave
import os
import glob

def has_wavs(fpath):
    wav_files = glob.glob(os.path.join(fpath,'*.wav'))
    if len(wav_files) == 0:
        return False
    else:
        return True

def is_right_stats(fpath, type):
    fp = wave.open(fpath, 'rb')
    n_channels = fp.getnchannels()
    bytedepth = fp.getsampwidth()
    fs = fp.getframerate()
    if type == "stem":
        if n_channels == 2 and bytedepth == 2 and fs == 44100:
            return True
        else:
            return False
    elif type == "raw":
        if n_channels == 1 and bytedepth == 2 and fs == 44100:
            return True
        else:
            return False
    else:
        print "Incorrect Type."
        return False

def get_length(fpath):
    fp = wave.open(fpath, 'rb')
    length = fp.getnframes()
    return length

def is_right_length(fpath, ref_length):
    length = get_length(fpath)
    if length == ref_length:
        return True
    else:
        return False

def is_silence(wavefile, threshold=16, framesize=None):
    """Check if a wave file is 'silent', i.e. all values are smaller than a
    given threshold.

    Parameters
    ----------
    wavefile : str
        Path to a wavefile.
    threshold : int
        Value for the upper bound in determining silence.
    framesize : int, default=None
        Number of datapoints to consider at a time, defaults to 1 second.

    Returns
    -------
    status : bool
        True if the file all values are less than the given threshold.
    """
    fp = wave.open(wavefile, 'rb')
    framesize = fp.getframerate() if framesize is None else framesize
    for frame in frame_buffer(fp, framesize):
        if max([abs(min(frame)), max(frame)]) >= threshold:
            return False
    return True


def frame_buffer(fp, framesize):
    """Provide frames of numerical wave data.

    Parameters
    ----------
    fp : wave.Wave_read
        An open wavefile object to buffer.
    framesize : int
        Number of frames to return per channel.

    Yields
    ------
    frame : tuple
        Numerical data for the wavefile as signed integers.
        Note:
            1. Multiple channels will be interleaved, and the length will be
               framesize * 2.
            2. The final frame will have length L, where
               n_channels <= L <= framesize * 2, i.e. it will not be empty.
    """
    n_channels = fp.getnchannels()
    bytedepth = fp.getsampwidth()
    raw_data = fp.readframes(framesize)
    frame = _byte_string_to_data(raw_data, n_channels, bytedepth)
    while len(frame) == framesize * n_channels:
        yield frame
        raw_data = fp.readframes(framesize)
        frame = _byte_string_to_data(raw_data, n_channels, bytedepth)
    if frame:
        yield frame


def _byte_string_to_data(byte_string, channels, bytedepth):
    """Convert a byte string into a numpy array.

    Parameters
    ----------
    byte_string : str
        raw byte string
    channels : int
        number of channels to unpack from frame
    bytedepth : int
        byte-depth of audio data

    Returns
    -------
    array : np.ndarray of floats
        array with shape (num_samples, channels), bounded on [-1.0, 1.0)
    """
    # Number of values per channel.
    N = len(byte_string) / channels / bytedepth
    # Assume 2-byte encoding.
    fmt = 'h'
    if bytedepth == 3:
        tmp = list(byte_string)
        byte_string = "".join(
            [tmp.insert(n * 4 + 3, struct.pack('b', 0)) for n in range(N)])

    if bytedepth in [3, 4]:
        fmt = "i"

    return struct.unpack('%d%s' % (N, fmt) * channels, byte_string)

