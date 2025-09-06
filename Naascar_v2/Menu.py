import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *
from TrackSelection import TrackSelection
from Pixels import Pixels
from Track import Track
from LaptimeData import LaptimeData

class Menu:
    def __init__(self):
        self.settings = {
            "aspect_x": 1100,
            "aspect_y": 900,
            "viewport": {"x": 0, "y": 0, "width": 2200, "height": 1800},
            "num_of_players": 2,
            "num_of_laps": 5
        }
        pygame.display.init()
        pygame.display.set_mode((self.settings["aspect_x"], self.settings["aspect_y"]), DOUBLEBUF|OPENGL)
        glClearColor(0.0, 0.0, 0.0, 1.0)

        self.text = Pixels() # PIXEL FONT
        self.track = Track()

        #---------------------------- Menu Screens -------------------------------
        self.start = Start()
        self.mainmenu = MainMenu()

        self.address = "start"
        self.back_arrow_image = [[0,20],[20,40],[20,30],[50,30],[50,10],[20,10],[20,0]]

    def run(self):
        self.display({})
        while True:
            self.root_loop()

    def set_menu_buttons(self):
        if self.address == "start":
            return self.start.buttons
        elif self.address == "menu":
            return self.mainmenu.buttons
        elif self.address == "settings":
            return self.settings.buttons
        elif self.address == "laptimes":
            return self.laptimes.buttons

    def root_loop(self):
        buttons = self.set_menu_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    x, y = self.mouse_to_world(x, y)
                    print(f"Mouse clicked at screen coordinates: ({x}, {y})")

                    for button, info in buttons.items():
                        button_x, button_y = info["pos"]
                        bw, bh = info["size"]
                        rx = button_x - info["text_size"] * 5
                        ry = button_y - info["text_size"] * 6
                        if self.point_in_rect(x, y, rx, ry, bw, bh):
                            print(f"Button '{button}' clicked!")
                            self.click_button(info["action"])
                            break

                    if self.address != "start":
                        # Check if back arrow clicked
                        bx, by = self.settings["viewport"]["x"] + self.settings["viewport"]["width"] - 70, self.settings["viewport"]["y"] + self.settings["viewport"]["height"] - 70
                        if self.point_in_rect(x, y, bx - 35, by - 35, 70, 70):
                            print("Back arrow clicked!")
                            self.click_button("Back")
                            break

        self.display(buttons)

    def mouse_to_world(self, sx, sy):
        """Convert screen-space mouse to world-space (OpenGL ortho) coords"""
        sy_flipped = self.settings["aspect_y"] - sy
        wx = sx * (self.settings["viewport"]["width"] / self.settings["aspect_x"])   # 2200/1100 = 2
        wy = sy_flipped * (self.settings["viewport"]["height"] / self.settings["aspect_y"])  # 1800/900 = 2
        return wx, wy
    
    def point_in_rect(self, px, py, rx, ry, rw, rh):
        return (rx <= px <= rx + rw) and (ry <= py <= ry + rh)

    def click_button(self, action):
        if action == "start_menu":
            print("Start button clicked")
            self.address = "menu"
        elif action == "view_laptimes":
            print("Laptimes button clicked")
            #self.address = "laptimes"
        elif action == "open_settings":
            print("Settings button clicked")
            #self.address = "settings"
        elif action == "Back":
            print("Back button clicked")
            self.address = "start"
        elif action == "start_game":
            trackSelection = TrackSelection(self.settings)
            trackSelection.start_game()
        elif action == "quit_game":
            print("Quit button clicked")
            pygame.quit()
            quit()
            

    def display(self, buttons):
        '''Displays the game and all of it's components in the pygame viewport'''
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glViewport(0, 0, self.settings["aspect_x"], self.settings["aspect_y"])
        gluOrtho2D(self.settings["viewport"]["x"], self.settings["viewport"]["width"], self.settings["viewport"]["y"], self.settings["viewport"]["height"])

        #Logo
        self.display_logo()
        self.text.display_text(500, 1200, "NAASCAR", 20)
        #Buttons
        for button, info in buttons.items():
            x, y = info["pos"]
            self.display_button(info["text"], x, y, 700, 140, 6)
        
        if self.address != "start":
            self.display_back_arrow()

        pygame.display.flip() #display frame buffer

    def display_back_arrow(self):
        '''Displays the back arrow in the top left of the screen'''
        ####### Circle #######
        posx, posy = self.settings["viewport"]["x"] + self.settings["viewport"]["width"] - 70, self.settings["viewport"]["y"] + self.settings["viewport"]["height"] - 70
        sides = 32
        radius = 35
        angle = 2*pi/sides
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POLYGON)
        for i in range(sides):
            cosine= radius * cos(i*angle) + posx
            sine  = radius * sin(i*angle) + posy
            glVertex2f(cosine, sine)
        glEnd()
        ######## Arrow #######
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_TRIANGLE_FAN)
        for c in range(len(self.back_arrow_image)):
            glVertex2f(self.back_arrow_image[c][0] + posx - 25, self.back_arrow_image[c][1] + posy - 20)
        glEnd()

    def display_logo(self):
        glBegin(GL_TRIANGLE_FAN)
        logo_points = [
            (1000, 1700), (1200, 1700), (1300, 1600), (1400, 1500),
            (1500, 1400), (1600, 1300), (1700, 1200), (1800, 1100),
            (1900, 1000), (1800, 900), (1700, 800), (1600, 700),
            (1500, 600), (1400, 500), (1300, 400), (1200, 300),
            (1100, 200), (1000, 300), (900, 400), (800, 500),
            (700, 600), (600, 700), (500, 800), (400, 900),
            (300, 1000), (400, 1100), (500, 1200), (600, 1300),
            (700, 1400), (800, 1500), (900, 1600)
        ]
        
        # Use pygame time to create smooth animation
        time = pygame.time.get_ticks() * 0.001  # Convert to seconds
        
        for i, point in enumerate(logo_points):
            hue_offset = (i / len(logo_points)) * 6.28  # Full circle in radians
            time_offset = time * 2.0  # Speed of color change
            hue = (time_offset + hue_offset) % (2 * pi)
            h = (hue / (2 * pi)) % 1.0
        
            # Create smooth transitions through the spectrum
            if h < 1/6:  # Red to Yellow
                r, g, b = 1.0, h * 6, 0.0
            elif h < 2/6:  # Yellow to Green
                r, g, b = 2.0 - h * 6, 1.0, 0.0
            elif h < 3/6:  # Green to Cyan
                r, g, b = 0.0, 1.0, (h - 2/6) * 6
            elif h < 4/6:  # Cyan to Blue
                r, g, b = 0.0, (4/6 - h) * 6, 1.0
            elif h < 5/6:  # Blue to Magenta
                r, g, b = (h - 4/6) * 6, 0.0, 1.0
            else:  # Magenta to Red
                r, g, b = 1.0, 0.0, (1.0 - h) * 6
            
            glColor3f(r, g, b)
            glVertex2f(point[0], point[1])
        
        glEnd()

    
    def display_button(self, button, x, y, width, height, text_size, corner_radius=25):
        glColor3f(0.0, 0.0, 1.0)
        
        # Draw rounded rectangle using triangle fan for each corner and rectangles for sides
        self.draw_rounded_rectangle(x - text_size*5, y - text_size*6, width, height, corner_radius)
        
        glColor3f(1.0, 1.0, 1.0)
        self.text.display_text(x, y, button, text_size)

    def draw_rounded_rectangle(self, x, y, width, height, radius):
        """Draw a rounded rectangle using OpenGL primitives"""
        
        # Middle rectangle
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x + radius, y)
        glVertex2f(x + width - radius, y)
        glVertex2f(x + width - radius, y + height)
        glVertex2f(x + radius, y + height)
        glEnd()
        
        # Top rectangle
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x + radius, y)
        glVertex2f(x + width - radius, y)
        glVertex2f(x + width - radius, y + radius)
        glVertex2f(x + radius, y + radius)
        glEnd()
        
        # Bottom rectangle
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x + radius, y + height - radius)
        glVertex2f(x + width - radius, y + height - radius)
        glVertex2f(x + width - radius, y + height)
        glVertex2f(x + radius, y + height)
        glEnd()
        

        # Left rectangle
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y + radius)
        glVertex2f(x + radius, y + radius)
        glVertex2f(x + radius, y + height - radius)
        glVertex2f(x, y + height - radius)
        glEnd()
        
        # Right rectangle
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x + width - radius, y + radius)
        glVertex2f(x + width, y + radius)
        glVertex2f(x + width, y + height - radius)
        glVertex2f(x + width - radius, y + height - radius)
        glEnd()
        
        # Draw the four rounded corners
        segments = 16  # Number of segments for smooth corners
        
        # Top-left corner
        self.draw_corner(x + radius, y + height - radius, radius, pi/2, pi, segments)
        
        # Top-right corner
        self.draw_corner(x + width - radius, y + height - radius, radius, 0, pi/2, segments)
        
        # Bottom-right corner
        self.draw_corner(x + width - radius, y + radius, radius, 3*pi/2, 2*pi, segments)
        
        # Bottom-left corner
        self.draw_corner(x + radius, y + radius, radius, pi, 3*pi/2, segments)


        
    def draw_corner(self, center_x, center_y, radius, start_angle, end_angle, segments):
        """Draw a quarter circle for rounded corners"""
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(center_x, center_y)  # Center point
        
        for i in range(segments + 1):
            angle = start_angle + (end_angle - start_angle) * i / segments
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            glVertex2f(x, y)
        
        glEnd()

    def aspect_ratio(self):
        return self.settings["aspect_x"] / self.settings["aspect_y"]

    def viewport_to_aspect(self, x, y):
        aspect_x = (x - self.settings["viewport"]["x"]) * (self.settings["aspect_x"] / self.settings["viewport"]["width"])
        aspect_y = (y - self.settings["viewport"]["y"]) * (self.settings["aspect_y"] / self.settings["viewport"]["height"])
        return aspect_x, aspect_y

class Start:
    def __init__(self):
        self.buttons = {
            "Start" : {
                "pos" : [800, 1000], 
                "text": "START GAME",
                "action": "start_menu",
                "size": [700, 140],
                "text_size": 6
            },
            "Quit" : {
                "pos" : [800, 800], 
                "text": "QUIT",
                "action": "quit_game",
                "size": [400, 100],
                "text_size": 2
            }
        }

class MainMenu:
    def __init__(self):
        self.buttons = {
            "Play": {
                "pos" : [800, 1000], 
                "action": "start_game",
                "text": "PLAY",
                "size": [700, 140],
                "text_size": 6
            },
            "Laptimes": {
                "pos" : [800, 800], 
                "action": "view_laptimes",
                "text": "LAPTIMES",
                "size": [700, 140],
                "text_size": 6
            },
            "Settings": {
                "pos" : [800, 600], 
                "action": "open_settings",
                "text": "SETTINGS",
                "size": [700, 140],
                "text_size": 6
            }
        }

if __name__ == "__main__":
    menu = Menu()
    menu.run()