from tokenizer import Tokenizer

punctuation = list(u'~@#$%^&*()_+\'[]“”‘’—<>»«›‹–„/')
spaces = list(u' \u00A0\n')
stop_characters = list('.?!')

class Language(object):
    def __init__(self, io, name):
        self._name = name
        tokenizer= Tokenizer(punctuation, spaces, stop_characters)
        self._characters, self._vectors = tokenizer.tokenize(io)



