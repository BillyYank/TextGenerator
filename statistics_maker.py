import json
import sys
import os, os.path
import string
import re


class StatMaker:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        self.stat_path = './statistics.json'
        self.stat = {}

    def make_stat(self):
        stat_file = open(self.stat_path, "w")

        for root, dirs, files in os.walk(self.corpus_path):
            for f in files:
                if f.endswith(".txt"):
                    full_path = os.path.join(root, f)
                    current_file = open(full_path, "r")
                    try:
                        new_data = current_file.read()
                        new_data = self.prepare_text_data(new_data)
                    finally:
                        current_file.close()
                        print full_path + " completed"

                    self.update_stat(new_data)

        stat_file.write(json.dumps(self.stat))
        stat_file.close()

    def prepare_text_data(self, data):
        endings = [".", "!", "?"]
        for ending in endings:
            data = data.replace(ending, ' ' + ending, 1000000000)  #TODO

        delimiters = ' ', ',', '\n', '-', '--'
        regexPattern = '|'.join(map(re.escape, delimiters))
        return map(lambda word: word.lower(), re.split(regexPattern, data))

    def update_stat(self, new_data):
        for i in range(len(new_data) - 2):   #TODO Refactoring
            if new_data[i] not in self.stat:
                self.stat[new_data[i]] = {new_data[i+1]: {new_data[i+2]: 1}}
            elif new_data[i+1] not in self.stat[new_data[i]]:
                self.stat[new_data[i]][new_data[i+1]] = {new_data[i+2]: 1}
            elif new_data[i+2] not in self.stat[new_data[i]][new_data[i+1]]:
                self.stat[new_data[i]][new_data[i+1]][new_data[i+2]] = 1
            else:
                self.stat[new_data[i]][new_data[i+1]][new_data[i+2]] += 1

            if ".count" not in self.stat[new_data[i]]:
                self.stat[new_data[i]][".count"] = 1
            else:
                self.stat[new_data[i]][".count"] += 1

            if ".count" not in self.stat[new_data[i]][new_data[i+1]]:
                self.stat[new_data[i]][new_data[i+1]][".count"] = 1
            else:
                self.stat[new_data[i]][new_data[i+1]][".count"] += 1
