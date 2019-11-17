import random

from common.engine.mechanics.object import NPC


class Player(NPC):
    type = 'player'

    width = 40
    height = 60

    max_speed = 2
    max_items = 10
    render_radius = 2

    def __init__(self, world, user):
        super(Player, self).__init__(world)
        self.name = user.name
        self.id = user.id
        self.user = user
        self.inventory = []
        self.active_item = 0  # TODO: Fists

        self.render_chunks = set()

        self.state = {}
        self.achievements = []

    def kill(self):
        self.world.channel.send_pm({'type': 'dead', 'data': 'You dead.'}, self.name)  # TODO: send death data
        self.chunk.remove(self)
        self.hp = Player.hp
        for item in self.inventory.copy():
            item.drop()
        self.spawn(random.randint(100, self.world.width - 100), random.randint(100, self.world.height - 100))
        # TODO: respawn after request

    def action(self, act, data):
        if act == 'left':
            self.speed.x = -self.max_speed
        elif act == 'right':
            self.speed.x = self.max_speed
        elif act == 'up':
            self.speed.y = -self.max_speed
        elif act == 'down':
            self.speed.y = self.max_speed
        elif act == 'stop':
            if data == 'horizontal':
                self.speed.x = 0
            elif data == 'vertical':
                self.speed.y = 0
            else:
                raise Exception("Wrong direction")
        elif act == 'hit':
            if self.active_item:
                self.active_item.hit()
        elif act == 'action':
            print(self.active_item)  # FIXME: Add logger
            print(act, data if data else "")
            if not self.active_item:
                return
            if data is not None:
                self.active_item.action(self, data)
            else:
                self.active_item.action(self)
        elif act == 'active_item_change':
            try:
                self.active_item = self.inventory[data]
            except IndexError:
                self.active_item = None
        elif act == 'drop':
            if not self.active_item:
                return
            self.drop_item(self.active_item)
            self.active_item = None
        else:
            raise Exception(act)

    def drop_item(self, item):
        """
        :param item: id or class
        :return: None
        """
        if type(item) == str:
            item = self.canon_id(item)
            for i in self.inventory:
                if i.id == item:
                    break
            else:
                return
            self.drop_item(i)
            return
        item.drop()
        self.inventory.remove(item)

    def get_item(self, item):
        item.owner = self
        self.inventory.append(item)
        item.chunk.entities.remove(item)
        item.dropped = False

    def spawn(self, x, y, *_):
        super().spawn(x, y)
        self.render_chunks = self.chunk.get_near_chunks(self.render_radius)
        self.world.reload_active_chunks()

    def check_chunk(self):
        if super().check_chunk():
            self.render_chunks = self.chunk.get_near_chunks(self.render_radius)
            self.world.reload_active_chunks()