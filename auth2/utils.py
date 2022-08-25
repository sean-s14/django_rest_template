import random

def code_generator():
    code = ''
    for x in range(6):
        num = random.randint(0, 9)
        code += str(num)
    return code

def name_generator():
    num = str(random.randint(10000,99999))
    name = 'user' + num
    return name