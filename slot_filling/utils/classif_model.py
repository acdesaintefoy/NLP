import pickle
from keras.preprocessing.sequence import pad_sequences

def multi_lab_to_query_type(lab):
    return list_of_query_type[np.argmax(lab)]

def predict(query_batch):
    # loading tokenizer
    with open(f"{models_path}tokenizer.pickle", 'rb') as handle:
        tokenizer = pickle.load(handle)
    
    X = tokenizer.texts_to_sequences(query_batch)
    X = pad_sequences(X, maxlen = 40)
    
    model = load_model(f"{models_path}lstm_classif_type.h5")
    pred = model.predict(X)
    print(pred)
    
    n = len(X)
    lab_pred = np.zeros(n)
    
    for i in range(n):
        lab_pred[i] = np.argmax(pred[i])
    
    return lab_pred