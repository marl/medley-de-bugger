import unittest
import os
from new_multitrack import new_multitrack, validation
import glob
import math
from unittest import TestCase


TestCase.maxDiff = None

def relpath(f):
    return os.path.join(os.path.dirname(__file__), f)



#test inputs here with our files
# VALID_MIX = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_MIX.wav')

# VALID_RAW = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW')
# VALID_STEMS = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS')

# WRONG_LENGTH_MIX = relpath('data/Phoenix_ScotchMorris/Piano_L.R.wav')

# EMPTY_STEMS = relpath('data/Phoenix_ScotchMorris/Empty_Test_STEMS')
# EMPTY_RAW = relpath('data/Phoenix_ScotchMorris/Empty_Test_RAW')

# MISALIGNED_RAW = relpath('data/Phoenix_ScotchMorris_Alignment/Phoenix_ScotchMorris_RAW')
# MISALIGNED_STEMS = relpath('data/Phoenix_ScotchMorris_Alignment/Phoenix_ScotchMorris_STEMS')

# MISALIGNED_STEM1 = relpath('data/Phoenix_ScotchMorris_Alignment/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_03_AW.wav')
# MISALIGNED_STEM2 = relpath('data/Phoenix_ScotchMorris_Alignment/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_01_AW.wav')

# MISALIGNED_STEMS_LIST = [MISALIGNED_STEM1, MISALIGNED_STEM2]

# RAW_INPUT1 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_01_01.wav')
# RAW_INPUT2 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_02_01.wav')
# RAW_INPUT3 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_03_01.wav')
# RAW_INPUT4_1 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_04_01.wav')
# RAW_INPUT4_2 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_04_02.wav')

# STEM_INPUT1 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_01.wav')
# STEM_INPUT2 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_02.wav')
# STEM_INPUT3 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_03.wav')
# STEM_INPUT4 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_04.wav')

# WRONG_CHANNELS_INDIV_RAW = relpath('data/Phoenix_ScotchMorris_ChannelTest/Phoenix_ScotchMorris_RAW/stem_wrong.wav')
# SILENT_FILE = relpath('data/Phoenix_ScotchMorris/Piano_L.R.wav')

# WRONG_LENGTH = relpath('data/Phoenix_ScotchMorris/wrong_length.wav')
# WRONG_CHANNELS_RAW = relpath('data/Phoenix_ScotchMorris_ChannelTest/Phoenix_ScotchMorris_RAW')
# WRONG_CHANNELS_STEMS = relpath('data/Phoenix_ScotchMorris_ChannelTest/Phoenix_ScotchMorris_STEMS')

# WRONG_CHANNELS_LIST = [RAW_INPUT1, RAW_INPUT2, RAW_INPUT3, RAW_INPUT4_1, RAW_INPUT4_2, WRONG_CHANNELS_INDIV_RAW]

# RAW_FILES_LIST = [RAW_INPUT1, RAW_INPUT2, RAW_INPUT3, RAW_INPUT4_1, RAW_INPUT4_2]
# STEM_FILES_LIST = [STEM_INPUT1, STEM_INPUT2, STEM_INPUT3, STEM_INPUT4]

# WRONG_SR_STEM = relpath('data/Phoenix_ScotchMorris/wrong_sr.wav')
# WRONG_BYTE_STEM = relpath('data/Phoenix_ScotchMorris/wrong_bitdepth.wav')

#test inputs here with our files
VALID_MIX = relpath('data/Short_Files/Mix.wav')
VALID_RAW = relpath('data/Short_Files/Raw')
VALID_STEMS = relpath('data/Short_Files/Stems')

WRONG_LENGTH_MIX = relpath('data/Short_Files/Error_Throwers/Piano_L.R.wav')

EMPTY_STEMS = relpath('data/Short_Files/Empty_Test_STEMS')
EMPTY_RAW = relpath('data/Short_Files/Empty_Test_RAW')

MISALIGNED_RAW = relpath('data/Short_Files/Raw')
MISALIGNED_STEMS = relpath('data/Short_Files/MisalignedStems')

MISALIGNED_STEM1 = relpath('data/Short_Files/MisalignedStems/Stem1Misaligned.wav')
MISALIGNED_STEM2 = relpath('data/Short_Files/MisalignedStems/Stem3Misaligned.wav')

MISALIGNED_STEMS_LIST = [MISALIGNED_STEM1, MISALIGNED_STEM2]

RAW_INPUT1 = relpath('data/Short_Files/Raw/Raw1.wav')
RAW_INPUT2 = relpath('data/Short_Files/Raw/Raw2.wav')
RAW_INPUT3 = relpath('data/Short_Files/Raw/Raw3.wav')
RAW_INPUT4_1 = relpath('data/Short_Files/Raw/Raw4.wav')
RAW_INPUT4_2 = relpath('data/Short_Files/Raw/Raw4_2.wav')

