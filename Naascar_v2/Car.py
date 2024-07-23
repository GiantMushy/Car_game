from OpenGL.GL import *
from OpenGL.GLU import *
import math


class Car:
    def __init__(self, car_coordinates = [[0,0], [0,0]], car_direction = [[0,1],[0,1]]):

        self.MAX_SPEED = 1

        self.game_start = True
        #--------------------------------- CAR Location/Orientation DATA -------------------------------------------
        #self.car_coordinates = [[230, 850], [170, 850]]
        self.car_coordinates = car_coordinates
        #self.car_direction = [[0,1],[0,1]]
        self.car_direction = car_direction
        self.car_speed = [0.00, 0.00]
        #---------------------------- CAR IMAGE COARDINATES ------------------------------------
        self.car1_image_coords = [[0,15],[10,15],[10,12.5],[10,10],[5,10],[5,-5],[-10,-5],[10,-7.5],[10,-10],[5,-10],[3,-15],[-3,-15],[-5,-10],[-10,-10],[-10,-7.5],[-10,-5],[-5,-5],[-5,10],[-10,10],[-10,12.5],[-10,15],[0,1]]
        self.car2_image_coords = [[0,15],[10,15],[10,12.5],[10,10],[5,10],[5,-5],[-10,-5],[10,-7.5],[10,-10],[5,-10],[3,-15],[-3,-15],[-5,-10],[-10,-10],[-10,-7.5],[-10,-5],[-5,-5],[-5,10],[-10,10],[-10,12.5],[-10,15],[0,1]]
        self.image_coords = [self.car1_image_coords, self.car2_image_coords]
        self.backwheel_coords= [[[-5,-7.5],[5,-7.5],[5,7.5],[-5,7.5]],[[-5,-7.5],[5,-7.5],[5,7.5],[-5,7.5]]]
        self.frontwheel_coords= [[[-4,-6],[4,-6],[4,6],[-4,6]],[[-4,-6],[4,-6],[4,6],[-4,6]]]
        if self.car_direction[0] == [1,0]:
            for p in range(2):
                self.turn_car_degrees(p, -1.57)


    def rotate_vector(v, deg):
        '''function inputs given vector data into the rotational equation'''
        x = math.cos(deg)*v[0] - math.sin(deg)*v[1]
        y = math.sin(deg)*v[0] + math.cos(deg)*v[1]
        return [round(x ,4), round(y ,4)]


    def turn_car(self, p, direction):
        '''Turns the car by TURN_SPEED while either the Left or Right key's are held down'''

        turn = self.car_speed[p] * (1.2 - self.car_speed[p]) * direction * 0.3
        self.car_direction[p][0], self.car_direction[p][1] = Car.rotate_vector(self.car_direction[p], turn)
        self.turn_car_degrees(p, turn)


    def turn_car_degrees(self, p, degrees):
        for n in range(len(self.image_coords[p])-1):
            self.image_coords[p][n] = Car.rotate_vector(self.image_coords[p][n], degrees)
        for n in range(len(self.backwheel_coords[p])):
            self.backwheel_coords[p][n] = Car.rotate_vector(self.backwheel_coords[p][n], degrees)
        for n in range(len(self.frontwheel_coords[p])):
            self.frontwheel_coords[p][n] = Car.rotate_vector(self.frontwheel_coords[p][n], degrees)


    def move_car_forward(self, p, time_delta):
        '''moves the car's cooardinates "forward" by its speed depending on its direction vector'''

        if self.car_direction[p][0] > 0:
            self.car_coordinates[p][0] += self.car_direction[p][0]*self.car_speed[p]*time_delta
        if self.car_direction[p][0] < 0:
            self.car_coordinates[p][0] += self.car_direction[p][0]*self.car_speed[p]*time_delta
        if self.car_direction[p][1] > 0:
            self.car_coordinates[p][1] += self.car_direction[p][1]*self.car_speed[p]*time_delta
        if self.car_direction[p][1] < 0:
            self.car_coordinates[p][1] += self.car_direction[p][1]*self.car_speed[p]*time_delta


    def display(self):
        for p in range(2):
            glColor3f(0.0, 0.0, 0.0)
        #----Front Wheels---
            glBegin(GL_TRIANGLE_FAN)
            for n in range(4):
                glVertex2f(self.car_coordinates[p][0] + self.image_coords[p][2][0] + self.frontwheel_coords[p][n][0], self.car_coordinates[p][1] + self.image_coords[p][2][1] + self.frontwheel_coords[p][n][1])
            glColor3f(0.0, 0.0, 0.0)
            glEnd()
            glBegin(GL_TRIANGLE_FAN)
            for n in range(4):
                glVertex2f(self.car_coordinates[p][0] + self.image_coords[p][19][0] + self.frontwheel_coords[p][n][0], self.car_coordinates[p][1] + self.image_coords[p][19][1] + self.frontwheel_coords[p][n][1])
            glColor3f(0.0, 0.0, 0.0)
            glEnd()
        #----Back Wheels---
            glBegin(GL_TRIANGLE_FAN)
            for n in range(4):
                glVertex2f(self.car_coordinates[p][0] + self.image_coords[p][7][0] + self.backwheel_coords[p][n][0], self.car_coordinates[p][1] + self.image_coords[p][7][1] + self.backwheel_coords[p][n][1])
            glColor3f(0.0, 0.0, 0.0)
            glEnd()
            glBegin(GL_TRIANGLE_FAN)
            for n in range(4):
                glVertex2f(self.car_coordinates[p][0] + self.image_coords[p][14][0] + self.backwheel_coords[p][n][0], self.car_coordinates[p][1] + self.image_coords[p][14][1] + self.backwheel_coords[p][n][1])
            glColor3f(0.0, 0.0, 0.0)
            glEnd()
        #-----#----Car Frame----#-----#
            glColor3f(not p,1.0,1.0)                   
            glBegin(GL_TRIANGLE_FAN)
            for n in range(len(self.image_coords[p])-1):
                glVertex2f(self.car_coordinates[p][0] + self.image_coords[p][n][0], self.car_coordinates[p][1] + self.image_coords[p][n][1])
            glColor3f(not p, 1.0, 1.0)
            glEnd()