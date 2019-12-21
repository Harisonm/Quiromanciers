import numpy as np
from tensorflow.python.keras import preprocessing
from tensorflow.python.keras import layers
from tensorflow.python.keras import Sequential, callbacks, utils
from tensorflow.python.keras.activations import linear, tanh
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.losses import mse
from tensorflow.python.keras.optimizers import SGD, Adam
from tensorflow.python import keras


class charLSTMmodel():
    
    def fit(self,text,epochs=100):
        self._load(text)
        self._build()
        self._train(epochs)
        
    def _load(self, text):
        self.idx_token = dict(enumerate(set(self._tokenise(text)),start=2))
        self.idx_token[0] = '<PAD>'
        self.idx_token[1] = '<UNK>' 
        self.token_idx = {word:i for i,word in self.idx_token.items()}       
        token_ids = [[self.token_idx[token] for token in self._tokenise(sentence)] for sentence in self._chunk(text)]
        inouts = [tokens[:i+1] for tokens in token_ids for i in range(1,len(tokens))]
        self.x_dim = max([len(x) for x in inouts]) - 1
        self.y_dim = len(self.idx_token) 
        inouts = np.array(keras.preprocessing.sequence.pad_sequences(inouts,maxlen=self.x_dim + 1, padding='pre'))
        self.X, self.Y = inouts[:,:-1], inouts[:,-1]
        
    def _tokenise(self,text):
        return list(' '.join(text.split()).replace(" ","_"))

    def generate(self,words,i=150):
        for _ in range(i):
            x = [self.token_idx[token] if token in self.token_idx else 1 for token in self._tokenise(words)] 
            x = keras.preprocessing.sequence.pad_sequences([x], maxlen=self.x_dim, padding = 'pre')
            y_hat = self.model.predict_classes(x, verbose=0)[0] #maximise
            words += self.idx_token[y_hat]
            return words.replace("_"," ")
    
    def _chunk(self,text,chunk_size = 100):
        return ''.join([c + '<S>' if not i % chunk_size else c for i,c in enumerate(text,start=1)]).split('<S>')

    def _build(self):
        self.model = keras.models.Sequential()
        self.model.add(keras.layers.Embedding(self.y_dim, 10, input_length=self.x_dim))
        self.model.add(keras.layers.LSTM(150, return_sequences = True))
        self.model.add(keras.layers.LSTM(100))
        self.model.add(keras.layers.Dense(self.y_dim, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    def _train(self,epochs):
        earlystop =  keras.callbacks.EarlyStopping(monitor='loss', min_delta=0, patience=5, verbose=0, mode='auto')
        onehot_y = keras.utils.to_categorical(self.Y, num_classes=self.y_dim)
        self.model.fit(self.X, onehot_y, epochs=epochs, verbose=1, callbacks=[earlystop])  