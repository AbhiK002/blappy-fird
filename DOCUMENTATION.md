# Blappy Fird
A remake by Abhineet Kelley of the classic game Flappy Bird, for a fun learning experience

# 1. Introduction
Welcome to Blappy Fird, a remake of the classic game 'Flappy Bird' with a few more features like customisable backgrounds, etc. I made this game mostly for fun, but to also get an idea of how a project is carried out in the real world with documentation and other important stuff.

(user documentation to be added here)

# 2. About the Game
## 2.1 Rules
This game contains the classic gameplay of the original game, in addition to some things I added myself.
The rules are simple:
- Click or press SPACEBAR to make the bird hop
- The bird will automatically come down (because gravity)
- Hop through infinite obstacles to score 1 point
- If you touch the ground or any obstacle, you lose
- Reach the highest score you can

### 2.1.1 Extra features
- None yet, will be added soon

# 3. Technical Details
Blappy Fird has been made using the Python language and tkinter has been used for the GUI of the game. I used tkinter because the game doesn't have advanced graphics or mechanisms that require complex frameworks like PyQt5.

## 3.1 Libraries/Modules Used
- `tkinter`: To make the GUI of the game.
- `random`: To generate random values used for the obstacles in the game
- `pathlib`: Generating cross-platform folder/file paths since different operating systems have different path representations (`/` or `\\`)
- `os`:  Making a function `resource_path(relative_path)` that'll help us embed assets into the exe file made using `pyinstaller` 
- `sys`: Same usage as `os`
- `platform`: To check the user's operating system

## 3.2 Game Directory Structure
- For Windows, the game's user data, which is stuff like settings, etc is located at:
  - `C:\Users\<user>\AppData\Local\AbhineetKelley\BlappyFird\`
which is equivalent to
  - `%localappdata%\AbhineetKelley\BlappyFird\`


- For other operating systems (Linux, MacOS):
  - `~/AbhineetKelley/BlappyFird/`  
    where `~` represents the OS's respective home directory

### 3.2.1 Code Structure
Alright, so the game's source code directory looks like this:

```
blappyFird/
    |
    |- main.py
    |- backend.py
    |
    |= assets/
        |- (PNG Files)
        |
        |= bg/
            |- (PNG Files)

        |= birds/
            |- (PNG Files)

        |= pillars/
            |- (PNG Files)
```

Details about each file/folder:
- `main.py`: This file contains the GUI logic of the game. It does most of the work like making the bird fall due to gravity, detect if the user has lost the game, etc.
- `backend.py`: This file does the job of getting assets from the game's directory by utilising cross platform libraries like pathlib, etc. It also checks or creates the game's user data directory and saves user settings for future use.
- `assets/`: This directory contains the image files for the game. It has 3 subfolders:
  - `bg/`: Contains image(s) used for the background (by default the sky image)
  - `birds/`: Contains image(s) used for the player icon (by default a yellow bird)
  - `pillars/`: Contains image(s) used for the pillars (by default the green pillars)

After the game has been converted into an exe file, the 2 python files will become 1 exe file instead. Also, the default images will get embedded into the exe file itself so that the game doesn't crash in case it doesn't find any of the image files/assets.

# 4. How Blappy Fird Works
### 4.0.1 Overview
Blappy Fird is a fun little game and therefore has a simple working mechanism. It basically has 3 states/scenes:
- Main Menu
  - ACTIVE when the bird dies, or user starts the game 
  - PLAY button, EXIT button visible
  - bird hovers mid air in the background, unaffected by the user's actions
  - current score displayed on the top


- Pre-round
  - ACTIVE when the user clicks the PLAY button
  - main menu is hidden
  - score count resets to 0
  - game waits for the user to click anywhere/press spacebar again
  - as soon as the user presses spacebar/clicks anywhere, the game will start
  - bird hovers mid air and no obstacles spawn yet


- Actual round gameplay
  - ACTIVE when the user clicks anywhere during the pre round
  - gravity starts acting on the bird
  - obstacles start spawning and the bird travels through them
  - the score count increases by 1 everytime the bird passes an obstacle without dying
  - as soon as the bird dies, the game goes to the Main Menu state


This is how the game works on the outside. Now, for the inside part I will explain the working of the code in 2 parts:
1. Starting the game
2. Running the game

NOTE: the `tkinter` library will be referred to as `tk` in the entire documentation, since I imported it with the alias `tk` in the source code

## 4.1 Starting the game
These are some important details to remember about the game's GUI:
- The game window only has a single `tk.Canvas` widget that covers the entire window area
- All the things you see on the screen are image files drawn onto the canvas widget itself
- I will refer to the `tk.Canvas` widget as "the canvas" throughout the documentation
  - no confusion, since there's only 1 canvas in the entire source code

### 4.1.1 Run main.py
To start the game, we run `main.py`, that contains a class named `App` which will then be initialised in the main block inside the file.
```python
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # stuff happens here
        pass

