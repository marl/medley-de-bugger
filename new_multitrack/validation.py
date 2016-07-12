import os
import glob
import struct
import wave
import sox
import numpy as np
import tempfile
import librosa
import matplotlib.pyplot as plt

# Dictionary that creates the invalid dialog error messages associated with error checks. #
PROBLEMS = {
    'Silent': 'File is silent.',
    'Empty': 'Folder is empty.',
    'Wrong_Stats': 'File format is incorrect.', 
    'Length_As_Mix': 'File is not correct length.', 
    'Stems_Have_Raw': 'Stems are missing corresponding raw files.',  
    'Raw_Sum_Alignment': 'Raw files are not aligned with the mix.',  # sum of raws
    'Stem_Sum_Alignment': 'Stem files are not aligned with the mix.', # sum of stems
    'Instrument_Label': 'Instruments are incorrectly labelled.',
    'Raws_Match_Stems': 'Raw files do not correspond to correct stems.',
    'Stem_Duplicates': 'Duplicate stem files exist.',
    'Raw_Duplicates': 'Duplicate raw files exist.',
    'Silent_Sections': 'File contains silent sections.',
    'Speech': 'File contains speech segments.',
    'Stem_Present_In_Mix': 'Stems do not add up to the mix correctly.'
}


def fill_file_status(file_status, status_dict, secondary_key):
    """Map inner keys of file_status to status_dict keys. Use this to 
    populate final file_status dict in check_audio.

    Parameters
    ----------
    file_status : dict
        Outer dictionary containing status_dict. 
        Keys = list of files, values = status_dict contents (check : T/F).
    status_dict : dict
        Inner dictionary that gives T/F for each check for each included file.
        Keys = check name, i.e. 'Silent', values = bool (True if check passes). 
    secondary_key : str
        Inner key of file_status containing the error check name, i.e. 'Silent'.

    Returns
    -------
    file_status : dict
        Outer dictionary containing status_dict. 
        Keys = list of files, values = status_dict contents (check : T/F).
    """
    for key in status_dict:
        file_status[key][secondary_key] = status_dict[key]
    return file_status


def check_audio(raw_path, stem_path, mix_path):
    """Populate file_status dict with correct error check results. Send
    this result to create_problems.

    Parameters
    ----------
    raw_path : str
        Path to raw folder.
    stem_path : str
        Path to stem folder.
    mix_path : str
        Path to mix file.

    Returns
    -------
    file_status : dict
        Outer dictionary containing status_dict. 
        Keys = list of files, values = status_dict contents (check : T/F).
    """

    file_list = []
    file_status = {}
    

    mix_file = [os.path.basename(mix_path)]
    stem_files = glob.glob(os.path.join(stem_path, '*.wav'))
    raw_files = glob.glob(os.path.join(raw_path, '*.wav'))

    # specifies base file instead of full file path
    new_stems = [os.path.basename(path) for path in stem_files]
    new_raws = [os.path.basename(path) for path in raw_files]

    file_list = mix_file + new_stems + new_raws + [os.path.basename(raw_path)] + [os.path.basename(stem_path)]

    for item in file_list:
        file_status[item] = {
            'Silent': None,
            'Empty': None,
            'Wrong_Stats': None,
            'Length_As_Mix': None,
            'Stems_Have_Raw': None,
            'Raw_Sum_Alignment': None,  # Sum of raws are not aligned with mix.
            'Stem_Sum_Alignment': None, # Sum of stems are not aligned with mix.
            'Instrument_Label': None,
            'Raws_Match_Stems': None,
            'Stem_Duplicates': None,
            'Raw_Duplicates': None,
            'Silent_Sections': None,
            'Speech': None,
            'Stem_Present_In_Mix': None
        }

    stats_status = stats_check(raw_files, stem_files, mix_path)
    file_status = fill_file_status(file_status, stats_status, 'Wrong_Stats')

    length_status = length_check(raw_files, stem_files, mix_path)
    file_status = fill_file_status(file_status, length_status, 'Length_As_Mix')

    silence_status = silence_check(raw_files, stem_files, mix_path)
    file_status = fill_file_status(file_status, silence_status, 'Silent')

    empty_status = empty_check(raw_path, stem_path)
    file_status = fill_file_status(file_status, empty_status, 'Empty')

    # Sum of raws not aligned with mix
    raw_sum_alignment_status, stem_sum_alignment_status = is_aligned(raw_files, stem_files, raw_path, stem_path, mix_path)
    file_status = fill_file_status(file_status, raw_sum_alignment_status, 'Raw_Sum_Alignment')

    raw_sum_alignment_status, stem_sum_alignment_status = is_aligned(raw_files, stem_files, raw_path, stem_path, mix_path)
    file_status = fill_file_status(file_status, stem_sum_alignment_status, 'Stem_Sum_Alignment')

    # print(json.dumps(file_status, sort_keys=False, indent=4)) for pretty print checks
    return file_status


