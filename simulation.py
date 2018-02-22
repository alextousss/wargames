import pygame
import copy
from multiprocessing import Process, Queue
from pygame.locals import *
from intelligentsoldier import Soldier
from bullet import Bullet
from getch import KBHit
from random import randrange

def rot_center(image, angle):
    """rotate an image while keeping its center and size""" #Coming from : https://www.pygame.org/wiki/RotateCenter
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Simulation:
    def __init__(self):
        self.mutation_factor = 0.2
        self.keyboard = KBHit()
        self.graphics = False
        self.soldiers_number = 10

        if(self.graphics): self.initGraphics()


        self.soldiers = list()


        self.state = 0

    def initGraphics(self):
        pygame.init()
        pygame.key.set_repeat(50, 50)

        self.screen = pygame.display.set_mode((1600, 900))
        self.red_entity_img = pygame.image.load("img/red_turret.png").convert_alpha()
        self.blue_entity_img = pygame.image.load("img/blue_turret.png").convert_alpha()

    def run(self):
        for i in range(self.soldiers_number):
            self.soldiers.append(Soldier(randrange(500,1500),randrange(250,750),""))
            self.soldiers[i].health = 1
            if(i % 2 == 0): self.soldiers[i].team = "red"
            else:           self.soldiers[i].team = "blue"

        generation = 0
        while True:
            print("Generation number : {}".format(generation))
            for sol in self.soldiers:
                sol.kills = 0
            fights = []
            for sol in self.soldiers:
                for opponent in self.soldiers:
                    if opponent is not sol:
                        if(self.keyboard.kbhit()):
                            if( self.keyboard.getch() == "g"):
                                self.graphics = True
                                self.initGraphics()

                        sol.health = 1
                        opponent.health = 1
                        sol.team = "red"
                        opponent.team = "blue"
                        sol.setPosition(randrange(500,1500),randrange(250,750),0)
                        opponent.setPosition(randrange(500,1500),randrange(250,750),0)

                        que = Queue()
                        p = Process()
                        if(not self.graphics):
                            p = Process(target=self.simulateOneGame, args=([copy.deepcopy(sol),copy.deepcopy(opponent)], que, ))
                            p.start()
                            fights.append([p,que,sol,opponent,True])

                        else:
                            self.simulateOneGame([copy.deepcopy(sol),copy.deepcopy(opponent)], que)
                            fights.append([p,que,sol,opponent,False])
                            #We store the fact that we didn't used the threading module on this fight, so the next set of instructions
                            #dont do a p.join() when the thread wasn't created




            for f in fights:
                p = f[0]
                q = f[1]
                sol = f[2]
                opponent = f[3]
                kills_sol, kills_opponent = q.get()
                sol.kills += kills_sol
                opponent.kills += kills_opponent
                if(f[4]): p.join()



            print("")
            print("--------- Generation overview ---------- ")

            self.soldiers = sorted(self.soldiers, key=lambda sol: sol.kills, reverse=True)

            for i, sol in enumerate(self.soldiers):
                print("{} did {} kills !".format(i,sol.kills))
            ponderated_soldiers = []

            for sol in self.soldiers:
                for i in range(sol.kills * 3): ponderated_soldiers.append(sol)
            if(len(ponderated_soldiers) != 0):
                for i in range(self.soldiers_number):
                    if(len(ponderated_soldiers) != 0):
                        index = randrange(0, len(ponderated_soldiers))
                        self.soldiers.append(copy.deepcopy(ponderated_soldiers[index - 1]))
                for i in range(self.soldiers_number):
                    self.soldiers.pop(0)
                for sol in self.soldiers: sol.mutate(0.10)
            generation += 1


    def simulateOneGame(self,soldiers,que):
        step = 0
        stop = False
        bullets = []
        while step < 1250 and not stop:
            step += 1

            if(self.graphics):
                self.draw(soldiers, bullets)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                    if event.type == KEYDOWN and event.key == K_g:
                        self.graphics = False
                        pygame.quit()
                    if event.type == KEYDOWN and event.key == K_s:
                        stop = True



            for bullet in bullets:
                for el in soldiers:
                    if(bullet.intersectsWithCircle(el.position_x, el.position_y,25) and bullet.shooter is not el):
                        el.health -= 5
                        el.last_hurter = bullet.shooter
                        bullet.shooter.damage_caused += 5
                bullet.update()


            for el in soldiers:

                el.giveEnvironnement(soldiers)
                el.update()
                if(el.shooting and el.updates_since_last_shot > 200):
                    el.updates_since_last_shot = 0
                    bullets.append(Bullet(el.position_x,el.position_y, 100 ,el.angle + 90, el))
                if(el.health < 0):
                    stop = True
                    if(el.team != el.last_hurter.team):
                        el.last_hurter.kills += 1
                    else:
                        el.last_hurter.kills -= 1

        bullets = []
        que.put((soldiers[0].kills, soldiers[1].kills))
        print('.', end='', flush=True)


    def draw(self,soldiers, bullets):

        self.screen.fill([0, 0, 0])
        for el in bullets:
            pygame.draw.line(self.screen, [255,0,0], (el.pos.x, el.pos.y), (el.pos.x + el.move.x, el.pos.y + el.move.y))

        for el in soldiers:
            if(el.team == "red"):
                sprite = pygame.transform.scale(self.red_entity_img, (50,50))
            else:
                sprite = pygame.transform.scale(self.blue_entity_img, (50,50))

            sprite = rot_center(sprite, el.angle)
            self.screen.blit(sprite, (el.position_x - sprite.get_width() / 2, el.position_y - sprite.get_height() / 2))



        pygame.display.flip()
