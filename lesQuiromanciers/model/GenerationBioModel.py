from tensorflow.python.keras import preprocessing
from tensorflow.python.keras import layers
from tensorflow.python.keras import Sequential, callbacks, utils
from tensorflow.python.keras.activations import linear, tanh
from tensorflow.python.keras.layers import Dense, Activation, LSTM, Dropout
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
import re



class GenerationBioModel:

    def __init__(self):
        self.X = None
        self.Y = None
        self.biographie = None
        self.chars = None
        self.maxlen = 40
        self.step = 3
        self.char_indices = None
        self.indices_char = None
        
        
    def fit(self,dataframe,epochs=100):
        self._load(dataframe)
        self._build()
        generate_text = LambdaCallback(on_epoch_end=self.on_epoch_end)
        self._train(generate_text,epochs)
        
    def _load(self, dataframe):
        sentences = []
        next_chars = []
        text = []
        
        # biographie = df_biographie.biographie
        self.biographie = dataframe.biographie.apply(lambda x: self.clean_data(x))

        n_messages = len(self.biographie)
        n_chars = len(' '.join(map(str, self.biographie)))

        print("DataFrame biographie for %d messages" % n_messages)
        print("Their messages add up to %d characters" % n_chars)
        
        sample_size = int(len(self.biographie) * 0.2)
        self.biographie = self.biographie[:sample_size]
        self.biographie = ''.join(map(str, self.biographie)).lower()
        
        self.chars = sorted(list(set(self.biographie)))
        print('Count of unique characters (i.e., features):', len(self.chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))
        
        for i in range(0, len(self.biographie) - self.maxlen, self.step):
            sentences.append(self.biographie[i: i + self.maxlen])
            next_chars.append(self.biographie[i + self.maxlen])
        print('Number of sequences:', len(sentences), "\n")
        
        self.X = np.zeros((len(sentences), self.maxlen, len(self.chars)), dtype=np.bool)
        self.Y = np.zeros((len(sentences), len(self.chars)), dtype=np.bool)
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
        #model.add(Embedding(len(y), 10, input_length=len(x)))
        self.model.add(LSTM(128, input_shape=(self.maxlen, len(self.chars)),return_sequences=True))
        self.model.add(LSTM(128))
        self.model.add(Dense(len(self.chars)))
        self.model.add(Dropout(0.2))
        self.model.add(Activation('softmax'))
        
        self.model.summary()
        
        optimizer = RMSprop(lr=0.01)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer,metrics=['accuracy'])
        

    def _train(self,generate_text,epochs):
        # define the checkpoint
        filepath = "weights.hdf5"
        checkpoint = ModelCheckpoint(filepath, 
                                    monitor='loss', 
                                    verbose=1, 
                                    save_best_only=True, 
                                    mode='min')

        # serialize model to YAML
        model_yaml = self.model.to_yaml()
        with open("model.yaml", "w") as yaml_file:
            yaml_file.write(model_yaml)
            
        # fit model using our gpu
        with tf.device('/cpu:0'):
            self.model.fit(self.X, self.Y,
                    batch_size=128,
                    epochs=epochs,
                    verbose=2,
                    callbacks=[generate_text, checkpoint])
    
    @staticmethod
    def clean_data(data):
      data = str(data)
      return re.sub(r'\(.*?\)', '', data)
  
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

            start_index = random.randint(0, len(self.biographie) - self.maxlen - 1)
            for diversity in [0.2, 0.5, 1.0, 1.2]:
                print('----- diversity:', diversity)

                generated = ''
                sentence = self.biographie[start_index: start_index + self.maxlen]
                generated += sentence
                print('----- Generating with seed: "' + sentence + '"')
                sys.stdout.write(generated)

                for i in range(400):
                    x_pred = np.zeros((1, self.maxlen, len(self.chars)))
                    for t, char in enumerate(sentence):
                        x_pred[0, t, self.char_indices[char]] = 1.

                    preds = self.model.predict(x_pred, verbose=0)[0]
                    next_index = sample(preds, diversity)
                    next_char = indices_char[next_index]

                    generated += next_char
                    sentence = sentence[1:] + next_char

                    sys.stdout.write(next_char)
                    sys.stdout.flush()
                print()
        else:
            print()
            print('----- Not generating text after Epoch: %d' % epoch)
