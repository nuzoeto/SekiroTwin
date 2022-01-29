import random

# funções futuras


def rand_array(array: list, string: bool = True):
    random_num = random.choice(array)
    return str(random_num) if string else random_num
