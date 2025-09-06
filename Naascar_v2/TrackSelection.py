import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Game import Naascar
from Track import Track
from Pixels import Pixels
from LaptimeData import LaptimeData
from math import *

class TrackSelection:
    def __init__(self, settings):
        self.settings = settings
        self.aspect_x = settings["aspect_x"]
        self.aspect_y = settings["aspect_y"]
        self.world_w = settings["viewport"]["width"]
        self.world_h = settings["viewport"]["height"]
        self.ass_x = round(settings["aspect_x"] * 0.25)
        self.ass_y = round(settings["aspect_y"] * 0.25)
        self.number_of_players = 2
        self.text = Pixels()
        self.track = Track()
        self.tracks_list = []
        for n in range(len(self.track.cells_list)):
            self.tracks_list.append(Track(n))
        pygame.display.init()
        pygame.display.set_mode((settings["aspect_x"], settings["aspect_y"]), DOUBLEBUF|OPENGL)
        glClearColor(0.0, 0.0, 0.0, 1.0)

        #--------------------------------- IMAGE COORDINATES ----------------------------------
        self.window_frame_1 = [[50,10],[10,50],[10,400],[50,440],[500,440],[540,400],[540,50],[500,10]]
        self.window_frame_2 = [[45,5],[5,45],[5,405],[45,445],[505,445],[545,405],[545,45],[505,5]]
        self.window_frame_3 = [[40,0],[0,40],[0,410],[40,450],[510,450],[550,410],[550,40],[510,0]]

        self.back_arrow_image = [[0,20],[20,40],[20,30],[50,30],[50,10],[20,10],[20,0]]
        #---------------------------- Window Hitbox Coordinates -------------------------------
        self.track_selection_grid = []
        for y in range(3):
            for x in range(3):
                # Calculate actual screen positions for track windows
                screen_x = round(settings["aspect_x"] * 0.1 + (settings["aspect_x"] * 0.275) * x)
                screen_y = round(settings["aspect_y"] * 0.555 - (settings["aspect_y"] * 0.257) * y)
                self.track_selection_grid.append([screen_x, screen_y])
        
        self.running = False


    def select_track(self, x, y):
        opengl_y = self.aspect_y - y
    
        cell_count = 0
        for cell in self.track_selection_grid:
            # Calculate the actual screen position of each track window
            track_x = cell[0]
            track_y = cell[1]
            track_width = self.ass_x  # Width of each track window
            track_height = self.ass_y  # Height of each track window
            
            # Check if click is within this track window
            if track_x <= x <= track_x + track_width and track_y <= opengl_y <= track_y + track_height:
                print(f"Selected track {cell_count}")
                self.start_track(cell_count)
                return 
            cell_count += 1

    def start_track(self, track):
        game_naascar = Naascar(track, self.settings)
        game_naascar.start_game()


    def display_track_window(self, track_nmbr, x , y):
        '''Displays the track in a small selectable window'''
        glViewport(x, y, self.ass_x, self.ass_y)
        self.tracks_list[track_nmbr].display()


    def display_window_frame(self, x, y):
        glViewport(x, y, self.aspect_x, self.aspect_y)
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


    def display_back_arrow(self):
        '''Displays the back arrow in the top-right of the screen (world-space)'''
        glViewport(0, 0, self.aspect_x, self.aspect_y)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.world_w, 0, self.world_h)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        posx, posy = self.world_w - 70, self.world_h - 70
        sides = 32
        radius = 35
        angle = 2*pi/sides

        # Circle
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POLYGON)
        for i in range(sides):
            cosine= radius * cos(i*angle) + posx
            sine  = radius * sin(i*angle) + posy
            glVertex2f(cosine, sine)
        glEnd()
        # Arrow
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_TRIANGLE_FAN)
        for c in range(len(self.back_arrow_image)):
            glVertex2f(self.back_arrow_image[c][0] + posx - 25, self.back_arrow_image[c][1] + posy - 20)
        glEnd()
        

    def display(self):
        '''Displays the game and all of it's components in the pygame viewport'''
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glViewport(0, 0, self.aspect_x, self.aspect_y)
        gluOrtho2D(0, self.world_w, 0, self.world_h)
        self.text.display_text(200, 1600, "SELECT A TRACK TO PLAY", 6) #display_text(xpos, ypos, "text", pixel_size)
        self.text.display_text(200, 1500, "23:45", 4)

        for track_nmbr in range(len(self.track.cells_list)):
            x = round(self.aspect_x*0.1 + (self.aspect_x*0.275)*(track_nmbr%3))
            y = round(self.aspect_y*0.555 - (self.aspect_y*0.257)*(track_nmbr//3))
            self.display_window_frame(x, y)
            self.display_track_window(track_nmbr, x, y)

        self.display_back_arrow()

        pygame.display.flip() #display frame buffer


    def mouse_to_world(self, sx, sy):
        """Convert screen-space mouse to world-space (OpenGL ortho) coords"""
        sy_flipped = self.aspect_y - sy
        wx = sx * (self.world_w / self.aspect_x)   # 2200/1100 = 2
        wy = sy_flipped * (self.world_h / self.aspect_y)  # 1800/900 = 2
        return wx, wy


    def point_in_rect(self, px, py, rx, ry, rw, rh):
        return (rx <= px <= rx + rw) and (ry <= py <= ry + rh)


    def game_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    print(f"Mouse clicked at screen coordinates: ({x}, {y})")
                    self.select_track(x, y)

                    wx, wy = self.mouse_to_world(x, y)
                    posx, posy = self.world_w - 70, self.world_h - 70
                    radius = 35
                    if (wx - posx)*(wx - posx) + (wy - posy)*(wy - posy) <= radius*radius:
                        print("Back arrow clicked - exiting track selection")
                        self.running = False
                        return
        
        self.display()

    def start_game(self):
        self.running = True
        while self.running:
            self.game_loop()

if __name__ == "__main__":
    track_select = TrackSelection()
    track_select.start_game()