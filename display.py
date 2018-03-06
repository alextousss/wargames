import pickle
import json
from simulation import Simulation
import time
import pygame
from pygame.locals import *

def rot_center(image, angle):
    """rotate an image while keeping its center and size""" #Coming from : https://www.pygame.org/wiki/RotateCenter
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Display:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(50, 50)

        self.screen = pygame.display.set_mode((1600, 900))
        self.red_entity_img = pygame.image.load("img/red_turret.png").convert_alpha()
        self.blue_entity_img = pygame.image.load("img/blue_turret.png").convert_alpha()
        with open('file', 'rb') as f:
            self.soldiers = pickle.load(f)
        self.sim = Simulation()
        self.last_frame_time = time.time()
        self.framerate = 150

    def run(self):
        for sol1 in self.soldiers:
            for sol2 in self.soldiers:
                if sol1 is not sol2:
                    self.sim = Simulation()
                    self.sim.giveSoldiers([sol1, sol2])
                    stop = False
                    while True and not stop:


                        self.sim.update()
                        stop = self.sim.stop
                        self.draw(self.sim.soldiers, self.sim.bullets)
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                quit()
                            if event.type == KEYDOWN and event.key == K_g:
                                self.graphics = False
                                pygame.quit()
                            if event.type == KEYDOWN and event.key == K_s:
                                stop = True


    def draw(self, soldiers, bullets):
        while time.time() - self.last_frame_time < 1/self.framerate:
            pass
        self.last_frame_time = time.time()
        self.screen.fill([0, 0, 0])
        for el in bullets:
            pygame.draw.line(self.screen, [255,0,0], (el.pos.x, el.pos.y), (el.pos.x + el.move.x, el.pos.y + el.move.y), 5)

        for el in soldiers:
            if(el.team == "red"):
                sprite = pygame.transform.scale(self.red_entity_img, (50,50))
            else:
                sprite = pygame.transform.scale(self.blue_entity_img, (50,50))

            sprite = rot_center(sprite, el.angle)
            self.screen.blit(sprite, (el.position_x - sprite.get_width() / 2, el.position_y - sprite.get_height() / 2))

        pygame.display.flip()
