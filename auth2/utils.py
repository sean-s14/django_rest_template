import random
import os

def code_generator():
    code = ''
    for x in range(6):
        num = random.randint(0, 9)
        code += str(num)
    return code

def name_generator():
    words = None
    try:
        file = os.path.dirname(os.path.realpath(__file__)) + '/username_words.txt'
        words = open(file, "r").read().split('\n')
    except FileNotFoundError as e:
        print(e)
        return "randomUser" + str(random.randint(10000,99999))

    name = ""
    for x in range(0, 2):
        index = random.randint(0,9578)
        try:
            name += words[index]
        except IndexError as e:
            print(e)
            return "randomUser" + str(random.randint(10000,99999))

    name += str(random.randint(10000,99999))
    return name