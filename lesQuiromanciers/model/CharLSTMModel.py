import numpy as np
from tensorflow.python.keras import preprocessing
from tensorflow.python.keras import layers
from tensorflow.python.keras import Sequential, callbacks, utils
from tensorflow.python.keras.activations import linear, tanh
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.losses import mse
from tensorflow.python.keras.optimizers import SGD, Adam
import pandas as pd


class CharLSTMModel(object):
    def fit(self, dataframe, epochs: int = 100):

        self._load(dataframe)
        self._build()
        self._train(epochs)

    def generate(self, words, i=150):
        pass

    @staticmethod
    def _chunk(text: str, chunk_size=10000):
        pass

    def _tokenise(self, text):
        pass

    def _load(self, text):
        pass

    def _build(self):
        self.model = Sequential()
        self.model.add(layers.Embedding(self.y_dim, 10, input_length=self.x_dim))
        self.model.add(layers.LSTM(150, return_sequences=True))
        self.model.add(layers.LSTM(100))
        self.model.add(layers.Dense(self.y_dim, activation="softmax"))
        self.model.compile(
            loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
        )
        print(self.model.summary())

    def _train(self, epochs):
        earlystop = callbacks.EarlyStopping(
            monitor="val_loss", min_delta=0, patience=5, verbose=0, mode="auto"
        )
        onehot_y = utils.to_categorical(self.Y, num_classes=self.y_dim)
        self.model.fit(
            self.X, onehot_y, epochs=epochs, verbose=1, callbacks=[earlystop]
        )

