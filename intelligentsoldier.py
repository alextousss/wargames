from random import randrange
import random
import math
import numpy as np
from bullet import Coord
from fightingentity import FightingEntity

class NeuralNetwork:
    def __init__(self):
        self.input_layer_size = 2
        self.hidden_layer_size = 8
        self.output_layer_size = 7

        self.W1 = np.random.randn(self.input_layer_size, self.hidden_layer_size)
        self.W2 = np.random.randn(self.hidden_layer_size, self.output_layer_size)

        self.nearest_opponent_distance = 0
        self.nearest_opponent_angle = 0
        self.nearest_friend_distance = 0
        self.nearest_friend_angle = 0

    def forwardPropagation(self, X):
        self.z2 = np.dot(X, self.W1)
        self.a2 = self.sigmoid(self.z2)
        self.z3 = np.dot(self.a2, self.W2)
        y_hat = self.sigmoid(self.z3)
        return y_hat


    def mutate(self, mutation_factor):
        proba_w1 = 1/(self.input_layer_size * self.hidden_layer_size)
        proba_w2 = 1/(self.hidden_layer_size * self.output_layer_size)
        mutate = 0
        for (x,y), el in np.ndenumerate(self.W1):
            if(random.random() < proba_w1):
                self.W1[x,y] = random.uniform(-2.0,2.0)

        for (x,y), el in np.ndenumerate(self.W2):
            if(random.random() < proba_w2):
                self.W2[x,y] = random.uniform(-2.0,2.0)





    def sigmoid(self, z):
        return 1/(2+np.exp(-z))

class Soldier(FightingEntity):
    def __init__(self, x_pos, y_pos, team):
        FightingEntity.__init__(self, x_pos, y_pos, team)
        self.neurons = NeuralNetwork()
        self.nearest_opponent_distance = 0
        self.nearest_opponent_angle = 0
        self.nearest_friend_distance = 0
        self.nearest_friend_angle = 0


    def giveEnvironnement(self, soldiers):
        self.nearest_opponent_distance = 0
        self.nearest_opponent_angle = 0
        self.nearest_friend_distance = 0
        self.nearest_friend_angle = 0

        for sol in soldiers:
            if sol is not self:
                distance = math.sqrt( (sol.position_x - self.position_x ) ** 2 + (sol.position_y - self.position_y) ** 2 )
                sol_to_self_vec = Coord(self.position_x - sol.position_x, self.position_y - sol.position_y)
                angle = 0
                if(sol_to_self_vec.y != 0):
                    angle = (self.angle % 360) - (math.degrees(math.atan(sol_to_self_vec.x/sol_to_self_vec.y))) - 180
                if(sol_to_self_vec.y > 0 and sol_to_self_vec.x < 0):
                    angle -= 180
                if(sol_to_self_vec.y > 0 and sol_to_self_vec.x > 0):
                    angle += 180

                if(sol.team == self.team):
                    if(self.nearest_friend_distance == 0 or self.nearest_friend_distance > distance):
                        self.nearest_friend_distance = distance
                        self.nearest_friend_angle = math.fabs(angle)
                else:
                    if(self.nearest_opponent_distance == 0 or self.nearest_opponent_distance > distance):
                        self.nearest_opponent_distance = distance
                        self.nearest_opponent_angle = math.fabs(angle)


    def mutate(self, mutation_factor):
        self.neurons.mutate(mutation_factor)


    def resetNeurons(self):
        self.neurons = NeuralNetwork()



    def update(self):
        FightingEntity.update(self)
        neural_input = np.array([#self.nearest_friend_angle / 180, \
                                #self.nearest_friend_distance / 500, \
                                (self.nearest_opponent_angle )/ 90, \
                                self.nearest_opponent_distance / 1500])



        neural_output = self.neurons.forwardPropagation(neural_input)
        if(neural_output[0] > 0.25): self.shooting = True
        else:                       self.shooting = False

        move = Coord(0,0)
        move.x = neural_output[1] * 10 - neural_output[2] * 10
        move.y = neural_output[3] * 10 - neural_output[4] * 10
        self.move(move.x, move.y)

        rotation =  neural_output[5] * 10 - neural_output[6] * 10
        self.rotate(rotation)
