# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 22:20:38 2023

@author: stell
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from keras.models import Sequential
from keras.layers import Conv1D, GlobalMaxPooling1D, Dense, LSTM, Embedding, SpatialDropout1D
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.initializers import Constant
from gensim.models import KeyedVectors
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pickle



root = 'C:/Users\stell\Documents\Académico\Centennial College\Fall 2023\COMP 313 - Software Project/NN'
file = 'Data.csv'
path = os.path.join(root,file)

df = pd.read_csv(path)

(df['label'] == 0).sum() #639
(df['label'] == 1).sum() #360

X = np.array(df['noun_phrase'])
y = np.array(df['label'])

split = StratifiedShuffleSplit(n_splits = 1, test_size=0.20, random_state=00)

# 20% testing set | 80% training and validation sets combined
for trainval_index, test_index in split.split(X, y):
    X_trainval, X_test = X [trainval_index], X[test_index]
    y_trainval, y_test = y[trainval_index], y[test_index]


# 70% training set and 30% validation set
split2 = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=00)

for train_index, val_index in split2.split (X_trainval, y_trainval):
    X_train, X_val = X_trainval[train_index], X_trainval[val_index]
    y_train, y_val = y_trainval[train_index], y_trainval[val_index]
    

''' 

Parameters for the Embedding Layers, path and other embedding stuff
    
'''

max_num_words = 10000
max_sequence = 50
emb_dim = 300
word2vec_path = 'C:/Users\stell\Documents\Académico\Centennial College\Fall 2023\COMP 262 - NLP/GoogleNews-vectors-negative300.bin'



'''  ------ Tokenizer, sequences and more ------  '''

tokenizer = Tokenizer(num_words=max_num_words)
tokenizer.fit_on_texts(X_train)

# Converting text to a vector of word indexes; will be used to get the vector
# from w2v and to form the embedding matrix to feed the Embedding Layer
train_sequences = tokenizer.texts_to_sequences(X_train) 
val_sequences = tokenizer.texts_to_sequences (X_val)
test_sequences = tokenizer.texts_to_sequences(X_test)
word_index = tokenizer.word_index


''' -------- Padding ---------------'''

X_train_final = pad_sequences(train_sequences, maxlen=max_sequence)
X_val_final = pad_sequences(val_sequences, maxlen=max_sequence)
X_test_final = pad_sequences(test_sequences, maxlen=max_sequence)


''' ---------------  Word2 Vec  ------------- '''

''' 
word_index is a dictionary of all the unique words in the corpus with a unique 
integer number given by Keras' tokenizer. 

'''

# Load the model
w2v_model = KeyedVectors.load_word2vec_format(word2vec_path, binary=True,)

num_words_w2v = min(max_num_words, len(word_index)) + 1
embedding_matrix_w2v = np.zeros((num_words_w2v, emb_dim))

for key, val in word_index.items():
    if val > max_num_words:
        continue
    
    if key in w2v_model:
        embedding_vector= w2v_model.get_vector(key)
    else:
        embedding_vector = np.zeros(emb_dim)
    
    embedding_matrix_w2v[val] = embedding_vector


embedding_layer_w2v = Embedding(input_dim=num_words_w2v, output_dim=emb_dim, 
                          embeddings_initializer=Constant(embedding_matrix_w2v),
                          input_length=max_sequence, trainable = False)


''' ----------   CNN Model (replica) ---------  '''

cnn_w2v = Sequential()
cnn_w2v.add(Embedding(input_dim=694, output_dim=300, 
                          embeddings_initializer=Constant(embedding_matrix_w2v),
                          input_length=50, trainable = False))
cnn_w2v.add(Conv1D(128, 5, activation='relu'))
cnn_w2v.add(GlobalMaxPooling1D())
cnn_w2v.add(Dense(10, activation='relu'))
cnn_w2v.add(Dense(1, activation='sigmoid'))

cnn_w2v.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

cnn_w2v.summary()

# # Fitting the CNN
cnn_w2v_history = cnn_w2v.fit(X_train_final, y_train, batch_size=100, 
                              epochs=20, validation_data=(X_val_final, y_val))


# # Evaluating test set
score, acc = cnn_w2v.evaluate(X_test_final, y_test)
print('Test accuracy with CNN:', acc)

# # Predictions
cnn_w2v_preds = cnn_w2v.predict(X_test_final)

# Converting probabilities to 0 and 1 using a threshold
threshold = 0.5
y_pred_binary = (cnn_w2v_preds > threshold).astype(int)


# # Plot confusion matrix
cm = confusion_matrix(y_test, y_pred_binary, labels = [0,1])

print (cm)

labels = [0,1]

# Seaborn to the rescue
ax = sns.heatmap(cm, annot=True, annot_kws={'size': 10}, xticklabels=labels, yticklabels=labels, cmap='Blues', linewidths=1, linecolor='black', fmt='d')
ax.set_xlabel ('Predicted', fontsize=10)
ax.set_ylabel('True', fontsize=10)
plt.title ('Confusion Matrix')
plt.axis()
plt.show()


# # saving model
cnn_w2v.save('CNN_model.keras')


## Saving other
cnn_w2v.save('CNN_modelExplicit.keras')

# # Pickling tokenizer

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)


# # Pickling word matrix

with open('embedding_matrix_w2v.pickle', 'wb') as handle:
    pickle.dump(embedding_matrix_w2v, handle, protocol=pickle.HIGHEST_PROTOCOL)



''' ----------   LSTM Model (replica) ---------  '''

lstm_w2v = Sequential()
lstm_w2v.add(embedding_layer_w2v)
lstm_w2v.add(SpatialDropout1D(0.2))  # Using an ideal value for RNN's
lstm_w2v.add(LSTM(256, dropout=0.2, recurrent_dropout=0.2))
lstm_w2v.add(Dense(128, activation='relu'))
lstm_w2v.add(Dense(64, activation='relu'))
lstm_w2v.add(Dense(32, activation='relu'))
lstm_w2v.add(Dense(1, activation='sigmoid'))

lstm_w2v.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

lstm_w2v.summary()

lstm_w2v_history = lstm_w2v.fit(X_train_final, y_train, batch_size=100, 
                              epochs=20, validation_data=(X_val_final, y_val))



# # Evaluating test set
score, acc = lstm_w2v.evaluate(X_test_final, y_test)
print('Test accuracy with LSTM:', acc)

# # Predictions
lstm_w2v_preds = lstm_w2v.predict(X_test_final)

# Converting probabilities to 0 and 1 using a threshold
threshold = 0.5
y_predLSTM_binary = (lstm_w2v_preds > threshold).astype(int)


# # Plot confusion matrix
cm_lstm = confusion_matrix(y_test, y_predLSTM_binary, labels = [0,1])

print (cm)

labels = [0,1]

# Seaborn to the rescue
ax = sns.heatmap(cm_lstm, annot=True, annot_kws={'size': 10}, xticklabels=labels, yticklabels=labels, cmap='Blues', linewidths=1, linecolor='black', fmt='d')
ax.set_xlabel ('Predicted', fontsize=10)
ax.set_ylabel('True', fontsize=10)
plt.title ('Confusion Matrix')
plt.axis()
plt.show()


# # saving LSTM model
lstm_w2v.save('LSTM_model.keras')








