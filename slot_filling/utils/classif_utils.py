import numpy as np

def flatten(dict_data):
    dict_data = dict_data["data"]
    sentence = ""
    for words in dict_data:
        sentence += words['text']
    return sentence

def multi_label(i):
    multi_lab = np.zeros(8)
    multi_lab[i] = 1
    return multi_lab