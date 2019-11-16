from pygame.math import Vector2


class NPC(Entity):
    type = 'NPC'
    collide = True
    touchable = False
    vision_radius = 100
    hp = 100

    max_speed = 2

    def __init__(self, world):
        super(NPC, self).__init__(world)
        self.effects = []

    def update(self):
        super(NPC, self).update()
        for effect in self.effects:
            effect.update()
        if self.hp <= 0:
            self.kill()

    def kill(self):
        self.chunk.npc.remove(self)


class EnemyNPC(NPC):
    hp = 50

    damage_value = 5
    damage_delay = 30
    damage_radius = 3

    loot = {}  # id: [freq, count]

    max_speed = 3

    def __init__(self, world):
        super(EnemyNPC, self).__init__(world)
        self.last_damage_tick = 0

    def hit(self):
        if self.world.tick - self.last_damage_tick < self.damage_delay:
            return
        for player in self.chunk.get_near('players'):
            if Vector2(abs(player.rect.centerx - self.rect.centerx),
                       abs(player.rect.centery - self.rect.centery)).length() < self.damage_radius:
                self.damage(player)
        self.last_damage_tick = self.world.tick

    def update(self):
        super(EnemyNPC, self).update()
        for player in self.chunk.get_near('players'):
            polar = Vector2(abs(player.rect.centerx - self.rect.centerx),
                            abs(player.rect.centery - self.rect.centery)).as_polar()
            if polar[0] <= self.vision_radius:
                self.speed.from_polar((self.max_speed, polar[1]))
                break
        else:
            self.speed.x, self.speed.y = 0, 0

        self.hit()

    def damage(self, npc):
        npc.hp -= self.damage_value

    def kill(self):
        for item_id, param in zip(self.loot, self.loot.values()):
            item = self.world.get_object_by_id(item_id)  # TODO: drop (need Stack structure)
        super().kill()