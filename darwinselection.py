from simulation import Simulation
from intelligentsoldier import Soldier
from multiprocessing import Pool
from getch import KBHit
from random import randrange
import os
import pickle
import time
import copy


def launchSimulation(soldiers):
    sim = Simulation()
    return sim.simulateOneGame(copy.deepcopy(soldiers))

class DarwinSelection:
    def __init__(self, soldiers_file=None):
        self.keyboard = KBHit()
        self.soldiers_number = 20
        self.soldiers = []
        self.generation = 0
        self.pow_proba = 2
        self.sim = Simulation()

        if soldiers_file == None:
            for i in range(self.soldiers_number):
                self.soldiers.append(Soldier(randrange(750, 1250),
                                             randrange(250, 750),
                                             ""))

        else:
            with open(soldiers_file, 'rb') as f:
                self.soldiers = pickle.load(f)
                self.soldiers_number = len(self.soldiers)

        self.save_id = 0
        if not os.path.exists("saves"):
            os.makedirs("saves")
        while os.path.exists("saves/save_" + str(self.save_id)):
            self.save_id += 1
        os.makedirs("saves/save_" + str(self.save_id))

    def save(self, generation):
        path = 'saves/save_' + str(self.save_id) + "/" + str(generation)
        with open(path, 'wb') as f:
            pickle.dump(self.soldiers, f)
            print("Successfull save at : {} !".format(path))

    def run(self):
        generation = 0
        while True:
            time_beggining = time.time()

            if generation % 10 == 0:
                self.save(generation)

            print("Generation number : {}".format(generation))
            print("Press (S) to save the current state ")
            print("Press (Q) to quit and save ")

            if(self.keyboard.kbhit()):
                char = self.keyboard.getch()
                if(char == "s"):
                    self.save(generation)
                elif(char == "q"):
                    self.save(generation)
                    quit()

            for sol in self.soldiers:
                sol.kills = 0

            fights = []

            for sol in self.soldiers:
                for sol2 in self.soldiers:
                    if sol is not sol2:
                        fights.append([sol, sol2])


            pool = Pool(processes=12)
            results = pool.map(launchSimulation, copy.deepcopy(fights))
            pool.close()

            average_steps = 0
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

            self.reproduce()

            generation += 1

    def reproduce(self):
        self.soldiers = sorted(self.soldiers,
                               key=lambda sol: sol.kills,
                               reverse=True)
        total_probability = 0
        for sol in self.soldiers:
            total_probability += sol.kills ** self.pow_proba

        for i, sol in enumerate(self.soldiers):
            print("{} did {} kills ! {}/100".format(i, sol.kills, round(((sol.kills ** self.pow_proba)/ total_probability) * 100), 2))

        ponderated_soldiers = []

        for sol in self.soldiers:
            if(sol.kills > 0):
                for i in range((sol.kills) ** self.pow_proba):
                    ponderated_soldiers.append(sol)
            else:
                    ponderated_soldiers.append(Soldier(0,0,"none"))

        self.soldiers = []
        for i in range(self.soldiers_number):
            index = randrange(0, len(ponderated_soldiers))
            self.soldiers.append(copy.deepcopy(
                ponderated_soldiers[index - 1])
                )

        self.soldiers = sorted(self.soldiers,
                               key=lambda sol: sol.kills,
                               reverse=True)

        for i, sol in enumerate(self.soldiers):
            if(i != 0):
                sol.mutate(0.10)
