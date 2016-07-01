#here we are going to put all the checks together -> maybe something with unit tests?
#so we could see either how many pass/fails or a full display of which ones were incorrect
#i.e. display the error message
import sys
import os
import glob
import struct
import wave
import json
from PyQt4 import QtGui, QtCore
from functools import partial
import multitrack_utils as mu
from os.path import basename
#import wave_silence as W


def fill_file_status(file_status, status_dict, secondary_key):

    #print file_status['Phoenix_ScotchMorris_STEM_01.wav']
#changed file_lists from file_status
    for key in status_dict:
        file_status[key][secondary_key] = status_dict[key]
        #status_dict[key] = file_status[key][secondary_key]
    return file_status


#Calls all the error checks
def checkAudio(raw_path, stem_path, mix_path):
    "MAKING NESTED STATUS DICTIONARY"""
    # file_list is our outer dictionary, file_status is outer
    file_list = []
    file_status = {}

    # get list of files -paths #
    mix_file = [os.path.basename(mix_path)]
    stem_files = glob.glob(os.path.join(stem_path, '*.wav'))
    raw_files = glob.glob(os.path.join(raw_path, '*.wav'))

    # this gets the base file so it's not the long path version
    new_stems = [os.path.basename(path) for path in stem_files]
    new_raws = [os.path.basename(path) for path in raw_files]

    print mix_file
    print new_stems
    print new_raws

    file_list = mix_file + new_stems + new_raws + [os.path.basename(raw_path)] + [os.path.basename(stem_path)]

    mix_length = get_length(mix_path)

    # initializes outer dictionary #
    for item in file_list:
        file_status[item] = {
            'Silent': None,
            'Empty': None,  # done
            'Wrong_Stats': None,  # done
            'Length_As_Mix': None,  # done
            'Stems_Have_Raw': None,  # done
            'Alignment': None,  # multiple checks in here...TBD
            'Instrument_Label': None,
            'Raws_Match_Stems': None,
            'Stem_Duplicates': None,
            'Raw_Duplicates': None,
            'Silent_Sections': None,
            'Speech': None,
            'Stem_Present_In_Mix': None
        }

    print(file_status.keys())
    print(file_status['Phoenix_ScotchMorris_STEM_01.wav'])

    # make these nameofcheck_status -> changed these to be file list in fill file status args
    stats_status = stats_check(raw_files, stem_files)
    file_status = fill_file_status(file_status, stats_status, 'Wrong_Stats')

    length_status = length_check(raw_files, stem_files, mix_length)
    file_status = fill_file_status(file_status, length_status, 'Length_As_Mix')

    silence_status = silence_check(raw_files, stem_files)
    file_status = fill_file_status(file_status, silence_status, 'Silent')

    empty_status = empty_check(raw_path, stem_path)
    file_status = fill_file_status(file_status, empty_status, 'Empty')

        #also eventually only print items in file status whose inner keys are false
        # pretty json print # (sort keys sorts alphabetically)
    #print(json.dumps(file_status, sort_keys=False, indent=4))

    return file_status

 # also add mix_path as arg to these tests and fix the helpers to check the mix statistics

def stats_check(raw_files, stem_files):
    # make these checkname_dict
    stats_dict = {}

    for stem in stem_files:
        if not is_right_stats(stem, "stem"):
            stats_dict[os.path.basename(stem)] = False
        else:
            stats_dict[os.path.basename(stem)] = True

    for raw in raw_files:
        if not is_right_stats(raw, "raw"):
            stats_dict[os.path.basename(raw)] = False
        else:
            stats_dict[os.path.basename(raw)] = True

    return stats_dict


def length_check(raw_files, stem_files, mix_length):

    length_dict = {}

    for stem in stem_files:
        if not is_right_length(stem, mix_length):
            length_dict[os.path.basename(stem)] = False
        else:
            length_dict[os.path.basename(stem)] = True      

    for raw in raw_files:
        if not is_right_length(raw, mix_length):
            length_dict[os.path.basename(raw)] = False
        else:
            length_dict[os.path.basename(raw)] = True

    return length_dict


def silence_check(raw_files, stem_files):

    silence_dict = {}

    for stem in stem_files:
        if is_silence(stem):
            silence_dict[os.path.basename(stem)] = False
        else:
            silence_dict[os.path.basename(stem)] = True

    for raw in raw_files:
        if is_silence(raw):
            silence_dict[os.path.basename(raw)] = False
        else:
            silence_dict[os.path.basename(raw)] = True

    return silence_dict

def empty_check(raw_path, stem_path):
    empty_dict = {}

    if not has_wavs(stem_path):  # if it doesnt have wavs (returns true)
        empty_dict[os.path.basename(stem_path)] = False
    else:
        empty_dict[os.path.basename(stem_path)] = True

    if not has_wavs(raw_path):
        empty_dict[os.path.basename(raw_path)] = False
    else:
        empty_dict[os.path.basename(raw_path)] = True

    return empty_dict


#TAKEN FROM WAVE_SILENCE (use most of these as helper functions)
"""Routines to test the 'emptiness' of a wave file. Mostly helper functions"""


def has_wavs(folder_path):
    wav_files = glob.glob(os.path.join(folder_path, '*.wav'))
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
        print("Incorrect Type.")
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
