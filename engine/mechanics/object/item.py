from pygame.math import Vector2

from engine.mechanics.object import Entity


class Item(Entity):
    type = 'item'

    stackable = True  # TODO: check name

    def __init__(self, world, owner):
        super(Item, self).__init__(world)
        self.dropped = False
        self.name = None

        self.owner = owner
        self.stack = None

        self.action_delay = 15
        self.last_action_tick = 0

    def action(self, *args):
        if self.world.tick - self.last_action_tick < self.action_delay:
            return
        self.last_action_tick = self.world.tick

    def stop_action(self, *args):
        pass

    def collide_action(self, players):
        if not self.dropped:
            return
        player = players[0]
        if len(player.inventory) <= player.max_items:
            player.get_item(self)


class Stack:

    max_count = 99

    def __init__(self, item, count=1):
        self.item = item
        self.count = count

    def add(self, n=1):
        if self.count + n > self.max_count:
            raise OverflowError()
        self.count += n


class Weapon(Item):
    width = 10
    height = 15

    stackable = False

    damage_value = 0
    damage_radius = 70
    damage_delay = 15

    def __init__(self, world, owner):

        super(Weapon, self).__init__(world, owner)
        self.last_damage_tick = 0

    def hit(self):
        if self.world.tick - self.last_damage_tick < self.damage_delay:
            return
        self.last_damage_tick = self.world.tick
        npcs = self.owner.chunk.get_near('npc', 'players')
        npcs.remove(self.owner)
        for npc in npcs:
            if Vector2(abs(npc.rect.centerx - self.owner.rect.centerx),
                       abs(npc.rect.centery - self.owner.rect.centery)).as_polar()[0] < self.damage_radius:
                self.damage(npc)

    def damage(self, npc):
        npc.hp -= self.damage_value

    def drop(self):
        self.dropped = True
        if self.owner.rect.y <= 70:
            x, y = self.owner.rect.x, self.owner.rect.y - 50
        else:
            x, y = self.owner.rect.x, self.owner.rect.y + 70
        self.spawn(x, y)


class Potion(Item):
    drink_delay = 30

    def __init__(self, world, owner):
        super().__init__(world, owner)
        self.is_drinking = False
        self.drink_tick = 0

    def update(self):
        super().update()
        if self.is_drinking:
            self.drink_tick += 1

        if self.drink_tick >= self.drink_delay:
            self.drink_tick = 0
            self.drink_action()

    def drink_action(self, *args):
        pass

    def action(self, *_):
        self.is_drinking = True

    def stop_action(self, *_):
        self.is_drinking = False
        self.drink_tick = 0