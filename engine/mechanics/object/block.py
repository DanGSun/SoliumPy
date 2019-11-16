from engine.mechanics.object import Object
from pygame import Rect


class Block(Object):
    name = 'System Block'
    id = '-1'
    width = 16
    height = 16

    def __init__(self, world, x, y):

        super(Block, self).__init__(world, Rect(x, y, self.width, self.height))
