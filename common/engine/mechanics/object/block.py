import typing

from common.engine.mechanics.object.main import Object
from pygame import Rect


class Block(Object):
    name = 'System Block'
    description = "The Block, which doesn't matter. At all"

    id = '-1'
    width = 16
    height = 16
    size = 32

    hp = 48

    def __init__(self, world, x: typing.Union[float, int], y: typing.Union[float, int]):

        super(Block, self).__init__(world, Rect(x, y, self.width, self.height))
