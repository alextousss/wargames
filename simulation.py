import copy
import time
from multiprocessing import Pool
from intelligentsoldier import Soldier
from bullet import Bullet
from getch import KBHit
from random import randrange
import os
import pickle

class Simulation:
    def __init__(self):
        self.soldiers = []
        self.blue_team_kills = 0
        self.red_team_kills = 0
        self.bullets = []
        self.state = 0
        self.stop = False

    def giveSoldiers(self, soldiers, player_number):
        player_number = 1
        for i, sol in enumerate(soldiers):
            for y in range(player_number):
                if(i % 2 == 0):
                    sol.team = "red"
                else:
                    sol.team = "blue"

                self.soldiers.append(copy.deepcopy(sol))

        for i, sol in enumerate(self.soldiers):
            if(sol.team == "red"):
                sol.setPosition(750,
                                randrange(250, 750),
                                0)
                sol.angle = 90
            elif(sol.team == "blue"):
                sol.setPosition(1250,
                                randrange(250, 750),
                                0)
                sol.angle = 240

            sol.kills = 0
            sol.setPosition(randrange(750, 1250),
                            randrange(250, 750),
                            0)
            sol.health = 14
            if(i % 2 == 0):
                sol.team = "red"
            else:
                sol.team = "blue"

    def simulateOneGame(self, soldiers):
        self.giveSoldiers(soldiers, 1)
        step = 0
        self.stop = False
        while step < 1250 and not self.stop:
            self.update()
            step += 1
        print('.', end='', flush=True)
        return self.red_team_kills, self.blue_team_kills, step

    def update(self):
        blue_team_alive_soldiers = 0
        red_team_alive_soldiers = 0
        for sol in self.soldiers:
            if   sol.team == "red": red_team_alive_soldiers += 1
            elif sol.team == "blue": blue_team_alive_soldiers += 1
        if blue_team_alive_soldiers == 0 or red_team_alive_soldiers == 0:
            self.stop = True
        for bullet in self.bullets:
            for el in self.soldiers:
                if(bullet.intersectsWithCircle(el.position_x, el.position_y, 25) and bullet.shooter is not el):
                    el.health -= 5
                    el.last_hurter = bullet.shooter
                    bullet.shooter.damage_caused += 5
            bullet.update()

        for el in self.soldiers:
            el.giveEnvironnement(self.soldiers)
            el.update()
            if(el.shooting and el.updates_since_last_shot > 200):
                el.updates_since_last_shot = 0
                self.bullets.append(Bullet(el.position_x,
                                    el.position_y,
                                    50,
                                    el.angle + 90,
                                    el))
            if(el.health < 0):
                if(el.team != el.last_hurter.team):
                    if(el.last_hurter.team == "red"):
                        self.red_team_kills += 1
                    elif(el.last_hurter.team == "blue"):
                        self.blue_team_kills += 1
                    el.last_hurter.kills += 1
                else:
                    if(el.last_hurter.team == "red"):
                        self.red_team_kills -= 1
                    elif(el.last_hurter.team == "blue"):
                        self.blue_team_kills -= 1
                    el.last_hurter.kills -= 1
                self.soldiers.remove(el)
