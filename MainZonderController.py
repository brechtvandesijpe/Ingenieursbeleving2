import numpy as np
import sdl2
import sdl2.ext
import winsound

from numba import jit, cuda
import time
import cProfile
import pstats

SCREENWIDTH = 800
SCREENHEIGHT = 600
TEXTURESIZE = 64
STEPSIZE = 0.05
HOEK_STEPSIZE = 0.2
GROOTTE_HITBOX = 0.8
MAXHEALTH = 99
MAXSTAMINA = 10

# SDL LATEN WERKEN
sdl2.ext.init()
window = sdl2.ext.Window("Project Ingenieursbeleving 2", size=(SCREENWIDTH, SCREENHEIGHT))
renderer = sdl2.ext.Renderer(window)
resources = sdl2.ext.Resources(__file__, "res")
factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
key_states = sdl2.SDL_GetKeyboardState(None)

soundWapens = ["resources\punch.wav", "resources\mes.wav", "resources\chainsaw.wav", "resources\kling.wav"]
soundMonsters = ["resources\zombie.wav", "resources\zombie.wav", "resources\zombie.wav"]

texMuren = [factory.from_image(resources.get_path("walls.png")),
            factory.from_image(resources.get_path("wallsdark.png"))]

texSprites = [factory.from_image(resources.get_path("sprites.png")),
              factory.from_image(resources.get_path("movingSprites.png"))]

texBasis = [
    factory.from_image(resources.get_path("lucht.png")),            # 0
    factory.from_image(resources.get_path("vloer.png")),            # 1
    factory.from_image(resources.get_path("overlay1.png")),         # 2
    factory.from_image(resources.get_path("shading.png")),          # 3
    factory.from_image(resources.get_path("pijn.png")),             # 4
    factory.from_image(resources.get_path("bloedspatten.png")),     # 5
    factory.from_image(resources.get_path("healthbar.png")),        # 6
    factory.from_image(resources.get_path("ScoreBar.png")),         # 7
    factory.from_image(resources.get_path("win.png")),              # 8
    factory.from_image(resources.get_path("gameOver.png"))          # 9
]

texInventory = [factory.from_image(resources.get_path("inventory.png")),
                factory.from_image(resources.get_path("inventoryBackground.png"))]

texWapens = [
    [factory.from_image(resources.get_path("fist1.png")),
     factory.from_image(resources.get_path("fist2.png")),
     factory.from_image(resources.get_path("fist3.png"))],
    [factory.from_image(resources.get_path("mes1.png")),
     factory.from_image(resources.get_path("mes2.png"))],
    [factory.from_image(resources.get_path("chainsaw1.png")),
     factory.from_image(resources.get_path("chainsaw2.png"))],
    [factory.from_image(resources.get_path("crowbar1.png")),
     factory.from_image(resources.get_path("crowbar2.png")),
     factory.from_image(resources.get_path("crowbar3.png")),
     factory.from_image(resources.get_path("crowbar4.png"))]]

texStartscherm = [factory.from_image(resources.get_path("leeg.png")),
                        factory.from_image(resources.get_path("startscherm1.png")),
                        factory.from_image(resources.get_path("startscherm2.png")),
                        factory.from_image(resources.get_path("startscherm3.png")),
                        factory.from_image(resources.get_path("startscherm4.png")),
                        factory.from_image(resources.get_path("startscherm5.png")),
                        ]

texScore = factory.from_image(resources.get_path("score.png"))

texPauzescherm = [factory.from_image(resources.get_path("RESUME.png")),
                        factory.from_image(resources.get_path("QUIT.png"))]

texJumpscares = [
    0,
    [factory.from_image(resources.get_path("invlieg1.png")),
     factory.from_image(resources.get_path("invlieg2.png")),
     factory.from_image(resources.get_path("invlieg3.png")),
     factory.from_image(resources.get_path("invlieg4.png")),
     factory.from_image(resources.get_path("invlieg5.png")),
     factory.from_image(resources.get_path("invlieg6.png")),
     factory.from_image(resources.get_path("invlieg7.png")),
     factory.from_image(resources.get_path("invlieg8.png")),
     factory.from_image(resources.get_path("invlieg9.png")),
     factory.from_image(resources.get_path("invlieg10.png")),
     factory.from_image(resources.get_path("invlieg11.png")),
     factory.from_image(resources.get_path("invlieg12.png")),
     factory.from_image(resources.get_path("invlieg13.png")),
     factory.from_image(resources.get_path("invlieg14.png")),
     factory.from_image(resources.get_path("invlieg15.png")),
     factory.from_image(resources.get_path("invlieg16.png"))],
    [factory.from_image(resources.get_path("beest1.png")),
     factory.from_image(resources.get_path("beest2.png")),
     factory.from_image(resources.get_path("beest3.png")),
     factory.from_image(resources.get_path("beest4.png")),
     factory.from_image(resources.get_path("beest5.png")),
     factory.from_image(resources.get_path("beest6.png")),
     factory.from_image(resources.get_path("beest7.png")),
     factory.from_image(resources.get_path("beest8.png")),
     factory.from_image(resources.get_path("beest9.png")),
     factory.from_image(resources.get_path("beest10.png")),
     factory.from_image(resources.get_path("beest11.png")),
     factory.from_image(resources.get_path("beest12.png")),
     factory.from_image(resources.get_path("beest13.png")),
     factory.from_image(resources.get_path("beest14.png")),
     factory.from_image(resources.get_path("beest15.png")),
     factory.from_image(resources.get_path("beest16.png"))],
    [factory.from_image(resources.get_path("freddy1.png")),
     factory.from_image(resources.get_path("freddy2.png")),
     factory.from_image(resources.get_path("freddy3.png")),
     factory.from_image(resources.get_path("freddy4.png")),
     factory.from_image(resources.get_path("freddy5.png")),
     factory.from_image(resources.get_path("freddy6.png")),
     factory.from_image(resources.get_path("freddy7.png")),
     factory.from_image(resources.get_path("freddy8.png")),
     factory.from_image(resources.get_path("freddy9.png")),
     factory.from_image(resources.get_path("freddy10.png")),
     factory.from_image(resources.get_path("freddy11.png")),
     factory.from_image(resources.get_path("freddy12.png")),
     factory.from_image(resources.get_path("freddy13.png")),
     factory.from_image(resources.get_path("freddy14.png")),
     factory.from_image(resources.get_path("freddy15.png")),
     factory.from_image(resources.get_path("freddy16.png")),
     factory.from_image(resources.get_path("freddy17.png")),
     factory.from_image(resources.get_path("freddy18.png")),
     factory.from_image(resources.get_path("freddy19.png")),
     factory.from_image(resources.get_path("freddy20.png")),
     factory.from_image(resources.get_path("freddy21.png")),
     factory.from_image(resources.get_path("freddy22.png")),
     factory.from_image(resources.get_path("freddy23.png")),
     factory.from_image(resources.get_path("freddy24.png")),
     factory.from_image(resources.get_path("freddy25.png")),
     factory.from_image(resources.get_path("freddy26.png")),
     factory.from_image(resources.get_path("freddy27.png")),
     factory.from_image(resources.get_path("freddy28.png")),
     factory.from_image(resources.get_path("freddy29.png")),
     factory.from_image(resources.get_path("freddy30.png")),
     factory.from_image(resources.get_path("freddy31.png")),
     factory.from_image(resources.get_path("freddy32.png")),
     factory.from_image(resources.get_path("freddy33.png")),
     factory.from_image(resources.get_path("freddy34.png")),
     factory.from_image(resources.get_path("freddy35.png")),
     factory.from_image(resources.get_path("freddy36.png")),
     factory.from_image(resources.get_path("freddy37.png")),
     factory.from_image(resources.get_path("freddy38.png")),
     factory.from_image(resources.get_path("freddy39.png")),
     factory.from_image(resources.get_path("freddy40.png")),
     factory.from_image(resources.get_path("freddy41.png"))]
    ]

