import unittest
import os
from new_multitrack import new_multitrack, validation
import glob
import math
from unittest import TestCase


TestCase.maxDiff = None

def relpath(f):
    return os.path.join(os.path.dirname(__file__), f)

# TESTS WITH SHORTENED FILES
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

# Empty helper function 
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


class TestIsSilence(unittest.TestCase):

    def test_is_silence_valid(self):
        silent_file = SILENT_FILE
        actual = validation.is_silence(silent_file)
        expected = True
        self.assertEqual(actual, expected)

    def test_is_silence_invalid(self):
        silent_file = RAW_INPUT1
        actual = validation.is_silence(silent_file)
        expected = False
        self.assertEqual(actual, expected)


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


class TestAnalyzeMix(unittest.TestCase):

    def test_get_coeffs(self):
        raw_files = RAW_FILES_LIST
        stem_files = STEM_FILES_LIST
        mix_path = VALID_MIX

        actual = validation.get_coeffs(raw_files, stem_files, mix_path)
        expected = ({'Stem4.wav': 0.3, 'Stem2.wav': 0.3914442544097783, 'Stem3.wav': 0.5948751700839973, 'Stem1.wav': 0.33008826259331703}, {'Raw2.wav': 0.0, 'Raw3.wav': 0.0, 'Raw4.wav': 0.15583858172757337, 'Raw4_2.wav': 0.0, 'Raw1.wav': 0.0})
        self.assertEqual(actual, expected) #0.6847636702791934


class TestAlignmentHelper(unittest.TestCase):

    def test_alignment_helper(self):
        raw_files = [RAW_INPUT1]
        target_path = STEM_INPUT1

        actual = validation.alignment_helper(raw_files, target_path)
        expected = True
        self.assertEqual(actual, expected)

    def test_alignment_helper_invalid(self):
        raw_files = [RAW_INPUT4_2, RAW_INPUT4_1]
        target_path = STEM_INPUT4

        actual = validation.alignment_helper(raw_files, target_path)
        expected = True
        self.assertEqual(actual, expected)

    def test_helper(self):
        stem_files = STEM_FILES_LIST
        target_path = VALID_MIX

        actual = validation.alignment_helper(stem_files, target_path)
        expected = True
        self.assertEqual(actual, expected)


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
        raw_files = RAW_FILES_LIST
        stem_files = MISALIGNED_STEMS_LIST
        mix_path = VALID_MIX
        raw_info = {'Raw2.wav': {'path': '/Users/juliawilkins/Desktop/medleydb_work/medleydb_app/tests/data/Short_Files/Raw/Raw2.wav', 'inst': 'darbuka', 'stem': 'Stem3Misaligned.wav'}, 'Raw3.wav': {'path': '/Users/juliawilkins/Desktop/medleydb_work/medleydb_app/tests/data/Short_Files/Raw/Raw3.wav', 'inst': 'distorted electric guitar', 'stem': 'Stem1Misaligned.wav'}, 'Raw4.wav': {'path': '/Users/juliawilkins/Desktop/medleydb_work/medleydb_app/tests/data/Short_Files/Raw/Raw4.wav', 'inst': 'darbuka', 'stem': 'Stem3Misaligned.wav'}, 'Raw4_2.wav': {'path': '/Users/juliawilkins/Desktop/medleydb_work/medleydb_app/tests/data/Short_Files/Raw/Raw4_2.wav', 'inst': 'darbuka', 'stem': 'Stem3Misaligned.wav'}, 'Raw1.wav': {'path': '/Users/juliawilkins/Desktop/medleydb_work/medleydb_app/tests/data/Short_Files/Raw/Raw1.wav', 'inst': 'distorted electric guitar', 'stem': 'Stem1Misaligned.wav'}}

        file_status = validation.check_multitrack(raw_files, stem_files, mix_path, raw_info)

        actual = validation.create_problems(file_status)
        expected = ['MisalignedStems : Stem files are not aligned with the mix.', 'Stem1Misaligned.wav : The raw files associated with this stem file are not correctly aligned.', 'Stem3Misaligned.wav : The raw files associated with this stem file are not correctly aligned.']
        
        self.assertEqual(actual, expected)


# We also need a check audio/check multitrack test...TBD it will be slow.ste