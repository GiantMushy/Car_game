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

# TODO: Tweak bouncing physics
# TODO: Main menu
    # - num of player selection
    # - high scores
    # - player name input
# TODO: have viewport smaller and follow the car around the track (only singleplayer)


class Naascar:
    def __init__(self, track_id = 0, settings = {}):
        self.aspect_x = settings["aspect_x"]
        self.aspect_y = settings["aspect_y"]
        self.viewport = settings["viewport"]
        self.num_of_players = settings["num_of_players"]
        self.num_of_laps = settings["num_of_laps"]

        self.text = Pixels()
        self.Laptime = LaptimeData()
        pygame.display.init()
        pygame.display.set_mode((self.aspect_x, self.aspect_y), DOUBLEBUF|OPENGL)
        glClearColor(0.0, 0.0, 0.0, 1.0)

        self.track_id = track_id
        self.track = Track(track_id)
        self.physics = Physics(self.track)
        self.init_cars()
        
        self.arrow_key_data = [[False, False, False, False] for _ in range(self.num_of_players)]  # Left, Right, Up, Down

        self.back_arrow_image = [[0,20],[20,40],[20,30],[50,30],[50,10],[20,10],[20,0]]
        self.back_arrow_pos = [2000, 1700]
        self.back = False

        self.lap_count_image = [[-5,-15],[-15,-5],[-15,5],[-5,15],[5,15],[15,5],[15,-5],[5,-15]]
        self.lap_count = [0] * self.num_of_players
        self.lap_check1 = [False] * self.num_of_players
        self.lap_check2 = [False] * self.num_of_players

        self.player_time = [False] * self.num_of_players
        self.winner = None
    
    def init_cars(self):
        self.cars = []
        id = 0

        x, y = self.track.finish_line_cell
        shift_x = x * 400 + 100 
        shift_y = y * 400 + 100

        if self.track.cells[(x, y)] == self.track.vert_left_image:  # Creating the Car Class with correct car_position and car_direction
            for n in range(self.num_of_players):
                self.place_car(shift_x + 130 - 60*n, shift_y + 350, [0, 1], id)
                id += 1
            
        elif self.track.cells[(x, y)] == self.track.vert_right_image:
            for n in range(self.num_of_players):
                self.place_car(shift_x + 330 - 60*n, shift_y + 350, [0, 1], id)
                id += 1

        elif self.track.cells[(x, y)] == self.track.horiz_top_image:
            for n in range(self.num_of_players):
                self.place_car(shift_x + 350, shift_y + 130 - 60*n, [1, 0], id)
                id += 1

        elif self.track.cells[(x, y)] == self.track.horiz_bot_image:
            for n in range(self.num_of_players):
                self.place_car(shift_x + 350, shift_y + 330 - 60*n, [1, 0], id)
                id += 1

    def place_car(self, x, y, rotation, id):
        color = [not id, 1.0, 1.0]  # Cycle through Red, Green, Blue for each car
        self.cars.append(Car([x, y], rotation, color, id))


    def update(self, car):
        delta = self.__clock.tick(60)

        self.physics.wall_boundries(car)
        car.update(delta, self.arrow_key_data[car.id])

        self.lap_direction_checks(car)


    def lap_direction_checks(self, car):
        '''Checks if the car is heading in the correct direction. Both lap_check's must be True in order for
            the player's lap_count to increase when crossing the finish line'''
        x, y = self.track.finish_line_cell
        shift_x = x * 400 + 100 
        shift_y = y * 400 + 100

        p = car.id
        
        x_car = car.coordinates[0]
        y_car = car.coordinates[1]

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
        if self.lap_check1[p] and self.lap_check2[p]:
            self.lap_count[p] += 1
            self.lap_check1[p] = False
            self.lap_check2[p] = False
            # Winner detection
            if self.winner is None and self.lap_count[p] >= self.num_of_laps:
                self.player_time[p] = self.format_time(time.time())
                self.save_laptime(self.player_time[p])
                self.winner = p + 1          # car.id + 1
                print(f"Player {self.winner} has won!")

    def win_screen(self):
        # Full screen overlay
        glColor4f(0.0, 0.0, 0.0, 0.6)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)
        glVertex2f(0, self.viewport["height"])
        glVertex2f(self.viewport["width"], self.viewport["height"])
        glVertex2f(self.viewport["width"], 0)
        glEnd()

        glColor3f(self.winner % 2, 1.0, 1.0)

        self.text.display_text(900, 1000, f"PLAYER {self.winner} WINS!", 10)
        self.text.display_text(920, 900, "PRESS ESC OR CLICK BACK", 4)


    def init_timer(self):
        self.start_time = time.time()


    def init_clock(self):
        self.__clock = pygame.time.Clock()


    def format_time(self, time):
        stopwatch = round(time - self.start_time,2)
        seconds, milliseconds = str(stopwatch).split('.')
        milliseconds = int(milliseconds)
        seconds = int(seconds)
        minutes = seconds // 60
        seconds = seconds % 60
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


    def display(self, start, countdown):
        '''Displays the game and all of it's components in the pygame viewport'''
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glViewport(0, 0, self.aspect_x, self.aspect_y)
        gluOrtho2D(self.viewport["x"], self.viewport["width"], self.viewport["y"], self.viewport["height"])

        self.track.display()
        for car in self.cars:
            car.display()
        self.display_lapcount()
        self.display_back_arrow()
        #self.display_best_laptime()

        for n in range(self.num_of_players):
            if self.player_time[n]:
                self.text.display_text(130, 1690, f"P{n}: " + self.player_time[n], 2)
            
        if start:
            self.display_time()
        else:
            self.text.display_text(1000, 900, str(3 - countdown), 10)

        if self.winner:
            self.win_screen()

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
                if self.winner is None:
                    if event.key == K_LEFT:       self.arrow_key_data[0][0] = True
                    elif event.key == K_RIGHT:      self.arrow_key_data[0][1] = True
                    elif event.key == K_UP:         self.arrow_key_data[0][2] = True
                    elif event.key == K_DOWN:       self.arrow_key_data[0][3] = True
                    if self.num_of_players == 2:
                        if event.key == K_a:        self.arrow_key_data[1][0] = True
                        elif event.key == K_d:      self.arrow_key_data[1][1] = True
                        elif event.key == K_w:      self.arrow_key_data[1][2] = True
                        elif event.key == K_s:      self.arrow_key_data[1][3] = True
                
            elif event.type == pygame.KEYUP:
                if event.key == K_LEFT:         self.arrow_key_data[0][0] = False
                elif event.key == K_RIGHT:      self.arrow_key_data[0][1] = False
                elif event.key == K_UP:         self.arrow_key_data[0][2] = False
                elif event.key == K_DOWN:       self.arrow_key_data[0][3] = False
                if self.num_of_players == 2:
                    if event.key == K_a:        self.arrow_key_data[1][0] = False
                    elif event.key == K_d:      self.arrow_key_data[1][1] = False
                    elif event.key == K_w:      self.arrow_key_data[1][2] = False
                    elif event.key == K_s:      self.arrow_key_data[1][3] = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    wx, wy = self.mouse_to_world(x, y)
                    if self.point_in_rect(wx, wy, self.back_arrow_pos[0], self.back_arrow_pos[1], 70, 40):
                        self.back = True

        self.display(True, 0)
        if not self.winner:
            for car in self.cars:
                self.update(car)
    

    def point_in_rect(self, px, py, rx, ry, rw, rh):
        return (rx <= px <= rx + rw) and (ry <= py <= ry + rh)
    

    def mouse_to_world(self, sx, sy):
        """Convert screen-space mouse to world-space (OpenGL ortho) coords"""
        sy_flipped = self.aspect_y - sy
        wx = sx * (self.viewport["width"] / self.aspect_x)   # 2200/1100 = 2
        wy = sy_flipped * (self.viewport["height"] / self.aspect_y)  # 1800/900 = 2
        return wx, wy


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
    settings = {
        "aspect_x": 1100,
        "aspect_y": 900,
        "viewport": {
            "x": 0,
            "y": 0,
            "width": 2200,
            "height": 1800
        },
        "num_of_players": 2,
        "num_of_laps": 5
    }
    game = Naascar(0, settings)
    game.start_game()