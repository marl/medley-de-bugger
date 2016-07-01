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
#import wave_silence as W


"""This generates the unique errors thrown by each test -> needs to call each check"""

def error_gen(raw_files, stem_files, mix_file, file_list, file_status):  # HELP
    print "Checking audio files..."

    global valid
    global error_message
    valid = True
    error_message = ''

    # checks
    valid, error_message = stats_check(raw_files, stem_files, file_list, file_status)

    # actually writes error message
    for item in file_list:
        for status in file_status:
            if status:
                print 'Pass!'

            else:
                print 'Error: ' + error_message

    return valid, error_message


#Calls all the error checks
def checkAudio(raw_path, stem_path, mix_path):
    "MAKING NESTED STATUS DICTIONARY"""
    # file_list is our outer dictionary, file_status is outer
    file_list = []
    file_status = {}

    # get list of files #
    mix_file = [mix_path]
    stem_files = glob.glob(os.path.join(stem_path, '*.wav'))
    raw_files = glob.glob(os.path.join(raw_path, '*.wav'))

    file_list = mix_file + stem_files + raw_files

    mix_length = get_length(mix_path)

    valid, error_message = error_gen(raw_files, stem_files, mix_file, file_list, file_status)

    # Populates nested dictionary containing all the information for the error checks #

    for item in file_list:
        file_status[item] = {
            'Silent': None,  # done
            'Empty_Raw': None,  # done
            'Empty_Stems': None,  # done
            'Wrong_Stats': None,  # done
            'Length_As_Mix': None,  # done
            'Stems_Have_Raw': None,  # ? was this already written? is empty_folder same as if stems have corr. raw
            'Alignment': None,  # multiple checks in here...TBD
            'Instrument_Label': None,
            'Raws_Match_Stems': None,
            'Stem_Duplicates': None,
            'Raw_Duplicates': None,
            'Silent_Sections': None,
            'Speech': None,
            'Stem_Present_In_Mix': None
        }

        #also eventually only print items in file status whose inner keys are false
        # pretty json print # (sort keys sorts alphabetically)
    print json.dumps(file_status, sort_keys=False, indent=4)


    return valid, file_list
# change check tests to make valid false if any one test fails (outside of loops)
# check with this first


def stats_check(raw_files, stem_files, file_list, file_status):
    for stem in stem_files:
        if not is_right_stats(stem, "stem"):
            file_list[file_status]['Wrong_Stats'] = False
            error_message = 'Files with incorrect stats exist:'
            # for wstat in wrong_stats:
            #     error_message += wstat
            # error_message += " "
            valid = False

    for raw in raw_files:
        if not is_right_stats(raw, "raw"):
            file_list[file_status]['Wrong_Stats'] = False
            error_message = 'Files with incorrect stats exist:'
            # for wstat in wrong_stats:
            #     error_message += wstat
            # error_message += " "
            valid = False

    return valid, error_message


def length_check(raw_files, stem_files, mix_length, file_list, file_status):
    for stem in stem_files:
        if not is_right_length(stem, mix_length):
            file_list[file_status]['Length_As_Mix'] = False
            error_message = 'Not all file lengths match the mix length:'
            # for wlen in wrong_length:
            #     error_message += wlen
            # error_message += " "
            valid = False

    for raw in raw_files:
        if not is_right_length(raw, mix_length):
            file_list[file_status]['Length_As_Mix'] = False
            error_message = 'Not all file lengths match the mix length:'
            valid = False

    return valid, error_message


def silence_check(raw_files, stem_files, file_list, file_status):
    for stem in stem_files:
        if is_silence(stem):
            file_list[file_status]['Silent'] = False
            error_message = 'Silent files exist.'
            # for slnt in silent:
            #     error_message += slnt
            valid = False

    for raw in raw_files:
        if is_silence(raw):
            file_list[file_status]['Silent'] = False
            error_message = 'Silent files exist.'
            # for slnt in silent:
            #     error_message += slnt
            valid = False

    return valid, error_message


def empty_check(raw_path, stem_path, file_list, file_status):
    """
    Checks to make sure the selected raw and stem paths are not empty.

    Parameters
    ----------
    raw_path : str
        Path to raw folder (contains raw wav files).
    stem_path : str
        Path to stem folder (contains stem wav files).

    Yields
    -------
    valid : bool
        True if stem or raw folders contain wav files (i.e. not empty)
    """
    # valid is set True as default in checkAudio

    if not has_wavs(stem_path):  # if it doesnt have wavs (returns true)
        file_list[file_status]['Empty_Stems'] = False
        error_message = 'Path contains no stem wav files.'
        valid = False

    if not has_wavs(raw_path):
        file_list[file_status]['Empty_Raw'] = False
        error_message = 'Path contains no raw wav files.'
        valid = False

    return valid, error_message


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
