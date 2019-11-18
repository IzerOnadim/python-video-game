# TURN YOUR .PY FILES INTO .EXE FILES

# import cx_Freeze library, which I PIP installed
# cx_Freeze freezes python scripts into executable files
import cx_Freeze
# import os module
import os

# define executables, which is the executable file I want to make
# use cx_Freeze's Executable function, on the file I want to turn to a .exe
executables = [cx_Freeze.Executable("MY_GAME.py")]

# not sure what these lines are doing - does not work without them, retruns an error, stack overflow gave this solution, it works.
os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python35-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files\Python35-32\tcl\tk8.6'

# use setup function from cx_Freeze
cx_Freeze.setup(
    # name executable file will have
    name="My Game",
    # include all the packages and files that my .exe will need to run.
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["functions.py", "classes.py",
                                             "highlevel.txt", "highscore.txt",
                                             "savedgame.bak", "savedgame.dat", "savedgame.dir", "savegame.txt", "savegame",
                                             "music.mp3", "bullet.wav", "hit.wav", "money.wav", "explosionSound.wav",
                                             "Lightning.jpg", "sand.jpg", "sea.jpg",
                                             "beach.png", "bullet.png", "explosion.png", "fence.png", "heart.png", "infinity.png",
                                             "kraken.png", "lightning.png", "lightningBolt.png", "mainBoat.png", "nuke.png",
                                             "sailBoat.png", "skip.png", "star.png", "torpedo.png", "treasure.png", "waves.png"
                                             ]}},
    # set executables parameter to the executables variable made at the top
    executables=executables
)