STEM_INPUT1 = relpath('data/Short_Files/Stems/Stem1.wav')
STEM_INPUT2 = relpath('data/Short_Files/Stems/Stem2.wav')
STEM_INPUT3 = relpath('data/Short_Files/Stems/Stem3.wav')
STEM_INPUT4 = relpath('data/Short_Files/Stems/Stem4.wav')

RAW_FILES_LIST = [RAW_INPUT1, RAW_INPUT2, RAW_INPUT3, RAW_INPUT4_1, RAW_INPUT4_2]
STEM_FILES_LIST = [STEM_INPUT1, STEM_INPUT2, STEM_INPUT3, STEM_INPUT4]

SILENT_FILE = relpath('data/Short_Files/Error_Throwers/Piano_L.R.wav')

WRONG_LENGTH = relpath('data/Short_Files/Error_Throwers/wrong_length.wav')

WRONG_CHANNELS_RAW = relpath('data/Short_Files/StemInRawChannels')
WRONG_CHANNELS_INDIV_RAW = relpath('data/Short_Files/StemInRawChannels/stem_wrong.wav')
WRONG_CHANNELS_LIST = [RAW_INPUT1, RAW_INPUT2, RAW_INPUT3, RAW_INPUT4_1, RAW_INPUT4_2, WRONG_CHANNELS_INDIV_RAW]

WRONG_SR_STEM = relpath('data/Short_Files/Error_Throwers/wrong_sr.wav')
WRONG_BYTE_STEM = relpath('data/Short_Files/Error_Throwers/wrong_bitdepth.wav')


class TestLengthCheck(unittest.TestCase):

    def test_valid_length(self):
        raw_files = RAW_FILES_LIST
        stem_files = STEM_FILES_LIST
        mix_path = VALID_MIX

        actual = validation.length_check(raw_files, stem_files, mix_path)
        expected = {
            'Raw1.wav': True,
            'Raw2.wav': True,
            'Raw3.wav': True,
            'Raw4.wav': True,
            'Raw4_2.wav': True,
            'Stem1.wav': True,
            'Stem2.wav': True,
            'Stem3.wav': True,
            'Stem4.wav': True
        }
        self.assertEqual(actual, expected)

    def test_invalid_length(self):
        raw_files = RAW_FILES_LIST
        stem_files = STEM_FILES_LIST
        mix_path = WRONG_LENGTH_MIX

        actual = validation.length_check(raw_files, stem_files, mix_path)
        expected = {
            'Raw1.wav': False,
            'Raw2.wav': False,
            'Raw3.wav': False,
            'Raw4.wav': False,
            'Raw4_2.wav': False,
            'Stem1.wav': False,
            'Stem2.wav': False,
            'Stem3.wav': False,
            'Stem4.wav': False
        }
        self.assertEqual(actual, expected)

# get_length and is_right_length test
class TestLengthHelper(unittest.TestCase):

    def test_valid_helper_length(self):
        raw_file = RAW_INPUT1
        mix_path = VALID_MIX
        mix_length = validation.get_length(mix_path)

        actual = validation.is_right_length(raw_file, mix_length)
        expected = True
        self.assertEqual(actual, expected)

    def test_invalid_helper_length(self):
        bad_length = WRONG_LENGTH
        mix_path = VALID_MIX
        mix_length = validation.get_length(mix_path)

        actual = validation.is_right_length(bad_length, mix_length)
        expected = False
        self.assertEqual(actual, expected)


class TestEmptyCheck(unittest.TestCase):

    def test_valid_empty(self):
        raw_path = VALID_RAW
        stem_path = VALID_STEMS

        actual = validation.empty_check(raw_path, stem_path)
        expected = {
            'Raw': True,
            'Stems': True,
        }
        self.assertEqual(actual, expected)

    def test_invalid_empty(self):
        raw_path = EMPTY_RAW
        stem_path = VALID_STEMS

        actual = validation.empty_check(raw_path, stem_path)
        expected = {
            'Empty_Test_RAW': False,
            'Stems': True,
        }
        self.assertEqual(actual, expected)

    def test_invalid_empty2(self):
        raw_path = VALID_RAW
        stem_path = EMPTY_STEMS

        actual = validation.empty_check(raw_path, stem_path)
        expected = {
            'Raw': True,
            'Empty_Test_STEMS': False,
        }
        self.assertEqual(actual, expected)

    def test_invalid_empty3(self):
        raw_path = EMPTY_RAW
        stem_path = EMPTY_STEMS

        actual = validation.empty_check(raw_path, stem_path)
        expected = {
            'Empty_Test_RAW': False,
            'Empty_Test_STEMS': False,
        }
        self.assertEqual(actual, expected)

