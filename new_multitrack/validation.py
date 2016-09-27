import os
import glob
import struct
import wave
import sox
import numpy as np
import tempfile
import librosa
import scipy.io.wavfile as wavfile
import scipy.optimize.nnls as nnls
import argparse
import json


# Dictionary that creates the invalid dialog error messages associated with error checks. #
PROBLEMS = {
    'Silent': 'File is silent.',
    'Empty': 'Folder is empty.',
    'Wrong_Stats': 'File format is incorrect. All files must be 44.1k and 16bit. Mix and stem files should be stereo, raw files should be mono.', 
    'Length_As_Mix': 'File is not correct length.', 
    'Raws_In_Stems': 'This raw file was not found in its corresponding stem.', 
    'Stems_In_Mix': 'Mix is missing corresponding stem files.', 
    'Raw_Sum_Alignment': 'Raw files are not aligned with the mix.',  
    'Stem_Sum_Alignment': 'Stem files are not aligned with the mix.', 
    'Raw_to_Stem_Alignment': 'The raw files associated with this stem file are not correctly aligned.',
    'Instrument_Label': 'Instruments are incorrectly labelled.',
    'Raws_Match_Stems': 'Raw files do not correspond to correct stems.',
    'Stem_Duplicates': 'Duplicate stem files exist.',
    'Raw_Duplicates': 'Duplicate raw files exist.',
    'Silent_Sections': 'File contains silent sections.',
    'Speech': 'File contains speech segments.',
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
            'Instrument_Label': None,
            'Raws_Match_Stems': None,
            'Stem_Duplicates': None,
            'Raw_Duplicates': None,
            'Silent_Sections': None,
            'Speech': None,
            'Stem_Present_In_Mix': None
        }

    empty_status = empty_check(raw_path, stem_path)
    file_status = fill_file_status(file_status, empty_status, 'Empty')

    if not np.all(empty_status.values()):
        return file_status

    stats_status = stats_check(raw_files, stem_files, mix_path)
    file_status = fill_file_status(file_status, stats_status, 'Wrong_Stats')

    length_status = length_check(raw_files, stem_files, mix_path)
    file_status = fill_file_status(file_status, length_status, 'Length_As_Mix')

    silence_status = silence_check(raw_files, stem_files, mix_path)
    file_status = fill_file_status(file_status, silence_status, 'Silent')

    return file_status


def check_multitrack(raw_files, stem_files, mix_path, raw_info):
    """Populate file_status dict with correct error check results. Send
    this result to create_problems. This is the second check, after the raw
    and stem information is collected.

    Parameters
    ----------
    raw_files : str
        List of paths to raw folder
    stem_files : str
        List of paths to stem folder
    mix_path : str
        Path to mix file.
    raw_info: dict
        Maps raw to stems.

    Returns
    -------
    file_status : dict
        Outer dictionary containing status_dict. 
        Keys = list of files, values = status_dict contents (check : T/F).
    """

    file_list = []
    file_status = {}

    mix_file = [os.path.basename(mix_path)]

    raw_names = [os.path.basename(f) for f in raw_files]
    stem_name = [os.path.basename(f) for f in stem_files]

    stem_path = os.path.dirname(stem_files[0]).split('/')[-1]
    raw_path = os.path.dirname(raw_files[0]).split('/')[-1]

    file_list = mix_file + raw_names + stem_name + [stem_path] + [raw_path]

    for item in file_list:
        file_status[item] = {
            'Stems_In_Mix': None,
            'Raws_In_Stems': None,
            'Raw_Sum_Alignment': None,  # Sum of raws are not aligned with mix.
            'Stem_Sum_Alignment': None, # Sum of stems are not aligned with mix.
            'Raw_to_Stem_Alignment': None,
            'Instrument_Label': None,
            'Raws_Match_Stems': None,
            'Stem_Duplicates': None,
            'Raw_Duplicates': None,
        }

    # Sum of raws not aligned with mix
    raw_sum_alignment_status, stem_sum_alignment_status, raw_to_stem_alignment_status = is_aligned(raw_files, stem_files, raw_path, stem_path, mix_path, raw_info)
    file_status = fill_file_status(file_status, raw_sum_alignment_status, 'Raw_Sum_Alignment')

    # Sum of stems aligned with mix
    raw_sum_alignment_status, stem_sum_alignment_status, raw_to_stem_alignment_status = is_aligned(raw_files, stem_files, raw_path, stem_path, mix_path, raw_info)
    file_status = fill_file_status(file_status, stem_sum_alignment_status, 'Stem_Sum_Alignment')

    # individual raws aligned with stems
    raw_sum_alignment_status, stem_sum_alignment_status, raw_to_stem_alignment_status = is_aligned(raw_files, stem_files, raw_path, stem_path, mix_path, raw_info)
    file_status = fill_file_status(file_status, raw_to_stem_alignment_status, 'Raw_to_Stem_Alignment')

    raw_inclusion_status, stem_inclusion_status = is_included(stem_files, raw_files, stem_path, mix_path, raw_info)
    file_status = fill_file_status(file_status, raw_inclusion_status, 'Raws_In_Stems')

    raw_inclusion_status, stem_inclusion_status = is_included(stem_files, raw_files, stem_path, mix_path, raw_info)
    file_status = fill_file_status(file_status, stem_inclusion_status, 'Stems_In_Mix')

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
    fp = wave.open(fpath, 'rb')
    n_channels = sox.file_info.channels(fpath)
    bytedepth = fp.getsampwidth()
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
        return False


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


