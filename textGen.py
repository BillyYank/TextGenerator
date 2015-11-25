import json
import random
import numpy


class TextGenerator:
    endings = ['.', '!', '?']

    def __init__(self, output_path):
        self.output_path = output_path
        self.stat = {}

    def load_stat(self, stat_path):
        stat_file = open(stat_path, "r")
        self.stat = json.loads(stat_file.read())

    def gen_text(self, size):
        text = ""
        last_words = ["", "."]
        for i in range(size):
            current_word = self.gen_word(last_words)
            text += " " + current_word
            last_words = last_words[1:] + [current_word.lower()]

        return text

    def gen_word(self, last_words):
        new_word = ""
        if last_words[-1] in self.endings:
            new_word = random.sample(self.stat.keys(), 1)[0].title()
        elif last_words[-2] in self.endings:
            dic = self.stat[last_words[-1]]
            probs = [float(dic[word][".count"])/dic[".count"] for word in dic if word != ".count"]
            new_word = random.sample([key for key in dic.keys() if key != ".count"], 1)[0] #numpy.random.choice(dic.keys(), probs)
        else:
            dic = self.stat[last_words[-2]][last_words[-1]]
            denom = self.stat[last_words[-2]][last_words[-1]][".count"]
            probs = [float(value)/denom for value in dic.values()]
            new_word = random.sample([key for key in dic.keys() if key != ".count"], 1)[0] #numpy.random.choice(dic.keys(), probs)

        return new_word

    def save_text(self, size):
        output_file = open(self.output_path, "w")
        output_file.write(self.gen_text(size).encode('utf-8').strip())
        output_file.close()