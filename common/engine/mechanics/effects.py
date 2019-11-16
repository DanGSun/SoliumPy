class Effect:
    type = 'effect'
    id = '100'

    delay = 2
    ticks = 20

    def __init__(self, npc):
        self.npc = npc

        for eff in npc.effects:
            if eff.id == self.id:
                npc.effects.remove(eff)
        npc.effects.append(self)

    def update(self):
        if self.ticks == 0:
            self.npc.effects.remove(self)
            return
        if not self.ticks % self.delay:
            self.action()
        self.ticks -= 1

    def action(self):
        pass
