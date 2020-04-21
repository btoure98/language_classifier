from neuralnetwork import Network
import os
from keras.models import load_model, model_from_json
from language import Language
from glob import glob
from io import StringIO
import io

def language_name(file_name):
    basename, ext = os.path.splitext(os.path.basename(file_name))
    return basename.split('_')[0]


def load_glob(pattern):
    result = []
    for file_name in glob(pattern):
        with open(file_name) as f:
            result.append(Language(f.read()
            ,language_name(file_name)))
    return result


matthew_languages = load_glob('data/*_0.txt')
model = Network(matthew_languages)
model.train()


while True:
    sentence = input("Tapez une phrase: (stop pour arreter)")
    if sentence=="stop":
        break
    print(model.predict(sentence))