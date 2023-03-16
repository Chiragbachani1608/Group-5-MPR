import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
#In the run() method, the StartScreen is displayed first. Once the user presses any key, the game loop starts, where the user input events are checked in the check_events() method, and the game objects are updated and rendered in the update() and draw() methods, respectively. This loop continues until the player quits the game or presses the ESC key.
GAME_NAME = "Steel Sentinel game made by Chirag Bachani"

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.Font(None, 64)
        self.title = self.font.render("Shooting Game Group no 5", True, (255, 255, 255))
        self.subtitle = self.font.render("Press any key to start", True, (255, 255, 255))

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    running = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.title, (RES[0] / 2 - self.title.get_width() / 2, RES[1] / 3))
            self.screen.blit(self.subtitle, (RES[0] / 2 - self.subtitle.get_width() / 2, RES[1] / 2))
            pg.display.flip()

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f} - {GAME_NAME}')

    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        start_screen = StartScreen(self.screen)
        start_screen.run()
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()