def create_problems(file_status):
    """Search for errors (false results) in file_status dict then map
    to readable error messages from PROBLEMS dictionary.

    Parameters
    ----------
    file_status : dict
        Outer dictionary containing status_dict. 
        Keys = list of files, values = status_dict contents (check : T/F).

    Returns
    -------
    problems : list
        Contains all error messages and associated file names that
        resulted from a false error check.
    """
    problems = []

    for f_name in file_status:
        if False in file_status[f_name].values():
            for key in file_status[f_name]:
                if file_status[f_name][key] is False:
                    problems.append("{} : {}".format(f_name, PROBLEMS[key]))
    return problems


def stats_check(raw_files, stem_files, mix_path):
    """Use is_right_stats to check if each file is correctly formatted,
    then populate stats_dict with bool result associated with each file check.

    Parameters
    ----------
    raw_files : list
        Raw files contained within raw_path folder. 
    stem_files: list
        Stem files contained within stem_path folder.
    mix_path : str
        Path to mix file.

    Returns
    -------
    stats_dict : dict
        Contains bool associated with each file after checking if files are
        correctly formatted.
        Keys = files, values = bool (True if format is correct).
    """
    
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

    if not is_right_stats(mix_path, "mix"):
        stats_dict[os.path.basename(mix_path)] = False
    else:
        stats_dict[os.path.basename(mix_path)] = True

    return stats_dict


def length_check(raw_files, stem_files, mix_path):
    """Use is_right_length to check if stem and raw files are the same length as mix,
    then populate length_dict with bool result associated with each file check.

    Parameters
    ----------
    raw_files : list
        Raw files contained within raw_path folder. 
    stem_files: list
        Stem files contained within stem_path folder.
    mix_path : str
        Path to mix file

    Returns
    -------
    length_dict : dict
        Contains bool associated with each file after checking if files are
        the correct length.
        Keys = files, values = bool (True if length is correct).
    """

    length_dict = {}
    mix_length = get_length(mix_path)

    for stem in stem_files:
        if is_right_length(stem, mix_length):
            length_dict[os.path.basename(stem)] = True
        else:
            length_dict[os.path.basename(stem)] = False    

    for raw in raw_files:
        if is_right_length(raw, mix_length):
            length_dict[os.path.basename(raw)] = True
        else:
            length_dict[os.path.basename(raw)] = False

    return length_dict


def silence_check(raw_files, stem_files, mix_path):
    """Use is_silence to check for silent files, then populates
    silence_dict with bool associated with each file check.

    Parameters
    ----------
    raw_files : list
        Raw files contained within raw_path folder. 
    stem_files: list
        Stem files contained within stem_path folder.
    mix_path : str
        Path to mix file.

    Returns
    -------
    silence_dict : dict
        Contains bool associated with each file after checking if files
        are silent.
        Keys = files, values = bool (True if file is not silent).
    """

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

    if is_silence(mix_path):
        silence_dict[os.path.basename(mix_path)] = False
    else:
        silence_dict[os.path.basename(mix_path)] = True

    return silence_dict


