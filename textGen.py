import json
import random
import tg_utils
import string


class TextGenerator:
    endings = ['.', '!', '?']
    sentence_number_in_paragraph = 15

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
            if current_word in self.endings:
                if random.sample(range(self.sentence_number_in_paragraph), 1)[0] == 1:
                    current_word += "\n    "

            text += " " + current_word
            last_words = last_words[1:] + [current_word.lower().strip()]

        return self.polish_text(text)

    def polish_text(self, text):
        for ending in self.endings:
            text = text.replace(" " + ending, ending, 100000000)
        return "    " + text

    def gen_word(self, last_words):
        new_word = ""
        if last_words[-1] in self.endings:
            new_word = random.sample(self.stat.keys(), 1)[0].title()
        elif last_words[-2] in self.endings:
            dic = self.stat[last_words[-1]]
            dic_keys = [key for key in dic if key != ".count"]
            probs = [dic[key][".count"] for key in dic_keys]
            new_word = tg_utils.choose_random(dic_keys, probs)
        else:
            dic = self.stat[last_words[-2]][last_words[-1]]
            dic_keys = [key for key in dic if key != ".count"]
            probs = [dic[key] for key in dic_keys]
            new_word = tg_utils.choose_random(dic_keys, probs)

        return new_word

    def save_text(self, size):
        output_file = open(self.output_path, "w")
        output_file.write(self.gen_text(size).encode('utf-8').strip())
        output_file.close()