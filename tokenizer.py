import collections
from io import StringIO

punctuation = list(u'~@#$%^&*()_+\'[]“”‘’—<>»«›‹–„/')
spaces = list(u' \u00A0\n')
stop_characters = list('.?!')

class Tokenizer(object):
    def __init__(self, punctuation, spaces, stop_characters):
        self.punctuation = punctuation
        self.spaces = spaces
        self.stop_characters = stop_characters

    def tokenize(self, string):
        io= StringIO(string)
        dict = collections.defaultdict(int)
        vectors = []
        characters = set()

        for character in io.read():
            if character in self.stop_characters:
                if len(dict) > 0:
                    vectors.append(self.normalize(dict))
                    dict = collections.defaultdict(int)
            else:
                if character not in self.spaces and character not in self.punctuation:
                    character.lower()
                    dict[character] += 1
                    characters.add(character)
        
        if len(dict) > 0:
            vectors.append(self.normalize(dict))
            dict = collections.defaultdict(int)
        return characters, vectors
    
    def normalize(self , dict):
        if len(dict) > 0:
            total = sum(dict.values())
            for key in dict:
                dict[key] = dict[key]/total
        return dict
