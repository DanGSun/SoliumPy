from common.engine.mechanics.effects import *


class PoisonEffect(Effect):
    id = '100'
    damage_value = 1

    def action(self) -> None:
        self.npc.hp -= self.damage_value


class ExtraPoisonEffect(PoisonEffect):
    id = '100:1'
    damage_value = 5


class HealingEffect(Effect):
    id = '101'
    healing_value = 1

    def action(self) -> None:
        self.npc.hp += self.healing_value


class FireEffect(ExtraPoisonEffect):
    id = '102'
