
# filepath: /Users/totomcfrodo/Documents/Skoli/Haust2025/TGRA/Assignments/Car_game-main/Naascar_v2/Physics.py
from Track import *
from Car import *
import math

class Physics:
    TILE = 400
    MARGIN = 15
    LANE_INNER_A = 185
    LANE_INNER_B = 215

    # Global render offset used by Track.draw_cell (shift_x = x*400 + 100)
    OFFSET_X = 100
    OFFSET_Y = 100

    def __init__(self, track):
        self.track = track
        self.debug = False  # flip to True to draw debug boxes if you add a draw routine

    @staticmethod
    def _normalize(nx, ny):
        l = math.sqrt(nx*nx + ny*ny)
        if l == 0:
            return 0.0, 0.0
        return nx / l, ny / l

    def collide(self, car, nx, ny):
        nx, ny = Physics._normalize(nx, ny)
        v = car.direction
        dot = v[0]*nx + v[1]*ny

        impact = abs(dot)
        if car.speed > 0.6 * car.MAX_SPEED and impact > 0.15:
            # Base loss 12%, plus up to +18% depending on how head-on
            loss_fraction = 0.12 + 0.18 * impact          # range ≈ 0.12 .. 0.30
            car.speed = max(car.MIN_SPEED, car.speed * (1.0 - loss_fraction))

        v[0] = v[0] - 2*dot*nx
        v[1] = v[1] - 2*dot*ny

        # Re-normalize direction to preserve unit length
        mag = math.hypot(v[0], v[1])
        if mag:
            v[0] /= mag
            v[1] /= mag
        
        car.coordinates[0] += nx * 2
        car.coordinates[1] += ny * 2
        car.update_image_coordinates()

    def wall_boundries(self, car):
        TILE = self.TILE
        OX = self.OFFSET_X
        OY = self.OFFSET_Y

        # Convert world -> tile index using the same +100 offset Track uses when drawing
        # (car outside track safe-guard)
        gx = car.coordinates[0] - OX
        gy = car.coordinates[1] - OY
        if gx < 0 or gy < 0:
            return
        cx_index = int(gx // TILE)
        cy_index = int(gy // TILE)

        try:
            cell_data = self.track.get_cell_data(cx_index, cy_index)
        except KeyError:
            return
        if cell_data is None:
            return

        origin_x = cx_index * TILE + OX
        origin_y = cy_index * TILE + OY

        lx = car.coordinates[0] - origin_x
        ly = car.coordinates[1] - origin_y

        def top_hit():    return ly >= TILE - self.MARGIN
        def bot_hit():    return ly <= self.MARGIN
        def left_hit():   return lx <= self.MARGIN
        def right_hit():  return lx >= TILE - self.MARGIN

        def bounce(nx, ny):
            self.collide(car, nx, ny)
            raise StopIteration

        try:
            if cell_data == self.track.up_right_image:
                if ly >= lx + 85:      bounce(0.707, -0.707)
                if ly <= lx - 185:     bounce(-0.707, 0.707)
                if top_hit():          bounce(0, -1)
                if left_hit():         bounce(1, 0)

            elif cell_data == self.track.up_left_image:
                s = lx + ly
                if s >= 485:           bounce(-0.707, -0.707)
                if s <= 215:           bounce(0.707, 0.707)
                if top_hit():          bounce(0, -1)
                if right_hit():        bounce(-1, 0)

            elif cell_data == self.track.down_right_image:
                s = lx + ly
                if s >= 585:           bounce(-0.707, -0.707)
                if s <= 315:           bounce(0.707, 0.707)
                if bot_hit():          bounce(0, 1)
                if left_hit():         bounce(1, 0)

            elif cell_data == self.track.down_left_image:
                d = ly - lx
                if d >= 185:           bounce(0.707, -0.707)
                if d <= -85:           bounce(-0.707, 0.707)
                if bot_hit():          bounce(0, 1)
                if right_hit():        bounce(-1, 0)

            elif cell_data == self.track.vert_left_image:
                if lx >= 185:          bounce(-1, 0)
                if left_hit():         bounce(1, 0)

            elif cell_data == self.track.vert_right_image:
                if right_hit():        bounce(-1, 0)
                if lx <= 215:          bounce(1, 0)

            elif cell_data == self.track.horiz_top_image:
                if top_hit():          bounce(0, -1)
                if ly <= 215:          bounce(0, 1)

            elif cell_data == self.track.horiz_bot_image:
                if ly >= 185:          bounce(0, -1)
                if bot_hit():          bounce(0, 1)

            elif cell_data == self.track.right_up_60_image:
                if top_hit():          bounce(0, -1)
                if bot_hit():          bounce(0, 1)
                v = lx * 0.666667 - ly
                if v <= -185:          bounce(-0.55, 0.83)
                if v >= 51.4:          bounce(0.55, -0.83)

            elif cell_data == self.track.right_down_60_image:
                if top_hit():          bounce(0, -1)
                if bot_hit():          bounce(0, 1)
                v = lx * 0.666667 + ly
                if v >= 451.68:        bounce(-0.55, -0.83)
                if v <= 215:           bounce(0.55, 0.83)

            elif cell_data == self.track.up_right_60_image:
                if right_hit():        bounce(-1, 0)
                if left_hit():         bounce(1, 0)
                v = lx * 1.5 - ly
                if v <= -77.5:         bounce(-0.83, 0.55)
                if v >= 277.5:         bounce(0.83, -0.55)

            elif cell_data == self.track.up_left_60_image:
                if right_hit():        bounce(-1, 0)
                if left_hit():         bounce(1, 0)
                v = lx * 1.5 + ly
                if v >= 677.5:         bounce(-0.83, -0.55)
                if v <= 322.5:         bounce(0.83, 0.55)

            elif cell_data == self.track.top_right_corner_image:
                if lx + ly <= 615:     bounce(0.707, 0.707)

            elif cell_data == self.track.bot_right_corner_image:
                if (ly + 215) >= lx:   bounce(0.707, -0.707)

            elif cell_data == self.track.top_left_corner_image:
                if (ly - 215) <= lx:   bounce(-0.707, 0.707)

            elif cell_data == self.track.bot_left_corner_image:
                if lx + ly >= 185:     bounce(-0.707, -0.707)

        except StopIteration:
            return