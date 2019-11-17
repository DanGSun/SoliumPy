import typing

from common.engine.mechanics.object.main import Object
from common.engine.mechanics.object.item import Item

from pygame import Rect
from pprint import pprint


class Block(Object):
    name = 'System Block'
    description = "A Block, which doesn't matter. At all"

    id = '-1'
    width = 16
    height = 16
    size = 32

    hp = 48

    loot = {"-1": [1, 1]}

    def update(self):
        pass

    def action(self, data):
        """
        Create or break block.
        :param data: Action
        :return:
        """
        print(f"Action on block {self.id} received")

        return {"success": False}

    @classmethod
    def place(cls, chunk, x, y):
        chunk.add(cls(chunk.world, x, y))

    def __init__(self, world, x: typing.Union[float, int], y: typing.Union[float, int]):
        super(Block, self).__init__(world, Rect(x, y, self.width, self.height))


class BlockItem(Item):
    name = "System Block Item"
    description = "A Block, which doesn't matter. At all"

    related_block: Block

    def __init__(self, world, owner):
        super(Item, self).__init__(world)
        self.dropped = False
        self.name = None

        self.owner = owner
        self.stack = None

        self.action_delay = 15
        self.last_action_tick = 0

    def action(self, *args):
        super().action()
        pprint(args)

        place_x = 0
        place_y = 0

        if (self.owner.x - place_x <= self.owner.vision_radius) and (
                self.owner.y - place_y <= self.owner.vision_radius):
            Block.place(self.chunk, place_x, place_y)

        return {}
