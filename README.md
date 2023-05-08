<p align='center'>
<img src='https://user-images.githubusercontent.com/68178267/236674506-59f01fa5-6f53-4667-936b-3f5cbad0499e.png' height=64>

<h1 align='center'> Blappy Fird </h1>
A remake by Abhineet Kelley of the classic game Flappy Bird, for a fun learning experience

# 1. Introduction
Welcome to Blappy Fird, a clone of the classic game 'Flappy Bird'. I made this game mostly for fun, but to also get an idea of how a project is carried out in the real world with documentation and other important stuff.
![image](https://user-images.githubusercontent.com/68178267/236674414-c7abc771-2f6e-491f-a28b-d344ee8dd150.png)


## 1.1 Download
To download Blappy Fird and play it, go to the latest [Releases tab here](https://github.com/AbhiK002/blappy-fird/releases/latest) and download the ZIP file.
Extract it and play the game by running the EXE file inside that extracted folder.  

- If you want to run the python file `main.py` directly, then you can install the Python programming language in your computer from [Python's official site](https://www.python.org/downloads/), download the repository as a ZIP file, extract the ZIP file and run `main.py` to play the game.
- You can also clone the repository by running this command in an empty folder:
```git
git clone https://github.com/AbhiK002/blappy-fird.git
```

# 2. About the Game
## 2.1 Rules
This game contains the classic gameplay of the original game, in addition to some things I added myself.
The rules are simple:
- Click or press SPACEBAR to make the bird hop
- The bird will automatically come down (because gravity)
- Hop through infinite obstacles to score 1 point
- If you touch the ground or any obstacle, you lose
- Reach the highest score you can

![image](https://user-images.githubusercontent.com/68178267/236674618-0292087a-0cae-4562-9926-7d9056d795f9.png)


### 2.1.1 Extra features
- None yet, will be added soon


# 3. Technical Details (for developers)
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

# 4. How Blappy Fird Works  (for developers)
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


That was a small insight into the logic of the game. Now, for the inside part I will explain the working of the code in 3 parts:
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
- `HELP`: path to the help image that shows how the user can play the game (right click/spacebar)
- `LOGO`: path to the logo image file of the game

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
- these variables that will store the currently used game assets are initialised:
  - `game_background_image`: initialised to `DEFAULT_BACKGROUND`
  - `game_player_image`: initialised to `DEFAULT_BIRD`
  - `game_pillar_up_image`: initialised to `DEFAULT_PILLAR_UP`
  - `game_pillar_down_image`: initialised to `DEFAULT_PILLAR_DOWN`
  - `game_play_button_image`: initialised to `PLAY_BUTTON`
  - `game_exit_button_image`: initialised to `EXIT_BUTTON`
  - `game_help_image`: initialised to `HELP`
  - `game_logo_image`: initialised to `LOGO`

- `user_has_windows`: self-explanatory boolean value, True if user has Windows OS
- `classic_game_mode`: another boolean value that will be True in case the game is unable to access its assets directory
  - not being used right now, will be used when customisations are added
  - the idea is, if the game can't access its assets, the default image files embedded into the EXE file will be used


- `init_game_directory()`: this method is called that stores the game's user data directory for use throughout the class
  
- to control and store the highscore:
  - `current_highscore_in_file` (String): when the game is initially started, the current highscore from the file is read and stored in this
  - `highscore_file` (Path object): stores the path to the file that contains the saved highscore
    - stored at `self.settings_directory / highscore.txt`
  - `create_highscore_file_if_not_exists()`: this method creates the highscore text file if it doesn't exist
  - `get_highscore_from_file()`: this method reads the highscore from the file and stores it into `current_highscore_in_file` class attribute
  
This is a summary of what happens when the `__init__` methods of both the classes `App` and `Backend` are called, when the game is started.
Now that the game has started, what happens next?

## 4.2 Running the game
Now that the game has started, each method will do its job in making the code alive and visible on the screen.

### 4.2.1 Summary
The 'Running the game' section will explain each method of both the classes in detail, in addition to the sequence by which the methods are called and what all happens.

Before I go into detail, here's an overview of how the game works:
- After starting the game:
  - the main menu is visible with 2 buttons: PLAY and EXIT, the logo of the game and the current highscore
  - an infinitely scrolling background is visible
  - the bird/player icon is visible in the foreground, hovering mid air
  - the game is waiting for you to click any of the buttons
- When you click the EXIT button, the game closes
- In case of the PLAY button, you will now enter the Pre-Round stage
  - the main menu is hidden and a help image is displayed, which shows you the controls of the game
  - the game is now waiting for you to click anywhere in the screen to start playing the game
  - the score resets to 0
  - the bird is in an idle animation, hovering up and down
  - gravity is still disabled
- When you click anywhere or press spacebar, the game starts
  - gravity on the bird is enabled
  - obstacles start spawning and the bird seems to move towards the pillars
  - the obstacles are placed at random heights to make the game challenging
- During the gameplay round, 5 separate concurrent threads with different purposes are running:
  - background image(s) scrolling towards the left
  - bird being moved downwards due to gravity
  - pillars/obstacles moving towards the bird
  - off screen pillar/obstacles being shifted accordingly to enable an infinite obstacle gameplay
  - keep checking whether the player has lost and increase score when the bird passes an obstacle without dying
  - bird's idle animation stops
- As soon as the player touches the ground or the pillars, round ends
  - main menu is visible again
  - This time, when you press the PLAY button:
    - the pillars currently on the canvas are shifted back to their default positions off screen to the right
    - the bird is shifted to its default position and now hovers mid air
    - current score gets reset to 0


This is pretty much it. Now going into the details, the next section will explain each method present in the game.


# 5. Detailed Code Documentation (for developers)
This section will list all the methods present in both the classes `App` and `Backend`, and explain what all they do.
## 5.1 `main.py`: class `App`
### 0. `__init__(self)`
  - has been explained in section 4.1.1

### 1. `store_currently_used_assets(self)`
  - calls the respective methods of the `Backend` class to get the `tk.PhotoImage` objects of the image paths defined in the `Backend` class
    - tkinter can only work with images via `tk.PhotoImage` instances
    - only then we can draw those images on the canvas
    - the methods of `Backend` class have been discussed in section 5.2
  - defines these class attributes, each of them storing `tk.PhotoImage` objects of all the currently used assets in the game:
    - `self.background_image`
    - `self.player_icon_image`
    - `self.pillar_up_image` and `self.pillar_down_image`
    - `self.help_image`
    - `self.logo_image`
  - these attributes will be useful in drawing the widgets on the canvas later on

### 2. `init_window(self)`
  - note: `self` is an instance of `App` class, which inherits from `tk.Tk` parent class, therefore making `self` an instance of `tk.Tk` as well. This means you can configure the main game window via `self` itself
  - this method configures the game window:
    - title set to "Blappy Fird"
    - resizable property set to False
    - title bar icon added
    - class attributes that will be used later are defined:
      - `self.game_window_width`: 600
      - `self.game_window_height`: 500
      - `self.canvas`: a `tk.Canvas` widget placed in the window
        - it is stretched to fit the entire window and is the only widget present in the window
        - all the images will be drawn inside the canvas itself
    - ensures the game window spawns in the center of the screen
      - done by getting the user's screen dimensions and configuring `self.geometry` accordingly

### 3. `init_background(self)`
  - 3 background images placed side to side are drawn onto the canvas
  - `self.canvas_bg_images` is set to a list of those 3 canvas images' tags
    - tags are basically unique integers assigned to all the drawn widgets on the canvas
    - these can be used to access the properties of any drawn canvas widget (text, image, shapes, etc)
    - `self.canvas.move(tag, x_increment, y_increment)` for example can be used to move a drawn widget by `x_increment` and `y_increment` pixels via its tag
  - `self.scroll_background()` method is called, explained below

### 4. `scroll_background(self)`
  - this is a recursive method running in its own separate thread (using tkinter's `self.after(milliseconds, function_obj)` method)
  - on each call, it iterates through the `self.canvas_bg_images` and moves each background image to the left by 2 pixels
  - calls the `self.shift_unseen_background()` method, explained below
  - runs every 50 milliseconds in a separate thread to not block the main thread events

### 5. `shift_unseen_background(self)`
  - this method checks if the first background image has gone out of view or not
    - since the image and the window have a 600 pixel width, it checks if the top left corner of the first image is less than -602
  - if it is, the image is shifted to the right side of the third image, basically by around (600*2) units, since that's the width of 2 images placed side to side
    - this shift is also done to the `self.canvas_bg_images` list so that it is in sync with the visual order of the images
    ```python
    imgs = [2, 3, 4]
    imgs.append(imgs.pop(0))
    print(imgs)  # [3, 4, 2]
    ```

### 6. `init_bird(self)`
  - draws the bird image onto the canvas at the location 200, 200
  - `self.bird_canvas_image`: the bird's canvas image tag is stored in this
  - defines the properties required for the gravity effect on the bird:
    - `self.bird_velocity = 0`: the current velocity of the bird (amount of pixels that the bird is moved everytime `self.make_bird_fall()` is called)
    - `self.terminal_velocity = 9.5`: maximum downwards velocity that the bird can reach
    - `self.gravity_acceleration = 0.6`: the amount of pixels `self.bird_velocity` increases by every `self.gravity_interval` amount of milliseconds
    - `self.gravity_interval = 15`: the amount of milliseconds after which the `self.make_brid_fall()` recursively calls itself (discussed later)
    - `self.bottom_death_limit = (self.game_window_height - 30)`: defines the coordinates of the false 'ground' in the bottom of the screen at which the bird should die if it reaches this
  - binds LEFT_CLICK and SPACEBAR to the `make_bird_hop()` (explained later) method, which is basically the jump the bird makes when the user clicks
  - defines some properties used by the `idle_bird_animation()` method
    - enables a continuous up and down motion when the round hasn't started. This is the bird's idle animation

### 7. `idle_bird_animation(self)`
  - a recursive method that runs in its own thread, running the idle animation of the bird when a round isn't going on
  - makes the bird move up or down by 1 pixel on every call and stores the pixels moved till now 
  - the way this animation works is, it keeps moving the bird up/down until it has been moved 30 pixels. Then it switches to the other direction and resets the pixel count to 0. Then counts till 30 again.
  - this recursion is stopped by making the `self.idle_interrupt` boolean `True` while the thread is running
  - runs every 20 milliseconds

### 8. `make_bird_fall(self)`
  - a recursive method that run its own thread while the boolean `self.gravity_enabled` is `True`
  - if `self.gravity_enabled` is set to `False`, the thread stops immediately
  - the logic of the gravity is pretty simple. when this function is called:
    - `self.bird_velocity` increases by `self.gravity_acceleration` amount of pixels
    - it is set to `self.terminal_velocity` in case it goes over the defined terminal velocity
    - moves `self.bird_canvas_image` (the drawn bird image) in the y-direction by `self.bird_velocity` pixels
    - calls itself after `self.gravity_interval` milliseconds in a separate thread using tkinter's `self.after(ms, func)` method
  - basically, just like the real world, every moment the bird falls down slightly more than the previous instant
    - at t=0ms, bird is at 200y, its velocity increases by 0.6 px
    - at t=15ms, bird will be at 200y + velocity = 200.6y, velocity increases by the same amount again and becomes 1.2px
    - at t=30ms, bird will be at 200.6y + velocity = 201.8y, velocity then becomes 1.2px + 0.6px = 1.8px
    - at t=45ms, bird will now be at 201.8y + velocity = 203.6y and so on...
  - runs every `self.gravity_interval` milliseconds

### 9. `make_bird_hop(self)`
  - this method is called whenever the user clicks on the screen or presses spacebar to make the bird jump/hop
  - the velocity is set to a fixed negative value -> -10.5
  - this means a constant upwards velocity is assigned to the bird, leading to a "jump" effect since the gravity is still active
  - if `self.main_menu_screen` is `True`, this function will not run, since the bird should not hop while the main menu is active

### 10. `init_mainmenu(self)`
  - this method draws the widgets present in the main menu and stores their tags in class attributes:
    - `self.play_button_canvas_image`: play button image
    - `self.exit_button_canvas_image`: exit button image
    - `self.highscore_canvas_label`: shows the current highscore on the main menu
    - `self.logo_canvas_image`: the logo of the game
  - calls `init_help()` method which draws the help image on the canvas, which will show up on the pre round screen
  - binds mouse LEFT_CLICK event to button images to run their respective methods `self.new_game()` and `self.exit_game()`

### 11. `hide_mainmenu(self)`
  - hides the drawn main-menu widgets which include:
    - the buttons, logo and the highscore label
  - this is done by using the `state` property of canvas widgets which can changed to `'hidden'` to hide them

### 12. `show_mainmenu(self)`
  - shows the hidden main-menu widgets
  - this is also done by using the `state` property of canvas widgets which can changed to `'normal'` to hide them
  - the widgets are also brought above all the background widgets to make them visible

### 13. `init_help(self)`
  - draws the help image on the canvas, which will only be displayed on the pre round screen
  - stores the image tag in `self.help_canvas_image` and makes it hidden by default
  - the help image indicates the user what can be used to play the game. In our case, left mouse click and spacebar

### 14. `show_help(self)`
  - changes the `state` property of `self.help_canvas_image` to `'normal'` to show the widget, which was previously hidden

### 15. `hide_help(self)`
  - hides the help image by changing the `state` property of `self.help_canvas_image` to `'hidden'` to hide the widget

### 16. `init_scoreboard(self)`
  - draws the text widget displaying the current score at the top of the window
  - stores its tag in `self.scoreboard`
  - it displays the current value of `self.current_score` variable, which is by default 0 on the opening of the game

### 17. `update_scoreboard(self)`
  - changes the text of `self.scoreboard` to the current value of `self.current_score`

### 18. `increment_score(self)`
  - increases the `self.current_score` by 1 and calls `self.update_scoreboard()`

### 19. `reset_score(self)`
  - sets `self.current_score` to 0 and calls `self.update_scoreboard()`

### 20. `init_pillars(self)`
  - defines some properties related to the obstacles/pillars:
    - `self.pillar_spawnpoint_x`: x coordinate of the first off-screen pillar in a new round
    - `self.pillar_distance`: distance between 2 pillars' top left corners
    - `self.pillar_height`: height of the pillar (also the image file's height)
    - `self.pillar_hole_gap`: height of the gap between the top and bottom edges of 2 pillars through which the bird will pass
    - `self.STANDARD_PILLAR_UP_Y`: the default y coordinate of the upper pillar, making the pillar hole gap lie exactly in the center of the game window
    - `self.STANDARD_PILLAR_DOWN_Y`: the default y coordinate of the lower pillar, making the pillar hole gap lie exactly in the center of the game window


  - 3 pairs of upper and lower pillars are spawned
    - these pairs are shifted to their positions by calling `self.reset_pillars_to_initial_position()`, discussed below
    - each pair of the pillars' tags are stored together in `self.canvas_pillar_images` as a tuple like `[(7,8), (9,10), (10,11)]`
    - note: `self.canvas_pillar_images` stores each pair of pillars as 1 element in the form of a tuple and I mentioned this again for no reason. Anyways.

### 21. `reset_pillars_to_initial_position(self)`
  - when a new round is about to start, this method resets the position of the pair of pillars to their initial positions
  - starting from the `self.pillar_spawnpoint_x` coordinate, these pairs are separated by `self.pillar_distance` pixels of distance
  - a random value from -100 to 100 in the factor of 10 (-100, -90, ... 90, 100) is added to their y-coordinate
    - this ensures randomness in the heights of hole gaps and makes the game challenging

### 22. `shift_unseen_pillar(self)`
  - similar to `shift_unseen_background()`
    - it shifts the first pillar to `self.pillar_spawnpoint_x` and randomises the height again
    - this gives an illusion of infinitely spawning pillars
  - the shift is also done to the `self.canvas_pillar_images` list where the first element is appended at the last
  - called by `self.keep_shifting_pillars()` whenever the first pillar goes off screen

### 23. `keep_moving_pillars(self)`
  - recursive method that runs in its own thread
  - if `self.main_menu_screen` is `True`, this function will not run, since the obstacles should not move while the main menu is active
  - when called, it moves all the pairs of pillars towards the left by 3 pixels
  - runs every 10 milliseconds

### 24. `keep_shifting_pillars(self)`
  - recursive method that runs in its own thread
  - if `self.main_menu_screen` is `True`, this function will not run, since the obstacles should not be shifted at all while the main menu is active
  - it checks whether the first pillar has gone off-screen or not
    - if it has, it calls `self.shift_unseen_pillar()` to shift the first pillar to the right end of the queue both visually and the `self.canvas_pillar_images` list, as explained before
  - this method basically keeps shifting the pillars as soon as the first pillar goes out of vision to give an illusion of infinitely spawning pillars
  - since it uses the same 3 pillars drawn at the start of the program, there is no need for the canvas to keep drawing and deleting pillar images
  - runs every 50 milliseconds

### 25. `lose_game(self)`
  - this method is called when the player loses due to collision of the bird with the ground, off screen pillar or the on screen pillar
  - `self.main_menu_screen` is set to `True`
  - these methods are called:
    - `self.disable_gravity()`: switch off gravity on the bird
    - `self.backend.update_highscore_in_file(self.current_score)`: update highscore in the highscore text file, if applicable
    - `self.show_mainmenu()`: shows main menu
  - the `self.scoreboard` canvas image is brought in front of all the other widgets
  - left click and spacebar events get disabled to disallow accidental bird hops

### 26. `new_game(self)`
  - called when the player presses the PLAY button the main menu
  - represents the Pre-Round stage of the game
  - `self.main_menu_screen` set to `False`
  - when the user starts the game, the scoreboard is initially hidden. this method makes it visible and the scoreboard then remains visible until the game is closed
  - these methods are called:
    - `self.reset_score()`: set the score to 0
    - `self.reset_pillars_to_initial_position()`: reset the obstacles for a new round
    - `self.show_help()`: shows the image widget indicating the controls of the game, since this is pre-round
    - `self.idle_bird_animation()`: starts the idle bird animation
  - the left click and spacebar events are binded to `self.start_game()`
    - `self.bird_canvas_image` which is the drawn bird image, is moved to its initial position (200, 200)

### 27. `start_game(self)`
  - this method is called when the user starts the round via mouse click or spacebar in the pre round stage
  - these methods are called:
    - `self.hide_help()`: the help image is hidden
    - `self.enable_gravity()`: switch on the gravity on the bird
    - `self.keep_moving_pillars()`: start moving the obstacles/pillars
    - `self.keep_shifting_pillars()`: start the infinite obstacle effect
    - `self.keep_checking_if_player_lost()`: a recursive method that will be discussed later, checks if the bird collided anywhere
    - `self.make_bird_hop()`: since the left click and space bar events aren't binded to the bird_hop function yet, the trigger won't make the bird jump. Therefore this function is called manually to give the initial jump to the bird.
  - left click and keyboard events are again binded to `self.make_bird_hop()`
  - `self.idle_interrupt` is set to `True` since the bird's idle animation is active during the pre round, which stops the `self.idle_bird_animation()` recursive thread

### 28. `exit_game(self)`
  - the scoreboard widget is deleted manually
    - this has been done to avoid a weird tkinter `alloc` error
  - the game window is destroyed after 800 milliseconds

### 29. `check_pillar_for_score(self)`
  - checks if the bird has crossed a pillar
  - if it has, it will now check whether the bird is currently flying higher than the game window
    - if it is flying higher, this means the bird should collide with the offscreen upper pillar
      - therefore it returns `True` (this will be used in `self.keep_checking_if_player_lost()`, discussed below)
    - else, call `self.increment_scoreboard()` to increase the score

### 30. `keep_checking_if_player_lost(self)`
  - this is a recursive method that runs in its own thread
  - it has two purposes:
    - check if player lost
    - increase score if player passed a pillar
  - it first calls `self.check_pillar_for_score()` and keeps track of its return value in a local variable
    - if it returns `True` this means the player collided with an off screen pillar
    - therefore, `self.lose_game()` is called and the thread ends here
    - otherwise, nothing happens
  - next, to see if the bird collided with any pillar, a method `find_overlapping(*args)` of class `tk.Canvas` is utilised
    - the coordinates of the top-left corner (x1, y1) and the bottom-right corner (x2, y2) of the rectangle surrounding the `self.bird_canvas_image` are stored
    - using these coordinates, the coordinates of 2 smaller rectangles that cover the bird's visual body and beak are derived, for accurate deaths due to collision. This is done so that the bird doesn't die due to invisible collisions (where the bird doesn't touch the obstacle visually, but its rectangle does)
      ```python
      x1, y1, x2, y2 = self.canvas.bbox(self.bird_canvas_image)  # main rectangle containing the entire bird image
      rectangle_of_body = (x1+7, y1, x2-16, y2-1)  # 32x42 rectangle
      rectangle_of_beak = (x1+7+32, y1+18, x2, y2-1)  # 16x24 rectangle
      ```
      (ADD AN IMAGE HERE)
    - the `tk.Canvas.find_overlapping(*args)` method returns a list of all the tags of the widgets that are currently coinciding with the passed rectangle coordinates (in this case, the rectangles we made)
    - in our case, the background images are always overlapping with the bird visually, so they should be ignored
    - the way I implemented this is:
      - if the sum of the tags (which are unique integers) is greater than 10, this implies the bird collided with any of the pillars, therefore `self.lose_game()` is called and the thread ends here
      - otherwise, the bird is safe
    - the reason this works is that firstly, I noticed that the tags of the background images are always 2, 3 and 4 and the pillars go from 7 to 12.
      - when the bird isn't colliding with the pillars, the possible list values returned by the `find_overlapping()` function are like:
        - `[1, 2], [1, 3], [1, 4]` or sometimes rarely `[1, 2, 3], [1, 3, 4], [1, 4, 2]`
        - notice, the sums of all these lists is always less than 10
        - since the pillars' tags go from 7 to 12, if any one of them gets added to the returned list, the sum always exceeds 10


  - this method runs every 10 milliseconds. Due to its superfast interval, I had to find a way which won't take up too much time or processing to see whether the bird collided with any pillars. This is why I adopted the easy `sum(tags_list) > 10` approach. Quick and efficient.

### 31. `disable_gravity(self)`
  - `self.gravity_enabled` is set to `False`
  - this automatically stops the `self.make_bird_fall()` recursive thread if it's running currently

### 32. `enable_gravity(self)`
  - `self.gravity_enabled` is set to `True`
  - `self.make_bird_fall()` is called, which starts a new thread controlling the bird's gravity

## 5.2 `backend.py`: class `Backend`
Before we discuss the methods of the `Backend` class, there's a global function defined before that:

- `resource_path(relative_path)`:
  - this function returns the absolute path from a given relative path of a file/folder
  - however, here it has been defined to facilitate embedding asset files into the bundled EXE file made using `pyinstaller` module
  - this is a workaround for `pyinstaller` to easily find asset files while bundling the EXE file

Now, we discuss each method of class `Backend`
### 0. `__init__(self)`
  - discussed before in section 4.1.2

### 1. `init_game_directory(self)`
  - `self.settings_directory` which is a Path object is defined
  - this class variable contains the path to the game's user data directory
    - For Windows, as discussed in the latest code snippet, `self.root_directory_for_windows` is used
    - For any other OS, `self.root_directory` is used as the root directory 
  - makes all the parent and subdirectories by using `Path.mkdir(parents=True, exist_ok=True)`, in case they don't exist

### 2. `check_game_directory(self)`
  - creates the game's user data directory stored in `self.settings_directory` incase it doesn't exist
    - also creates all the parent folders if required
  - in case of some error, `self.classic_game_mode` is set to `True`
    - this does not have a purpose yet

### 3. `create_highscore_file_if_not_exists(self)`
  - calls `self.check_game_directory()` to ensure parent folders exist
  - makes an empty text file at path `self.highscore_file` in case it doesn't exist
  - if there's a folder with the same name (highscores.txt), that folder is renamed to "rename this to something else" and the highscores.txt text file is created

### 4. `get_highscore_from_file(self)`
  - calls `self.create_highscore_file_if_not_exists()`
  - reads the file `self.highscore_file` and stores its contents altogether as a string in a local variable `content`, stripped of any whitespace characters leaving just the main text of the file
    - if the `content` string doesn't only contain numbers, the score is invalid and therefore "0" is written into the file
    - in case it does contain only numbers,
      - `content` is converted into an integer by using `int(content)`
      - if that integer is above 1500, the player is a God apparently and has spent a lot of time on the game (or changed the text file manually)
        - `self.current_highscore_in_file` is set to `"GOD???"`
      - if it is above 100000, the player is a Cheater.
        - `self.current_highscore_in_file` is set to `"CHEATER"`
      - these string values will be displayed to the user in the GUI later on >:)
      - else, `self.current_highscore_in_file` is set to the integer itself which was the high score of the player last time they played Blappy Fird

### 5. `update_highscore_in_file(self, score: int)`
  - if `self.current_highscore_in_file` is set to the God or Cheater string values, stop the function here
  - if the given argument `score` is less than or equal to the integer value of `self.current_highscore_in_file`, that means the player hasn't beaten the current highscore. the function stops here
  - otherwise, the `self.check_game_directory()` is called and the `score` is written into the file
    - implying the player beat their highscore
  - `self.current_highscore_in_file` is set to the string form of `score`

### 6. `get_current_highscore(self)`
  - returns the string `self.current_highscore_in_file`
  - this string will be displayed in the GUI of the game in the `self.highscore_canvas_label` if you remember.

### 7. `get_current_bg_image(self)`
  - returns the `PhotoImage` object of `self.game_background_image`
  - in case of an error, returns the `PhotoImage` object of `self.DEFAULT_BACKGROUND`
  - tkinter only works with images by using the `PhotoImage` class. This is why we need to pass our image paths as these objects so they can be drawn on the canvas in the GUI.

### 8. `get_current_player_image(self)`
  - returns the `PhotoImage` object of `self.game_player_image`
  - in case of an error, returns the `PhotoImage` object of `self.DEFAULT_BIRD`

### 9. `get_current_pillar_images(self)`
  - returns the `PhotoImage` objects of `self.game_pillar_up_image` and `self.game_pillar_down_image` as a list
  - in case of an error, returns the `PhotoImage` objects of `self.DEFAULT_PILLAR_UP` and `self.DEFAULT_PILLAR_DOWN`

### 10. `get_buttons_images(self)`
  - returns the `PhotoImage` objects of `self.game_play_button_image` and `self.game_exit_button_image` as a list
  - in case of an error, returns  the `PhotoImage` objects of `self.PLAY_BUTTON` and `self.EXIT_BUTTON`

### 11. `get_logo_image(self)`
  - returns the `PhotoImage` object of `self.game_logo_image`
  - in case of an error, returns the `PhotoImage` object of `self.LOGO`

### 12. `get_help_image(self)`
  - returns the `PhotoImage` object of `self.game_help_image`
  - in case of an error, returns the `PhotoImage` object of `self.HELP`

# 6. Conclusion
I hope you understood this game's working and the source code behind this from this documentation. I've never written documentation for any project before, so this might not have been the beset document you've read today. But it was really fun writing all this.

I hope you enjoy this weird clone of Flappy Bird. I will maybe add extra stuff in the future like themes, etc.

See you in the next project!

Blappy Fird made by Abhineet Kelley, 2023
