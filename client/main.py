from client.lib import Connection, world

import pygame
import os

NAME = "admin"
DEBUG = True

print(os.getcwd())

pygame.init()
pygame.display.set_caption("Solium")
pygame.font.init()

font = pygame.font.SysFont('Roboto', 30)

winx = 1000
winy = 500
win = pygame.display.set_mode((winx, winy))

CameraY = 0
CameraX = 0

connection = Connection(total_debug=False, handler=world.handler, auth=("admin", "1234"))

run = True
stopped_v = True
stopped_h = True


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    c_player = None

    while not world.data:
        pass

    for i in world.data["players"]:
        if i["name"] == NAME:
            c_player = i

    CameraX = c_player['x'] - winx / 2
    CameraY = c_player['y'] - winy / 2
    keys = pygame.key.get_pressed()

    if keys[pygame.K_e]:
        connection.action("action", {"x": 5, "y": 5})
    if keys[pygame.K_a] and c_player['x'] > 0 and stopped_h:
        connection.action("left")
        stopped_h = False
    if keys[pygame.K_d] and c_player['x'] < winx - 40 and stopped_h:
        connection.action("right")
        stopped_h = False
    if keys[pygame.K_w] and c_player['y'] > 0 and stopped_v:
        connection.action("up")
        stopped_v = False
    if keys[pygame.K_s] and c_player['y'] < winy - 40 and stopped_v:
        connection.action("down")
        stopped_v = False
    if not (keys[pygame.K_w] or keys[pygame.K_s]) and not stopped_v:
        connection.action("stop", "vertical")
        stopped_v = True
    if not (keys[pygame.K_a] or keys[pygame.K_d]) and not stopped_h:
        connection.action("stop", "horizontal")
        stopped_h = True

    for player in world.data["players"]:
        x = player['x'] - CameraX
        y = player['y'] - CameraY
        image = pygame.transform.scale(pygame.image.load('assets/players/playerred.png').convert_alpha(),
                                       (40, 40))
        win.blit(image, (x, y))
        image = pygame.transform.scale(pygame.image.load("assets/players/eyeL.png").convert_alpha(), (40, 40))
        win.blit(image, (x, y))
        win.blit(font.render(player['name'], False, (255, 255, 255)), (x, y - 30))

    if DEBUG:
        win.blit(font.render(f"x: {c_player['x']}; y: {c_player['y']}", False, (255, 255, 255)), (winx - 200, 20))

    pygame.draw.rect(win, (232, 81, 81), (0, int(winy - 20), c_player["hp"] / 100 * winx, 20))
    pygame.display.update()
    pygame.time.delay(1)
    win.fill((50, 50, 50))