if __name__ == '__main__':
    App()
```
I decided to inherit from the Tk class instead of making a `self.root = tk.Tk()` object and using it throughout the class because I have no idea, it just looks cooler.

1 small advantage can be, writing `self.geometry` is easier than `self.root.geometry` since I don't have to type root again and again. But the difference isn't significant. Anyways moving on, the `__init__()` method of `App` is called.

Here are the things that happen inside the `__init__()` method of `App` class:
- `super().__init__()`: initialiser method of parent class `tk.Tk` is called.
  - this creates the main `Tk` window, which will be referred to as the game window in the code as well as this document


- `gravity_enabled`: boolean is initialised to `False`
  - indicates whether the bird is currently under the effect of gravity or not
  - turns to `True` when a game round is started
- `main_menu_screen`: boolean is initialised to `True`
  - indicates whether the main menu is visible (the play, exit buttons)
  - turns to `False` when a game round is started

- `backend`: stores an instance of class `Backend` to be used throughout the `App` class
  - this class is present in the `backend.py` file and will be talked about soon  


- `canvas_bg_images`: an empty list to store the IDs (called tags in the tkinter world) of the background images drawn onto the main canvas
  - this list will help in giving an infinitely scrolling background effect

- `canvas_pillar_images`: an empty list to store the IDs/tags of the pillars' images drawn onto the canvas
  - pillars are the obstacles in the game, just to make it clear

- `current_score`: an integer storing the current score of the user

- these methods are called:
  - `store_currently_used_assets()`: fetches the currently used image assets from the `Backend` class via `self.backend` instance
    - stuff like the currently selected background image, player icon image and pillar images
    - these are stored as class attributes (`self.some_attribute`) so that they can be used anywhere inside the `App` class
  - `init_window()`: configure the game window (dimensions, coordinates on the screen, resizable properties, etc)
  - `init_background()`: draws the background images on the canvas, adds their tags to `self.canvas_bg_images` list and starts animating them
    - 3 images in total for an infinite scrolling effect
  - `init_bird()`: draws the player icon (which is by default a yellow bird) on the canvas
    - defines properties like gravity, terminal velocity etc for the physics of the bird
  - `init_mainmenu()`: draws the main menu buttons and other widgets onto the canvas and binds them to related functions
  - `init_pillars()`: draws the obstacles/pillars off-screen onto the canvas and adds their tags to `self.canvas_pillar_images` list
  - `init_scoreboard()`: draws the score label(text widget) displaying the current score on the canvas
  - `mainloop()`: keeps the game window visible

Once these methods have been called, the game now waits for the user to click on any of the buttons and eventually play the game.
Each and every function present in the code is explained in detail later in this document.

### 4.1.2 Inside backend.py
If you don't remember (although it's only a few lines up), we initialised the `Backend` class inside the `__init__` method of `App` class. 

Now, here are the things that happen inside the `__init__` method of `Backend` class that is present inside the `backend.py` file:
```python
from pathlib import Path
from tkinter import PhotoImage
import os
import platform
import sys

class Backend:
    # prepatory stuff here
    def __init__(self):
        # normal stuff here
        pass
```
#### 4.1.2.1 Prepatory Stuff
Inside the `Backend` class definition, these class attributes are defined:
- `root_directory` (Path object): contains the path to the home directory of the user, which will become the root directory for the game's user data directory
  - something like `C:\Users\YOURNAME\` in Windows
  - for Linux it's `/home/YOURNAME/`
  - This attribute will be used by systems running anything other than Windows


- `root_directory_for_windows` (Path object): for Windows machines, this will contain the path to the root directory of the game's user data directory, initialised to: 
  - `%HOME%\AppData\Local\` OR `%localappdata%\`
  - here `%HOME%` represents the home directory
  - This attribute will be used by systems runing Windows


- `creator_root_directory` (String): name of the parent directory named after me, which will contain the main game directory
- `game_directory` (String): name of the game directory that will contain the settings files
- `assets_directory` (Path object): path to the assets folder that contains the game's image files
 
- `DEFAULT_BACKGROUND`: path to the default sky background image file
- `DEFAULT_BIRD`: path to the default yellow bird image file
- `DEFAULT_PILLAR_UP`: path to the default green pillar (pointing down) image file
- `DEFAULT_PILLAR_DOWN`: path to the default green pillar (pointing up) image file
- `PLAY_BUTTON`: path to the PLAY button image file
- `EXIT_BUTTON`: path to the EXIT button image file

```python
from pathlib import Path
import platform

