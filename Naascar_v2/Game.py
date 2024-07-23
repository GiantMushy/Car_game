import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *
import time
from LaptimeData import LaptimeData
from Physics import Physics
from Pixels import Pixels
from Track import Track
from Car import Car

NUM_OF_LAPS = 5
ASS_X, ASS_Y = 2200, 1800 #Full Aspect Ratio
#ASPECT_X, ASPECT_Y = 1760, 1440 #2200 * 0.8 = 1760 .... 1800 * 0.8 = 1440
ASPECT_X, ASPECT_Y = 1100, 900 #2200 * 0.8 = 1760 .... 1800 * 0.8 = 1440
ASPECT_X_RATIO = ASS_X/ASPECT_X
ASPECT_Y_RATIO = ASS_Y/ASPECT_Y
class Naascar:
    def __init__(self, track = 0):
        self.text = Pixels()
        self.Laptime = LaptimeData()
        pygame.display.init()
        pygame.display.set_mode((ASPECT_X, ASPECT_Y), DOUBLEBUF|OPENGL)
        glClearColor(0.0, 0.0, 0.0, 1.0)

        self.track_id = track
        self.track = Track(track)
        x, y = self.track.finish_line_cell
        shift_x = x * 400 + 100 
        shift_y = y * 400 + 100
        if self.track.cells[(x, y)] == self.track.vert_left_image:  # Creating the Car Class with correct car_position and car_direction
            self.car = Car([[shift_x + 130, shift_y + 350],[shift_x + 70, shift_y + 350]], [[0,1],[0,1]])
        elif self.track.cells[(x, y)] == self.track.vert_right_image:
            self.car = Car([[shift_x + 330, shift_y + 350],[shift_x + 270, shift_y + 350]], [[0,1],[0,1]])
        elif self.track.cells[(x, y)] == self.track.horiz_top_image:
            self.car = Car([[shift_x + 350, shift_y + 330],[shift_x + 350, shift_y + 270]], [[1,0],[1,0]])
        elif self.track.cells[(x, y)] == self.track.horiz_bot_image:
            self.car = Car([[shift_x + 350, shift_y + 130],[shift_x + 350, shift_y + 70]], [[1,0],[1,0]])

        self.physics = Physics(self.car, track)
        
        self.arrow_key_data = [[False, False, False, False],[False, False, False, False]]

        self.back_arrow_image = [[0,20],[20,40],[20,30],[50,30],[50,10],[20,10],[20,0]]
        self.back_arrow_pos = [2000, 1700]
        self.back = False
        self.lap_count_image = [[-5,-15],[-15,-5],[-15,5],[-5,15],[5,15],[15,5],[15,-5],[5,-15]]
        self.lap_count = [0,0]
        self.lap_check1 = [False,False]
        self.lap_check2 = [False,False]
        self.winning_state = [False, False]
        self.player_time = [False, False]


    def update(self, p):
        car_pos = (round((self.car.car_coordinates[p][0] - 100) // 400), round((self.car.car_coordinates[p][1] - 100) // 400))
        delta = self.__clock.tick(60)
        self.physics.improved_wall_boundries(car_pos, p)
        self.move_car(p)
        self.auto_slowdown(p)
        self.car.move_car_forward(p, delta)
        self.lap_direction_check(p)
        #naascar.bump_cars()


    def move_car(self,p):
        '''Turns the car by TURN_SPEED while either the Left [0] or Right [1] key's are held down'''
        if self.arrow_key_data[p][0]:
            self.car.turn_car(p, 1)

        if self.arrow_key_data[p][1]:
            self.car.turn_car(p,-1)
        
        '''increases or decreases the cars speed'''
        if self.arrow_key_data[p][2] and self.car.car_speed[p] < self.car.MAX_SPEED:
            self.car.car_speed[p] += 0.01

        if self.arrow_key_data[p][3] and self.car.car_speed[p] > 0:
            self.car.car_speed[p] -= 0.01


    def auto_slowdown(self, p):
        '''slows down the player when the forward button is not being pushed'''
        if self.car.car_speed[p] > 0 and not self.arrow_key_data[p][2]:
            self.car.car_speed[p] -= 0.01 * self.car.MAX_SPEED


    def lap_direction_check(self, p):
        '''Checks if the car is heading in the correct direction. Both lap_check's must be True in order for
            the player's lap_count to increase when crossing the finish line'''
        x, y = self.track.finish_line_cell
        shift_x = x * 400 + 100 
        shift_y = y * 400 + 100
        x_car = self.car.car_coordinates[p][0]
        y_car = self.car.car_coordinates[p][1]

        if self.track.cells[(x, y)] == self.track.vert_left_image:
            if (shift_x) <= x_car <= (shift_x + 200) and (shift_y) <= y_car <= (shift_y + 20):
                self.lap_check_1(p)
            elif (shift_x) <= x_car <= (shift_x + 200) and (shift_y + 100) <= y_car <= (shift_y + 120):
                self.lap_check_2(p)
            elif (shift_x) <= x_car <= (shift_x + 200) and (shift_y + 380) <= y_car <= (shift_y + 400):
                self.lap(p)

        elif self.track.cells[(x, y)] == self.track.horiz_top_image:
            if (shift_x + 100) <= x_car <= (shift_x + 120) and (shift_y + 200) <= y_car <= (shift_y + 400):
                self.lap_check_1(p)
            elif (shift_x + 200) <= x_car <= (shift_x + 220) and (shift_y + 200) <= y_car <= (shift_y + 400):
                self.lap_check_2(p)
            elif (shift_x + 380) <= x_car <= (shift_x + 400) and (shift_y + 200) <= y_car <= (shift_y + 400):
                self.lap(p)

        elif self.track.cells[(x, y)] == self.track.vert_right_image:
            if (shift_x + 200) <= x_car <= (shift_x + 400) and (shift_y) <= y_car <= (shift_y + 20):
                self.lap_check_1(p)
            elif (shift_x + 200) <= x_car <= (shift_x + 400) and (shift_y + 100) <= y_car <= (shift_y + 120):
                self.lap_check_2(p)
            elif (shift_x + 200) <= x_car <= (shift_x + 400) and (shift_y + 380) <= y_car <= (shift_y + 400):
                self.lap(p)

        elif self.track.cells[(x, y)] == self.track.horiz_bot_image:
            if (shift_x + 100) <= x_car <= (shift_x + 120) and (shift_y) <= y_car <= (shift_y + 200):
                self.lap_check_1(p)
            elif (shift_x + 200) <= x_car <= (shift_x + 220) and (shift_y) <= y_car <= (shift_y + 200):
                self.lap_check_2(p)
            elif (shift_x + 380) <= x_car <= (shift_x + 400) and (shift_y) <= y_car <= (shift_y + 200):
                self.lap(p)


    def lap_check_1(self, p):
        if self.lap_check1[p] == False:
            if self.lap_check2[p] == False:
                self.lap_check1[p] = True
            else:
                self.lap_check2[p] = False
                self.lap_check1[p] = False
        else:
            if self.lap_check2[p] == True:
                self.lap_check1[p] = False
                self.lap_check2[p] = False


    def lap_check_2(self, p):
        if self.lap_check2[p] == False:
            if self.lap_check1[p] == True:
                self.lap_check2[p] = True
            else:
                self.lap_check2[p] = False
    

    def lap(self, p):
        if self.lap_check1[p] == True and self.lap_check2[p] == True:
            self.lap_count[p] += 1
            self.lap_check1[p] = False
            self.lap_check2[p] = False


    def back_click(self, xpos, ypos):
        x = xpos - self.back_arrow_pos[0] - 25
        y = ypos - self.back_arrow_pos[1] - 20
        if sqrt(x*x + y*y) <= 35:
            self.back = True


    def win_screen(self, n):
        '''
        Colors the screen white if player 1 wins
        Colors the screen blue if player 2 wins
        '''
        glColor3f(n, 1.0, 1.0)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(400,300)
        glVertex2f(400,900)
        glVertex2f(1200,900)
        glVertex2f(1200,300)
        glEnd()


    def init_timer(self):
        self.start_time = time.time()


    def init_clock(self):
        self.__clock = pygame.time.Clock()


    def format_time(self, time):
        stopwatch = round(time - self.start_time,2)
        seconds, milliseconds = str(stopwatch).split('.')
        milliseconds = int(milliseconds)
        seconds = int(seconds)
        minutes = 0
        if seconds // 60 > 0:
            minutes += 1
            seconds -= 60
        print_format= '{:02d}:{:02d}:{:02d}'
        return print_format.format(minutes, seconds, milliseconds)


    def save_laptime(self, time):
        self.Laptime.add_laptime(track_id = self.track_id, time = time)


    def display_best_laptime(self):
        best_lap = self.Laptime.get_best_track_laptime(self.track_id)
        self.text.display_text(50, 100, "PB: " + best_lap, 2)


    def display_time(self):
        # 'seconds': '{:02d}:{:02d}:{:02d}',
        self.ctime = self.format_time(time.time())
        self.text.display_text(130, 1725, self.ctime, 2)
        pass


    def display_lapcount(self):
        '''Displays one *Player* colored circle in the top left for each laps remaining'''
        glColor3f(0.0, 1.0, 1.0)
        for n in range(2):
            for m in range(5-self.lap_count[n]):
                glColor3f(not n, 1.0, 1.0)
                glBegin(GL_TRIANGLE_FAN)
                for c in range(len(self.lap_count_image)):
                    glVertex2f(self.lap_count_image[c][0] + 50 + 40*n, self.lap_count_image[c][1] + 1600 + 35*m)
                glEnd()


    def display_back_arrow(self):
        '''Displays the back arrow in the top left of the screen'''
        self.back_arrow_hitbox = []
        ####### Circle #######
        posx, posy = self.back_arrow_pos[0] + 25, self.back_arrow_pos[1] + 20
        sides = 32
        radius = 35
        angle = 2*pi/sides
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POLYGON)
        for i in range(sides):
            cosine= radius * cos(i*angle) + posx
            sine  = radius * sin(i*angle) + posy
            glVertex2f(cosine, sine)
            self.back_arrow_hitbox.append([cosine, sine])
        glEnd()
        ######## Arrow #######
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_TRIANGLE_FAN)
        for c in range(len(self.back_arrow_image)):
            glVertex2f(self.back_arrow_image[c][0] + self.back_arrow_pos[0], self.back_arrow_image[c][1] + self.back_arrow_pos[1])
        glEnd()


    def display(self, start, n):
        '''Displays the game and all of it's components in the pygame viewport'''
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glViewport(0, 0, ASPECT_X, ASPECT_Y)
        gluOrtho2D(0, 2200, 0, 1800)

        self.track.display()
        self.car.display()
        self.display_lapcount()
        self.display_back_arrow()
        #self.display_best_laptime()

        if self.player_time[0]:
            self.text.display_text(130, 1690, "P1: " + self.player_time[0], 2)
        if self.player_time[1]:
            self.text.display_text(130, 1655, "P2: " + self.player_time[1], 2)
            
        if start:
            self.display_time()
        else:
            self.text.display_text(1000, 900, str(3 - n), 10)

        pygame.display.flip() #display frame buffer


    def game_loop(self):
        if self.lap_count[0] == 5 and not self.player_time[0]: 
            if not self.player_time[1]:
                print("Player 1 has won!!")
            self.player_time[0] = self.format_time( time.time() )
            self.save_laptime(self.player_time[0])
            
        if self.lap_count[1] == 5 and not self.player_time[1]:
            if not self.player_time[0]:
                print("Player 2 has won!!")
            self.player_time[1] = self.format_time( time.time() )
            self.save_laptime(self.player_time[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE: #escape key
                    pygame.quit()
                    quit()
                elif event.key == K_LEFT:
                    self.arrow_key_data[0][0] = True
                elif event.key == K_RIGHT:
                    self.arrow_key_data[0][1] = True
                elif event.key == K_UP:
                    self.arrow_key_data[0][2] = True
                elif event.key == K_DOWN:
                    self.arrow_key_data[0][3] = True
                elif event.key == K_a:
                    self.arrow_key_data[1][0] = True
                elif event.key == K_d:
                    self.arrow_key_data[1][1] = True
                elif event.key == K_w:
                    self.arrow_key_data[1][2] = True
                elif event.key == K_s:
                    self.arrow_key_data[1][3] = True
                
            elif event.type == pygame.KEYUP:
                if event.key == K_LEFT:
                    self.arrow_key_data[0][0] = False
                elif event.key == K_RIGHT:
                    self.arrow_key_data[0][1] = False
                elif event.key == K_UP:
                    self.arrow_key_data[0][2] = False
                elif event.key == K_DOWN:
                    self.arrow_key_data[0][3] = False
                if event.key == K_a:
                    self.arrow_key_data[1][0] = False
                elif event.key == K_d:
                    self.arrow_key_data[1][1] = False
                elif event.key == K_w:
                    self.arrow_key_data[1][2] = False
                elif event.key == K_s:
                    self.arrow_key_data[1][3] = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = (pygame.mouse.get_pos()[0]) * ASPECT_X_RATIO
                    y = (ASPECT_Y - pygame.mouse.get_pos()[1]) * ASPECT_Y_RATIO
                    self.back_click(x, y)

        '''update() runs twice, once for each player'''
        self.display(True, 0)
        for n in range(2):
            self.update(n) #update both players positions


    def start_game(self):
        for n in range(3):
            self.display(False, n)
            time.sleep(1)
        self.init_timer()
        self.init_clock()
        while True:
            self.game_loop()
            if self.back:
                break


if __name__ == "__main__":
    game = Naascar(8)
    game.start_game()