import sox
import librosa
import tempfile as tmp
import numpy as np
from sklearn.externals import joblib

CLF = joblib.load("instrument_clf.pkl")
MFCC_MEANS = np.load("mfcc_means.npy")
MFCC_STD = np.load("mfcc_std.npy")
LABEL_VALUES = np.load("label_values.npy")
THRESH = 0.5

def clf_predict(audio_fpath, user_label):
    # normalizing volume, removing silence
    temp_fpath = tmp.NamedTemporaryFile(suffix=".wav")
    tfm = sox.Transformer()
    tfm.norm(db_level=-6)
    tfm.silence()
    tfm.build(audio_fpath, temp_fpath.name)
        
    # load audio
    y, fs = librosa.load(temp_fpath.name)
        
    # compute MFCCs
    M = librosa.feature.mfcc(y, sr=fs, n_mfcc=40)
    M_normal = (M - MFCC_MEANS)/MFCC_STD
    
    predicted_label = CLF.predict(M_normal.T)

    user_label_index = np.where(LABEL_VALUES==user_label)[0]

    user_label_prob = np.mean(predicted_label[user_label_index])

    if user_label_prob < THRESH:
        return False
    else:
        return True
