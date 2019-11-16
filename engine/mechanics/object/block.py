from engine.mechanics.object import Object
from pygame import Rect


class Block(Object):
    name = 'System Block'
    description = "The Block, which doesn't matter. At all"

    id = '-1'
    width = 16
    height = 16
    size = max(width, height)

    destructibility = 48  # Ticks


    def __init__(self, world, x, y):

        super(Block, self).__init__(world, Rect(x, y, self.width, self.height))
