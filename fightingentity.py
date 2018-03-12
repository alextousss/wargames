import math

class FightingEntity:
    """Classe définissant notre soldat"""
    def __init__(self, x_pos, y_pos, team):
        self.position_x = x_pos
        self.position_y = y_pos
        self.angle = 0
        self.health = 14
        self.target = self
        self.shooting = False
        self.kills = 0
        self.damage_caused = 0
        self.team = team
        self.last_hurter = self
        self.updates_since_last_shot = 5000

    def setTarget(self, target):
        self.target = target

    def moveCartesian(self, x, y):
        self.position_x += x
        self.position_y += y

    def move(self, x, y):
        max_val = 1
        min_val = -1
        if(x > max_val):
            x = max_val
        elif(x < min_val):
            x = min_val
        if(y > max_val):
            y = max_val
        elif(y < min_val):
            y = min_val

        angle = math.radians(self.angle)
        self.position_x += math.cos(angle) * y
        self.position_y += -math.sin(angle) * y
        self.position_x += math.cos(angle + math.radians(90)) * x
        self.position_y += -math.sin(angle + math.radians(90)) * x


    def setPosition(self, x, y, angle):
        self.position_x = x
        self.position_y = y
        self.angle = angle

    def rotate(self,angle):
        self.angle += angle
    def rotateLeft(self):
        self.angle += 1.5
    def rotateRight(self):
        self.angle -= 1.5

    def update(self):
        self.updates_since_last_shot += 1
