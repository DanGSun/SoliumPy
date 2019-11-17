import typing

from common.engine.mechanics.object.main import Object
from common.engine.mechanics.object.item import Item

from pygame import Rect
from pprint import pprint
from traceback import print_exc


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

    def action(self, actioneer, data):
        """
        Create or break block.
        :param data: Action
        :return:
        """
        print(f"Action on block {self.id} received")

        return {"success": False}

    @classmethod
    def place(cls, chunk, x, y):
        print("Block Placed.")
        try:
            chunk.add(cls(chunk.world, x, y))
        except Exception as e:
            print_exc()
            raise e

    def __init__(self, world, x: typing.Union[float, int], y: typing.Union[float, int]):
        super(Block, self).__init__(world, x, y)
        # FIXME:
        #  [2019-11-17 19:45:07,985]
        #  ERROR: ('127.0.0.1', 63592) - {'type': 'action_error', 'data': 'Argument must be rect style object'}


class BlockItem(Item):
    name = "System Block Item"
    description = "A Block, which doesn't matter. At all"

    related_block: Block

    def __init__(self, world, owner):
        super(Item, self).__init__(world)
        self.actioneer = None
        self.dropped = False
        self.name = None

        self.owner = owner
        self.stack = None

        self.action_delay = 15
        self.last_action_tick = 0

    def action(self, actioneer, data):
        super().action()
        print("BlockItem triggered.")
        pprint(data)

        place_x = data["x"]
        place_y = data["y"]

        if (
            self.owner.x - place_x <= self.owner.vision_radius
            and self.owner.y - place_y <= self.owner.vision_radius
        ):
            Block.place(actioneer.chunk, place_x, place_y)

        return {}
