# Blappy Fird
A remake by Abhineet Kelley, just for a fun learning experience

## Introduction
(I've never written documentation for a project before, so this might not be the best document you read today, for that I apologise in advance :P)

Welcome to Blappy Fird, a remake of the classic game 'Flappy Bird' with a few more features like customisable backgrounds, etc. I made this game mostly for fun, but to also get an idea of how a professional project is carried out in real life with documentation and everything.

## About the Game
### Rules
This game contains the classic gameplay of the original game, in addition to some things I added myself.
The rules are simple:
- Click or press SPACEBAR to make the bird go up
- The bird will automatically come down (because gravity)
- Hop through the obstacles without touching them to score 1 point
- If you touch the ground or any obstacle, you lose
- Reach the highest score you can

### Extra features
- None yet, will definitely be added

## Technical Stuff
Blappy Fird has been made using the Python language and tkinter has been used for the GUI of the game. I used tkinter because the game doesn't have advanced graphics that require complex frameworks like PyQt5.

### Game Directory
- For Windows, the game's assets are located at:
  - `C:\Users\<user>\AppData\Local\AbhineetKelley\BlappyFird\`
which is equivalent to
  - `%localappdata%\AbhineetKelley\BlappyFird\`


- For other operating systems (Linux, MacOS):
  - `~/AbhineetKelley/BlappyFird/`  
    where `~` represents the OS's respective home directory


This directory contains the background, player icon and pillars image files in 3 separate folders named:
- `bg`
- `birds`
- `pillars`

### 