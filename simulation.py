import copy
import time
from multiprocessing import Pool
from intelligentsoldier import Soldier
from bullet import Bullet
from getch import KBHit
from random import randrange
import pickle

def launchSimulation(soldiers):
    sim = Simulation()
    return sim.simulateOneGame(copy.deepcopy(soldiers))

class DarwinSelection:
    def __init__(self):
        self.keyboard = KBHit()
        self.soldiers_number = 10
        self.soldiers = []
        self.generation = 0

        self.sim = Simulation()

        for i in range(self.soldiers_number):
            self.soldiers.append(Soldier(randrange(750, 1250),
                                         randrange(250, 750),
                                         ""))
            self.soldiers[i].health = 1
            if(i % 2 == 0):
                self.soldiers[i].team = "red"
            else:
                self.soldiers[i].team = "blue"

    def run(self):
        generation = 0
        while True:
            print("Generation number : {}".format(generation))
            print("Press (S) to save the current state ")
            if(self.keyboard.kbhit()):
                if( self.keyboard.getch() == "s"):
                    with open('file', 'wb') as f:
                        pickle.dump(self.soldiers, f)
                        print("Successfull save!!!")


            for sol in self.soldiers:
                sol.kills = 0

            fights = []
            time_beggining = time.time()

            for sol in self.soldiers:
                for sol2 in self.soldiers:
                    if sol is not sol2:
                        fights.append([sol, sol2])

            average_steps = 0
            results = []

            pool = Pool()
            results = pool.map(launchSimulation, copy.deepcopy(fights))
            pool.close()

            for i, result in enumerate(results):
                fights[i][0].kills += result[0]
                fights[i][1].kills += result[1]
                average_steps += result[2]

            average_steps /= len(fights)
            average_steps = round(average_steps, 0)
            generation_time = round(time.time() - time_beggining, 2)
            print(chr(27) + "[2J")
            print("--------- Generation overview : ({}) seconds ---------- "
                  .format(generation_time))
            print("Average steps to kill : ({}/1250)".format(average_steps))

            self.soldiers = sorted(self.soldiers,
                                   key=lambda sol: sol.kills,
                                   reverse=True)

            for i, sol in enumerate(self.soldiers):
                print("{} did {} kills !".format(i, sol.kills))
            ponderated_soldiers = []

            for sol in self.soldiers:
                for i in range(sol.kills ** 4):
                    ponderated_soldiers.append(sol)
            if(len(ponderated_soldiers) != 0):
                for i in range(self.soldiers_number):
                    if(len(ponderated_soldiers) != 0):
                        index = randrange(0, len(ponderated_soldiers))
                        self.soldiers.append(copy.deepcopy(
                            ponderated_soldiers[index - 1])
                            )
                for i in range(self.soldiers_number):
                    self.soldiers.pop(0)
                for sol in self.soldiers:
                    sol.mutate(0.10)
            generation += 1


class Simulation:
    def __init__(self):

        self.soldiers = []
        self.bullets = []
        self.state = 0
        self.stop = False

    def giveSoldiers(self, soldiers):
        self.soldiers = soldiers
        for i, sol in enumerate(soldiers):
            sol.kills = 0
            sol.setPosition(randrange(750, 1250),
                            randrange(250, 750),
                            0)
            sol.health = 1
            if(i % 2 == 0):
                sol.team = "red"
            else:
                sol.team = "blue"

    def simulateOneGame(self, soldiers):
        self.giveSoldiers(soldiers)
        step = 0
        self.stop = False
        while step < 1250 and not self.stop:
            self.update()
            step += 1
        print('.', end='', flush=True)
        return self.soldiers[0].kills, self.soldiers[1].kills, step

    def update(self):
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
                                    100,
                                    el.angle + 90,
                                    el))
            if(el.health < 0):
                self.stop = True
                if(el.team != el.last_hurter.team):
                    el.last_hurter.kills += 1
                else:
                    el.last_hurter.kills -= 1