afsluiten = False
hit = False
actie = False
playerScore = 0
pSpeler = []
rSpeler = []
inventory = []
items = []
selectedItem = 0
health = 0
stamina = 0
wapen = 0
sleutels = 0
framecountWapens = 0
startschermIndex = 1
startscherm = True
gameOver = False
win = False
spelen = False
pauze = False
pauzeNummer = 0
onthoudX = 0
onthoudY = 0
activeerJumpscare = False
framecounter = 0
keuzeJumpscare = 0
toggle = True


def init():
    global pSpeler, rSpeler, playerScore, sleutels, wereld, sprites, items, inventory, health, stamina, MAXHEALTH, MAXSTAMINA

    wereld = np.array([[ 1, 37, 41, 27, 44, 27, 37, 39, 37, 42, 28, 43, 28,  1, 48, 50, 53, 48, 51, 48, 49, 48, 48, 49, 48, 48, 49, 48, 48, 49, 48, 51, 49, 48],  # 1
                       [ 4,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0, 37, 51,  0,  0,  0, -3,  0,  0, 48,  0,  0, 48,  0,  0, 51,  0,  0, 48,  0,  0, 48],   # 3
                       [ 1,  0,  0,  0,  0,  0,  0, 29,  0,  0,  0,  0,  0,  1, 54,  0,  0,  0, 51,  0,  0, 48,  0,  0,  0,  0,  0, 48,  0,  0, 48,  0,  0, 48],   # 4
                       [ 1,  0,  1,  0,  0,  0,  1,  1,  1, 32,  1,  0,  0, 17, 48,  0,  0,  0,  0, 48,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 48],   # 5
                       [ 1, 37,  3,  0,  1,  1,  3, 37,  3, 37,  1,  0,  1, 18,  3, 53, 48, 55, 48, 48, 51, 48, 56, 55, 51, 48, 55, 48, 51, 55, 48,  0,  0, 51],   # 6
                       [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  5,  0, 40,  5, 40,  3,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 48,  0,  0, 54],   # 7
                       [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, 48,  0,  0,  0,  0,  0,  0, 51,  0,  0, 48,  0,  0, 48,  0,  0, 48,  0,  0, 48],   # 2
                       [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  1,  1,  1, 40,  1,  0,  1,  7],   # 8
                       [ 1, 37,  3,  0,  0,  1,  3, 37,  3,  37, 1,  1,  0,  0,  0,  1,  3,  1,  0,  0,  0,  1,  0,  0,  0,  0,  1,  1,  0,  0,  0,  0,  0,  7],   # 9
                       [ 1,  1, 37,  0, 37, 37,  1, 31,  1,  3,  0,  1,  0,  0,  5,  0,  0,  0,  5,  0,  0,  1,  0,  0,  0,  0,  9,  0,  0,  0,  0,  0,  0,  1],   # 10
                       [ 1,  0,  0,  0,  0,  0,  0,  0,  0, 35,  5,  0,  0,  3,  0,  0,  0,  0,  0,  3,  0,  0,  1,  0,  0,  0,  1,  0,  0,  1, 40,  3, 40,  1],   # 11
                       [39,  0,  0,  0,  0,  0,  0,  0,  0, 39,  1,  0,  0,  8,  0,  0,  0,  0,  0,  7,  0,  0,  1,  0,  0,  0,  5,  0,  0,  0,  0,  0,  0, 27],   # 12
                       [ 1,  0,  0,  0,  0,  0,  0,  0,  1,  7,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  1,  0,  0,  1, 40,  1,  0, 17,  0,  0,  5],   # 13
                       [35,  0,  0,  0,  0,  0,  0,  1, 10,  0,  0,  0,  5,  0,  0,  0,  0,  0,  0,  0,  5,  0,  0,  0,  5,  0, 10,  0,  0,  0, 17,  0,  0, 24],   # 14
                       [ 1, 27, 37, 38, 33, 37, 27,  1, 31,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  3,  0,  5,  0,  0,  0, 17,  0,  0, 11],   # 15
                       [ 1, 27,  3,  5, 27,  3,  4,  5,  3,  0,  0,  5,  0,  0,  1,  0,  0,  0,  1,  0,  0, 40,  0,  0,  5,  0,  1,  1, 17, 17, 17, 17,  0, 39],   # 16
                       [16,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  1,  0,  1,  0,  0,  3,  0,  0,  1, 17,  0,  0,  0,  0,  5],   # 17
                       [15,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  1,  0, 12,  0,  0,  5,  0,  0,  1, 33,  0,  0,  0,  0, 27],   # 18
                       [ 1, 27,  3,  5, 27,  3,  0,  5,  3,  0,  0,  5,  0,  0,  1,  0,  0,  0,  1,  0,  0, 40,  0,  0,  3,  0,  0,  1,  1, 18, 17,  0,  0, 11],   # 19
                       [ 1,  1,  1,  1,  3,  1,  0,  1,  1,  0,  0,  7,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  5,  0,  0,  1,  5,  0,  0,  0,  0, 29],   # 20
                       [ 1,  1,  1,  1,  0,  0,  0,  0,  1,  0,  0,  0,  5,  0,  0,  0,  0,  0,  0,  0,  5,  0,  0,  0,  3,  0,  0,  1, 29,  0,  0,  0, 17,  1],   # 21
                       [ 1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  1,  0,  0,  0,  1, 22,  0,  0, 17, 18,  1],   # 22
                       [ 1,  8,  0,  0,  0,  0,  0,  0,  5,  3,  5,  0,  0,  9,  0,  0,  0,  0,  0,  8,  0,  0,  1,  0,  0,  0,  0,  1, 17,  0,  0,  0,  0, 17],   # 23
                       [ 1,  5,  0,  0,  0,  0,  0,  0, 33,  0,  1,  0,  0,  3,  0,  0,  0,  0,  0,  3,  0,  0,  1,  0,  0,  0,  0,  1, 18,  0,  0,  0,  0,  5],   # 24
                       [ 1, 29,  0,  0,  1,  3,  0,  0,  1,  0,  0,  1,  0,  0,  5,  0,  0,  0,  5,  0,  0,  1,  0,  0,  0,  0,  0,  1,  1, 17, 17,  0,  0, 29],   # 25
                       [ 1,  3,  0,  0,  0,  4,  0,  0, 35,  0,  0,  8,  0,  0,  0,  1,  3,  1,  0,  0,  0,  1,  0,  0,  0,  0,  0,  1, 19,  0,  0,  0,  0,  4],   # 26
                       [ 1,  5,  0,  0,  0, 27,  0,  0,  9,  0,  0,  0,  5,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  1, 21,  0,  0,  0,  0, 29],   # 27
                       [ 1,  7,  0,  0,  0,  3, 35,  1,  1,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  1,  5,  0,  0,  0,  0,  5],   # 28
                       [ 1,  1,  1,  0,  0,  0,  0, 25,  1, 10, 34, 35,  1,  1,  5,  3,  0,  0,  3, 40,  3, 37,  3, 40,  3, 37,  3, 40,  1,  0,  0,  1,  1,  1],   # 29
                       [ 1, 30,  0,  0,  0,  0,  0,  0, 32,  0,  0,  0,  0, 45,  1, 37,  0,  0,  0,  0,  0,  0,  0, -2,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1],   # 30
                       [ 1,  1,  0,  0,  0,  0,  0,  0, 26,  0,  0,  0,  0, 10,  1,  1,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1],   # 31
                       [ 1,  1,  7,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0, 24,  1,  1,  1,  0,  0,  1,  0,  0,  1,  0,  0,  1,  0,  0,  1,  0,  0,  1,  1,  1],   # 32
                       [ 1,  1,  0,  1,  0,  0,  0,  0, -1,  0,  0,  0,  0, 34,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],   # 33
                       [ 1,  1,  1,  1,  5,  1,  3, 31, 35, 11, 11, 11,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1]])  # 34

    sprites = [
        # scary women:
        [1, 7, 7, 5, False, True, False, True, True, 8, -5, 0, 0, 8, 0],
        [1, 5, 2, 5, False, True, False, True, True, 8, -5, 0, 0, 8, 0],
        [1, 10, 3, 5, False, True, False, True, True, 8, -5, 0, 0, 8, 0],
        [1, 30, 32, 5, False, True, False, True, True, 8, -5, 0, 0, 8, 0],

        # vuurmonster:
        [3, 5, 21, 7, False, True, False, True, True, 4, -5, 0, 0, 4, 0],
        [3, 2, 32, 7, False, True, False, True, True, 4, -5, 0, 0, 4, 0],
        [3, 10, 32, 7, False, True, False, True, True, 4, -5, 0, 0, 4, 0],
        [3, 16, 32, 7, False, True, False, True, True, 4, -5, 0, 0, 4, 0],

        # PINKY:
        [0, 16, 17, 15, False, True, False, True, True, 4, -7, 0, 0, 7, 0],
        [0, 16, 21, 15, False, True, False, True, True, 4, -7, 0, 0, 7, 0],
        [0, 16, 14, 15, False, True, False, True, True, 4, -7, 0, 0, 7, 0],

        # Black zombie:
        [2, 20, 3, 8, False, True, False, True, True, 3, -7, 0, 0, 3, 0],
        [2, 28, 3, 8, False, True, False, True, True, 3, -7, 0, 0, 3, 0],
        [2, 32, 7, 8, False, True, False, True, True, 3, -7, 0, 0, 3, 0],
        [2, 31, 17, 8, False, True, False, True, True, 3, -7, 0, 0, 3, 0],

        # sleutels:
        [4, 17, 17, 0, False, False, True, True, False, 0, 0, 0, 0, 2, 0],
        [4, 2, 32, 0, False, False, True, True, False, 0, 0, 0, 0, 2, 0],
        [4, 17, 31, 0, False, False, True, True, False, 0, 0, 0, 0, 2, 0],

        # ton:
        [4, 2, 27, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [4, 3, 23, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [4, 6, 31, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [4, 5, 30, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [4, 12, 32, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [4, 12, 30, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [4, 12, 2, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [4, 7, 11, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [4, 32, 25, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [4, 29, 32, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],

        # schatkist:
        [8, 15, 17, 0, False, False, True, False, False, 0, 0, 6, 0, 0, 0],
        [8, 8, 23, 0, False, False, True, False, False, 0, 0, 6, 0, 0, 0],
        [8, 7, 22, 0, False, False, True, False, False, 0, 0, 6, 0, 0, 0],
        [8, 6, 23, 0, False, False, True, False, False, 0, 0, 6, 0, 0, 0],
        [8, 2, 31, 0, False, False, True, False, False, 0, 0, 6, 0, 0, 0],
        [8, 9, 31, 0, False, False, True, False, False, 0, 0, 6, 0, 0, 0],
        [8, 10, 31, 0, False, False, True, False, False, 0, 0, 6, 0, 0, 0],
        [8, 12, 3, 0, False, False, True, False, False, 0, 0, 6, 0, 0, 0],

        # beker:
        [10, 16, 12, 0, False, False, True, False, False, 0, 0, 4, 0, 0, 0],
        [10, 17, 13, 0, False, False, True, False, False, 0, 0, 4, 0, 0, 0],
        [10, 16, 22, 0, False, False, True, False, False, 0, 0, 4, 0, 0, 0],
        [10, 17, 21, 0, False, False, True, False, False, 0, 0, 4, 0, 0, 0],
        [10, 5, 17, 0, False, False, True, False, False, 0, 0, 4, 0, 0, 0],
        [10, 7, 17, 0, False, False, True, False, False, 0, 0, 4, 0, 0, 0],
        [10, 9, 17, 0, False, False, True, False, False, 0, 0, 4, 0, 0, 0],
        [10, 10, 4, 0, False, False, True, False, False, 0, 0, 4, 0, 0, 0],
        [10, 11, 4, 0, False, False, True, False, False, 0, 0, 4, 0, 0, 0],
        [10, 10, 3, 0, False, False, True, False, False, 0, 0, 4, 0, 0, 0],
        [10, 32, 32, 0, False, False, True, False, False, 0, 0, 4, 0, 0, 0],
        [10, 17, 32, 0, False, False, True, False, False, 0, 0, 4, 0, 0, 0],
        [10, 16, 31, 0, False, False, True, False, False, 0, 0, 4, 0, 0, 0],

        # diamant
        [11, 16, 13, 0, False, False, True, False, False, 0, 0, 3, 0, 0, 0],
        [11, 17, 12, 0, False, False, True, False, False, 0, 0, 3, 0, 0, 0],
        [11, 30, 13, 0, False, False, True, False, False, 0, 0, 3, 0, 0, 0],
        [11, 30, 6, 0, False, False, True, False, False, 0, 0, 3, 0, 0, 0],
        [11, 32, 10, 0, False, False, True, False, False, 0, 0, 3, 0, 0, 0],
        [11, 32, 16, 0, False, False, True, False, False, 0, 0, 3, 0, 0, 0],
        [11, 23, 32, 0, False, False, True, False, False, 0, 0, 3, 0, 0, 0],

        # red ruby
        [12, 10, 20, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 10, 14, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 12, 23, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 12, 11, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 14, 8, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 13, 26, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 16, 21, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 17, 22, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 4, 29, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0, 0],
        [12, 4, 31, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0, 0],
        [12, 6, 12, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0, 0],
        [12, 3, 10, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0, 0],
        [12, 4, 7, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 17, 7, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 20, 9, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 22, 13, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 23, 16, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 23, 20, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 21, 23, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],
        [12, 20, 25, 0, False, False, True, False, False, 0, 0, 2, 0, 0, 0],

        # kroon
        [9, 18, 17, 0, False, False, True, False, False, 0, 0, 10, 0, 0, 0],
        [9, 23, 18, 0, False, False, True, False, False, 0, 0, 10, 0, 0, 0],
        [9, 28, 20, 0, False, False, True, False, False, 0, 0, 10, 0, 0, 0],
        [9, 16, 32, 0, False, False, True, False, False, 0, 0, 10, 0, 0, 0],

        # oven
        [6, 6, 5, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [6, 7, 4, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],

        # plant
        [5, 5, 2, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [5, 4, 3, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [5, 6, 27, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [5, 8, 27, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [5, 10, 27, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [5, 15, 27, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [5, 17, 27, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],

        # standbeeld
        [7, 18, 3, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [7, 21, 3, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [7, 24, 3, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [7, 27, 3, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [7, 30, 3, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [7, 15, 23, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [7, 18, 23, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [7, 15, 11, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [7, 18, 11, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [7, 19, 14, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [7, 14, 14, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [7, 19, 21, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],
        [7, 14, 21, 0, False, False, False, False, False, 0, 0, 0, 0, 0, 0],

        # knife
        [1, 12, 4, 0, False, False, True, False, False, 0, 0, 0, 0, 0, 0],

        # kettingzaag
        [2, 29, 20, 0, False, False, True, False, False, 0, 0, 0, 0, 0, 0],

        # koevoet
        [3, 2, 21, 0, False, False, True, False, False, 0, 0, 0, 0, 0, 0],
    ]

    pSpeler = [3 , 16.5]
    rSpeler = [-1 / np.sqrt(2), -1 / np.sqrt(2)]

    playerScore = 0
    sleutels = 0

    # ITEMS: TEXTURE / KRACHT / REACH
    items = [[0, 1, 1.25], [1, 2, 1.25], [2, 1.5, 1.25], [3, 1.25, 2]]

    # INVENTORY: SLOT 1 / SLOT 2 / SLOT 3 / SLOT 4
    inventory = [0, 0, 0, 0]

    health = MAXHEALTH
    stamina = MAXSTAMINA


def updateInventory():
    global wapen, selectedItem

    # ACHTERGROND INVENTORY TOEVOEGEN
    renderer.copy(texInventory[1],
                  srcrect=(0, 0, texInventory[1].size[0] * 2, texInventory[1].size[1] * 2),
                  dstrect=(SCREENWIDTH - 100, texBasis[7].size[1],
                           texInventory[1].size[0] * 2, texInventory[1].size[1] * 2))

    renderer.copy(texInventory[1],
                  srcrect=(4 * TEXTURESIZE, 0, TEXTURESIZE, TEXTURESIZE),
                  dstrect=(SCREENWIDTH - 70, texBasis[7].size[1] + 5 + selectedItem * 60,
                           TEXTURESIZE, TEXTURESIZE))

    # SLOTS TOEVOEGEN
    offset = 0
    for i in range(0, 4):
        if i == wapen:
            renderer.copy(texInventory[0],
                          srcrect=(4 * TEXTURESIZE, 0, TEXTURESIZE, TEXTURESIZE),
                          dstrect=(SCREENWIDTH - 70, texBasis[7].size[1] + offset,
                                   TEXTURESIZE, TEXTURESIZE))


        if inventory[i] > 0:
            renderer.copy(texInventory[0],
                          srcrect=(i * TEXTURESIZE, 0, TEXTURESIZE, TEXTURESIZE),
                          dstrect=(SCREENWIDTH - 70, texBasis[7].size[1] + offset,
                                   TEXTURESIZE, TEXTURESIZE))
        else:
            renderer.copy(texInventory[0],
                          srcrect=(0, 0, TEXTURESIZE, TEXTURESIZE),
                          dstrect=(SCREENWIDTH - 70, texBasis[7].size[1] + offset,
                                   TEXTURESIZE, TEXTURESIZE))
        offset += TEXTURESIZE

    wapen = inventory[selectedItem]


def updateHealthbar():
    a = SCREENWIDTH / 800

    renderer.copy(texBasis[6],
                  srcrect=(0, 0, texBasis[6].size[0], texBasis[6].size[1]),
                  dstrect=(0, int(texBasis[7].size[1] * a),
                           int(texBasis[6].size[0] * 3 * a), int(texBasis[6].size[1] * 3 * a)))

    healthMultiplier = 110 / MAXHEALTH
    staminaMultiplier = 110 / MAXSTAMINA

    for i in range(0, 6):
        renderer.draw_line((int(SCREENHEIGHT / 10),
                            int(a * (texBasis[7].size[1] + 63 + i)),
                            int(a * ((SCREENHEIGHT / 10) + abs(int(health * healthMultiplier)))),
                            int(a * (texBasis[7].size[1] + 63 + i))),
                            color=sdl2.ext.Color(250, 0, 0))
    for i in range(0, 6):
        renderer.draw_line((int(SCREENHEIGHT / 10),
                            int(a * (texBasis[7].size[1] + 102 + i)),
                            int(a * ((SCREENHEIGHT / 10) + abs(int(stamina * staminaMultiplier)))),
                            int(a * (texBasis[7].size[1] + 102 + i))),
                            color=sdl2.ext.Color(0, 0, 250))


def updateField(input, basisTexture):
    # basisTexture = -1 indien fps, 7 indien score
    a = SCREENWIDTH / 800
    ps = str(input)
    if basisTexture == -1:
        offset = 800 - len(ps) * TEXTURESIZE
    else:
        offset = texBasis[basisTexture].size[0]
        renderer.copy(texBasis[basisTexture],
                      srcrect=(0, 0, texBasis[basisTexture].size[0], texBasis[basisTexture].size[1]),
                      dstrect=(0, 0, int(texBasis[basisTexture].size[0] * a),
                                     int(texBasis[basisTexture].size[1] * a)))

    for i in range(len(ps)):
        getal = int(ps[i])
        renderer.copy(texScore,
                      srcrect=(getal * TEXTURESIZE, 0, TEXTURESIZE, TEXTURESIZE),
                      dstrect=(int((offset + i * TEXTURESIZE) * a), 0, int(TEXTURESIZE * a), int(TEXTURESIZE * a)))


def eenheidsVector(input):
    len = np.sqrt(input[0] * input[0] + input[1] * input[1])
    input[0] /= len
    input[1] /= len
    return input


def rotate(input, arc):
    input = [np.cos(arc) * input[0] - np.sin(arc) * input[1],
             np.sin(arc) * input[0] + np.cos(arc) * input[1]]
    return input


def getRStraal(kolom):
    output = [rSpeler[0] + (2 * (kolom / SCREENWIDTH) - 1) * rSpeler[1],
              rSpeler[1] - (2 * (kolom / SCREENWIDTH) - 1) * rSpeler[0]]
    output = eenheidsVector(output)
    return output


def rayCast(rStraal):
    # DELTA_V EN DELTA_H IN ELKE SITUATIE BEREKENEN
    if rStraal[0] == 0:
        dv = 1e30
    else:
        dv = 1 / abs(rStraal[0])

    if rStraal[1] == 0:
        dh = 1e30
    else:
        dh = 1 / abs(rStraal[1])

    # D_HORIZONTAAL EN D_VERTICAAL IN ELKE SITUATIE BEREKENEN
    if rStraal[1] < 0:
        dHor = (pSpeler[1] - np.floor(pSpeler[1])) * dh
    else:
        dHor = (1 - pSpeler[1] + np.floor(pSpeler[1])) * dh

    if rStraal[0] < 0:
        dVer = (pSpeler[0] - np.floor(pSpeler[0])) * dv
    else:
        dVer = (1 - pSpeler[0] + np.floor(pSpeler[0])) * dv

    # STARTWAARDEN WHILE-LOOP
    hInc = dHor
    vInc = dVer
    hit = False
    iCor = [0.0, 0.0]

    while not hit:
        if hInc <= vInc:
            iCor[0] = round(pSpeler[0] + hInc * rStraal[0], 3)
            iCor[1] = round(pSpeler[1] + hInc * rStraal[1], 3)

            hInc += dh
            intersectie = 1

            # TE CONTROLEREN VAK BEREKENEN
            mapX = int(np.floor(iCor[0]))
            if rStraal[1] < 0:  # VAK ONDER CHECKEN
                mapY = int(wereld.shape[1] - 1 - np.floor(iCor[1] - 1))
            else:  # VAK BOVEN CHECKEN
                mapY = int(wereld.shape[1] - 1 - np.floor(iCor[1]))
        else:
            iCor[0] = round(pSpeler[0] + vInc * rStraal[0], 3)
            iCor[1] = round(pSpeler[1] + vInc * rStraal[1], 3)

            vInc += dv
            intersectie = 0

            # TE CONTROLEREN VAK BEREKENEN
            mapY = int(wereld.shape[1] - 1 - np.floor(iCor[1]))
            if rStraal[0] < 0:  # VAK ONDER CHECKEN
                mapX = int(np.floor(iCor[0] - 1))
            else:  # VAK BOVEN CHECKEN
                mapX = int(np.floor(iCor[0]))

        # KIJKEN OF HET VAK BUITEN DE MAP LIGT
        if mapX > (wereld.shape[0] - 1) or mapX < 0 or mapY > (wereld.shape[1] - 1) or mapY < 0:
            dMuur, kMuur, intersectie = 100, 0, 0
            hit = True

        elif wereld[mapY][mapX] > 0:
            dMuur = np.sqrt(((iCor[0] - pSpeler[0]) ** 2) + ((iCor[1] - pSpeler[1]) ** 2))
            kMuur = wereld[mapY][mapX]
            hit = True

    if intersectie == 0:
        hoekAfstand = abs(np.ceil(iCor[1]) - iCor[1])
    else:
        hoekAfstand = iCor[0] - np.floor(iCor[0])

    return dMuur, kMuur, intersectie, hoekAfstand


def offsets(kMuur):
    if kMuur <= 8:
        offset = [int(np.floor((kMuur - 1) * TEXTURESIZE)), 0]
    else:
        rest = kMuur % 8
        if rest == 0:
            offset = [7 * TEXTURESIZE,
                      int(( np.floor(kMuur / 8) - 1) * TEXTURESIZE)]
        else:
            offset = [int(np.floor((rest - 1) * TEXTURESIZE)),
                      int(np.floor(kMuur / 8) * TEXTURESIZE)]
    return offset


def renderKolom(kolom, dMuur, offset, hoekAfstand, intersectie):
    lengteStrook = int(np.floor(SCREENWIDTH / (2 * dMuur)))

    renderer.copy(texMuren[intersectie],
                  srcrect=(offset[0] + int(np.floor(hoekAfstand * TEXTURESIZE)),
                           offset[1],
                           1,
                           TEXTURESIZE),
                  dstrect=(kolom,
                           int((SCREENHEIGHT - lengteStrook) / 2),
                           1,
                           lengteStrook))


def verwerkInput():
    global pSpeler, rSpeler, afsluiten, selectedItem, hit, actie, pauzeNummer, pauze, spelen, startscherm, startschermIndex, gameOver, win, pauze, stamina, toggle, STEPSIZE, HOEK_STEPSIZE

    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            afsluiten = True
            break

    if key_states[sdl2.SDL_SCANCODE_ESCAPE]:
        afsluiten = True

    if spelen:
        if key_states[sdl2.SDL_SCANCODE_LSHIFT]:
            if stamina > 0:
                stamina -= 1
                STEPSIZE = 0.5
            else:
                STEPSIZE = 0.25
        else:
            if stamina < MAXSTAMINA:
                stamina += 0.5
            STEPSIZE = 0.25

        if key_states[sdl2.SDL_SCANCODE_U]:
            actie = True
            hit = True

        if not key_states[sdl2.SDL_SCANCODE_U]:
            hit = False

        if key_states[sdl2.SDL_SCANCODE_I]:
            rSpeler = rotate(rSpeler, HOEK_STEPSIZE)
            rSpeler = eenheidsVector(rSpeler)

        if key_states[sdl2.SDL_SCANCODE_O]:
            rSpeler = rotate(rSpeler, -HOEK_STEPSIZE)
            rSpeler = eenheidsVector(rSpeler)

        if key_states[sdl2.SDL_SCANCODE_W]:
            pSpeler[0] += STEPSIZE * rSpeler[0]
            pSpeler[1] += STEPSIZE * rSpeler[1]

        if key_states[sdl2.SDL_SCANCODE_A]:
            pSpeler[0] -= STEPSIZE * rSpeler[1]
            pSpeler[1] += STEPSIZE * rSpeler[0]

        if key_states[sdl2.SDL_SCANCODE_D]:
            pSpeler[0] += STEPSIZE * rSpeler[1]
            pSpeler[1] -= STEPSIZE * rSpeler[0]

        if key_states[sdl2.SDL_SCANCODE_S]:
            pSpeler[0] -= STEPSIZE * rSpeler[0]
            pSpeler[1] -= STEPSIZE * rSpeler[1]

        if key_states[sdl2.SDL_SCANCODE_V]:
            # print("M")
            if toggle:
                toggle = False
                testBool = True
                teller = 1
                while testBool:
                    if selectedItem + teller in inventory:
                        testBool = False
                        if selectedItem == 3:
                            selectedItem = 0
                        else:
                            selectedItem += 1
                    teller += 1
                    if teller >= 4:
                        selectedItem = 0
                        testBool = False
        else:
            if not toggle:
                toggle = True
                testBool = True
                teller = 1
                while testBool:
                    if selectedItem + teller in inventory:
                        testBool = False
                        if selectedItem == 3:
                            selectedItem = 0
                        else:
                            selectedItem += 1
                    teller += 1
                    if teller >= 4:
                        selectedItem = 0
                        testBool = False

        if key_states[sdl2.SDL_SCANCODE_P]:
            spelen = False
            pauze = True

    if startscherm:
        if startschermIndex == 0:
            startscherm = False
            spelen = True

        elif startschermIndex == 1:
            if key_states[sdl2.SDL_SCANCODE_D]:
                startschermIndex = 0

            if key_states[sdl2.SDL_SCANCODE_N]:
                startschermIndex = 2
                time.sleep(0.3)

        elif startschermIndex == 2:
            if key_states[sdl2.SDL_SCANCODE_B]:
                startschermIndex = 1
                time.sleep(0.3)

            if key_states[sdl2.SDL_SCANCODE_D]:
                startschermIndex = 3

            if key_states[sdl2.SDL_SCANCODE_N]:
                startschermIndex = 4
                time.sleep(0.3)

        elif startschermIndex == 3:
            if key_states[sdl2.SDL_SCANCODE_A]:
                startschermIndex = 2

        elif startschermIndex == 4:
            if key_states[sdl2.SDL_SCANCODE_B]:
                startschermIndex = 2
                time.sleep(0.3)

            if key_states[sdl2.SDL_SCANCODE_D]:
                startschermIndex = 5

        elif startschermIndex == 5:
            if key_states[sdl2.SDL_SCANCODE_A]:
                startschermIndex = 4

    if gameOver:
        if key_states[sdl2.SDL_SCANCODE_D]:
            gameOver = False
            spelen = False
            startscherm = True

            init()
            time.sleep(1)

    if win:
        if key_states[sdl2.SDL_SCANCODE_D]:
            win = False
            startscherm = True
            time.sleep(1)

    if pauze:
        if pauzeNummer == 0:
            if key_states[sdl2.SDL_SCANCODE_D]:
                spelen = True
                pauze = False
        else:
            if key_states[sdl2.SDL_SCANCODE_D]:
                startschermIndex = 1
                startscherm = True
                time.sleep(0.5)
                pauze = False

        if key_states[sdl2.SDL_SCANCODE_B]:
            if pauzeNummer == 0:
                pauzeNummer = 1
            else:
                pauzeNummer = 0
            time.sleep(0.5)

        elif key_states[sdl2.SDL_SCANCODE_N]:
            if pauzeNummer == 0:
                pauzeNummer = 1
            else:
                pauzeNummer = 0
            time.sleep(0.5)

    sdl2.SDL_SetRelativeMouseMode(True)


def renderSprite(spritenummer, afstand, a, isAnimatie):
    global SCREENWIDTH, SCREENHEIGHT, sprites, zBuffer

    # AF TE BEELDEN KOLOMMEN BEREKENEN
    lengteStrook = SCREENHEIGHT / (2 * afstand)
    mintex, maxtex, mins, maxs = TEXTURESIZE, 0, SCREENWIDTH, 0

    for i in range(-int(np.floor(TEXTURESIZE / 2)), int(np.floor(TEXTURESIZE / 2)), 1):
        kolom = int(np.floor(a + (i * lengteStrook / TEXTURESIZE)))
        if 0 <= kolom < SCREENWIDTH and afstand < zBuffer[kolom]:
            if kolom < mins:
                mins = kolom
                mintex = int(np.floor((TEXTURESIZE / 2) + i))

            elif kolom > maxs:
                maxs = kolom
                maxtex = int(np.floor((TEXTURESIZE / 2) + i))

    deltas = maxs - mins

    # FRAME VOLGENS FRAMECOUNT BEPALEN
    if isAnimatie:
        if sprites[spritenummer][9] < sprites[spritenummer][13] - 1:
            sprites[spritenummer][9] += 1
        else:
            sprites[spritenummer][9] = 0

        renderer.copy(texSprites[1],
                      srcrect=(sprites[spritenummer][9] * TEXTURESIZE + mintex, sprites[spritenummer][0] * TEXTURESIZE,
                               maxtex - mintex, TEXTURESIZE),
                      dstrect=(mins,
                               int(np.floor((SCREENHEIGHT / 2) - (lengteStrook / 2) + (TEXTURESIZE / afstand))),
                               deltas, int(np.floor(lengteStrook))))

    else:
        offset = offsets(sprites[spritenummer][0])
        renderer.copy(texSprites[0],
                      srcrect=(offset[0] + mintex, offset[1],
                               maxtex - mintex, TEXTURESIZE),
                      dstrect=(mins,
                               int(np.floor((SCREENHEIGHT / 2) - (lengteStrook / 2) + (TEXTURESIZE / afstand))),
                               deltas, int(np.floor(lengteStrook))))


def verwerkSprite(spritenummer):
    global rSpeler, pSpeler, sprites, health, actie, hit, soundWapens, playerScore, sleutels

    #            0     1   2      3                 4          5           6             7          8           9            10             11          12         13          14
    # SPRITES: SPRITE / X / Y / AANTAL LEVENS / VERWIJDEREN / ACTIEF / MEENEEMBAAR / ANIMATIE / KAN DOOD / FRAMECOUNT / DELTA HEALTH / DELTA SCORE / AFSTAND / MAX FRAMES / AFSTAND

    # CAMERACOORDINATEN EN A BEPALEN
    wereldCoordinaten = np.array([[sprites[spritenummer][1] - pSpeler[0]], [sprites[spritenummer][2] - pSpeler[1]]])
    determinant = (rSpeler[1] * rSpeler[1]) + (rSpeler[0] * rSpeler[0])
    inverseTransformatieMatrix = np.array([[rSpeler[1], -rSpeler[0]],
                                           [rSpeler[0], rSpeler[1]]])

    cameracoordinaten = np.matmul(inverseTransformatieMatrix, wereldCoordinaten)
    cameracoordinaten[0][0] /= determinant
    cameracoordinaten[1][0] /= determinant
    a = int(np.floor(((cameracoordinaten[0][0] / cameracoordinaten[1][0]) + 1) * SCREENWIDTH / 2))

    # RENDEREN VAN DE SPRITE
    if not sprites[spritenummer][4] and cameracoordinaten[1][0] >= 0:
        renderSprite(spritenummer, sprites[spritenummer][14], a, sprites[spritenummer][7])

    if sprites[spritenummer][6] and sprites[spritenummer][14] <= GROOTTE_HITBOX / 2:
        sprites[spritenummer][4] = True
        health += sprites[spritenummer][10]
        playerScore += sprites[spritenummer][11]

        if sprites[spritenummer][0] == 4 and sprites[spritenummer][7]:
            sleutels += 1

        elif sprites[spritenummer][0] == 1 and not sprites[spritenummer][7]:
            inventory[1] = 1

        elif sprites[spritenummer][0] == 2 and not sprites[spritenummer][7]:
            inventory[2] = 2

        elif sprites[spritenummer][0] == 3 and not sprites[spritenummer][7]:
            inventory[3] = 3

        if health > MAXHEALTH:
            health = MAXHEALTH

    rStraalSP = eenheidsVector([pSpeler[0] - sprites[spritenummer][1],
                                pSpeler[1] - sprites[spritenummer][2]])


    # BEWEGING BIJ ACTIEVE SPRITES
    if sprites[spritenummer][5]:
        # MOGELIJKHEID TOT AANVALLEN VAN ACTIEVE SPRITES:
        if sprites[spritenummer][14] < items[selectedItem][2] and hit:
            sprites[spritenummer][3] -= items[selectedItem][1]
            winsound.PlaySound(soundWapens[wapen], winsound.SND_ASYNC | winsound.SND_ALIAS)
            renderer.copy(texBasis[5],
                          srcrect=(0, 0, texBasis[5].size[0],texBasis[5].size[1]),
                          dstrect=(0, 0, SCREENWIDTH, SCREENHEIGHT))

        if sprites[spritenummer][3] <= 0:
            sprites[spritenummer][4] = True
            playerScore += sprites[spritenummer][11]
            sprites[spritenummer][0] = 0
            sprites.append([5, sprites[spritenummer][1], sprites[spritenummer][2], 1, False, False, True, True, False, 0, 20, 0, 0, 2, 0])

        if sprites[spritenummer][14] < 5:
            sprites[spritenummer][1] += 0.5 * STEPSIZE * rStraalSP[0]
            sprites[spritenummer][2] += 0.5 * STEPSIZE * rStraalSP[1]

        if sprites[spritenummer][14] < GROOTTE_HITBOX / 2:
            if health > 0:
                health += sprites[spritenummer][10]

            renderer.copy(texBasis[4],
                          srcrect=(0, 0, texBasis[4].size[0], texBasis[4].size[1]),
                          dstrect=(0, 0, SCREENWIDTH, SCREENHEIGHT))

            sprites[spritenummer][1] -= 0.5 * STEPSIZE * rStraalSP[0]
            sprites[spritenummer][2] -= 0.5 * STEPSIZE * rStraalSP[1]

            pSpeler[0] += 0.5 * STEPSIZE * rStraalSP[0]
            pSpeler[1] += 0.5 * STEPSIZE * rStraalSP[1]

        # COLLISION DETECTION SPRITE
        for i, j in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            rStraalM = [0.5 * GROOTTE_HITBOX * i,
                       0.5 * GROOTTE_HITBOX * j]

            mapX = int(np.floor(sprites[spritenummer][1] + rStraalM[0]))
            mapY = int(wereld.shape[1] - 1 - np.floor(sprites[spritenummer][2] + rStraalM[1]))

            rStraalM = eenheidsVector(rStraalM)

            if mapX >= 0 and mapX < wereld.shape[0] and mapY >= 0 and mapY < wereld.shape[1]:
                if wereld[mapY][mapX] > 0:
                    sprites[spritenummer][1] -= STEPSIZE * rStraalM[0]
                    sprites[spritenummer][2] -= STEPSIZE * rStraalM[1]
            else:
                sprites[spritenummer][1] -= STEPSIZE * rStraalM[0]
                sprites[spritenummer][2] -= STEPSIZE * rStraalM[1]

        for i in range(len(sprites)):
            if i != spritenummer:
                dx = sprites[spritenummer][1] - sprites[i][1]
                dy = sprites[spritenummer][2] - sprites[i][2]
                afstandTotAndereSprite = np.sqrt(dx * dx + dy * dy)
                if afstandTotAndereSprite < GROOTTE_HITBOX / 4 and not sprites[i][6]:
                    vec = [dx, dy]
                    sprites[spritenummer][1] += STEPSIZE * vec[0]
                    sprites[spritenummer][2] += STEPSIZE * vec[1]

    else:
        if sprites[spritenummer][14] <= GROOTTE_HITBOX / 2 and not sprites[spritenummer][6]:
            pSpeler[0] += STEPSIZE * rStraalSP[0]
            pSpeler[1] += STEPSIZE * rStraalSP[1]


def cleanSprites():
    global sprites

    hoeveelheid = 0
    for spritenummer in range(len(sprites)):
        if sprites[spritenummer][4]:
            sprites.append([0, 0, 0, 1, False, False, False, False, False, 0, 0, 0, 0, 0, 0])
            sprites.pop(spritenummer)
            hoeveelheid += 1

    for i in range(hoeveelheid):
        sprites.pop(-1)


def gebruikWapen():
    global actie, hit, framecountWapens, selectedItem

    # WAPENS GEBRUIKEN
    if actie and framecountWapens < len(texWapens[selectedItem]) - 1:
        framecountWapens += 1

    elif not hit and actie:
        framecountWapens = 0
        actie = False

    elif hit:
        framecountWapens = 0

    renderer.copy(texWapens[selectedItem][framecountWapens],
                  srcrect=(0, 0, texWapens[selectedItem][framecountWapens].size[0],
                           texWapens[selectedItem][framecountWapens].size[1]),
                  dstrect=(0, 0, SCREENWIDTH, SCREENHEIGHT))


def toonSleutels():
    global sleutels

    for i in range(3):
        renderer.copy(texInventory[0],
                      srcrect=(5 * TEXTURESIZE, 0, TEXTURESIZE, TEXTURESIZE),
                      dstrect=(SCREENWIDTH - (i + 1) * TEXTURESIZE, SCREENHEIGHT - TEXTURESIZE, TEXTURESIZE, TEXTURESIZE))

    for i in range(sleutels):
        renderer.copy(texInventory[0],
                      srcrect=(6 * TEXTURESIZE, 0, TEXTURESIZE, TEXTURESIZE),
                      dstrect=(SCREENWIDTH - (3 - i) * TEXTURESIZE, SCREENHEIGHT - TEXTURESIZE, TEXTURESIZE, TEXTURESIZE))


def toonJumpscare():
    global texJumpscares, framecounter, wereld, activeerJumpscare, keuzeJumpscare

    if framecounter < len(texJumpscares[keuzeJumpscare]) - 1:
        framecounter += 1
    else:
        framecounter = 0
        activeerJumpscare = False

    ser.write(('v').encode())
    texture = texJumpscares[keuzeJumpscare][framecounter]
    renderer.copy(texture,
                  srcrect=(0, 0, texture.size[0], texture.size[1]),
                  dstrect=(0, 0, SCREENWIDTH, SCREENHEIGHT))


def checkMetTimer():
    ser.write(('p').encode())
    if (sleutels == 0):
        ser.write(('t').encode())
        #print(datetime.datetime.now(), " - ser.write : 't'.")
    if (sleutels == 1):
        ser.write(('w').encode())  # todo Stuur het aantal sleutels door
        #print(datetime.datetime.now(), " - ser.write : 'w'.")
    if (sleutels == 2):
        ser.write(('x').encode())
        #print(datetime.datetime.now(), " - ser.write : 'x'.")
    if (sleutels == 3):
        ser.write(('y').encode())
        #print(datetime.datetime.now(), " - ser.write : 'y'.")

    if health < 10:
        eenheid = health
        tiental = 0

    elif health >= 10:
        eenheid = health % 10
        tiental = int(str(health)[:1])

    if (tiental == 0): ser.write(('0').encode())
    if (tiental == 1): ser.write(('1').encode())
    if (tiental == 2): ser.write(('2').encode())
    if (tiental == 3): ser.write(('3').encode())
    if (tiental == 4): ser.write(('4').encode())
    if (tiental == 5): ser.write(('5').encode())
    if (tiental == 6): ser.write(('6').encode())
    if (tiental == 7): ser.write(('7').encode())
    if (tiental == 8): ser.write(('8').encode())
    if (tiental == 9): ser.write(('9').encode())
    #print(datetime.datetime.now(), " - ser.write : tiental = ", tiental)


    if (eenheid == 0): ser.write(('a').encode())
    if (eenheid == 1): ser.write(('b').encode())
    if (eenheid == 2): ser.write(('c').encode())
    if (eenheid == 3): ser.write(('d').encode())
    if (eenheid == 4): ser.write(('e').encode())
    if (eenheid == 5): ser.write(('f').encode())
    if (eenheid == 6): ser.write(('g').encode())
    if (eenheid == 7): ser.write(('h').encode())
    if (eenheid == 8): ser.write(('i').encode())
    if (eenheid == 9): ser.write(('j').encode())
    #print(datetime.datetime.now(), " - ser.write : eenheid = ", eenheid)


def speel():
    global zBuffer, pSpeler, rSpeler, wereld, playerScore, health, stamina, hit, sprites, onthoudX, onthoudY, activeerJumpscare, keuzeJumpscare

    if health <= 0:
        return

    elif health <= 50:
        ser.write(('p').encode())

    renderer.clear()
    startTime = time.time()

    zBuffer = [0] * SCREENWIDTH

    # RAYCASTING
    for kolom in range(SCREENWIDTH):
        rStraal = getRStraal(kolom)
        dMuur, kMuur, intersectie, hoekAfstand = rayCast(rStraal)
        zBuffer[kolom] = dMuur
        dMuur = dMuur * (rSpeler[0] * rStraal[0] + rSpeler[1] * rStraal[1])

        if kMuur != 0:
            offset = offsets(kMuur)
            renderKolom(kolom, dMuur, offset, hoekAfstand, intersectie)

    # COLLISION DETECTION SPELER
    for i, j in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
        rStraal = [0.5 * GROOTTE_HITBOX * i,
                   0.5 * GROOTTE_HITBOX * j]

        mapX = int(np.floor(pSpeler[0] + rStraal[0]))
        mapY = int(wereld.shape[1] - 1 - np.floor(pSpeler[1] + rStraal[1]))

        rStraal = eenheidsVector(rStraal)

        if mapX >= 0 and mapX < wereld.shape[0] and mapY >= 0 and mapY < wereld.shape[1]:
            if wereld[mapY][mapX] > 0:
                pSpeler[0] -= STEPSIZE * rStraal[0]
                pSpeler[1] -= STEPSIZE * rStraal[1]
        else:
            pSpeler[0] -= STEPSIZE * rStraal[0]
            pSpeler[1] -= STEPSIZE * rStraal[1]

    # JUMPSCARES
    mapX = int(np.floor(pSpeler[0]))
    mapY = wereld.shape[1] - 1 - int(np.floor(pSpeler[1]))

    for i in range(len(sprites)):
        sprites[i][14] = np.sqrt((sprites[i][1] - pSpeler[0]) * (sprites[i][1] - pSpeler[0]) +
                                 (sprites[i][2] - pSpeler[1]) * (sprites[i][2] - pSpeler[1]))

    # SPRITES SORTEREN OP AFSTAND TOT SPELER
    sprites = sorted(sprites, key=lambda x: x[14])
    sprites.reverse()

    for i in range(len(sprites)):
        verwerkSprite(i)

    # JUMPSCARE CHECKEN
    if wereld[mapY][mapX] < 0 or activeerJumpscare:
        if not activeerJumpscare:
            keuzeJumpscare = abs(wereld[mapY][mapX])
            activeerJumpscare = True
            wereld[mapY][mapX] = 0
        toonJumpscare()

    if hit:
        hit = False

    deltaTime = time.time() - startTime
    updateField(int(np.floor(1 / deltaTime)), -1)
    updateField(playerScore, 7)
    updateHealthbar()
    updateInventory()
    toonSleutels()
    gebruikWapen()
    cleanSprites()


def main():
    global startschermIndex, startscherm, texStartscherm, gameOver, win, spelen, pauze, health

    init()

    window.show()
    # renderer.copy(texBasis[0],
    #               srcrect=(0, 0, texBasis[0].size[0], texBasis[0].size[1]),
    #               dstrect=(0, 0, SCREENWIDTH, int(np.floor(SCREENHEIGHT / 2))))

    while not afsluiten:
        # INPUT VERWERKEN
        verwerkInput()

        if startscherm:
            renderer.copy(texStartscherm[startschermIndex],
                          srcrect=(0, 0, texStartscherm[startschermIndex].size[0],
                                   texStartscherm[startschermIndex].size[1]),
                          dstrect=(0, 0, SCREENWIDTH, SCREENHEIGHT))

        elif sleutels == 3 or win:
            win = True
            spelen = False
            gameOver = False
            pauze = False
            startscherm = False
            renderer.copy(texBasis[8],
                          srcrect=(0, 0, texBasis[8].size[0], texBasis[8].size[1]),
                          dstrect=(0, 0, SCREENWIDTH, SCREENHEIGHT))

        elif health <= 0 or gameOver:
            health = 0
            win = False
            spelen = False
            gameOver = True
            pauze = False
            startscherm = False
            renderer.copy(texBasis[9],
                          srcrect=(0, 0, texBasis[9].size[0],
                                   texBasis[9].size[1]),
                          dstrect=(0, 0, SCREENWIDTH, SCREENHEIGHT))

        elif pauze:
            if pauzeNummer == 0:
                renderer.copy(texPauzescherm[0],
                              srcrect=(0, 0, texPauzescherm[0].size[0],
                                       texPauzescherm[0].size[1]),
                              dstrect=(0, 0, SCREENWIDTH, SCREENHEIGHT))
            else:
                renderer.copy(texPauzescherm[1],
                              srcrect=(0, 0, texPauzescherm[1].size[0],
                                       texPauzescherm[1].size[1]),
                              dstrect=(0, 0, SCREENWIDTH, SCREENHEIGHT))

        elif spelen:
            speel()

        # SCHERM UPDATEN
        renderer.present()
        window.refresh()

with cProfile.Profile() as pr:
    main()

stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
# stats.print_stats()
stats.dump_stats(filename="test.prof")