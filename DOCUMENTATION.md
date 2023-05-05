# Blappy Fird
A remake by Abhineet Kelley, just for a fun learning experience

# Introduction
(I've never written documentation for a project before, so this might not be the best document you read today, and for that I apologise in advance :P)

Welcome to Blappy Fird, a remake of the classic game 'Flappy Bird' with a few more features like customisable backgrounds, etc. I made this game mostly for fun, but to also get an idea of how a professional project is carried out in real life with documentation and everything.

# About the Game
## Rules
This game contains the classic gameplay of the original game, in addition to some things I added myself.
The rules are simple:
- Click or press SPACEBAR to make the bird hop
- The bird will automatically come down (because gravity)
- Hop through the obstacles without touching them to score 1 point
- If you touch the ground or any obstacle, you lose
- Reach the highest score you can

### Extra features
- None yet, will be added soon

# Technical Stuff
Blappy Fird has been made using the Python language and tkinter has been used for the GUI of the game. I used tkinter because the game doesn't have advanced graphics or mechanisms that require complex frameworks like PyQt5.

## Libraries/Modules Used
- `tkinter`: To make the GUI of the game
- `pathlib`: Generating cross-platform folder/file paths since different operating systems have different path representations (`/` or `\\`)
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
- the `__init__` method of parent class `tk.Tk` is called


- a boolean `bird_paused` is initialised to `False`
  - this controls whether the bird is currently under the effect of gravity or not
  - will be set to `True` if the user pauses the game, since that won't end the game, only keep the bird frozen in place


- an instance of class `Backend` is stored in `self.backend` to be used throughout the `App` class
  - this class is present in the `backend.py` file and will be talked about soon  


- `self.background_images`: a list is initialised to `[]` that will contain the reference to images in the game's background
    - it always contains 3 images that have been placed side to side on a `tk.Canvas` widget
    - these 3 images are then moved from right to left
    - when the first image is out of view, it is shifted to the right side of the previously third image
    - the same happens to the list... `list.append(list.pop(0))`
    - this is how an infinitely scrolling background is achieved
  

- these methods are called:
  - `init_window()`: configure the game window (dimensions, coordinates on the screen, resizable properties, etc)
  - `update_used_assets()`: fetches the currently used image assets from the `Backend` class via `self.backend` instance
    - stuff like the currently selected background image, player icon image and pillar image (which are the classic ones by default, will be talked about later)
    - these are stored in 3 class variables to be used by the GUI code
  - `scroll_background()`: starts animating the background to give the effect of an infinite scroll
  - `init_bird()`: displays the player icon (which is by default a yellow bird) in the game
    - this method also defines the acceleration due to gravity on the bird
    - the `LEFT_MOUSE_CLICK` event, which is `<Button-1>` in tkinter, is binded to a function `make_bird_jump()` that will make the bird hop whenever the user clicks their mouse inside the window
  - `mainloop()`: start displaying the main `tk.Tk` game window


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

 
- `DEFAULT_BACKGROUND`: path to the default sky background image file
- `DEFAULT_BIRD`: path to the default yellow bird image file
- `DEFAULT_PILLARS`: path to the default green pillars image file


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


#### Normal Stuff
These things in particular happen inside the `__init__` method of `Backend` class:
- three variables that will store the currently used game assets are initialised:
  - `game_background_image`: initialised to `Backend.DEFAULT_BACKGROUND`
  - `game_player_image`: initialised to `Backend.DEFAULT_BIRD`
  - `game_pillar_image`: initialised to `Backend.DEFAULT_PILLARS`


- `user_has_windows`: self-explanatory boolean value, True if user has Windows OS
- `classic_game_mode`: another boolean value that will be True in case the game is unable to access its assets directory
  - not being used right now, will be used when customisations are added
  - the idea is, if the game can't access its assets, the default image files embedded into the EXE file will be used


- `init_game_directory()`: this method is called that does the following:
  - makes a class variable called `settings_directory` which is a Path object
  - this class variable contains the path to the game's user data directory
    - For Windows, as discussed in the latest code snippet, `Backend.root_directory_for_windows` is used
    - For any other OS, `Backend.root_directory` is used as the root directory 
  - makes all the parent and subdirectories by using `Path.mkdir(parents=True, exist_ok=True)`, in case they don't exist

  
This is a summary of what happens when the `__init__` methods of both the classes `App` and `Backend` are called, when the game is started.
Now that the game has started, what happens next?

## Running the game
Now that the game has started, each method will do its job in making the code alive and visible on the screen.

### Summary
The 'Running the game' section will explain each method of both the classes in detail, in addition to the sequence by which the methods are called and what all happens.

Before I go into detail, here's an overview of how the game works:
- After starting the game:
  - the game window is visible in the main thread
  - an infinitely scrolling background is being animated in a separate thread
  - the bird/player icon is visible in the foreground, hanging mid air
  - the game is waiting for the user to click or press spacebar


- When you click/press spacebar, a function `make_bird_hop()` that is binded to those events makes the bird hop, the boolean `bird_paused` is set to `False` and the game starts
- Gravity starts acting on the bird instantly via a function `make_bird_fall()` that animates the bird going down, which is called repeatedly every few milliseconds in a separate thread
- Everytime you click/press spacebar, the function `make_bird_hop()` is called
- if the bird touches the ground, the function `make_bird_fall()` detects that and sets `bird_paused` to `True`, freezing the bird in place so it doesn't go all the way down
- the thread running `make_bird_fall()` repeatedly is then stopped by the function itself since `bird_paused` becomes `True`