def empty_check(raw_path, stem_path):
    """Use has_wavs to make sure selected raw and stem folders
    are not empty.

    Parameters
    ----------
    raw_path : str
        Path to raw folder.
    stem_path : str
        Path to stem folder.

    Returns
    -------
    silence_dict : dict
        Contains bool associated with raw and stem folders after 
        checking if they are empty.
        Keys = files, values = bool (True if folders are not empty).
    """

    empty_dict = {}

    if not has_wavs(stem_path):
        empty_dict[os.path.basename(stem_path)] = False
    else:
        empty_dict[os.path.basename(stem_path)] = True

    if not has_wavs(raw_path):
        empty_dict[os.path.basename(raw_path)] = False
    else:
        empty_dict[os.path.basename(raw_path)] = True

    return empty_dict


# Helper functions that perform the heavy-lifting for the error-checks:
# The results of these checks are called above to create the nested dictionaries of errors.

def has_wavs(folder_path):
    """Check if folders contain wavefiles, i.e. are not empty.

    Parameters
    ----------
    folder_path : str
        Path to a folder, i.e. raw_path, stem_path.

    Returns
    -------
    status : bool
        True if folder path contains wavefiles.
    """
    wav_files = glob.glob(os.path.join(folder_path, '*.wav'))
    if len(wav_files) == 0:
        return False
    else:
        return True


def is_right_stats(fpath, type):
    """Check if files are correctly formatted.

    Parameters
    ----------
    fpath : str
        Path to a file.
    type: str
        Type of file, i.e. stem, raw, mix.

    Returns
    -------
    status : bool
        True if file is formatted correctly.
    """
    n_channels = sox.file_info.channels(fpath)
    bytedepth = sox.file_info.bitrate(fpath)
    float_s = sox.file_info.sample_rate(fpath)
    fs = int(float_s)
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
    elif type == "mix":
        if n_channels == 2 and bytedepth == 2 and fs == 44100:
            return True
        else:
            return False
    else:
        print("Incorrect Type.")
        return False

# Updated using pysox. #
def get_length(fpath):
    """Calculate number of samples i.e. length of the file.

    Parameters
    ----------
    fpath : str
        Path to a file. 

    Returns
    -------
    length : int
        Number of samples of file.
    """
    length = sox.file_info.num_samples(fpath)
    return length

# get duration in seconds
def get_dur(fpath):
    dur = sox.file_info.duration(fpath)
    return dur

def is_right_length(fpath, ref_length):
    """Check if stema and raw files are the same length as the mix.

    Parameters
    ----------
    fpath : str
        Path to a file.
    ref_length: int
        Reference length (num samples) of file.

    Returns
    -------
    status : bool
        True if file is the correcct length.
    """
    length = get_length(fpath)
    if length == ref_length:
        return True
    else:
        return False

