from common.engine.mechanics.object import Block, BlockItem


class Stone(Block):
    id = '1'


class Grass(Block):
    id = '2'


class Brick(Block):
    id = '3'


class Flag(Block):
    id = '4'


class StoneItem(BlockItem):
    id = "1001"
    related_block = Stone