# Empty helper function #

class TestHasWavsCheck(unittest.TestCase):

    def test_valid_has_wavs(self):
        raw_path = VALID_RAW

        actual = validation.has_wavs(raw_path)
        expected = True
        self.assertEqual(actual, expected)

    def test_invalid_has_wavs(self):
        raw_path = EMPTY_RAW

        actual = validation.has_wavs(raw_path)
        expected = False
        self.assertEqual(actual, expected)


#rawfiles stemfiles mix path
class TestSilenceCheck(unittest.TestCase):

    def test_valid_silence(self):
        raw_files = RAW_FILES_LIST
        stem_files = STEM_FILES_LIST
        mix_path = VALID_MIX

        actual = validation.silence_check(raw_files, stem_files, mix_path)
        expected = {
            'Raw1.wav': True,
            'Raw2.wav': True,
            'Raw3.wav': True,
            'Raw4.wav': True,
            'Raw4_2.wav': True,
            'Stem1.wav': True,
            'Stem2.wav': True,
            'Stem3.wav': True,
            'Stem4.wav': True,
            'Mix.wav': True,
        }
        self.assertEqual(actual, expected)

    # def test_invalid_silence(self):
    #     raw_files = RAW_FILES_LIST
    #     stem_files = STEM_FILES_LIST
    #     mix_path = VALID_MIX

    #     actual = validation.silence_check(raw_files, stem_files, mix_path)
    #     expected = {
    #         'Raw1.wav': True,
    #         'Raw2.wav': True,
    #         'Raw3.wav': True,
    #         'Raw4.wav': True,
    #         'Raw4_2.wav': True,
    #         'Stem1.wav': True,
    #         'Stem2.wav': True,
    #         'Stem3.wav': True,
    #         'Stem4.wav': True,
    #         'Mix.wav': True,
    #     }
    #     self.assertEqual(actual, expected)

class TestStatsCheck(unittest.TestCase):

    def test_valid_stats(self):
        raw_files = RAW_FILES_LIST
        stem_files = STEM_FILES_LIST
        mix_path = VALID_MIX

        actual = validation.stats_check(raw_files, stem_files, mix_path)
        expected = {
            'Raw1.wav': True,
            'Raw2.wav': True,
            'Raw3.wav': True,
            'Raw4.wav': True,
            'Raw4_2.wav': True,
            'Stem1.wav': True,
            'Stem2.wav': True,
            'Stem3.wav': True,
            'Stem4.wav': True,
            'Mix.wav': True
        }
        self.assertEqual(actual, expected)

    def test_invalid_stats(self):
        raw_files = WRONG_CHANNELS_LIST
        stem_files = STEM_FILES_LIST
        mix_path = VALID_MIX

        actual = validation.stats_check(raw_files, stem_files, mix_path)
        expected = {
            'Raw1.wav': True,
            'Raw2.wav': True,
            'Raw3.wav': True,
            'Raw4.wav': True,
            'Raw4_2.wav': True,
            'stem_wrong.wav': False,
            'Stem1.wav': True,
            'Stem2.wav': True,
            'Stem3.wav': True,
            'Stem4.wav': True,
            'Mix.wav': True
        }
        self.assertEqual(actual, expected)

# is_right_stats(fpath, type) (type = stem, raw, mix)
class TestStatsHelper(unittest.TestCase):

    def test_valid_stats_helper_raw(self):
        raw_file = RAW_INPUT1

        actual = validation.is_right_stats(raw_file, 'raw')
        expected = True
        self.assertEqual(actual, expected)

    def test_valid_stats_helper_stem(self):
        stem_file = STEM_INPUT1

        actual = validation.is_right_stats(stem_file, 'stem')
        expected = True
        self.assertEqual(actual, expected)

    def test_valid_stats_helper_mix(self):
        mix_file = VALID_MIX

        actual = validation.is_right_stats(mix_file, 'mix')
        expected = True
        self.assertEqual(actual, expected)

    # raw can't be 2 channels
    def test_invalid_channels_raw(self):
        raw_file = WRONG_CHANNELS_INDIV_RAW

        actual = validation.is_right_stats(raw_file, 'raw')
        expected = False
        self.assertEqual(actual, expected)

    def test_invalid_wrong_sr(self):
        stem_file = WRONG_SR_STEM

        actual = validation.is_right_stats(stem_file, 'stem')
        expected = False
        self.assertEqual(actual, expected)

    def test_invalid_wrong_bytedepth(self):
        raw_file = WRONG_BYTE_STEM

        actual = validation.is_right_stats(raw_file, 'raw')
        expected = False
        self.assertEqual(actual, expected)


