import math
import typing
from random import uniform


def my_random(count, freq):
    return int(sigmoid(uniform(1 / freq, 1) - 1) * 2 * count)


def sigmoid(z: typing.Union[float, int]) -> float:
    """Sigmoid function"""
    if z > 100:
        return 0
    return 1.0 / (1.0 + math.exp(z))