# Mostly updated using pysox. #
def get_file_stats(fpath):
    """Provide frames of numerical wave data.

    Parameters
    ----------
    fpath: str
        Path to file.
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
    n_channels = sox.file_info.channels(fpath)
    bytedepth = sox.file_info.bitrate(fpath)
    sample_rate = sox.file_info.sample_rate(fpath) 

# What kind of pysox thing should we use for the silence check?
# This isn't catching everything that it should be right now. Look back at this.
def is_silence(fpath, threshold=16, framesize=None): 
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
    # hold to fix with sox
    # fp = wave.open(fpath, 'rb')
    # float_s = sox.file_info.sample_rate(fpath)
    # fs = int(float_s)
    # framesize = fs if framesize is None else framesize
    # for frame in frame_buffer(fpath, fp, framesize): 
    #     if max([abs(min(frame)), max(frame)]) >= threshold:
    #         return False
    return False


def downsample(fpath, sr=2000): 
    """Downsample wav files to ease cross-correlation process.

    Parameters
    ----------
    fpath: str
        Path to a wavefile.
    sr: int > 0
        Sample rate. Default = 2000.

    Returns
    -------
    y:  np.ndarray [shape=(n,) or (2,n)]
        Audio time series (mono or stereo).
    sr: int > 0
        Sample rate.
    """
    output_file = tempfile.NamedTemporaryFile(suffix='.wav')
    output_path = output_file.name
    tfm = sox.Transformer(fpath, output_path)
    tfm.rate(sr, 'm')
    tfm.build()

    y, sr = librosa.load(output_path, sr=sr)

    return y, sr


# So far this only works on the sum of raw and sum of stems compared to the mix. 
# This also includes the check that feeds into fill file status.
def is_aligned(raw_files, stem_files, raw_path, stem_path, mix_path): 
    """Test if the sum of the raw files and the sum of the stem files are correctly
    aligned with the mix file. Includes check to populate alignment dicts with associated bools.

    Parameters
    ----------
    raw_files : list
        Raw files contained within raw_path folder. 
    stem_files: list
        Stem files contained within stem_path folder.
    raw_path: str
        Path to raw file folder.
    stem_path: str
        Path to stem file folder.
    mix_path : str
        Path to mix file.

    Returns
    -------
    raw_sum_alignment_dict: dict
        Contains bool associated with raw folder after
        checking if the sum isn't aligned with the mix.
    stem_sum_alignment_dict: dict
        Contains bool associated with stem folder after
        checking if the sum isn't aligned with the mix.
    """
    sr = 2000
    output_stem = tempfile.NamedTemporaryFile(suffix='.wav')  
    output_path_stem = output_stem.name 
    stem_sum = sox.Combiner(stem_files, output_path_stem, 'concatenate') 
    stem_sum.rate(2000, 'm')
    stem_sum.build()

    output_raw = tempfile.NamedTemporaryFile(suffix='.wav')
    output_path_raw = output_raw.name
    raw_sum = sox.Combiner(raw_files, output_path_raw, 'concatenate')
    raw_sum.rate(2000, 'm')
    raw_sum.build()

    y_stem, sr = librosa.load(output_path_stem, sr=sr, duration=30)
    y_raw, sr = librosa.load(output_path_raw, sr=sr, duration=30)
    y_mix, sr = librosa.load(mix_path, sr=sr, duration=30)

    stem_sum_corr = np.correlate(y_stem, y_mix, 'full')
    raw_sum_corr = np.correlate(y_raw, y_mix, 'full')

    N = len(y_mix)
    a = np.arange(1, N+1)
    a_rev = np.arange(1, N)
    b = a_rev[ : :-1]  
    c = np.concatenate((a, b))
    c = c.astype(float)

    stem_corr_val = np.abs(stem_sum_corr) / c
    raw_corr_val = np.abs(raw_sum_corr) / c

    raw_sum_alignment_dict = {} # raw sum dict
    stem_sum_alignment_dict = {} # stem sum dict

    center = N

    stem_index = np.argmax(stem_corr_val)
    raw_index = np.argmax(raw_corr_val)

    print('Stem index - center = {}').format(stem_index - center)
    print('Raw index - center = {}').format(raw_index - center)

    if not np.abs(stem_index - center) <= 5:
        stem_sum_alignment_dict[os.path.basename(stem_path)] = False
    else:
        alignment2_dict[os.path.basename(stem_path)] = True
    if not np.abs(raw_index - center) <= 5:
        stem_sum_alignment_dict[os.path.basename(raw_path)] = False
    else:
        raw_sum_alignment_dict[os.path.basename(raw_path)] = True

    return raw_sum_alignment_dict, stem_sum_alignment_dict
