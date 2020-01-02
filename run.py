from neuralnetwork import Network
import os
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

# filename = glob('data/*_0.txt')[0]
# with open(filename) as f:
#             langue=Language(f.read()
#             ,language_name(filename))
# print(langue._name)
# print(langue._vectors)

matthew_languages = load_glob('data/*_0.txt')
acts_languages = load_glob('data/*_1.txt')
matthew_verses = Network(matthew_languages)
matthew_verses.train()
acts_verses = Network(acts_languages)
acts_verses.train()


while True:
    sentence = input("Tapez une phrase: (stop pour arreter)")
    if sentence=="stop":
        break
    print(matthew_verses.predict(sentence))