def get_dur(fpath):
    """Get duration of a file in seconds.

    Parameters
    ----------
    fpath : str
        Path to a file.

    Returns
    -------
    dur : float
        Length of file in seconds.
    """
    dur = sox.file_info.duration(fpath)
    return dur


def is_right_length(fpath, ref_length):
    """Check if stem and raw files are the same length as the mix.

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
        True if values are less than the given threshold (i.e. if the file is silent)
    """
    return sox.file_info.silent(fpath)


def alignment_helper(file_list, target_path):
    """Downsample and perform cross-correlation on files relative
    to a target file to test if they are correctly aligned.

    Parameters
    ----------
    file_list : list
        List of files (i.e. stem_files, raw_files)
    target_path : str
        Filepath to compare files in file_list to.

    Returns
    -------
    status : bool
        True if the cross_correlation values are within a threshold, demonstrating
        that the files are correctly aligned.
    """
    sr = 1000
    output_handle = tempfile.NamedTemporaryFile(suffix='.wav')  
    output_path = output_handle.name

    if len(file_list) > 1: 
        file_sum = sox.Combiner()
        file_sum.build(
            file_list, output_path, 'mix'
        ) 
    else:
        file_sum = sox.Transformer()
        file_sum.build(file_list[0], output_path)

    file_sum.rate(sr,'m')

    target_handle = tempfile.NamedTemporaryFile(suffix='.wav')
    target_handle_path = target_handle.name
    target_sum = sox.Transformer()
    target_sum.build(target_path, target_handle_path)
    target_sum.rate(sr, 'm')

    dur = get_length(target_path)
    offset = (dur/44100.0) / 2.0
    y_files, sr = librosa.load(output_path, sr=sr, offset = offset, duration=30.0)
    y_target, sr = librosa.load(target_handle_path, sr=sr, offset = offset, duration=30.0)

    correlation = np.correlate(y_files, y_target, 'full')

    N = len(y_target)
    a = np.arange(1, N+1)
    a_rev = np.arange(1, N)
    b = a_rev[ : :-1]  
    c = np.concatenate((a, b))
    c = c.astype(float)

    correlation = np.abs(correlation) / c
    center = N
    corr_index = np.argmax(correlation)

    if np.abs(corr_index - center) > 5:
        return False
    else:
        return True


