from common.engine.player import Player
from common.engine.mechanics.object import Block, Rect, Object
from common.engine.world.chunk import Chunk
from common import model


class World:
    type = 'world'

    width = 5000
    height = 5000

    def __init__(self, channel):
        self.channel = channel

        self.players = {}

        self.active_chunks = set()
        self.chunks = [
            [
                Chunk(x, y, self)
                for y in range(self.width // Chunk.size // Block.size)
            ]
            for x in range(self.height // Chunk.size // Block.size)
        ]

        self.tick = 0

        self.rect = Rect(0, 0, self.width, self.height)

        self.all_objects = [
            getattr(model, x)
            for x in model.__dir__()
            if self.get_attr(getattr(model, x))
        ]

    @staticmethod
    def get_attr(obj, attr='id'):
        try:
            return getattr(obj, attr)
        except AttributeError:
            return False

    def reload_active_chunks(self):
        self.active_chunks = set()
        for player in self.players.values():
            self.active_chunks |= player.render_chunks

    def do_tick(self):
        for chunk in self.active_chunks:
            chunk.update()
        self.tick += 1

    def add_player(self, x, y, hp, inventory, active_item, user):
        player = Player(self, user)
        player.hp = hp
        player.inventory = inventory
        for i, item in enumerate(player.inventory):
            _item = item(self, player)
            player.inventory[i] = _item
            if i == active_item:
                player.active_item = _item
        self.players[user.name] = player
        player.spawn(x, y)
        return player

    @staticmethod
    def get_visible_objects(objects):
        return [obj for obj in objects if obj.visible]

    def get_object_by_id(self, item_id):
        if item_id is []:
            return []
        if type(item_id) == list:
            return [self.get_object_by_id(i) for i in item_id]
        ids = [obj.id for obj in self.all_objects]
        return self.all_objects[ids.index(item_id)]

    def get_chunk_by_coord(self, x, y):
        return self.chunks[x // (Block.size * Chunk.size)][y // (Block.size * Chunk.size)]
