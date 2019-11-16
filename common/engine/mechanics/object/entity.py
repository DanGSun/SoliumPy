import typing

from common.engine.mechanics.object import Object, Vector2, Rect


class Entity(Object):
    type = 'entity'
    static = False
    collide = False
    touchable = True

    def update(self):
        if not self.speed:
            return

        self.move(self.speed)

    def check_collide(self, rect: Rect) -> bool:
        objects = self.chunk.get_near('objects', 'players', 'npc', 'entities')
        objects.remove(self)
        return not (
            self.world.rect.contains(rect)
            and rect.collidelist(list(
                map(
                    lambda x: x.rect,
                    filter(lambda x: x.collide, objects)
                )
            ))
            or not self.collide
        )

    def move(self, speed: Vector2) -> None:
        """
        Change current coordinates with collision
        """
        move_x = self.rect.move(speed.x, 0)
        if not self.check_collide(move_x):
            self.rect = move_x

        move_y = self.rect.move(0, speed.y)
        if not self.check_collide(move_y):
            self.rect = move_y

        self.check_chunk()

        if self.touchable:
            objects = self.chunk.objects + self.chunk.players + self.chunk.npc + self.chunk.entities
            objects.remove(self)
            self.collide_action([objects[i] for i in self.rect.collidelistall(list(
                map(
                    lambda r: r.rect,
                    filter(
                        lambda r: r.collide,
                        objects
                    )
                ))
            )])

    def tp(self, x: int, y: int) -> None:
        """
        Change current coordinates
        """
        self.rect.center = x, y
        self.check_chunk()

    def check_chunk(self) -> bool:
        """
        Jump to another chunk
        """

        chunk = self.world.get_chunk_by_coord(self.rect.centerx, self.rect.centery)
        if chunk != self.chunk:
            self.chunk.remove(self)
            chunk.add(self)
            return True
        return False

    def collide_action(self, *_, **__):
        pass


class TempEntity(Entity):
    ttl = 10

    def update(self):
        super().update()
        self.ttl -= 1
        if self.ttl <= 0:
            self.chunk.remove(self)
