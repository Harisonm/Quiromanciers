from tensorflow.python.keras import preprocessing
from tensorflow.python.keras import layers
from tensorflow.python.keras import Sequential, callbacks, utils
from tensorflow.python.keras.activations import linear, tanh
from tensorflow.python.keras.layers import Dense, Activation, LSTM
from tensorflow.python.keras.losses import mse
from tensorflow.python.keras.optimizers import SGD, Adam,RMSprop
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.callbacks import LambdaCallback, ModelCheckpoint
from tensorflow.python import keras
import tensorflow as tf
import random
import numpy as np
import pandas as pd
import sys



class GenerationBioModel:

    def __init__(self):
        self.X = None
        self.Y = None
        self.global_bio = None
        self.maxlen = None
        self.step = None
        self.biographie_sort = None
        self.indices_char = None
        self.char_indices = None
        
    def fit(self,text,epochs=100):
        self._load(text)
        self._build()
        generate_text = LambdaCallback(on_epoch_end=self.on_epoch_end)
        self._train(generate_text,epochs)
        
    def _load(self, filename):
        sentences = []
        next_chars = []
        text = []
        biographie_df = pd.read_csv(filename, encoding="utf-8", sep=";", usecols = ['name', 'biographie'])
        print(biographie_df)
        for i in range(0,len(biographie_df['biographie'])):
            text += ''.join([''.join(sentence) for sentence in biographie_df['biographie'][i]])
        sample_size = int(len(text) * 0.2)
        
        global_bio = biographie_df.biographie
        global_bio = global_bio[:sample_size]
        global_bio = ''.join(map(str, global_bio)).lower()
        self.biographie_sort = sorted(list(set(global_bio)))
        self.char_indices = dict((c, i) for i, c in enumerate(self.biographie_sort))
        self.indices_char = dict((i, c) for i, c in enumerate(self.biographie_sort))
        self.maxlen = 40
        self.step = 3

        for i in range(0, len(global_bio) - self.maxlen, self.step):
            sentences.append(global_bio[i: i + self.maxlen])
            next_chars.append(global_bio[i + self.maxlen])
            
        self.X = np.zeros((len(sentences), self.maxlen, len(self.biographie_sort)), dtype=np.bool)
        self.Y = np.zeros((len(sentences), len(self.biographie_sort)), dtype=np.bool)
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                self.X[i, t, self.char_indices[char]] = 1
            self.Y[i, self.char_indices[next_chars[i]]] = 1
        
        
    def _tokenise(self,text):
        pass
    def generate(self,words,i=150):
        pass

    def _build(self):
        self.model = Sequential()
        self.model.add(LSTM(128, input_shape=(self.maxlen, len(self.biographie_sort))))
        self.model.add(Dense(len(self.biographie_sort)))
        self.model.add(Activation('softmax'))
        optimizer = RMSprop(lr=0.01)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer)
        print(self.model.summary())

    def _train(self,generate_text,epochs):
        # define the checkpoint
        filepath = "weights.hdf5"
        checkpoint = ModelCheckpoint(filepath, 
                                    monitor='loss', 
                                    verbose=1, 
                                    save_best_only=True, 
                                    mode='min')

        # fit model using our gpu
        with tf.device('/cpu:0'):
            self.model.fit(self.X, self.Y,
                    batch_size=128,
                    epochs=epochs,
                    verbose=2,
                    callbacks=[generate_text, checkpoint])
    
    @staticmethod
    def sample(preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def on_epoch_end(self,epoch, logs):
        # Function invoked for specified epochs. Prints generated text.
        # Using epoch+1 to be consistent with the training epochs printed by Keras
        if epoch+1 == 1 or epoch+1 == 15:
            print()
            print('----- Generating text after Epoch: %d' % epoch)

            start_index = random.randint(0, len(self.global_bio) - self.maxlen - 1)
            for diversity in [0.2, 0.5, 1.0, 1.2]:
                print('----- diversity:', diversity)

                generated = ''
                sentence = self.global_bio[start_index: start_index + self.maxlen]
                generated += sentence
                print('----- Generating with seed: "' + sentence + '"')
                sys.stdout.write(generated)

                for i in range(400):
                    x_pred = np.zeros((1, self.maxlen, len(self.biographie_sort)))
                    for t, char in enumerate(sentence):
                        x_pred[0, t, self.indices_char[char]] = 1.

                    preds = model.predict(x_pred, verbose=0)[0]
                    next_index = sample(preds, diversity)
                    next_char = self.indices_char[next_index]
                    generated += next_char
                    sentence = sentence[1:] + next_char

                    sys.stdout.write(next_char)
                    sys.stdout.flush()
                print()
        else:
            print()
            print('----- Not generating text after Epoch: %d' % epoch)
