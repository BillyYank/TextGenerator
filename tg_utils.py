import random


def choose_random(keys, probs):
    sum_ = sum(probs)
    choice = random.randint(1, sum_)
    if choice < probs[0]:
        return keys[0]
    elif choice >= probs[-1]:
        return keys[-1]
    else:
        for i in range(len(probs) - 1):
            if probs[i] <= choice < probs[i + 1]:
                return keys[i]