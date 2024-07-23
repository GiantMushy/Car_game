import OpenGL.GL


class Track:
    def __init__(self, track = 0):
        #------------------------------ Basic Grey-Track Image Coardinates ------------------------------------
        self.up_right_image =    [[0,0],[0,100],[300,400],[400,400],[400,200],[200,0]]
        self.up_left_image =     [[400,0],[200,0],[0,200],[0,400],[100,400],[400,100]]
        self.down_right_image =  [[400,0],[300,0],[0,300],[0,400],[200,400],[400,200]]
        self.down_left_image =   [[0,0],[0,200],[200,400],[400,400],[400,300],[100,0]]

        self.vert_left_image =   [[0,0],[0,400],[200,400],[200,0]]
        self.vert_right_image =  [[200,0],[200,400],[400,400],[400,0]]
        self.horiz_top_image =   [[0,200],[0,400],[400,400],[400,200]]
        self.horiz_bot_image =   [[0,0],[0,200],[400,200],[400,0]]

        self.right_up_60_image =       [[0,0],[0,200],[300,400],[400,400],[400,200],[100,0]]
        self.right_down_60_image =     [[400,0],[300,0],[0,200],[0,400],[100,400],[400,200]]
        self.up_right_60_image =       [[0,0],[0,100],[200,400],[400,400],[400,300],[200,0]]
        self.up_left_60_image =        [[400,0],[200,0],[0,300],[0,400],[200,400],[400,100]]

        self.top_right_corner_image =  [[400,200],[200,400],[400,400]]
        self.bot_right_corner_image =  [[400,0],[200,0],[400,200]]
        self.top_left_corner_image =   [[0,400],[200,400],[0,200]]
        self.bot_left_corner_image =   [[0,0],[0,200],[200,0]]

        self.empty =             [[0,0]]

        #------------------------------ Track Image Coardinates set into Cells ---------------------
        self.cells_list =[
        {(0,0) : self.down_right_image,       (0,1) : self.vert_left_image,        (0,2) : self.vert_left_image,        (0,3) : self.up_right_image,
         (1,0) : self.horiz_bot_image,        (1,1) : self.empty,                  (1,2) : self.empty,                  (1,3) : self.horiz_top_image,
         (2,0) : self.horiz_bot_image,        (2,1) : self.empty,                  (2,2) : self.empty,                  (2,3) : self.horiz_top_image,
         (3,0) : self.horiz_bot_image,        (3,1) : self.empty,                  (3,2) : self.empty,                  (3,3) : self.horiz_top_image,
         (4,0) : self.down_left_image,        (4,1) : self.vert_right_image,       (4,2) : self.vert_right_image,       (4,3) : self.up_left_image},          # Track 0 --> Big Loop & finishline test

        {(0,0) : self.down_right_image,       (0,1) : self.vert_left_image,        (0,2) : self.vert_left_image,        (0,3) : self.up_right_image,
         (1,0) : self.down_left_image,        (1,1) : self.vert_right_image,       (1,2) : self.bot_right_corner_image, (1,3) : self.right_down_60_image,
         (2,0) : self.top_right_corner_image, (2,1) : self.up_left_60_image,       (2,2) : self.bot_left_corner_image,  (2,3) : self.right_up_60_image,
         (3,0) : self.horiz_top_image,        (3,1) : self.empty,                  (3,2) : self.empty,                  (3,3) : self.horiz_top_image,
         (4,0) : self.top_left_corner_image,  (4,1) : self.vert_left_image,        (4,2) : self.up_right_60_image,      (4,3) : self.up_left_image},          # Track 1 --> corner/lane switch test

        {(0,0) : self.down_right_image,       (0,1) : self.vert_left_image,        (0,2) : self.vert_left_image,        (0,3) : self.up_right_image,
         (1,0) : self.horiz_bot_image,        (1,1) : self.down_right_image,       (1,2) : self.up_right_image,         (1,3) : self.horiz_top_image,
         (2,0) : self.horiz_bot_image,        (2,1) : self.horiz_bot_image,        (2,2) : self.horiz_top_image,        (2,3) : self.horiz_top_image,
         (3,0) : self.horiz_bot_image,        (3,1) : self.right_up_60_image,      (3,2) : self.right_down_60_image,    (3,3) : self.horiz_top_image,
         (4,0) : self.down_left_image,        (4,1) : self.up_left_image,          (4,2) : self.down_left_image,        (4,3) : self.up_left_image},          # Track 2

        {(0,0) : self.down_right_image,       (0,1) : self.vert_left_image,        (0,2) : self.vert_left_image,        (0,3) : self.up_right_image,
         (1,0) : self.down_left_image,        (1,1) : self.up_left_60_image,       (1,2) : self.up_right_image,         (1,3) : self.horiz_top_image,
         (2,0) : self.empty,                  (2,1) : self.empty,                  (2,2) : self.horiz_top_image,        (2,3) : self.horiz_top_image,
         (3,0) : self.empty,                  (3,1) : self.empty,                  (3,2) : self.right_down_60_image,    (3,3) : self.horiz_top_image,
         (4,0) : self.empty,                  (4,1) : self.empty,                  (4,2) : self.down_left_image,        (4,3) : self.up_left_image},          # Track 3

        {(0,0) : self.down_right_image,       (0,1) : self.vert_left_image,        (0,2) : self.vert_left_image,        (0,3) : self.up_right_image,
         (1,0) : self.down_left_image,        (1,1) : self.up_left_60_image,       (1,2) : self.up_right_image,         (1,3) : self.right_down_60_image,
         (2,0) : self.top_right_corner_image, (2,1) : self.bot_right_corner_image, (2,2) : self.horiz_top_image,        (2,3) : self.right_up_60_image,
         (3,0) : self.right_down_60_image,    (3,1) : self.down_left_image,        (3,2) : self.up_left_image,          (3,3) : self.right_down_60_image,
         (4,0) : self.down_left_image,        (4,1) : self.up_left_60_image,       (4,2) : self.vert_left_image,        (4,3) : self.bot_left_corner_image},  # Track 4

        {(0,0) : self.top_right_corner_image, (0,1) : self.vert_right_image,        (0,2) : self.bot_right_corner_image, (0,3) : self.empty,
         (1,0) : self.top_left_corner_image,  (1,1) : self.vert_left_image,       (1,2) : self.bot_left_corner_image,  (1,3) : self.empty,
         (2,0) : self.empty,                  (2,1) : self.empty,                  (2,2) : self.empty,                  (2,3) : self.empty,
         (3,0) : self.empty,                  (3,1) : self.empty,                  (3,2) : self.empty,                  (3,3) : self.empty,
         (4,0) : self.empty,                  (4,1) : self.empty,                  (4,2) : self.empty,                  (4,3) : self.empty},                  # Track 5 --> Small Loop

        {(0,0) : self.top_right_corner_image, (0,1) : self.vert_right_image,       (0,2) : self.vert_right_image,        (0,3) : self.bot_right_corner_image,
         (1,0) : self.top_left_corner_image,  (1,1) : self.up_right_image,         (1,2) : self.down_right_image,        (1,3) : self.bot_left_corner_image,
         (2,0) : self.top_right_corner_image, (2,1) : self.up_left_image,          (2,2) : self.down_left_image,         (2,3) : self.bot_right_corner_image,
         (3,0) : self.top_left_corner_image,  (3,1) : self.up_right_image,        (3,2) : self.down_right_image,         (3,3) : self.bot_left_corner_image,
         (4,0) : self.empty,                  (4,1) : self.top_left_corner_image,  (4,2) : self.bot_left_corner_image,   (4,3) : self.empty},                 # Track 6

        {(0,0) : self.down_right_image,       (0,1) : self.vert_left_image,        (0,2) : self.up_right_image,         (0,3) : self.empty,
         (1,0) : self.right_up_60_image,      (1,1) : self.top_right_corner_image, (1,2) : self.up_left_image,          (1,3) : self.empty,
         (2,0) : self.horiz_top_image,        (2,1) : self.top_left_corner_image,  (2,2) : self.vert_left_image,        (2,3) : self.up_right_image,
         (3,0) : self.right_down_60_image,    (3,1) : self.top_right_corner_image, (3,2) : self.vert_right_image,       (3,3) : self.up_left_image,
         (4,0) : self.down_left_image,        (4,1) : self.up_left_image,          (4,2) : self.empty,                  (4,3) : self.empty},                  # Track 7

        {(0,0) : self.top_right_corner_image, (0,1) : self.vert_right_image,       (0,2) : self.vert_right_image,        (0,3) : self.bot_right_corner_image,
         (1,0) : self.top_left_corner_image,  (1,1) : self.up_right_image,         (1,2) : self.down_right_image,        (1,3) : self.bot_left_corner_image,
         (2,0) : self.empty,                  (2,1) : self.horiz_top_image,        (2,2) : self.horiz_bot_image,         (2,3) : self.empty,
         (3,0) : self.empty,                  (3,1) : self.horiz_top_image,        (3,2) : self.horiz_bot_image,         (3,3) : self.empty,
         (4,0) : self.empty,                  (4,1) : self.top_left_corner_image,  (4,2) : self.bot_left_corner_image,   (4,3) : self.empty}]                 # Track 8

        self.cells = self.cells_list[track]  # Choosing which track to play
        #self.finish_line_cell = (0,1)
        self.finish_line_cell = (0,1)

        self.finish_line_box =    [[0,0],[20,0],[20,10],[0,10]]
        self.finish_line_box_90 = [[0,0],[0,20],[10,20],[10,0]]
        self.lane_marker_00 =     [[-10,-2.5],[-10,2.5],[10,2.5],[10,-2.5]]
        self.lane_marker_90 =     [[-2.5,-10],[2.5,-10],[2.5,10],[-2.5,10]]
        self.lane_marker_45 =     [[-5.30,-8.84],[-8.84,-5.30],[5.30,8.84],[8.84,5.30]]
        self.lane_marker_135 =    [[-8.84,5.30],[-5.30,8.84],[8.84,-5.30],[5.30,-8.84]]
        self.lane_marker_30 =     [[-7.411, -7.1643],[-9.9105, -2.834],[7.411, 7.1643],[9.9105, 2.834]]
        self.lane_marker_150 =    [[9.9103, -2.8349],[7.4103, -7.165],[-9.9103, 2.8349],[-7.4103, 7.165]]
        self.lane_marker_60 =     [[-2.8349, -9.9103],[-7.1651, -7.4103],[2.8349, 9.9103],[7.1651, 7.4103]] ##### Testing
        self.lane_marker_120 =    [[7.1651, -7.4103],[2.8349, -9.9103],[-7.1651, 7.4103],[-2.8349, 9.9103]] ##### Testing

        self.border_left = [[0,0], [0,400], [2, 400], [2,0]]
        self.border_right = [[400,0], [400, 400], [398,400], [398,0]]
        self.border_top = [[0,400], [400,400], [400,398], [0, 398]]
        self.border_bot = [[0,0], [400,0], [400,2], [0,2]]


    def display(self):
        for x in range(5):
            for y in range(4):
                self.draw_cell(x,y)
        self.draw_finishline()


    def get_cell_data(self, x, y):
        return self.cells[(x, y)]


    def draw_cell(self, x, y):
        shift_x = x * 400 + 100
        shift_y = y * 400 + 100
        if self.cells[(x,y)] != "":
            self.draw_road(self.cells[(x,y)], shift_x, shift_y)
            self.draw_decoration(self.cells[(x,y)], shift_x, shift_y)


    def draw_road(self, image_coards, shift_x, shift_y):
        OpenGL.GL.glColor3f(0.4, 0.4, 0.4)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for n in range(len(image_coards)):
            OpenGL.GL.glVertex2f(image_coards[n][0] + shift_x, image_coards[n][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()


    def draw_finishline(self):
        x, y = self.finish_line_cell
        shift_x = x * 400 + 100
        shift_y = y * 400 + 100
        if self.cells[(x, y)] == self.vert_left_image:
            OpenGL.GL.glColor3f(1.0, 1.0, 1.0)
            for n in range(10):
                for m in range(2):
                    OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
                    for t in range(4):
                        OpenGL.GL.glVertex2f(self.finish_line_box[t][0] + shift_x + 180 - n * 20, self.finish_line_box[t][1] + shift_y + 380 + m * 10)
                    OpenGL.GL.glColor3f(1.0 * (n % 2), 1.0 * (n % 2), 1.0 * (n % 2))
                    OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

        elif self.cells[(x, y)] == self.horiz_top_image:
            OpenGL.GL.glColor3f(1.0, 1.0, 1.0)
            for n in range(10):
                for m in range(2):
                    OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
                    for t in range(4):
                        OpenGL.GL.glVertex2f(self.finish_line_box_90[t][0] + shift_x + 380 + m * 10, self.finish_line_box_90[t][1] + shift_y + 380 - n * 20)
                    OpenGL.GL.glColor3f(1.0 * (n % 2), 1.0 * (n % 2), 1.0 * (n % 2))
                    OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

        elif self.cells[(x, y)] == self.vert_right_image:
            OpenGL.GL.glColor3f(1.0, 1.0, 1.0)
            for n in range(10):
                for m in range(2):
                    OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
                    for t in range(4):
                        OpenGL.GL.glVertex2f(self.finish_line_box[t][0] + shift_x + 380 - n * 20, self.finish_line_box[t][1] + shift_y + 380 + m * 10)
                    OpenGL.GL.glColor3f(1.0 * (n % 2), 1.0 * (n % 2), 1.0 * (n % 2))
                    OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

        elif self.cells[(x, y)] == self.horiz_bot_image:
            OpenGL.GL.glColor3f(1.0, 1.0, 1.0)
            for n in range(10):
                for m in range(2):
                    OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
                    for t in range(4):
                        OpenGL.GL.glVertex2f(self.finish_line_box_90[t][0] + shift_x + 380 + m * 10, self.finish_line_box_90[t][1] + shift_y + 180 - n * 20)
                    OpenGL.GL.glColor3f(1.0 * (n % 2), 1.0 * (n % 2), 1.0 * (n % 2))
                    OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        else:
            print("Error: printing finish line")


    def draw_decoration(self, cell, shift_x, shift_y):
        #################  Straightaways ###############
        if cell == self.horiz_bot_image:
            self.horiz_bot(shift_x, shift_y)

        elif cell == self.horiz_top_image:
            self.horiz_top(shift_x, shift_y)

        elif cell == self.vert_left_image:
            self.vert_left(shift_x, shift_y)

        elif cell == self.vert_right_image:
            self.vert_right(shift_x, shift_y)

        #################  90° Turns ###################
        elif cell == self.up_left_image:
            self.up_left(shift_x, shift_y)

        elif cell == self.up_right_image:
            self.up_right(shift_x, shift_y)

        elif cell == self.down_left_image:
            self.down_left(shift_x, shift_y)

        elif cell == self.down_right_image:
            self.down_right(shift_x, shift_y)

        #################  Lane Switch #################
        elif cell == self.right_down_60_image:
            self.right_down_60(shift_x, shift_y)

        elif cell == self.right_up_60_image:
            self.right_up_60(shift_x, shift_y)

        elif cell == self.up_left_60_image:
            self.up_left_60(shift_x, shift_y)

        elif cell == self.up_right_60_image:
            self.up_right_60(shift_x, shift_y)

        #################  Corners #####################
        elif cell == self.top_right_corner_image:
            self.top_right_corner(shift_x, shift_y)

        elif cell == self.top_left_corner_image:
            self.top_left_corner(shift_x, shift_y)

        elif cell == self.bot_right_corner_image:
            self.bot_right_corner(shift_x, shift_y)

        elif cell == self.bot_left_corner_image:
            self.bot_left_corner(shift_x, shift_y)

        elif cell == self.empty:
            pass

        else:
            print(f"Error: nothing in cell -- {cell}")

        ######################  Straightaways ####################
    def horiz_bot(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        for m in range(9):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_00[c][0] + shift_x + 22 + m * 44, self.lane_marker_00[c][1] + shift_y + 100)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_bot[c][0] + shift_x, self.border_bot[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_top[c][0] + shift_x, self.border_top[c][1] + shift_y - 200)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

    def horiz_top(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        for m in range(9):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_00[c][0] + shift_x + 22 + m * 44, self.lane_marker_00[c][1] + shift_y + 300)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_bot[c][0] + shift_x + 200, self.border_bot[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_top[c][0] + shift_x, self.border_top[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

    def vert_left(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        for m in range(9):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_90[c][0] + shift_x + 100, self.lane_marker_90[c][1] + shift_y + 22 + m * 44)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_left[c][0] + shift_x, self.border_left[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_right[c][0] + shift_x, self.border_right[c][1] + shift_y - 200)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

    def vert_right(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        for m in range(9):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_90[c][0] + shift_x + 300, self.lane_marker_90[c][1] + shift_y + 22 + m * 44)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_left[c][0] + shift_x, self.border_left[c][1] + shift_y + 200)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_right[c][0] + shift_x, self.border_right[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

        ######################  90° Turns ########################
    def up_left(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_00[c][0] + shift_x + 20, self.lane_marker_00[c][1] + shift_y + 300)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_90[c][0] + shift_x + 300, self.lane_marker_90[c][1] + shift_y + 20)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        for m in range(9):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_135[c][0] + shift_x + 290 - 30 * m, self.lane_marker_135[c][1] + shift_y + 50 + 30 * m)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_right[c][0] + shift_x, self.border_right[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_top[c][0] + shift_x, self.border_top[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

    def up_right(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_00[c][0] + shift_x + 360 + 20, self.lane_marker_00[c][1] + shift_y + 300)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_90[c][0] + shift_x + 100, self.lane_marker_90[c][1] + shift_y + 20)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        for m in range(9):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_45[c][0] + shift_x + 110 + 30 * m, self.lane_marker_45[c][1] + shift_y + 50 + 30 * m)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_left[c][0] + shift_x, self.border_left[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_top[c][0] + shift_x, self.border_top[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

    def down_left(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_00[c][0] + shift_x + 16, self.lane_marker_00[c][1] + shift_y + 100)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_90[c][0] + shift_x + 300, self.lane_marker_90[c][1] + shift_y + 380)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        for m in range(9):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_45[c][0] + shift_x + 50 + 30 * m, self.lane_marker_45[c][1] + shift_y + 110 + 30 * m)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_right[c][0] + shift_x, self.border_right[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_bot[c][0] + shift_x, self.border_bot[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

    def down_right(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_00[c][0] + shift_x + 380, self.lane_marker_00[c][1] + shift_y + 100)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_90[c][0] + shift_x + 100, self.lane_marker_90[c][1] + shift_y + 380)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        for m in range(9):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_135[c][0] + shift_x + 350 - 30 * m, self.lane_marker_135[c][1] + shift_y + 110 + 30 * m)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_left[c][0] + shift_x, self.border_left[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_bot[c][0] + shift_x, self.border_bot[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

        ######################  Lane Switch ######################
    def right_down_60(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_00[c][0] + shift_x + 20, self.lane_marker_00[c][1] + shift_y + 300)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_00[c][0] + shift_x + 380, self.lane_marker_00[c][1] + shift_y + 100)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        for m in range(9):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_150[c][0] + shift_x + 345 - 35 * m, self.lane_marker_150[c][1] + shift_y + 110 + 23 * m)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_bot[c][0] + shift_x, self.border_bot[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_top[c][0] + shift_x, self.border_top[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

    def right_up_60(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_00[c][0] + shift_x + 16, self.lane_marker_00[c][1] + shift_y + 100)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_00[c][0] + shift_x + 380, self.lane_marker_00[c][1] + shift_y + 300)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        for m in range(9):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_30[c][0] + shift_x + 65 + 35 * m, self.lane_marker_30[c][1] + shift_y + 110 + 23 * m)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_bot[c][0] + shift_x, self.border_bot[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_top[c][0] + shift_x, self.border_top[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

    def up_left_60(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_90[c][0] + shift_x + 100, self.lane_marker_90[c][1] + shift_y + 380)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_90[c][0] + shift_x + 300, self.lane_marker_90[c][1] + shift_y + 20)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        for m in range(9):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_120[c][0] + shift_x + 290 - 23 * m, self.lane_marker_120[c][1] + shift_y + 60 + 35 * m)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_left[c][0] + shift_x, self.border_left[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_right[c][0] + shift_x, self.border_right[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

    def up_right_60(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_90[c][0] + shift_x + 100, self.lane_marker_90[c][1] + shift_y + 20)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.lane_marker_90[c][0] + shift_x + 300, self.lane_marker_90[c][1] + shift_y + 380)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        for m in range(9):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_60[c][0] + shift_x + 110 + 23 * m, self.lane_marker_60[c][1] + shift_y + 60 + 35 * m)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_left[c][0] + shift_x, self.border_left[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        for c in range(4):
            OpenGL.GL.glVertex2f(self.border_right[c][0] + shift_x, self.border_right[c][1] + shift_y)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

        ######################  Corners ##########################
    def top_right_corner(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        for m in range(3):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_135[c][0] + shift_x + 385 - 30 * m, self.lane_marker_135[c][1] + shift_y + 320 + 30 * m)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        OpenGL.GL.glVertex2f(shift_x + 400, shift_y + 400)
        OpenGL.GL.glVertex2f(shift_x + 398, shift_y + 400)
        OpenGL.GL.glVertex2f(shift_x + 398, shift_y + 398)
        OpenGL.GL.glVertex2f(shift_x + 400, shift_y + 398)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

    def top_left_corner(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        for m in range(3):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_45[c][0] + shift_x + 20 + 30 * m, self.lane_marker_45[c][1] + shift_y + 320 + 30 * m)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        OpenGL.GL.glVertex2f(shift_x + 0, shift_y + 400)
        OpenGL.GL.glVertex2f(shift_x + 2, shift_y + 400)
        OpenGL.GL.glVertex2f(shift_x + 2, shift_y + 398)
        OpenGL.GL.glVertex2f(shift_x + 0, shift_y + 398)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

    def bot_right_corner(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        for m in range(3):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_45[c][0] + shift_x + 315 + 30 * m, self.lane_marker_45[c][1] + shift_y + 15 + 30 * m)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        OpenGL.GL.glVertex2f(shift_x + 400, shift_y + 0)
        OpenGL.GL.glVertex2f(shift_x + 398, shift_y + 0)
        OpenGL.GL.glVertex2f(shift_x + 398, shift_y + 2)
        OpenGL.GL.glVertex2f(shift_x + 400, shift_y + 2)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()

    def bot_left_corner(self, shift_x, shift_y):
        OpenGL.GL.glColor3f(1.0, 1.0, 0.0)
        for m in range(3):
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
            for c in range(4):
                OpenGL.GL.glVertex2f(self.lane_marker_135[c][0] + shift_x + 85 - 30 * m, self.lane_marker_135[c][1] + shift_y + 15 + 30 * m)
            OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()
        OpenGL.GL.glColor3f(0, 0, 0)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLE_FAN)
        OpenGL.GL.glVertex2f(shift_x + 0, shift_y + 0)
        OpenGL.GL.glVertex2f(shift_x + 2, shift_y + 0)
        OpenGL.GL.glVertex2f(shift_x + 2, shift_y + 2)
        OpenGL.GL.glVertex2f(shift_x + 0, shift_y + 2)
        OpenGL.GL.OpenGL.GL.OpenGL.GL.glEnd()