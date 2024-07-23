from Track import *
from Car import*
import math


class Physics:
    def __init__(self, car, track = 0):
        self.track = Track(track)
        self.car = car

    def bounce(self, nx, ny, p):
        '''Takes as input a given normalized vector and bounces player (p)'s direction vector and image coordinates with the input vector1'''
        self.car.car_direction[p] = Physics.bounce_direction(nx, ny, self.car.car_direction[p])

        self.car.image_coords[p] = Physics.bounce_image(nx, ny, self.car.image_coords[p], len(self.car.image_coords[p])-1)
        self.car.backwheel_coords[p] = Physics.bounce_image(nx, ny, self.car.backwheel_coords[p], 4)
        self.car.frontwheel_coords[p] = Physics.bounce_image(nx, ny, self.car.frontwheel_coords[p], 4)
        #self.car.car_speed[p] = self.car.car_speed[p] * 0.5

    def bounce_direction(nx, ny, car_direction):
        #----------------bounce car direction------------------
        reflected_x =car_direction[0] - 2 * (car_direction[0]*(nx) + car_direction[1]*(ny))*(nx)
        reflected_y =car_direction[1] - 2 * (car_direction[0]*(nx) + car_direction[1]*(ny))*(ny)
        return [round(reflected_x, 4), round(reflected_y, 4)]

    def bounce_image(nx, ny, image, image_size):
        #----------------bounce car image coordiantes----------
        for n in range(image_size):
            reflected_image_x =image[n][0] - 2 * (image[n][0]*(nx) + image[n][1]*(ny))*(nx)
            reflected_image_y =image[n][1] - 2 * (image[n][0]*(nx) + image[n][1]*(ny))*(ny)
            image[n] = [round(reflected_image_x, 4), round(reflected_image_y, 4)]
        return image

    def improved_wall_boundries(self, cell, p):
        cell_data = self.track.get_cell_data(cell[0], cell[1])
        cell_x = cell[0] * 400 + 100
        cell_y = cell[1] * 400 + 100

        #---------------------------- 90° TRUNS ---------------------------------
        if cell_data == self.track.up_right_image:
            if self.car.car_coordinates[p][1] - cell_y >= self.car.car_coordinates[p][0] - cell_x + 85:
                Physics.bounce(self, 0.707, -0.707, p)
            if self.car.car_coordinates[p][1] - cell_y <= self.car.car_coordinates[p][0] - cell_x - 185:
                Physics.bounce(self, -0.707, 0.707, p)
            if self.car.car_coordinates[p][1] >= cell_y + 385:
                Physics.bounce(self, 0, -1, p)
            if self.car.car_coordinates[p][0] <= cell_x + 15:
                Physics.bounce(self, 1, 0, p)

        elif cell_data == self.track.up_left_image:
            if self.car.car_coordinates[p][0] + self.car.car_coordinates[p][1] >= cell_x + cell_y + 485:
                Physics.bounce(self, -0.707, -0.707, p)
            if self.car.car_coordinates[p][0] + self.car.car_coordinates[p][1] <= cell_x + cell_y + 215:
                Physics.bounce(self, 0.707, 0.707, p)
            if self.car.car_coordinates[p][1] >= cell_y + 385:
                Physics.bounce(self, 0, -1, p)
            if self.car.car_coordinates[p][0] >= cell_x + 385:
                Physics.bounce(self, -1, 0, p)

        elif cell_data == self.track.down_right_image:
            if self.car.car_coordinates[p][0] + self.car.car_coordinates[p][1] >= cell_x + cell_y + 585:
                Physics.bounce(self, -0.707, -0.707, p)
            if self.car.car_coordinates[p][0] + self.car.car_coordinates[p][1] <= cell_x + cell_y + 315:
                Physics.bounce(self, 0.707, 0.707, p)
            if self.car.car_coordinates[p][1] <= cell_y + 15:
                Physics.bounce(self, 0, 1, p)
            if self.car.car_coordinates[p][0] <= cell_x + 15:
                Physics.bounce(self, 1, 0, p)

        elif cell_data == self.track.down_left_image:
            if self.car.car_coordinates[p][1] - cell_y >= self.car.car_coordinates[p][0] - cell_x + 185:
                Physics.bounce(self, 0.707, -0.707, p)
            if self.car.car_coordinates[p][1] - cell_y <= self.car.car_coordinates[p][0] - cell_x - 85:
                Physics.bounce(self, -0.707, 0.707, p)
            if self.car.car_coordinates[p][1] <= cell_y + 15:
                Physics.bounce(self, 0, 1, p)
            if self.car.car_coordinates[p][0] >= cell_x + 385:
                Physics.bounce(self, -1, 0, p)

        #--------------------------- STRAIGHT WAYS ----------------------------      
        elif cell_data == self.track.vert_left_image:
            if self.car.car_coordinates[p][0] >= cell_x + 185:
                Physics.bounce(self, -1, 0, p)
            if self.car.car_coordinates[p][0] <= cell_x + 15:
                Physics.bounce(self, 1, 0, p)

        elif cell_data == self.track.vert_right_image:
            if self.car.car_coordinates[p][0] >= cell_x + 385:
                Physics.bounce(self, -1, 0, p)
            if self.car.car_coordinates[p][0] <= cell_x + 215:
                Physics.bounce(self, 1, 0, p)

        elif cell_data == self.track.horiz_top_image: #####
            if self.car.car_coordinates[p][1] >= cell_y + 385:
                Physics.bounce(self, 0, -1, p)
            if self.car.car_coordinates[p][1] <= cell_y + 215:
                Physics.bounce(self, 0, 1, p)

        elif cell_data == self.track.horiz_bot_image:
            if self.car.car_coordinates[p][1] >= cell_y + 185:
                Physics.bounce(self, 0, -1, p)
            if self.car.car_coordinates[p][1] <= cell_y + 15:
                Physics.bounce(self, 0, 1, p)

        #--------------------------- Lane Switch -----------------------------
        elif cell_data == self.track.right_up_60_image:
            if self.car.car_coordinates[p][1] >= cell_y + 385:
                Physics.bounce(self, 0, -1, p)
            if self.car.car_coordinates[p][1] <= cell_y + 15:
                Physics.bounce(self, 0, 1, p)
            if (self.car.car_coordinates[p][0] - cell_x) * 0.666667 - (self.car.car_coordinates[p][1] - cell_y) <= -185:
                Physics.bounce(self, -0.55, 0.83, p)
            if (self.car.car_coordinates[p][0] - cell_x) * 0.666667 - (self.car.car_coordinates[p][1] - cell_y) >= 51.4:
                Physics.bounce(self, 0.55, -0.83, p)

        elif cell_data == self.track.right_down_60_image:
            if self.car.car_coordinates[p][1] >= cell_y + 385:
                Physics.bounce(self, 0, -1, p)
            if self.car.car_coordinates[p][1] <= cell_y + 15:
                Physics.bounce(self, 0, 1, p)
            if (self.car.car_coordinates[p][0] - cell_x) * 0.666667 + (self.car.car_coordinates[p][1] - cell_y) >= 451.68:
                Physics.bounce(self, -0.55, -0.83, p)
            if (self.car.car_coordinates[p][0] - cell_x) * 0.666667 + (self.car.car_coordinates[p][1] - cell_y) <= 215:
                Physics.bounce(self, 0.55, 0.83, p)

        elif cell_data == self.track.up_right_60_image: ########### NEEDS FIXING ##############
            if self.car.car_coordinates[p][0] >= cell_x + 385:
                Physics.bounce(self, -1, 0, p)
            if self.car.car_coordinates[p][0] <= cell_x + 15:
                Physics.bounce(self, 1, 0, p)
            if (self.car.car_coordinates[p][0] - cell_x) * 1.5 - (self.car.car_coordinates[p][1] - cell_y) <= -77.5: 
                Physics.bounce(self, -0.83, 0.55, p)
            if (self.car.car_coordinates[p][0] - cell_x) * 1.5 - (self.car.car_coordinates[p][1] - cell_y) >= 277.5:
                Physics.bounce(self, 0.83, -0.55, p)

        elif cell_data == self.track.up_left_60_image: ########### NEEDS FIXING ##############
            if self.car.car_coordinates[p][0] >= cell_x + 385:
                Physics.bounce(self, -1, 0, p)
            if self.car.car_coordinates[p][0] <= cell_x + 15:
                Physics.bounce(self, 1, 0, p)
            if (self.car.car_coordinates[p][0] - cell_x) * 1.5 + (self.car.car_coordinates[p][1] - cell_y) >= 677.5:
                Physics.bounce(self, -0.83, -0.55, p)
            if (self.car.car_coordinates[p][0] - cell_x) * 1.5 + (self.car.car_coordinates[p][1] - cell_y) <= 322.5:
                Physics.bounce(self, 0.83, 0.55, p)

        #--------------------------- Corners --------------------------------
        elif cell_data == self.track.top_right_corner_image:
            if self.car.car_coordinates[p][0] + self.car.car_coordinates[p][1] <= cell_x + cell_y + 615:
                Physics.bounce(self, 0.707, 0.707, p)

        elif cell_data == self.track.bot_right_corner_image:
            if self.car.car_coordinates[p][1] - cell_y + 215 >= self.car.car_coordinates[p][0] - cell_x:
                Physics.bounce(self, 0.707, -0.707, p)

        elif cell_data == self.track.top_left_corner_image:
            if self.car.car_coordinates[p][1] - cell_y - 215 <= self.car.car_coordinates[p][0] - cell_x:
                Physics.bounce(self, -0.707, 0.707, p)

        elif cell_data == self.track.bot_left_corner_image:
            if self.car.car_coordinates[p][0] + self.car.car_coordinates[p][1] >= cell_x + cell_y + 185:
                Physics.bounce(self, -0.707, -0.707, p)

        else:
            print("Cell Data Error")