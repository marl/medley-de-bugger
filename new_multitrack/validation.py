import os
import glob
import struct
import wave

# Dictionary that creates the invalid dialog error messages associated with error checks. #
PROBLEMS = {
    'Silent': 'File is silent.',
    'Empty': 'Folder is empty.',
    'Wrong_Stats': 'File format is incorrect.', 
    'Length_As_Mix': 'File is not correct length.', 
    'Stems_Have_Raw': 'Stems are missing corresponding raw files.',  
    'Alignment': 'Files are not aligned.',  
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
    mix_length = get_length(mix_path)

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
            'Alignment': None,  # multiple checks in here...might split up
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

    length_status = length_check(raw_files, stem_files, mix_length)
    file_status = fill_file_status(file_status, length_status, 'Length_As_Mix')

    silence_status = silence_check(raw_files, stem_files, mix_path)
    file_status = fill_file_status(file_status, silence_status, 'Silent')

    empty_status = empty_check(raw_path, stem_path)
    file_status = fill_file_status(file_status, empty_status, 'Empty')

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


def length_check(raw_files, stem_files, mix_length):
    """Use is_right_length to check if stem and raw files are the same length as mix,
    then populate length_dict with bool result associated with each file check.

    Parameters
    ----------
    raw_files : list
        Raw files contained within raw_path folder. 
    stem_files: list
        Stem files contained within stem_path folder.
    mix_length : int
        Number of samples in mix.

    Returns
    -------
    length_dict : dict
        Contains bool associated with each file after checking if files are
        the correct length.
        Keys = files, values = bool (True if length is correct).
    """

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
    elif type == "mix":
        if n_channels == 2 and bytedepth == 2 and fs == 44100:
            return True
        else:
            return False
    else:
        print("Incorrect Type.")
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
    fp = wave.open(fpath, 'rb')
    length = fp.getnframes()
    return length


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


# This isn't catching everything that it should be right now. Look back at this.
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
