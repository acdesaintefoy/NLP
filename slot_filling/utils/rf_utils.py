import re

def clean_word(word):
    word = word.replace(' ','')
    word = word.replace('.','')
    return word

def rm_mltp(text):
	text = re.sub(' +', ' ',text)
	return text

def alternative_data_base(data):
    new_data = []
    for element in data:
        for key,value in element.items():
            list_temp = []
            for dico in value:
                text = rm_mltp(dico['text'])
                for word in text.split(' '):
                    if word == ' ':
                        print(text)
                    cleaned_word = clean_word(word)
                    if cleaned_word != '':
                        unite_dico = {'text' : cleaned_word}
                        if 'entity' in dico.keys():
                            unite_dico['entity'] = dico['entity']
                        else :
                            unite_dico['entity'] = 'None'
                        list_temp.append(unite_dico)
        new_data.append(list_temp)
    return new_data

#Rajouter une fonction pour le nombre de majuscule par exemple
def word2features(query, i):
    word = query[i]['text']
    sentence = ' '.join([element["text"] for element in query])

    # Common features for all words
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'place_in_query=%s' % str(i),
        'len_query=%s' % str(len(query))
    ]

    # Features for words that are not
    # at the beginning of a query
    if i > 0:
        word1 = query[i-1]['text']
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isdigit=%s' % word1.isdigit()
        ])
    else:
        # Indicate that it is the 'beginning of a query'
        features.append('BOS')

    # Features for words that are not
    # at the end of a query
    if i < len(query)-1:
        word1 = query[i+1]['text']
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isdigit=%s' % word1.isdigit()
        ])

    features.append(sentence)
    return features

# A function for extracting features in queries
def extract_features(query):
    return [word2features(query, i) for i in range(len(query))]

# A function fo generating the list of labels for each query
def get_entities(query):
    return [word['entity'] for word in query]

def extract_words_from_X(X):
    return [features[1].replace('word.lower=','')for features in X]