class TestGetDur(unittest.TestCase):

    def test_valid_get_dur(self):
        example = WRONG_BYTE_STEM

        actual = math.floor(validation.get_dur(example))
        expected = 54.0
        self.assertEqual(actual, expected)

    def test_invalid_get_dur(self):
        example = WRONG_BYTE_STEM

        actual = math.floor(validation.get_dur(example))
        expected = 100.0
        self.assertNotEqual(actual, expected)


class TestIsAlignedCheck(unittest.TestCase):

    def test_valid_alignment(self):
        raw_files = RAW_FILES_LIST
        stem_files = STEM_FILES_LIST
        raw_path = VALID_RAW
        stem_path = VALID_STEMS
        mix_path = VALID_MIX

        actual = validation.is_aligned(raw_files, stem_files, raw_path, stem_path, mix_path)
        expected = {'Raw': True}, {'Stems': True}
        
        self.assertEqual(actual, expected)

    def test_invalid_alignment(self):
        raw_files = RAW_FILES_LIST
        stem_files = MISALIGNED_STEMS_LIST
        raw_path = MISALIGNED_RAW
        stem_path = MISALIGNED_STEMS
        mix_path = VALID_MIX

        actual = validation.is_aligned(raw_files, stem_files, raw_path, stem_path, mix_path)
        expected = {'Raw': True}, {'MisalignedStems': False}
        
        self.assertEqual(actual, expected)


# Works - need to make sure that empty check is before other checks because pysox can't run on empty #
class TestCreateProblems(unittest.TestCase):

    def test_empty_create_problems(self):
        raw_path = VALID_RAW
        stem_path = VALID_STEMS
        mix_path = VALID_MIX
        file_status = validation.check_audio(raw_path, stem_path, mix_path)

        actual = validation.create_problems(file_status)
        expected = []
        
        self.assertEqual(actual, expected)

    def test_error_create_problems(self):
        raw_path = VALID_RAW
        stem_path = MISALIGNED_STEMS
        mix_path = VALID_MIX
        file_status = validation.check_audio(raw_path, stem_path, mix_path)

        actual = validation.create_problems(file_status)
        expected = ['MisalignedStems : Stem files are not aligned with the mix.']
        
        self.assertEqual(actual, expected)


# Slow test... leave commented.
# class TestCheckAudio(unittest.TestCase):

#     def test_valid_check_audio(self):
#         raw_path = VALID_RAW
#         stem_path = VALID_STEMS
#         mix_path = VALID_MIX

#         actual = validation.check_audio(raw_path, stem_path, mix_path)
#         expected = {'Stem1.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Stem2.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Stem3.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Stem4.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Raw1.wav':
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Raw2.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Raw3.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Raw4.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Raw4_2.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Mix.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': None, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Raw': 
#         {
#             'Silent': None, 
#             'Length_As_Mix': None, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': None, 
#             'Empty': True, 
#             'Raw_Sum_Alignment': True, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Stems': 
#         {
#             'Silent': None, 
#             'Length_As_Mix': None, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': None, 
#             'Empty': True, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': True, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }}
#         self.assertEqual(actual, expected)

#def test_invalid_check_audio(self):
#         raw_path = VALID_RAW
#         stem_path = VALID_STEMS
#         mix_path = VALID_MIX

#         actual = validation.check_audio(raw_path, stem_path, mix_path)
#         expected = {'Stem1.wav': 
#         {
#             'Silent': False, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Stem2.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Stem3.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Stem4.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Raw1.wav':
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Raw2.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Raw3.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Raw4.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Raw4_2.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': True, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Mix.wav': 
#         {
#             'Silent': True, 
#             'Length_As_Mix': None, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': True, 
#             'Empty': None, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Raw': 
#         {
#             'Silent': None, 
#             'Length_As_Mix': None, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': None, 
#             'Empty': True, 
#             'Raw_Sum_Alignment': True, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': None, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }, 'Stems': 
#         {
#             'Silent': None, 
#             'Length_As_Mix': None, 
#             'Speech': None, 
#             'Stem_Duplicates': None, 
#             'Wrong_Stats': None, 
#             'Empty': True, 
#             'Raw_Sum_Alignment': None, 
#             'Instrument_Label': None, 
#             'Stem_Sum_Alignment': True, 
#             'Silent_Sections': None, 
#             'Stems_Have_Raw': None, 
#             'Stem_Present_In_Mix': None, 
#             'Raw_Duplicates': None, 
#             'Raws_Match_Stems': None
#         }}
#         self.assertEqual(actual, expected)
