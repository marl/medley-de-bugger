import unittest
import os
from new_multitrack import new_multitrack, validation, wave_silence

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

STEM_INPUT1 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_01.wav')
STEM_INPUT2 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_02.wav')
STEM_INPUT3 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_03.wav')
STEM_INPUT4 = relpath('data/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_04.wav')

EMPTY_STEMS = relpath('data/Phoenix_ScotchMorris/Empty_Test_STEMS')
EMPTY_RAW = relpath('data/Phoenix_ScotchMorris/Empty_Test_RAW')

SILENCE = relpath('data/silence.wav')

# def new_combiner(combiner='concatenate'):
#     return combine.Combiner(
#         [INPUT_WAV, INPUT_WAV], OUTPUT_FILE, combiner
#     )

class Test1(unittest.TestCase):

    # def setUp(self): #????
    #     self.cbn = new_combiner()

    def test_empty_stems(self):
        valid, problems = new_multitrack.checkAudio(RAW_FOLDER, EMPTY_STEMS, MIX_INPUT)
        self.assertEqual(valid, False)

        result = False
        if('Stem folder has no wav files' in problems):
            result = True

        self.assertEqual(result, True)

    def test_empty_raw(self): #CHECK ORDER OF CHECK AUDIO ARGS
        valid, problems = new_multitrack.checkAudio(EMPTY_RAW, RAW_FOLDER, MIX_INPUT)
        self.assertEqual(valid, False)
        self.assertIn('Raw folder has no wav files', problems)

    def test_silence(self):
        self.assertEqual(wave_silence.is_silence(SILENCE, threshold=16, framesize=None), True)


