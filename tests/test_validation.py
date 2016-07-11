import unittest
import os
from new_multitrack import new_multitrack, validation
import glob

#from validation import check_audio, create_problems
#UNIT TESTS!!!!



def relpath(f):
    return os.path.join(os.path.dirname(__file__), f)
    #return os.path.abspath(path)
#test inputs here with our files
MIX_INPUT = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_MIX.wav')

RAW_FOLDER = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW')
STEM_FOLDER = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS')

RAW_INPUT1 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_01_01.wav')
RAW_INPUT2 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_02_01.wav')
RAW_INPUT3 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_03_01.wav')
RAW_INPUT4_1 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_04_01.wav')
RAW_INPUT4_2 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_RAW/Phoenix_ScotchMorris_RAW_04_02.wav')

STEM_INPUT1 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_02.wav')
STEM_INPUT2 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_02.wav')
STEM_INPUT3 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_03.wav')
STEM_INPUT4 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_04.wav')

EMPTY_STEMS = relpath('data/Phoenix_ScotchMorris/Empty_Test_STEMS')
EMPTY_RAW = relpath('data/Phoenix_ScotchMorris/Empty_Test_RAW')

SILENCE = relpath('data/Phoenix_ScotchMorris/Piano_L.R.wav')

CHAN_TEST_RAW = relpath('data/Phoenix_ScotchMorris_ChannelTest/Phoenix_ScotchMorris_RAW')
CHAN_TEST_STEMS = relpath('data/Phoenix_ScotchMorris_ChannelTest/Phoenix_ScotchMorris_STEMS')
CHAN_TEST_MIX = relpath('data/Phoenix_ScotchMorris_ChannelTest/Phoenix_ScotchMorris_MIX.wav')

RAW_FILES = [RAW_INPUT1, RAW_INPUT2, RAW_INPUT3, RAW_INPUT4_1, RAW_INPUT4_2]
STEM_FILES = [STEM_INPUT1, STEM_INPUT2, STEM_INPUT3, STEM_INPUT4]

# class IsSilenceTest(unittest.TestCase):

#     def test_is_silence(self):
#         actual = validation.is_silence(SILENCE)
#         expected = True
#         self.assertEqual(actual, expected)

#     def test_is_not_silence(self):
#         actual = validation.is_silence(RAW_INPUT3)
#         expected = False
#         self.assertEqual(actual, expected)


class CheckAudioTest(unittest.TestCase):

    # This error-free initialization test passes - commented so other tests on same inputs will pass. #
    # def test_no_problems_1(self):
    #     file_status = validation.check_audio(RAW_FOLDER, STEM_FOLDER, MIX_INPUT)
    #     problems = validation.create_problems(file_status)

    #     self.assertEqual([], problems)

    def setUp(self):
        self.raw_files = glob.glob(os.path.join(RAW_FOLDER, "*.wav"))
        self.stem_files = glob.glob(os.path.join(STEM_FOLDER, "*.wav"))
        self.mix_path = MIX_INPUT

    # the first check is going to be empty check...pysox will not run if the folder is empty
    # def test_align_test(self):
    #     alignment_dict = validation.alignment_check(RAW_FILES, STEM_FILES, RAW_FOLDER, STEM_FOLDER, MIX_INPUT)
    #     self.assertTrue({'Phoenix_ScotchMorris_STEMS': True} in alignment_dict)

    def test_align_stuff(self):
        file_status = validation.check_audio(RAW_FOLDER, STEM_FOLDER, MIX_INPUT)
        problems = validation.create_problems(file_status)

        self.assertEqual([], problems)

    # def test_empty_stems(self):
    #     file_status = validation.check_audio(RAW_FOLDER, EMPTY_STEMS, MIX_INPUT)
    #     problems = validation.create_problems(file_status)

    #     self.assertIn('Empty_Test_STEMS : Folder is empty.', problems)

    # def test_empty_raw(self):
    #     file_status = validation.check_audio(EMPTY_RAW, STEM_FOLDER, MIX_INPUT)
    #     problems = validation.create_problems(file_status)
        
    #     self.assertIn('Empty_Test_RAW : Folder is empty.', problems)

    # def test_empty_both(self):
    #     file_status = validation.check_audio(EMPTY_RAW, EMPTY_STEMS, MIX_INPUT)
    #     problems = validation.create_problems(file_status)
        
    #     self.assertIn('Empty_Test_RAW : Folder is empty.', problems)
    #     self.assertIn('Empty_Test_STEMS : Folder is empty.', problems)

    # def test_silence_mix(self):
    #     file_status = validation.check_audio(RAW_FOLDER, STEM_FOLDER, SILENCE)
    #     problems = validation.create_problems(file_status)

    #     self.assertIn('Piano_L.R.wav : File is silent.', problems)

    # def test_channels_error(self):
    #     file_status = validation.check_audio(CHAN_TEST_RAW, CHAN_TEST_STEMS, CHAN_TEST_MIX)
    #     problems = validation.create_problems(file_status)
    
    #     self.assertIn('stem_wrong.wav : File format is incorrect.', problems)

    # def test_length_error(self):
    #     file_status = validation.check_audio(RAW_FOLDER, STEM_FOLDER, MIX_INPUT)
    #     problems = validation.create_problems(file_status)
    
    #     self.assertIn('wrong_length.wav : File is not correct length.', problems)




