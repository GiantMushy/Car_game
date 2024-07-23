import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Game import Naascar
from Track import Track
from Pixels import Pixels
from LaptimeData import LaptimeData

#ASPECT_X, ASPECT_Y = 1760, 1440 #2200 * 0.8 = 1760 .... 1800 * 0.8 = 1440
ASPECT_X, ASPECT_Y = 1100, 900 #2200 * 0.8 = 1760 .... 1800 * 0.8 = 1440
X_ASS = round(ASPECT_X * 0.25)
Y_ASS = round(ASPECT_Y * 0.25)

class TrackSelection:

    def __init__(self):
        self.text = Pixels()
        self.track = Track()
        self.tracks_list = []
        for n in range(len(self.track.cells_list)):
            self.tracks_list.append(Track(n))
        pygame.display.init()
        pygame.display.set_mode((ASPECT_X, ASPECT_Y), DOUBLEBUF|OPENGL)
        glClearColor(0.0, 0.0, 0.0, 1.0)

        #--------------------------------- IMAGE COORDINATES ----------------------------------
        self.window_frame_1 = [[50,10],[10,50],[10,400],[50,440],[500,440],[540,400],[540,50],[500,10]]
        self.window_frame_2 = [[45,5],[5,45],[5,405],[45,445],[505,445],[545,405],[545,45],[505,5]]
        self.window_frame_3 = [[40,0],[0,40],[0,410],[40,450],[510,450],[550,410],[550,40],[510,0]]

        #---------------------------- Window Hitbox Coordinates -------------------------------
        self.track_selection_grid = []
        for y in range(3):
            for x in range(3):
                self.track_selection_grid.append([(x * 480 + 150), (300 + 370 * y)])

    def select_track(self, x, y):
        cell_count = 0
        for cell in self.track_selection_grid:
            if cell[0] <= x <= cell[0] + ASPECT_X*0.25 and cell[1] <= y <= cell[1] + ASPECT_Y*0.229:
                self.start_track(cell_count)
            cell_count += 1

    def start_track(self, track):
        game_naascar = Naascar(track)
        game_naascar.start_game()


    def display_track_window(self, track_nmbr, x , y):
        '''Displays the track in a small selectable window'''
        glViewport(x, y, X_ASS, Y_ASS)
        self.tracks_list[track_nmbr].display()


    def display_window_frame(self, x, y):
        glViewport(x, y, ASPECT_X, ASPECT_Y)
        glColor3f(0.0, 0.0, 3.0)
        glBegin(GL_TRIANGLE_FAN)
        for c in range(len(self.window_frame_3)):
            glVertex2f(self.window_frame_3[c][0], self.window_frame_3[c][1])
        glEnd()
        glColor3f(0.0, 1.0, 1.0)
        glBegin(GL_TRIANGLE_FAN)
        for c in range(len(self.window_frame_2)):
            glVertex2f(self.window_frame_2[c][0], self.window_frame_2[c][1])
        glEnd()
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_TRIANGLE_FAN)
        for c in range(len(self.window_frame_1)):
            glVertex2f(self.window_frame_1[c][0], self.window_frame_1[c][1])
        glEnd()


    def display(self):
        '''Displays the game and all of it's components in the pygame viewport'''
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glViewport(0, 0, ASPECT_X, ASPECT_Y)
        gluOrtho2D(0, 2200, 0, 1800)
        self.text.display_text(200, 1600, "SELECT A TRACK TO PLAY", 6) #display_text(xpos, ypos, "text", pixel_size)
        self.text.display_text(200, 1500, "23:45", 4)

        for track_nmbr in range(len(self.track.cells_list)):
            x = round(ASPECT_X*0.1 + (ASPECT_X*0.275)*(track_nmbr%3))
            y = round(ASPECT_Y*0.555 - (ASPECT_Y*0.257)*(track_nmbr//3))
            self.display_window_frame(x, y)
            self.display_track_window(track_nmbr, x, y)

        pygame.display.flip() #display frame buffer


    def game_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE: #escape key
                    pygame.quit()
                    quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    print(f"Mouse (x,y) = ({pygame.mouse.get_pos()[0]},{pygame.mouse.get_pos()[1]}).... click (x,y) = ({x}, {y})")
                    self.select_track(x,y)
        
        self.display()

    def start_game(self):
        while True:
            self.game_loop()

if __name__ == "__main__":
    track_select = TrackSelection()
    track_select.start_game()