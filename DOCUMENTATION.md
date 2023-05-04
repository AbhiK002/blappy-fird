# Blappy Fird
A remake by Abhineet Kelley, just for a fun learning experience

# Introduction
(I've never written documentation for a project before, so this might not be the best document you read today, for that I apologise in advance :P)

Welcome to Blappy Fird, a remake of the classic game 'Flappy Bird' with a few more features like customisable backgrounds, etc. I made this game mostly for fun, but to also get an idea of how a professional project is carried out in real life with documentation and everything.

# About the Game
## Rules
This game contains the classic gameplay of the original game, in addition to some things I added myself.
The rules are simple:
- Click or press SPACEBAR to make the bird go up
- The bird will automatically come down (because gravity)
- Hop through the obstacles without touching them to score 1 point
- If you touch the ground or any obstacle, you lose
- Reach the highest score you can

### Extra features
- None yet, will definitely be added

# Technical Stuff
Blappy Fird has been made using the Python language and tkinter has been used for the GUI of the game. I used tkinter because the game doesn't have advanced graphics that require complex frameworks like PyQt5.

## Libraries/Modules Used
- `tkinter`: To literally make the entire GUI of the game
- `pathlib`: Making cross platform folder/file paths since OSes have different path representations (/ or \)
- `os`:  Making a function `resource_path(relative_path)` that'll help us embed assets into the exe file made using `pyinstaller` 
- `sys`: Same usage as `os`
- `platform`: To check the user's operating system

## Game Directory Structure
- For Windows, the game's user data, which is stuff like settings, etc is located at:
  - `C:\Users\<user>\AppData\Local\AbhineetKelley\BlappyFird\`
which is equivalent to
  - `%localappdata%\AbhineetKelley\BlappyFird\`


- For other operating systems (Linux, MacOS):
  - `~/AbhineetKelley/BlappyFird/`  
    where `~` represents the OS's respective home directory

### Code Structure
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

# How Blappy Fird Works
Blappy Fird is a fun little game and therefore has a simple working mechanism. I'll explain it in 2 parts: before the game starts and after the game starts.

## Starting the game
### Inside main.py
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

Okay 1 small reason, writing `self.geometry` is easier than `self.root.geometry` since I don't have to type root again and again. But that's not exactly the reason. Anyways moving on, the `__init__` method of App is called.

Here are the things that happen inside the `__init__` method of `App` class:
- the `__init__` method of class `tk.Tk` is called


- a boolean `bird_paused` is initialised to `False`
  - this controls whether the bird is currently under the effect of gravity or not
  - will be set to `True` if the user pauses the game, since that won't end the game, only keep the bird frozen in place


- an instance of class `Backend` is stored in `self.backend` to be used throughout the `App` class
  - this class is present in the `backend.py` file and will be talked about soon  
  

- these methods are called:
  - `init_window()`: configure the game window (dimensions, coordinates on the screen, resizable properties, etc)
  - `update_used_assets()`: fetches the currently used image assets from the `Backend` class via `self.backend` instance
    - stuff like the currently selected background image, player icon image and pillar image (which are the classic ones by default, will be talked about later)
  - `self.background_images`: a list containing the reference to images in the game's background
    - it always contains 3 images that have been placed side to side on a `tk.Canvas` widget
    - these 3 images are then moved from right to left
    - when the first image is out of view, it is shifted to the right side of the previously third image
    - the same happens to the list... `list.append(list.pop(0))`
    - this is how an infinitely scrolling background is achieved
  - `scroll_background()`: starts animating the background to an infinite scroll
  - `init_bird()`
  - `mainloop()`: start displaying the `tkinter.Tk` window


### Inside backend.py
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
#### Prepatory Stuff
Inside the `Backend` class definition, these class attributes are defined:
- `root_directory` (Path object): contains the path to the home directory of the user
  - something like `C:\Users\YOURNAME\` in Windows
  - for Linux it's `/home/YOURNAME/`
  - This attribute contains the root directory for the game's user data directory that was talked about earlier (Game Directory Structure)


- `root_directory_for_windows` (Path object): as the name suggests, for Windows machines, the user data directory is in `%HOME%\AppData\Local\`
  - here `%HOME%` represents the home directory
- `creator_root_directory` (String): the parent directory named after me, which will contain the main game directory
- `game_directory` (String): the game directory that will contain the settings files
```python
from pathlib import Path

root_directory = Path.home()
creator_root_directory = "AbhineetKelley"
game_directory = "BlappyFird"

final_path =  root_directory / creator_root_directory / game_directory
# this is a neat little feature of pathlib
# it generates cross-platform paths 
# according to the OS the file is being run in

print(final_path)
```
For Windows,
```python
Path("C:\\User\\YOURNAME\\AppData\\Local\\AbhineetKelley\\BlappyFird")
```
For Linux,
```python
Path("/home/YOURNAME/AbhineetKelley/BlappyFird")
```

- `DEFAULT_BACKGROUND`: path to the default sky background image file
- `DEFAULT_BIRD`: path to the default yellow bird image file
- `DEFAULT_PILLARS`: path to the default green pillars image file

#### Normal Stuff
These things in particular happen inside the `__init__` method of `Backend` class:
- three variables that will store the currently used game assets are initialised:
  - `game_background_image`: by default initialised to `DEFAULT_BACKGROUND` class attribute
  - `game_player_image`: by default initialised to `DEFAULT_BIRD`
  - `game_pillar_image`: by default initialised to `DEFAULT_PILLARS`


- `user_has_windows` defined: self-explanatory boolean value, True if user has Windows OS
- `classic_game_mode` defined: another boolean value that will be True in case the game is unable to access its assets directory
  - not being used right now, will be used when customisations are added


- `init_game_directory()`: this method is called that:
  - makes a class variable called `settings_directory` that uses the respective root directory depending upon the value of `user_has_windows` boolean.
  - this class variable stores the path to the user data directory discussed earlier
  - makes all the parent and sub directories, in case they don't exist

  
This is a summary of what happens when the `__init__` methods of both the classes `App` and `Backend` are called. Now I will explain each method of both the classes in some detail.
