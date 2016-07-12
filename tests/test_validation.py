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

# RAW_INPUT1 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_01_01.wav')
# RAW_INPUT2 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_02_01.wav')
# RAW_INPUT3 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_03_01.wav')
# RAW_INPUT4_1 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_04_01.wav')
# RAW_INPUT4_2 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_04_02.wav')

# STEM_INPUT1 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_01.wav')
# STEM_INPUT2 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_02.wav')
# STEM_INPUT3 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_03.wav')
# STEM_INPUT4 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_04.wav')

SILENT_FILE = relpath('data/Phoenix_ScotchMorris/Piano_L.R.wav')

WRONG_CHENNELS_RAW = relpath('data/Phoenix_ScotchMorris_ChannelTest/Phoenix_ScotchMorris_RAW')
WRONG_CHANNELS_STEMS = relpath('data/Phoenix_ScotchMorris_ChannelTest/Phoenix_ScotchMorris_STEMS')


# RAW_FILES = [RAW_INPUT1, RAW_INPUT2, RAW_INPUT3, RAW_INPUT4_1, RAW_INPUT4_2]
# STEM_FILES = [STEM_INPUT1, STEM_INPUT2, STEM_INPUT3, STEM_INPUT4]

# class IsSilenceTest(unittest.TestCase):

#     def test_is_silence(self):
#         actual = validation.is_silence(SILENT_FILE)
#         expected = True
#         self.assertEqual(actual, expected)

#     def test_is_not_silence(self):
#         actual = validation.is_silence(RAW_INPUT3)
#         expected = False
#         self.assertEqual(actual, expected)


#TEMPLATE
class TestLengthCheck(unittest.TestCase):

    def test_valid_length(self):
        raw_files = VALID_RAW
        stem_files = VALID_STEMS
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
        raw_files = VALID_RAW
        stem_files = VALID_STEMS
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


class CheckAudioTest(unittest.TestCase):

    # This error-free initialization test passes - commented so other tests on same inputs will pass. #
    # def test_no_problems_1(self):
    #     file_status = validation.check_audio(VALID_RAW, VALID_STEMS, VALID_MIX)
    #     problems = validation.create_problems(file_status)

    #     self.assertEqual([], problems)

    def setUp(self):
        self.raw_files = glob.glob(os.path.join(VALID_RAW, "*.wav"))
        self.stem_files = glob.glob(os.path.join(VALID_STEMS, "*.wav"))
        self.mix_path = VALID_MIX


    def test_align_false(self):
        file_status = validation.check_audio(MISALIGNED_STEMS, ALIGN_TEST_STEMS, ALIGN_TEST_MIX)
        problems = validation.create_problems(file_status)
        print problems
        self.assertIn('Phoenix_ScotchMorris_STEMS : Stem files are not aligned with the mix.', problems)
        self.assertNotIn('Phoenix_ScotchMorris_RAW : Raw files are not aligned with the mix.', problems)
    
    # def test_empty_stems(self):
    #     file_status = validation.check_audio(VALID_RAW, EMPTY_STEMS, VALID_MIX)
    #     problems = validation.create_problems(file_status)

    #     self.assertIn('Empty_Test_STEMS : Folder is empty.', problems)

    # def test_empty_raw(self):
    #     file_status = validation.check_audio(EMPTY_RAW, VALID_STEMS, VALID_MIX)
    #     problems = validation.create_problems(file_status)
        
    #     self.assertIn('Empty_Test_RAW : Folder is empty.', problems)

    # def test_empty_both(self):
    #     file_status = validation.check_audio(EMPTY_RAW, EMPTY_STEMS, VALID_MIX)
    #     problems = validation.create_problems(file_status)
        
    #     self.assertIn('Empty_Test_RAW : Folder is empty.', problems)
    #     self.assertIn('Empty_Test_STEMS : Folder is empty.', problems)

    # def test_silence_mix(self):
    #     file_status = validation.check_audio(VALID_RAW, VALID_STEMS, SILENT_FILE)
    #     problems = validation.create_problems(file_status)

    #     self.assertIn('Piano_L.R.wav : File is silent.', problems)

    # def test_channels_error(self):
    #     file_status = validation.check_audio(WRONG_CHENNELS_RAW, WRONG_CHANNELS_STEMS, CHAN_TEST_MIX)
    #     problems = validation.create_problems(file_status)
    
    #     self.assertIn('stem_wrong.wav : File format is incorrect.', problems)

    # def test_length_error(self):
    #     file_status = validation.check_audio(VALID_RAW, VALID_STEMS, VALID_MIX)
    #     problems = validation.create_problems(file_status)
    
    #     self.assertIn('wrong_length.wav : File is not correct length.', problems)




