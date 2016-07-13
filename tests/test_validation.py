import unittest
import os
from new_multitrack import new_multitrack, validation
import glob


def relpath(f):
    return os.path.join(os.path.dirname(__file__), f)


#test inputs here with our files
VALID_MIX = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_MIX.wav')

VALID_RAW = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW')
VALID_STEMS = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS')

WRONG_LENGTH_MIX = relpath('data/Phoenix_ScotchMorris/Piano_L.R.wav')

EMPTY_STEMS = relpath('data/Phoenix_ScotchMorris/Empty_Test_STEMS')
EMPTY_RAW = relpath('data/Phoenix_ScotchMorris/Empty_Test_RAW')

MISALIGNED_STEMS = relpath('data/Phoenix_ScotchMorris_Alignment/Phoenix_ScotchMorris_RAW')
MISALIGNED_RAW = relpath('data/Phoenix_ScotchMorris_Alignment/Phoenix_ScotchMorris_STEMS')

RAW_INPUT1 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_01_01.wav')
RAW_INPUT2 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_02_01.wav')
RAW_INPUT3 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_03_01.wav')
RAW_INPUT4_1 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_04_01.wav')
RAW_INPUT4_2 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_04_02.wav')

STEM_INPUT1 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_01.wav')
STEM_INPUT2 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_02.wav')
STEM_INPUT3 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_03.wav')
STEM_INPUT4 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_04.wav')

SILENT_FILE = relpath('data/Phoenix_ScotchMorris/Piano_L.R.wav')

WRONG_CHENNELS_RAW = relpath('data/Phoenix_ScotchMorris_ChannelTest/Phoenix_ScotchMorris_RAW')
WRONG_CHANNELS_STEMS = relpath('data/Phoenix_ScotchMorris_ChannelTest/Phoenix_ScotchMorris_STEMS')


RAW_FILES_LIST = [RAW_INPUT1, RAW_INPUT2, RAW_INPUT3, RAW_INPUT4_1, RAW_INPUT4_2]
STEM_FILES_LIST = [STEM_INPUT1, STEM_INPUT2, STEM_INPUT3, STEM_INPUT4]

# each check and helper should have seperate class

#class IsSilenceTest(unittest.TestCase):

    # def test_is_silence(self):
    #     actual = validation.is_silence(SILENT_FILE)
    #     expected = True
    #     self.assertEqual(actual, expected)

    # def test_is_not_silence(self):
    #     actual = validation.is_silence(RAW_INPUT3)
    #     expected = False
    #     self.assertEqual(actual, expected)


#TEMPLATE
class TestLengthCheck(unittest.TestCase):

    def test_valid_length(self):
        raw_files = RAW_FILES_LIST
        stem_files = STEM_FILES_LIST
        mix_path = VALID_MIX

        actual = validation.length_check(raw_files, stem_files, mix_path)
        expected = {
            'Phoenix_ScotchMorris_RAW_01_01.wav': True,
            'Phoenix_ScotchMorris_RAW_02_01.wav': True,
            'Phoenix_ScotchMorris_RAW_03_01.wav': True,
            'Phoenix_ScotchMorris_RAW_04_01.wav': True,
            'Phoenix_ScotchMorris_RAW_04_02.wav': True,
            'Phoenix_ScotchMorris_STEM_01.wav': True,
            'Phoenix_ScotchMorris_STEM_02.wav': True,
            'Phoenix_ScotchMorris_STEM_03.wav': True,
            'Phoenix_ScotchMorris_STEM_04.wav': True
        }
        self.assertEqual(actual, expected)

    def test_invalid_length(self):
        raw_files = RAW_FILES_LIST
        stem_files = STEM_FILES_LIST
        mix_path = WRONG_LENGTH_MIX

        actual = validation.length_check(raw_files, stem_files, mix_path)
        expected = {
            'Phoenix_ScotchMorris_RAW_01_01.wav': False,
            'Phoenix_ScotchMorris_RAW_02_01.wav': False,
            'Phoenix_ScotchMorris_RAW_03_01.wav': False,
            'Phoenix_ScotchMorris_RAW_04_01.wav': False,
            'Phoenix_ScotchMorris_RAW_04_02.wav': False,
            'Phoenix_ScotchMorris_STEM_01.wav': False,
            'Phoenix_ScotchMorris_STEM_02.wav': False,
            'Phoenix_ScotchMorris_STEM_03.wav': False,
            'Phoenix_ScotchMorris_STEM_04.wav': False
        }
        self.assertEqual(actual, expected)


class TestStatsCheck(unittest.TestCase):

    def test_valid_stats(self):
        raw_files = RAW_FILES_LIST
        stem_files = STEM_FILES_LIST
        mix_path = VALID_MIX

        actual = validation.stats_check(raw_files, stem_files, mix_path)
        expected = {
            'Phoenix_ScotchMorris_RAW_01_01.wav': True,
            'Phoenix_ScotchMorris_RAW_02_01.wav': True,
            'Phoenix_ScotchMorris_RAW_03_01.wav': True,
            'Phoenix_ScotchMorris_RAW_04_01.wav': True,
            'Phoenix_ScotchMorris_RAW_04_02.wav': True,
            'Phoenix_ScotchMorris_STEM_01.wav': True,
            'Phoenix_ScotchMorris_STEM_02.wav': True,
            'Phoenix_ScotchMorris_STEM_03.wav': True,
            'Phoenix_ScotchMorris_STEM_04.wav': True,
            'Phoenix_ScotchMorris_MIX.wav': True,
        }
        self.assertEqual(actual, expected)

    # fix this, make a file list that contains the wrong channel file
    def test_invalid_stats(self):
        raw_files = RAW_FILES_LIST
        stem_files = STEM_FILES_LIST
        mix_path = WRONG_LENGTH_MIX

        actual = validation.stats_check(raw_files, stem_files, mix_path)
        expected = {
            'Phoenix_ScotchMorris_RAW_01_01.wav': False,
            'Phoenix_ScotchMorris_RAW_02_01.wav': False,
            'Phoenix_ScotchMorris_RAW_03_01.wav': False,
            'Phoenix_ScotchMorris_RAW_04_01.wav': False,
            'Phoenix_ScotchMorris_RAW_04_02.wav': False,
            'Phoenix_ScotchMorris_STEM_01.wav': False,
            'Phoenix_ScotchMorris_STEM_02.wav': False,
            'Phoenix_ScotchMorris_STEM_03.wav': False,
            'Phoenix_ScotchMorris_STEM_04.wav': False
        }
        self.assertEqual(actual, expected)
