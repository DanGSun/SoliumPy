class Chunk:
    size = 20

    def __init__(self, x, y, world):
        self.x, self.y = x, y
        self.objects = []
        self.players = []
        self.npc = []
        self.entities = []
        self.world = world

    def update(self):
        for player in self.players:
            player.update()
        for npc in self.npc:
            npc.update()
        for entity in self.entities:
            entity.update()

    def remove(self, obj):
        self.get_group(obj.type).remove(obj)

    def add(self, obj):
        obj.chunk = self
        self.get_group(obj.type).append(obj)

    def get_group(self, t):
        """
        :type t: str
        :param t:  Type of object
        :return: list
        """
        if t == 'object':
            return self.objects
        if t == 'entity':
            return self.entities
        if t == 'npc':
            return self.npc
        if t == 'player':
            return self.players

    def get_near_chunks(self, r=2):
        """
        :return: set
        """
        chunks = set()
        for i in range(-r, r + 1):
            for j in range(-r, r + 1):
                if 0 <= self.x + i < len(self.world.chunks) and 0 <= self.y + j < len(self.world.chunks[0]):
                    chunks.add(self.world.chunks[self.x + i][self.y + j])
        return chunks

    def get_near(self, *args, r=1):
        objects = []
        for chunk in self.get_near_chunks(r):
            for arg in args:
                objects += getattr(chunk, arg)
        return objects