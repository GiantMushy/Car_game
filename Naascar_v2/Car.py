from OpenGL.GL import *
from OpenGL.GLU import *
import math


class Car:
    def __init__(self, coordinates = [0,0], direction = [0,1], color = [1.0, 0.0, 0.0], id = 0):
        self.id = id

        self.MAX_SPEED = 1
        self.MIN_SPEED = -0.5
        self.TURN_SPEED = 1
        self.ACCELERATION = 0.01

        self.game_start = True
        #--------------------------------- CAR Location/Orientation DATA -------------------------------------------
        self.coordinates = coordinates
        self.direction = direction
        self.speed = 0.00
        #---------------------------- CAR IMAGE COARDINATES ------------------------------------
        self.init_car_image_coords = [[0,15],[10,15],[10,12.5],[10,10],[5,10],[5,-5],[-10,-5],[10,-7.5],[10,-10],[5,-10],[3,-15],[-3,-15],[-5,-10],[-10,-10],[-10,-7.5],[-10,-5],[-5,-5],[-5,10],[-10,10],[-10,12.5],[-10,15],[0,1]]
        self.init_backwheel_coords= [[-5,-7.5],[5,-7.5],[5,7.5],[-5,7.5]]
        self.init_frontwheel_coords= [[-4,-6],[4,-6],[4,6],[-4,6]]

        #---------------------------- CURRENT ROTATED COORDINATES (CALCULATED EACH FRAME) ------------------------------------
        self.image_coords = []  # Will be calculated in update_image_coordinates()
        self.backwheel_coords = []
        self.frontwheel_coords = []
        self.color_a, self.color_b, self.color_c = color[0], color[1], color[2]

        self.update_image_coordinates()

    def update(self, delta, steering_data):
        self.update_movement(steering_data)
        self.move(delta)

        self.update_image_coordinates()

    def update_movement(self, steering_data):
        '''Turns the car by TURN_SPEED while either the Left [0] or Right [1] key's are held down'''
        if steering_data[0]:
            self.turn_car(self.TURN_SPEED)
        if steering_data[1]:
            self.turn_car(-self.TURN_SPEED)
        
        if steering_data[2] and self.speed < self.MAX_SPEED:
            self.speed += self.ACCELERATION
        elif steering_data[3] and self.speed > self.MIN_SPEED:
            self.speed -= self.ACCELERATION
        else:
            self.auto_slowdown()

    def rotate_vector(v, deg):
        '''function inputs given vector data into the rotational equation'''
        x = math.cos(deg)*v[0] - math.sin(deg)*v[1]
        y = math.sin(deg)*v[0] + math.cos(deg)*v[1]
        return [round(x ,4), round(y ,4)]

    def get_rotation_angle(self):
        return math.atan2(self.direction[1], self.direction[0]) - (math.pi / 2)
    
    def turn_car(self, turn_speed):
        '''Turns the car by TURN_SPEED while either the Left or Right key's are held down'''
        turn = self.speed * (1.2 - self.speed) * turn_speed * 0.3
        self.direction[0], self.direction[1] = Car.rotate_vector(self.direction, turn)
        mag = math.hypot(self.direction[0], self.direction[1])
        if mag:
            self.direction[0] /= mag
            self.direction[1] /= mag

    def move(self, time_delta):
        '''moves the car's coordinates "forward" by its speed depending on its direction vector'''
        self.coordinates[0] += self.speed*time_delta*self.direction[0]
        self.coordinates[1] += self.speed*time_delta*self.direction[1]
    
    def auto_slowdown(self):
        '''slows down the player when the forward button is not being pushed'''
        if self.speed > 0:
            self.speed -= 0.01 * self.MAX_SPEED


    def update_image_coordinates(self):
        '''Rotate all image coordinates from original positions based on direction'''
        angle = self.get_rotation_angle()
        
        # Rotate car image coordinates
        self.image_coords = []
        for coord in self.init_car_image_coords:
            rotated_coord = Car.rotate_vector(coord, angle)
            self.image_coords.append(rotated_coord)
        
        # Rotate wheel coordinates
        self.backwheel_coords = []
        for coord in self.init_backwheel_coords:
            rotated_coord = Car.rotate_vector(coord, angle)
            self.backwheel_coords.append(rotated_coord)
            
        self.frontwheel_coords = []
        for coord in self.init_frontwheel_coords:
            rotated_coord = Car.rotate_vector(coord, angle)
            self.frontwheel_coords.append(rotated_coord)


    def display(self):
        glColor3f(0.0, 0.0, 0.0)
    #----Front Wheels---
        glBegin(GL_TRIANGLE_FAN)
        for n in range(4):
            glVertex2f(self.coordinates[0] + self.image_coords[2][0] + self.frontwheel_coords[n][0], self.coordinates[1] + self.image_coords[2][1] + self.frontwheel_coords[n][1])
        glColor3f(0.0, 0.0, 0.0)
        glEnd()
        glBegin(GL_TRIANGLE_FAN)
        for n in range(4):
            glVertex2f(self.coordinates[0] + self.image_coords[19][0] + self.frontwheel_coords[n][0], self.coordinates[1] + self.image_coords[19][1] + self.frontwheel_coords[n][1])
        glColor3f(0.0, 0.0, 0.0)
        glEnd()
    #----Back Wheels---
        glBegin(GL_TRIANGLE_FAN)
        for n in range(4):
            glVertex2f(self.coordinates[0] + self.image_coords[7][0] + self.backwheel_coords[n][0], self.coordinates[1] + self.image_coords[7][1] + self.backwheel_coords[n][1])
        glColor3f(0.0, 0.0, 0.0)
        glEnd()
        glBegin(GL_TRIANGLE_FAN)
        for n in range(4):
            glVertex2f(self.coordinates[0] + self.image_coords[14][0] + self.backwheel_coords[n][0], self.coordinates[1] + self.image_coords[14][1] + self.backwheel_coords[n][1])
        glColor3f(0.0, 0.0, 0.0)
        glEnd()
    #-----#----Car Frame----#-----#
        glColor3f(self.color_a, self.color_b, self.color_c)                   
        glBegin(GL_TRIANGLE_FAN)
        for n in range(len(self.image_coords)-1):
            glVertex2f(self.coordinates[0] + self.image_coords[n][0], self.coordinates[1] + self.image_coords[n][1])
        glColor3f(self.color_a, self.color_b, self.color_c)
        glEnd()