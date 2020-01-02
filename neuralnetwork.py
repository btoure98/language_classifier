import numpy as np
from keras.callbacks import EarlyStopping#set early stopping monitor so the model stops training when it won't improve anymore
early_stopping_monitor = EarlyStopping(patience=3)
from keras.models import Sequential
from keras.layers import Dense
from tokenizer import Tokenizer
import pandas as pd


punctuation = list(u'~@#$%^&*()_+\'[]“”‘’—<>»«›‹–„/')
spaces = list(u' \u00A0\n')
stop_characters = list('.?!')


class Network(object):
    def __init__(self, languages, error=0.005):
        self._trainer = None
        self._net = None
        self.languages = languages
        self.error = error
        self.inputs = set()
        for language in languages:
            self.inputs.update(language._characters)
        self.inputs = sorted(self.inputs)
        self.tokenizer= Tokenizer(punctuation, spaces, stop_characters)

    def build_trainer(self):
        """ prepare the data for training"""
        inputs = []
        expected_outputs =[]
        for index_language , language in enumerate(self.languages):
            for vector in language._vectors:
                inputs.append(self.adapt(vector))
                expected_outputs.append(index_language)
        inputs = np.array(inputs, dtype=np.float32)
        expected_outputs = np.array(expected_outputs, dtype=np.int32)
        self._trainer = ((inputs), (expected_outputs))

        
    def build_nn(self):
        self._net = Sequential([
        Dense(len(self.inputs), activation='tanh', input_shape=((len(self.inputs),))),
        Dense(7, activation='softmax'),
        ])  
        self._net.compile(optimizer = 'adam',loss='sparse_categorical_crossentropy',metrics =['accuracy'])


    def adapt(self, vector):
        """ adapt un dictionnaire un vecteur de la bonne taille"""
        result = np.zeros(len(self.inputs))
        for char, freq in vector.items():
            if char in self.inputs:
                result[self.inputs.index(char)] = float(freq)
        return result



    def train(self):
        self.build_trainer()
        self.build_nn()
        self._net.fit(pd.DataFrame(self._trainer[0]), pd.DataFrame(self._trainer[1]),validation_split=0.2, epochs=5, callbacks=[early_stopping_monitor])
    
    def predict(self, sentence):
        if self._net is None or self._trainer is None:
            raise Exception('Must train first')
        characters, vectors = self.tokenizer.tokenize(sentence)
        if len(vectors) == 0:
            return None
        entree = np.array(self.adapt(vectors[0]),ndmin=2,dtype=np.float32)
        result = self._net.predict(entree)
        # la somme fait 1
        good_index = 0
        proba = 0
        for i in range(len(self.languages)):
            if result[0][i]> proba:
                proba = result[0][i]
                good_index = i
        return self.languages[good_index]._name
