import pickle
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import os, sys, numpy as np

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
models_path = f'{module_path}/models/'

def multi_lab_to_query_type(lab):
    return list_of_query_type[np.argmax(lab)]

def predict(query_batch):
    query_type_dict = {0: 'PlayMusic',1: 'BookRestaurant',2: 'AddToPlaylist',3: 'GetWeather',4: 
    'SearchCreativeWork',5: 'SearchScreeningEvent',6: 'RateBook'}
    # loading tokenizer
    with open(f"{models_path}tokenizer.pickle", 'rb') as handle:
        tokenizer = pickle.load(handle)
    
    X = tokenizer.texts_to_sequences(query_batch)
    X = pad_sequences(X, maxlen = 40)
    
    model = load_model(f"{models_path}lstm_classif_type.h5")
    pred = model.predict(X)
    
    n = len(X)
    lab_pred = np.zeros(n)
    
    for i in range(n):
        lab_pred[i] = np.argmax(pred[i])
    
    return [ query_type_dict[lab] for lab in lab_pred]