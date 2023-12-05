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

        # Set parameters
        MAX_NUM_WORDS = 10000
        MAX_SEQUENCE = 50
        EMB_DIM = 300
        THRESHOLD = 0.9

        # Loading Tokenizer
        with open("/app/Capabilities/tokenizer.pickle", "rb") as file:
            tokenizer = pickle.load(file)

        # Loading embedding matrix
        with open("/app/Capabilities/embedding_matrix_w2v.pickle", "rb") as file:
            embedding_matrix_w2v = pickle.load(file)

        # Loading dummy  model
        with open("/app/Capabilities/model_dummy.pkl", "rb") as file:
            model = pickle.load(file)

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

        # Tokenize data
        test_tok = tokenizer.texts_to_sequences(
            np.asarray(lowercased_noun_phrases))
        word_index = tokenizer.word_index
        print('\nTOKENS: {}'.format(test_tok))

        # Padding tokens
        test_tok_padding = pad_sequences(test_tok, maxlen=MAX_SEQUENCE)
        print('\nafter PADDING: {}'.format(test_tok_padding))

        num_words_w2v = min(MAX_NUM_WORDS, len(word_index)) + 1
        embedding_layer_w2v = Embedding(num_words_w2v, EMB_DIM,
                                        embeddings_initializer=Constant(
                                            embedding_matrix_w2v),
                                        input_length=MAX_SEQUENCE, trainable=False)

        # LSTM network
        lstm_w2v = Sequential()
        lstm_w2v.add(embedding_layer_w2v)
        lstm_w2v.add(SpatialDropout1D(0.2))  # Using an ideal value for RNN's
        lstm_w2v.add(LSTM(256, dropout=0.2, recurrent_dropout=0.2))
        lstm_w2v.add(Dense(128, activation='relu'))
        lstm_w2v.add(Dense(64, activation='relu'))
        lstm_w2v.add(Dense(32, activation='relu'))
        lstm_w2v.add(Dense(1, activation='sigmoid'))
        lstm_w2v.load_weights("/app/Capabilities/lstm_weights.h5")
        lstm_predictions = lstm_w2v.predict(test_tok_padding)
        index_lstm_pred = (lstm_predictions > THRESHOLD).flatten().tolist()

        print('Prediction from LSTM: {}'.format(lstm_predictions))
        print('boolean LSTM: {}'.format(index_lstm_pred))

        # get prediction from model
        # prediction = model.predict(lowercased_noun_phrases)
        # print("Dummy result is: ", prediction)
        # return list_noun_phrases[prediction == 1].tolist()
        return list_noun_phrases[index_lstm_pred].tolist()


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