root_directory = Path.home()
root_directory_for_windows = Path.home() / "AppData" / "Local"

creator_root_directory = "AbhineetKelley"
game_directory = "BlappyFird"

final_path =  root_directory / creator_root_directory / game_directory
final_path_for_windows =  root_directory_for_windows / creator_root_directory / game_directory
# this is a neat little feature of pathlib
# it generates cross-platform paths 
# according to the OS the file is being run in

if platform.system()=="Windows":
    print(final_path_for_windows) 
else: print(final_path)
```
The output of the above code for Windows will be,
```python
Path("C:\\User\\YOURNAME\\AppData\\Local\\AbhineetKelley\\BlappyFird")
```
and for Linux,
```python
Path("/home/YOURNAME/AbhineetKelley/BlappyFird")
```


#### 4.1.2.2 Normal Stuff
These things in particular happen inside the `__init__` method of `Backend` class:
- three variables that will store the currently used game assets are initialised:
  - `game_background_image`: initialised to `DEFAULT_BACKGROUND`
  - `game_player_image`: initialised to `DEFAULT_BIRD`
  - `game_pillar_up_image`: initialised to `DEFAULT_PILLAR_UP`
  - `game_pillar_down_image`: initialised to `DEFAULT_PILLAR_DOWN`


- `user_has_windows`: self-explanatory boolean value, True if user has Windows OS
- `classic_game_mode`: another boolean value that will be True in case the game is unable to access its assets directory
  - not being used right now, will be used when customisations are added
  - the idea is, if the game can't access its assets, the default image files embedded into the EXE file will be used


- `init_game_directory()`: this method is called that does the following:
  - makes a class variable called `settings_directory` which is a Path object
  - this class variable contains the path to the game's user data directory
    - For Windows, as discussed in the latest code snippet, `root_directory_for_windows` is used
    - For any other OS, `root_directory` is used as the root directory 
  - makes all the parent and subdirectories by using `Path.mkdir(parents=True, exist_ok=True)`, in case they don't exist

  
This is a summary of what happens when the `__init__` methods of both the classes `App` and `Backend` are called, when the game is started.
Now that the game has started, what happens next?

## 4.2 Running the game
Now that the game has started, each method will do its job in making the code alive and visible on the screen.

### 4.2.1 Summary
The 'Running the game' section will explain each method of both the classes in detail, in addition to the sequence by which the methods are called and what all happens.

Before I go into detail, here's an overview of how the game works:
- After starting the game:
  - the main menu is visible with 2 buttons: PLAY and EXIT
  - an infinitely scrolling background is visible
  - the bird/player icon is visible in the foreground, hovering mid air
  - the game is waiting for you to click any of the buttons
- When you click the EXIT button, the game closes
- In case of the PLAY button, you will now enter the Pre-Round stage
  - details about the pre-round stage have been discussed before
  - the game is now waiting for you to click anywhere in the screen to start playing the game
  - gravity is still disabled
- When you click anywhere or press spacebar, the game starts
  - gravity on the bird is enabled
  - obstacles start spawning and the bird seems to move towards the pillars
  - the obstacles are placed at random heights to make the game challenging
- During the gameplay round, 5 separate concurrent threads with different purposes are running:
  - background image(s) scrolling towards the left
  - pillars/obstacles moving towards the bird
  - bird being moved downwards due to gravity
  - off screen obstacles being shifted to the right repeatedly for an infinite obstacle gameplay
  - check whether the player has lost
- As soon as the player touches the ground or the pillars, round ends
  - main menu is visible again
  - This time, when you press the PLAY button:
    - the pillars currently on the canvas are shifted back to their default positions off screen to the right
    - the bird is shifted to its default position and now hovers mid air
    - current score gets reset to 0


This is pretty much it.