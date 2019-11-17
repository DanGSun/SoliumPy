from common.engine.mechanics.object import Block, BlockItem


class Stone(Block):
    id = '1'


class Grass(Block):
    id = '2'


class Brick(Block):
    id = '3'


class Flag(Block):
    id = '4'


class Wall(Block):
    id = '5'


class StoneItem(BlockItem):
    id = "1001"
    related_block = Stone


class BrickItem(BlockItem):
    id = "1003"
    related_block = Brick


class WallItem(BlockItem):
    id = "1005"
    related_block = Wall

