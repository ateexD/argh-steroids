#!/usr/bin/python

import random
import math

import pygame

import util
import asteroid
import text
import world

class Game(object):
    def __init__(self, surface):
        self.surface = surface
        self.world = world.World(surface)
        self.width = self.world.width
        self.height = self.world.height
        self.clock = pygame.time.Clock()
        self.level = 1

    def start_screen(self):
        self.world.add_text('ARGH ITS THE ASTEROIDS', scale = 20)
        self.world.add_text('PRESS ESC TO QUIT') 
        self.world.add_text('PRESS LEFT AND RIGHT TO ROTATE') 
        self.world.add_text('PRESS UP FOR THRUST')
        self.world.add_text('PRESS SPACE FOR FIRE')
        self.world.add_text('OR USE MOUSE CONTROLS') 
        self.world.add_text('WATCH OUT FOR ALLEN THE ALIEN')
        self.world.add_text('ANY KEY TO START', scale = 20)

        for i in range(4):
            asteroid.Asteroid(self.world, random.randint(50, 100))

        while not self.world.quit and not self.world.any_key:
            self.world.update()
            self.surface.fill(util.BLACK)
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def draw_hud(self):
        text.draw_string(self.surface, "SCORE %d" % self.world.score, 
                         util.WHITE, 10, [10, 20])
        text.draw_string(self.surface, "LEVEL %d" % self.level, 
                         util.WHITE, 10, [10, 40])

        if self.world.info:
            text.draw_string(self.surface, 
                             "FPS %d" % self.clock.get_fps(),
                             util.WHITE, 10, [10, self.height - 20])
            text.draw_string(self.surface, 
                             "OBJECTS %d" % self.world.n_objects(), 
                             util.WHITE, 10, [10, self.height - 40])

    def level_start(self):
        start_animation_frames = 100
        start_animation_time = start_animation_frames

        while not self.world.quit:
            if start_animation_time == 0:
                break

            self.world.update()
            if self.world.spawn:
                asteroid.Asteroid(self.world, random.randint(50, 100))

            self.surface.fill(util.BLACK)
            self.draw_hud()
            start_animation_time -= 1
            t = float(start_animation_time) / start_animation_frames
            text.draw_string(self.surface, "LEVEL START", util.WHITE,
                             t * 150,
                             [self.width / 2, self.height / 2],
                             centre = True, 
                             angle = t * 200.0)
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def play_level(self):
        while not self.world.quit:
            if self.world.n_asteroids == 0 or not self.world.player:
                break

            self.world.update()
            self.surface.fill(util.BLACK)
            self.draw_hud()
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def game_over(self):
        end_animation_frames = 100
        end_animation_time = end_animation_frames

        while not self.world.quit:
            if end_animation_time == 0:
                break

            self.world.update()

            self.surface.fill(util.BLACK)
            self.draw_hud()
            end_animation_time -= 1
            t = float(end_animation_time) / end_animation_frames
            text.draw_string(self.surface, "GAME OVER", util.WHITE,
                             math.log(t + 0.001) * 150,
                             [self.width / 2, self.height / 2],
                             centre = True,
                             angle = 180)
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def epilogue(self):
        while not self.world.quit:
            if self.world.any_key:
                break

            self.world.update()

            self.surface.fill(util.BLACK)
            text.draw_string(self.surface, "ANY KEY TO PLAY AGAIN", 
                             util.WHITE,
                             20,
                             [self.width / 2, self.height / 2],
                             centre = True,
                             angle = 0)
            self.draw_hud()
            self.world.draw()
            self.clock.tick(60)
            pygame.display.flip()

    def play_game(self):
        self.start_screen()

        while not self.world.quit:
            self.level = 1
            self.world.reset()

            while not self.world.quit:
                self.level_start()

                self.world.add_player()
                for i in range(2 ** self.level):
                    asteroid.Asteroid(self.world, random.randint(75, 100))

                self.play_level()

                if not self.world.player:
                    break

                self.level += 1

            self.game_over()
            self.epilogue()

def main():
    pygame.init()

    font = pygame.font.Font(None, 16)

    surface = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
    #surface = pygame.display.set_mode([640, 480])
    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Argh, it's the Asteroids!!")

    game = Game(surface)

    game.play_game()

    pygame.quit()

if __name__ == "__main__":
    main()
