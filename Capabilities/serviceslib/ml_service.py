import spacy
import pandas as pd
import numpy as np
import re
import json
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
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
        # define pipeline
        pipeline_preprocessing = Pipeline([
            ('pre_process_text', PreProcessText('jobDescription')),
            ('GetNounPhrases', GetNounPhrases('jobDescription'))
        ])

        # list with noun phrases
        list_noun_phrases = pipeline_preprocessing.transform(df)

        # to be used
        with open("/app/Capabilities/tokenizer.pickle", "rb") as file:
            tokenizer = pickle.load(file)

        # to be used
        test_t = tokenizer.texts_to_sequences(np.asarray(list_noun_phrases))
        test_t_padding = pad_sequences(test_t, 50)
        print(test_t_padding)

        # load keras model
        # model_cnn = load_model("/app/Capabilities/CNN_model.keras")

        # Opening dummy  model
        with open("/app/Capabilities/model_dummy.pkl", "rb") as file:
            model = pickle.load(file)

        # get prediction from model
        prediction = model.predict(list_noun_phrases)
        print("The result is", prediction)
        return list_noun_phrases[prediction == 1].tolist()


class PreProcessText(BaseEstimator):
    def __init__(self, col):
        self.col = col

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X[self.col] = X[self.col].str.replace(r'\.?\n+', '. ', regex=True)
        X[self.col] = X[self.col].str.replace(r'\x95', '', regex=True)
        X[self.col] = X[self.col].str.replace(r'^-\s?', '', regex=True)
        X[self.col] = X[self.col].str.replace(
            r'^\s?\d\)?\s?\.\s?', '', regex=True)
        X[self.col] = X[self.col].str.replace(r'[\.\.\.]', ' ', regex=True)
        X[self.col] = X[self.col].str.replace(r'"', ' ', regex=True)
        X[self.col] = X[self.col].str.replace(r':', ' ', regex=True)
        X[self.col] = X[self.col].str.replace(r'\*', '', regex=True)
        X[self.col] = X[self.col].str.replace(r'\(', ' ', regex=True)
        X[self.col] = X[self.col].str.replace(r'\)', ' ', regex=True)
        X[self.col] = X[self.col].str.replace(r'\s+', ' ', regex=True)
        return X


class GetNounPhrases(BaseEstimator):
    def __init__(self, col):
        self.col = col

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(X[self.col][0])
        all_noun_phrases = []
        for chunk in doc.noun_chunks:
            elements = []
            for token in chunk:
                if (token.pos_ != 'PRON' and token.pos_ != 'DET'):
                    elements.append(str(token))
            # list of elements to string
            if (len(elements) > 0):
                single_noun_phrase = ' '.join(elements)
                split_np = []
                if (',' in single_noun_phrase):
                    split_np = re.split(r'[,]', single_noun_phrase)
                    for i in range(len(split_np) - 1):
                        split_np[i] = re.sub(r'^\s+', '', split_np[i])
                        split_np[i] = re.sub(r'\s+$', '', split_np[i])
                        split_np[i] += " " + chunk.root.text
                    split_np[-1] = re.sub(r'^\s*[and]*\s*', '', split_np[-1])
                    for i in split_np:
                        all_noun_phrases.append(i.lower())
                else:
                    # add noun phrase string to total list
                    all_noun_phrases.append(single_noun_phrase.lower())
        all_noun_phrases = np.unique(all_noun_phrases)
        return np.asanyarray(all_noun_phrases)
