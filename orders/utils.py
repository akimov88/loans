import random
import time


def create_sign():
    return random.randint(1000, 9999)


def logic_imitation(a: int = 1, b: int = 5):
    time.sleep(random.randint(a, b))
