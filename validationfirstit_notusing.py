#here we are going to put all the checks together -> maybe something with unit tests?
#so we could see either how many pass/fails or a full display of which ones were incorrect
#i.e. display the error message
import sys
import os
import glob
import yaml
from PyQt4 import QtGui, QtCore
from functools import partial
import multitrack_utils as mu
import wave_silence as W


#Calls all the error checks
def checkAudio(raw_path, stem_path, mix_path):
    """
    Error checks the input files for the following potential problems: 
        -Stem/raw folders are empty
        -Silent files
        -Incorrectly formatted files
        -Stems without corresponding raw files
        -Stems/raw files not the same length as final mix
        -Alignment issues
        -Instruments labelled Incorrectly
        -Raw tracks matched to correct stems
        -Stem or raw exact duplicates
        -Chunks of silence at beginning/end
        -Speech extras
        -Stems not making it into mix

    Parameters
    ----------
    raw_path : str
        Path to raw folder (contains raw wav files).
    stem_path : str
        Path to stem folder (contains stem wav files).
    mix_path : str
        Path to mix wavefile.

    Yields
    -------
    valid : bool
        True if all checks pass (thus problems arr would be empty).
    problems: arr 
        Array of strings listing the errors thrown.
    """

    valid = True
    problems = []

    #empty folder check
    valid = emptyFolder(raw_path, stem_path)


    # maybe make a dictionary.... 
    #os.path.basename...how to get the files for dictionary

    # get list of files #
    mix_length = W.get_length(mix_path)
    stem_files = glob.glob(os.path.join(stem_path, '*.wav'))
    raw_files = glob.glob(os.path.join(raw_path, '*.wav'))
    wrong_stats = []
    wrong_length = []
    silent = []

    #makes sure that the stem and raw files has the correct stats  after getting a list of them
    print "Checking audio files..."
    for stem in stem_files:
        if not W.is_right_stats(stem, "stem"):
            wrong_stats.append(stem)
        if not W.is_right_length(stem, mix_length):
            wrong_length.append(stem)
        if W.is_silence(stem):
            silent.append(stem)
    for raw in raw_files:
        if not W.is_right_stats(raw, "raw"):
            wrong_stats.append(raw)
        if not W.is_right_length(raw, mix_length):
            wrong_length.append(raw)
        if W.is_silence(raw):
            silent.append(raw)


    #BASIC ERROR CHECKING THAT WE HAVE NOW
    if len(wrong_stats) > 0:
        problems.append("Files with incorrect stats exist:")
        for wstat in wrong_stats:
            problems.append(wstat)
        problems.append(" ")
        valid = False
    if len(wrong_length) > 0:
        problems.append("Not all file lengths match the mix length:")
        for wlen in wrong_length:
            problems.append(wlen)
        problems.append(" ")
        valid = False
    if len(silent) > 0:
        problems.append("Silent files exist.")
        for slnt in silent:
            problems.append(slnt)
        valid = False

    return valid, problems


def emptyFolder(raw_path, stem_path):
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
    #valid is set True as default in checkAudio

    if not W.has_wavs(stem_path):
        problems.append("Stem folder has no wav files.")
        valid = False
    if not W.has_wavs(raw_path):
        problems.append("Raw folder has no wav files.")
        valid = False
    return valid








    



