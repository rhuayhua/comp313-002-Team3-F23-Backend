import spacy
import pandas as pd
import numpy as np
import re
from sklearn.dummy import DummyClassifier
import pickle
from keras.preprocessing.sequence import pad_sequences
from keras.saving import load_model
from keras.models import Sequential
from keras.layers import Conv1D, MaxPool1D, GlobalMaxPooling1D, Dense, LSTM, Embedding, SpatialDropout1D
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.initializers import Constant
from gensim.models import KeyedVectors


class MLService:
    def get_keywords(self, df):
        # Pre-process data
        df['jobDescription'] = df['jobDescription'].str.replace(
            r'\x96', ' ', regex=True)
        lines_extracted = pre_process_text(df['jobDescription'][0])

        # Extract noun phrases
        list_noun_phrases = extract_noun_phrases(lines_extracted)
        lowercased_noun_phrases = [string.lower()
                                   for string in list_noun_phrases]
        print('\nORIG noun phrases:{}'.format(list_noun_phrases))
        print('\nLOWERCASE noun phrases:{}'.format(lowercased_noun_phrases))

        # # to be used
        # with open("/app/Capabilities/tokenizer.pickle", "rb") as file:
        #     tokenizer = pickle.load(file)

        # # to be used
        # test_t = tokenizer.texts_to_sequences(np.asarray(list_noun_phrases))
        # test_t_padding = pad_sequences(test_t, 50)
        # print(test_t_padding)

        # load keras model
        # model_cnn = load_model("/app/Capabilities/CNN_model.keras")

        # Opening dummy  model
        with open("/app/Capabilities/model_dummy.pkl", "rb") as file:
            model = pickle.load(file)

        # get prediction from model
        prediction = model.predict(lowercased_noun_phrases)
        print("The result is", prediction)
        return list_noun_phrases[prediction == 1].tolist()


def pre_process_text(text):
    pattern = r"(?m)^[\s]*([\u2022\xb7]|\d+\)|\-|\d+\.)\s*(.*)$"
    # Finding all matches in the text
    print('\nTEXT : {}'.format(text))
    matches = re.findall(pattern, text)
    print('\nMATCHES: {}'.format(matches))
    return matches


def extract_noun_phrases(list_text):
    clean_list_np = []
    nlp = spacy.load('en_core_web_sm')
    if (len(list_text) > 0):
        for line in list_text:
            print('\nLINE: {}'.format(line[-1]))
            text = line[-1]
            # print(text)
            doc = nlp(text)
            for chunk in doc.noun_chunks:
                clean_np = []
                for token in chunk:
                    if (token.pos_ != 'PRON' and token.pos_ != 'DET' and token.text != '(' and token.text != '"' and token.text != '*'):
                        clean_np.append(str(token))
                t1 = " ".join(clean_np)

                if (chunk.root.text not in ['that', '-', '#']):
                    if ((chunk.root.dep_ == 'dobj') and (chunk.root.pos_ != 'PROPN')):
                        # new_chunk = chunk.root.head.lemma_ + " " + chunk.text
                        new_chunk = chunk.root.head.lemma_ + " " + t1
                        clean_list_np.append(new_chunk.strip())
                    else:
                        if (len(t1) > 0):
                            clean_list_np.append(t1.strip())

    all_noun_phrases = np.unique(clean_list_np)
    return np.asanyarray(all_noun_phrases)
