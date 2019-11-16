import pygame
import threading
import time

# TODO: save world

from common.engine.player import Player
from common.engine.world import World


class Game(threading.Thread):
    tps = 30

    def __init__(self, channel):
        threading.Thread.__init__(self, target=self.run)
        self.channel = channel
        self.world = World(channel)

    def add_player(self, user):
        inventory = self.world.get_object_by_id(user.player_info['inventory'])
        try:
            active_item = inventory[user.player_info['active_item']]
        except IndexError:
            active_item = 0
        return self.world.add_player(user.player_info['x'], user.player_info['y'],
                                     user.player_info['hp'], inventory,
                                     active_item, user)

    def delete_player(self, user):
        user.me.chunk.remove(user.me)
        del self.world.players[user.name]
        self.world.reload_active_chunks()
        self.channel.send({'type': 'player_left', 'data': ''})  # TODO: send data

    @staticmethod
    def get_img(name):
        s = pygame.image.load('models/assets/img/' + name)
        return {
            'name': name,
            'assets': str(pygame.image.tostring(s, 'RGBA')),
            'size': s.get_size()
        }

    def run(self):
        while True:
            t = time.time()
            self.world.do_tick()
            for player in self.world.players.values():
                entities = []
                npc = []
                players = []
                for chunk in player.chunk.get_near_chunks(Player.render_radius):
                    entities += chunk.entities
                    npc += chunk.npc
                    players += chunk.players
                data = {
                    'players': [
                        {
                            'x': player.rect.x,
                            'y': player.rect.y,
                            'hp': player.hp,
                            'id': player.user.id,
                            'name': player.user.name,
                            'direction': player.direction,
                            'active_item': player.inventory.index(player.active_item)
                            if (getattr(player, 'active_item', None) in player.inventory) else -1,
                            'inventory': [item.id for item in player.inventory],
                            'effects': [
                                {
                                    'id': effect.id,
                                    'ticks': effect.ticks
                                } for effect in player.effects
                            ]
                        } for player in self.world.get_visible_objects(players)
                    ],
                    'entities': [
                        {
                            'x': entity.rect.x,
                            'y': entity.rect.y,
                            'id': entity.id
                        } for entity in self.world.get_visible_objects(entities)
                    ],
                    'npc': [
                        {
                            'x': npc.rect.x,
                            'y': npc.rect.y,
                            'hp': npc.hp,
                            'effects': [
                                {
                                    'id': effect.id,
                                    'ticks': effect.ticks
                                } for effect in npc.effects
                            ]
                        } for npc in self.world.get_visible_objects(npc)
                    ]
                }
                self.channel.send_pm({'type': 'tick', 'data': data}, player.name)
            if 1 / self.tps - time.time() + t > 0:
                time.sleep(1 / self.tps - time.time() + t)
            else:
                print(self.tps + 1 / self.tps - time.time() + t)