def is_aligned(raw_files, stem_files, raw_path, stem_path, mix_path, raw_info): 
    """Populate alignment dicts with associated bools.

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
    raw_info: dict
        Dictionary containing all information associated with each raw track.
        Includes path, instrument, and stem that it is mapped to.

    Returns
    -------
    raw_sum_alignment_dict: dict
        Contains bool associated with raw folder after
        checking if the sum isn't aligned with the mix.
    stem_sum_alignment_dict: dict
        Contains bool associated with stem folder after
        checking if the sum isn't aligned with the mix.
    raw_to_stems_dict: dict
        Contains bool associated with each stem if the
        mapped raws are not aligned.
    """

    raw_sum_alignment_dict = {} # Raws aligned with mix
    stem_sum_alignment_dict = {} # Stems aligned with mix
    raw_to_stems_dict = {} # Raws aligned with stems

    stem_sum_alignment_dict[os.path.basename(stem_path)] = alignment_helper(stem_files, mix_path)
    raw_sum_alignment_dict[os.path.basename(raw_path)] = alignment_helper(raw_files, mix_path)

    raw_to_stems_dict = {}
    for stem in stem_files:
        stem_raws = [v['path'] for k, v in raw_info.items() if v['stem'] == os.path.basename(stem)]
        raw_to_stems_dict[os.path.basename(stem)] = alignment_helper(stem_raws, stem)

    return raw_sum_alignment_dict, stem_sum_alignment_dict, raw_to_stems_dict


def loadmono(filename, is_mono=False):
    """Check if stem and raw files are the same length as the mix.

    Parameters
    ----------
    filename : str
        Path to a file.
    is_mono: bool
        True if input file is mono. Default=False.

    Returns
    -------
    w : np.array
        Audio file converted to mono.
    """
    _, w = wavfile.read(filename)
    if not is_mono:
        w = np.abs(w.sum(axis=1))
    else:
        w = np.abs(w)
    return w


def get_coeffs(file_list, target_path, is_mono):
    """Calculate weighted mixing coefficients.

    Parameters
    ----------
    file_list : list
        List of files to calculate coefficients of.
    target_path: str
        Path to file that the list will be tested against.
    is_mono: bool
        True if input file is mono. Default=False.

    Returns
    -------
    mixing_coeffs : dict
        Dictionary of each file and its associated mixing coefficient
        relative to target path.
    """

    target_audio = loadmono(target_path)

    full_audio = np.vstack(
        [loadmono(f, is_mono=is_mono) for f in file_list]
    )

    coeffs, _ = nnls(full_audio.T, target_audio.T)

    base_keys = [os.path.basename(s) for s in file_list]

    mixing_coeffs = { 
        i : float(c) for i, c in zip(base_keys, coeffs)
    }

    return mixing_coeffs


def is_included(stem_files, raw_files, stem_path, mix_path, raw_info):
    """Test to see if each file is actually included in its overhead file, i.e.
    stems are present in mix, raws are present in stems. Also populates inclusion
    dicts with associated bools.

    Parameters
    ----------
    stem_files: list
        Stem files contained within stem_path folder.
    raw_files : list
        Raw files contained within raw_path folder. 
    stem_path: str
        Path to stem file folder.
    mix_path : str
        Path to mix file.
    raw_info: dict
        Dictionary containing all information associated with each raw track.
        Includes path, instrument, and stem that it is mapped to.

    Returns
    -------
    raw_inclusion_dict: dict
        Contains bool associated with raws after
        checking if file is present in associated stem.
    stem_inclusion_dict: dict
        Contains bool associated with stems after
        checking if file is present in mix.

    """

    raw_inclusion_dict = {}
    stem_inclusion_dict = {}

    # Stems in mix
    stem_coeffs = get_coeffs(stem_files, mix_path, False)
    for k, v in stem_coeffs.items():
        stem_inclusion_dict[k] = check_weight(v)

    # Raws in stems
    for stem in stem_files:
        stem_inclusion = [v['path'] for k, v in raw_info.items() if v['stem'] == os.path.basename(stem)]
        raw_coeffs = get_coeffs(stem_inclusion, stem, True)
        for k, v in raw_coeffs.items():
            raw_inclusion_dict[k] = check_weight(v)

    return raw_inclusion_dict, stem_inclusion_dict


def check_weight(val):
    """Check if inclusion weight is below threshold.

    Parameters
    ----------
    val : float
        Weighted mixing coefficient.

    Returns
    -------
    status : bool
        True if mixing weight is above threshold.
    """
    if val < 0.01:
        return False
    else:
        return True







