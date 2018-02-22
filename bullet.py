import math

class Coord:
	def __init__(self,x,y):
		self.x = x
		self.y = y

#Code to check if two segments intersects, coming from : http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A,B,C):
	return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

def lines_intersect(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

class Bullet:
	def __init__(self, pos_x, pos_y, normal, angle, shooter=None):
		self.shooter = shooter
		angle = math.radians(angle)
		self.pos = Coord(pos_x,pos_y)
		self.move = Coord(math.cos(angle) * normal, -math.sin(angle) * normal)


	def intersectsWithCircle(self, circle_pos_x, circle_pos_y, radius):
		circle_pos = Coord(circle_pos_x, circle_pos_y)
		#Implementation of algorithm found on http://doswa.com/2009/07/13/circle-segment-intersectioncollision.html
		"""Returns true if the Bullet intersects with the given circle"""
		distance = Coord(circle_pos.x - self.pos.x, circle_pos.y - self.pos.y)

		move_normal = math.sqrt(self.move.x ** 2 + self.move.y ** 2)
		move_unit = Coord(self.move.x / move_normal, self.move.y / move_normal)

		proj_distance_length = distance.x * move_unit.x + distance.y * move_unit.y

		proj_distance = Coord(proj_distance_length * move_unit.x, proj_distance_length * move_unit.y)


		if(proj_distance_length < 0):
			closest = Coord( self.pos.x, self.pos.y )
		elif(proj_distance_length > move_normal):
			closest = Coord( self.pos.x + self.move.x, self.pos.y + self.move.y )
		else:
			closest = Coord(self.pos.x + proj_distance.x, self.pos.y + proj_distance.y)

		closest_distance = Coord(circle_pos.x - closest.x, circle_pos.y - closest.y)

		closest_distance_length = math.sqrt(closest_distance.x ** 2 + closest_distance.y ** 2)

		if(closest_distance_length < radius):
			return True
		else:
			return False


	def intersectsWithRectangle(self, rectangle_pos_x, rectangle_pos_y, rectangle_length_x, rectangle_length_y):
		bullet_A = self.pos
		bullet_B = Coord(self.pos.x + self.move.x, self.pos.y + self.move.y)

		rectangle_pos = Coord(rectangle_pos_x, rectangle_pos_y)
		rectangle_length = Coord(rectangle_length_x, rectangle_length_y)

		if  (rectangle_pos.x < self.pos.x) \
		and (rectangle_pos.y < self.pos.y) \
		and (rectangle_pos.x + rectangle_length.x > self.pos.x + self.move.x ) \
		and (rectangle_pos.y + rectangle_length.y > self.pos.y + self.move.y ):         #Here we check if the bullet is not entirely inside of the square
			return True
		#ABCD are the coordinates of the edges of the rectangle
		rectangle_A = Coord(rectangle_pos.x, rectangle_pos.y)
		rectangle_B = Coord(rectangle_pos.x, rectangle_pos.y + rectangle_length.y)
		rectangle_C = Coord(rectangle_pos.x + rectangle_length.x, rectangle_pos.y)
		rectangle_D = Coord(rectangle_pos.x + rectangle_length.x, rectangle_pos.y + rectangle_length.y)

		#We check if our bullet intersects each segment of the rectangle,
		if (lines_intersect(bullet_A, bullet_B, rectangle_A, rectangle_B)) \
		or (lines_intersect(bullet_A, bullet_B, rectangle_B, rectangle_C)) \
		or (lines_intersect(bullet_A, bullet_B, rectangle_C, rectangle_D)) \
		or (lines_intersect(bullet_A, bullet_B, rectangle_D, rectangle_A)):
			return True
		return False #If all checks were passed, then the bullet and the rectangle doesn't intersects

	def update(self):
		self.pos.x += self.move.x
		self.pos.y += self.move.y
