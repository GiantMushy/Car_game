# Naascar (Car Game)

A lightweight 2D top-down racing game built with Pygame and PyOpenGL. Race solo or with a friend, pick from multiple handcrafted tracks, and aim for your best lap times.

- Single or two-player split-screen
- Multiple tracks with corners, straights, and lane switches
- Simple physics with collisions and bounce
- Lap timer with CSV persistence
- Pixel-font UI

## Requirements

- Python 3.11 (recommended)
- pip packages:
  - pygame
  - PyOpenGL

Install dependencies:
```sh
pip install pygame PyOpenGL
```

## Run

From the repository root:
```sh
python Naascar_v2/main.py
```
Entry point: [Naascar_v2/main.py](Naascar_v2/main.py) launches the menu ([`Menu.Menu`](Naascar_v2/Menu.py)) -> track selection ([`TrackSelection.TrackSelection`](Naascar_v2/TrackSelection.py)) -> game ([`Game.Naascar`](Naascar_v2/Game.py)).

## Controls

- Player 1: Arrow keys (Left/Right steer, Up accelerate, Down brake)
- Player 2: WASD (A/D steer, W accelerate, S brake) — used when two players are selected
- Menus: Mouse to click buttons
- In-game: ESC to quit; Back arrow to return to previous screen

## Gameplay

- Choose a track in Track Selection
- Default laps: 5 (configurable)
- Cross the finish line in the correct direction to count a lap
- Winner is announced when required laps are completed
- Lap times persist in [Naascar_v2/Laptimes.csv](Naascar_v2/Laptimes.csv) via [`LaptimeData.LaptimeData`](Naascar_v2/LaptimeData.py)

CSV format: `track_id,time` (e.g., `5,00:22:64`)

## Configuration

Default settings are defined in [`Menu.Menu`](Naascar_v2/Menu.py) and passed through Track Selection into the game:
- aspect_x, aspect_y: window size (pixels)
- viewport: orthographic world size
- num_of_players: 1 or 2
- num_of_laps: lap target

These are bundled as a dictionary and consumed by [`Game.Naascar`](Naascar_v2/Game.py).

## Project Structure (key files)

- Core game:
  - [`Game.Naascar`](Naascar_v2/Game.py): main game loop, rendering, input, laps, and win logic
  - [`Car.Car`](Naascar_v2/Car.py): car state, motion, rotation, rendering
  - [`Physics.Physics`](Naascar_v2/Physics.py): tile-aware collision and bounce handling
  - [`Track.Track`](Naascar_v2/Track.py): track tiles, drawing, finish line and decorations
  - [`Pixels.Pixels`](Naascar_v2/Pixels.py): pixel font rendering (UI text)

- UI / Flow:
  - [`Menu.Menu`](Naascar_v2/Menu.py): start + main menu
  - [`TrackSelection.TrackSelection`](Naascar_v2/TrackSelection.py): select and preview tracks

- Timing / Data:
  - [`LaptimeData.LaptimeData`](Naascar_v2/LaptimeData.py): CSV persistence
  - [`Laptime.Laptime`](Naascar_v2/Laptime.py): data model

- Data:
  - [Naascar_v2/Laptimes.csv](Naascar_v2/Laptimes.csv): saved lap times

## Development Notes

- The physics and rendering are tuned for a fixed-timestep-ish loop using `pygame.time.Clock()`.
- Known areas to refine:
  - Bounce/impact tuning in [`Physics.Physics.collide`](Naascar_v2/Physics.py)
  - Menu extensions (settings, laptime viewer)
  - Camera/viewport follow for single player
- This was a largely personal project that started from a smaller school project in Computer Graphics course (Tölvugraffík). The code is messy and dissorganized, as this was done very early on in my programming career. 

### Learned lessons
- I learned a lot about the importance of code efficiency during this project, as I had to calculate and render the new screen hundreds of times per second, while keeping input responces fast and reliable.
- Files/classes and their relations were not well managed during this project. This caused big headaches when attempting to scale up the game. This was a valuable lesson for me, something I now always keep in mind when starting new projects.
- I didnt bother to keep an updated decision protocal, or any sort of documentation as this was a solo project. However, re-visting this only a year later, and I see its just a mess and I dont even know half of what I did. Another big lesson learned there, and something I have very much improved uppon in later projects.

## License

No license specified. Please add one if you intend to distribute.

