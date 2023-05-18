from pathlib import Path
from tkinter import PhotoImage
import os
import platform
import sys


def resource_path(relative_path: Path):
    """
- This function returns the absolute path from a given relative path of a file/folder
- However, here it has been defined to facilitate embedding asset files into the bundled EXE file made using `pyinstaller` module
- This is a workaround for `pyinstaller` to easily find asset files while bundling the EXE file

    :param relative_path:
    :return absolute_path:
    """

    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Backend:
    """
    This class handles the behind-the-scenes functioning of the game
    Blappy Fird, that includes stuff like reading and creating the
    game's user data directories, returning tkinter.PhotoImage objects
    of the assets used in the game, etc.
    """
    root_directory = Path.home()
    root_directory_for_windows = Path.home() / "AppData" / "Local"

    creator_root_directory = "AbhineetKelley"
    game_directory = "BlappyFird"
    assets_directory = Path("assets")

    DEFAULT_BACKGROUND = resource_path(assets_directory / "bg" / "1_skybg.png")
    DEFAULT_BIRD = resource_path(assets_directory / "birds" / "1_bird.png")
    DEFAULT_PILLAR_UP = resource_path(assets_directory / "pillars" / "1_pillar_up.png")
    DEFAULT_PILLAR_DOWN = resource_path(assets_directory / "pillars" / "1_pillar_down.png")

    PLAY_BUTTON = resource_path(assets_directory / "play.png")
    EXIT_BUTTON = resource_path(assets_directory / "exit.png")
    HELP = resource_path(assets_directory / "help.png")
    LOGO = resource_path(assets_directory / "logo.png")

    def __init__(self):
        self.game_background_image = self.DEFAULT_BACKGROUND
        self.game_player_image = self.DEFAULT_BIRD
        self.game_pillar_up_image = self.DEFAULT_PILLAR_UP
        self.game_pillar_down_image = self.DEFAULT_PILLAR_DOWN

        self.game_play_button_image = self.PLAY_BUTTON
        self.game_exit_button_image = self.EXIT_BUTTON
        self.game_help_image = self.HELP
        self.game_logo_image = self.LOGO

        self.user_has_windows = True if "win" in platform.system().lower() else False

        self.classic_game_mode = False
        # in case the game directory can't be accessed, the game will not allow customisations

        self.init_game_directory()

        self.current_highscore_in_file = "0"
        self.highscore_file = self.settings_directory / "highscore.txt"
        self.create_highscore_file_if_not_exists()
        self.get_highscore_from_file()

    def init_game_directory(self):
        """
- `self.settings_directory` which is a Path object is defined

This class variable contains the path to the game's user data directory
    - For Windows, the class attribute `self.root_directory_for_windows` is used
    - For any other OS, `self.root_directory` is used as the root directory

- Makes all the parent and subdirectories by using
  `Path.mkdir(parents=True, exist_ok=True)`, in case they don't exist
        """
        if self.user_has_windows:
            current_root_directory = self.root_directory_for_windows
        else:
            current_root_directory = self.root_directory

        self.settings_directory = current_root_directory / self.creator_root_directory / self.game_directory
        self.check_game_directory()

    def check_game_directory(self):
        """
Creates the game's user data directory stored in `self.settings_directory`
incase it doesn't exist
    - also creates all the parent folders if required

In case of some error, `self.classic_game_mode` is set to `True`
    - this does not have a purpose yet
        """
        try:
            self.settings_directory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.classic_game_mode = True

    def create_highscore_file_if_not_exists(self):
        """
- Calls `self.check_game_directory()` to ensure parent folders exist
- Makes an empty text file at path `self.highscore_file` in case it doesn't exist
- If there's a folder with the same name (highscores.txt), that folder is
  renamed to "rename this to something else" and the highscores.txt text
  file is created
        """
        self.check_game_directory()
        self.highscore_file.touch(exist_ok=True)
        if not self.highscore_file.is_file():
            try:
                self.highscore_file.rename(self.settings_directory / "rename this to something else")
                self.create_highscore_file_if_not_exists()
            except:
                Path(self.settings_directory / "DELETE highscores.txt NOW").mkdir(parents=True, exist_ok=True)
                sys.exit(0)

    def get_highscore_from_file(self):
        """
Calls `self.create_highscore_file_if_not_exists()`
      Reads the file `self.highscore_file` and stores its contents
      altogether as a string in a local variable `content`,
      stripped of any whitespace characters leaving just the main
      text of the file
            - if the `content` string doesn't only contain numbers,
              the score is invalid and therefore "0" is written into the file
            - in case it does contain only numbers, `content` is
              converted into an integer by using `int(content)`
      - If the score integer is above 5000, the player is most probably a Cheater,
        most probably. Therefore, `self.current_highscore_in_file` is set to `"CHEATER"`
      - these string values will be displayed to the user in the GUI later on >:)
      - else, `self.current_highscore_in_file` is set to the integer itself which
        was the high score of the player last time they played Blappy Fird
        """
        self.create_highscore_file_if_not_exists()
        with open(self.highscore_file, "r") as file:
            content = file.read().strip()
            if not content.isdecimal():
                with open(self.highscore_file, "w") as file:
                    file.write("0")

            else:
                if int(content) >= 5000:
                    self.current_highscore_in_file = "CHEATER"
                else:
                    self.current_highscore_in_file = content

    def update_highscore_in_file(self, score: int):
        """
- If `self.current_highscore_in_file` is set to the God or Cheater string values, stop the function here
- If the given argument `score` is less than or equal to the integer value of `self.current_highscore_in_file`, that means the player hasn't beaten the current highscore. the function stops here
- Otherwise, the `self.check_game_directory()` is called and the `score` is written into the file, implying the player beat their highscore
- `self.current_highscore_in_file` is set to the string form of `score`


        :param score:
        """
        if self.current_highscore_in_file in ("GOD???", "CHEATER"):
            return

        if score <= int(self.current_highscore_in_file):
            return

        self.check_game_directory()
        with open(self.highscore_file, "w") as file:
            file.write(str(score))

        self.current_highscore_in_file = str(score)

    def get_current_highscore(self):
        """
- Returns the string `self.current_highscore_in_file`
- This string will be displayed in the GUI of the game in the `self.highscore_canvas_label` of class `App` in `main.py`.
        """
        return self.current_highscore_in_file

    def get_current_bg_image(self):
        """
- returns the `PhotoImage` object of `self.game_background_image`
- in case of an error, returns the `PhotoImage` object of `self.DEFAULT_BACKGROUND`
- tkinter only works with images by using the `PhotoImage` class.
  This is why we need to pass our image paths as these objects
  so they can be drawn on the canvas in the GUI.
        """
        try:
            return PhotoImage(file=self.game_background_image)
        except Exception:
            print("bg image doesn't exist")
            return PhotoImage(file=self.DEFAULT_BACKGROUND)

    def get_current_player_image(self):
        """
- returns the `PhotoImage` object of `self.game_player_image`
- in case of an error, returns the `PhotoImage` object of `self.DEFAULT_BIRD`
        """
        try:
            return PhotoImage(file=self.game_player_image)
        except Exception:
            print("player image doesn't exist")
            return PhotoImage(file=self.DEFAULT_BIRD)

    def get_current_pillar_images(self) -> list[PhotoImage]:
        """
- returns the `PhotoImage` objects of `self.game_pillar_up_image` and `self.game_pillar_down_image` as a list
- in case of an error, returns the `PhotoImage` objects of `self.DEFAULT_PILLAR_UP` and `self.DEFAULT_PILLAR_DOWN`
        """
        try:
            img1 = PhotoImage(file=self.game_pillar_up_image)
            img2 = PhotoImage(file=self.game_pillar_down_image)
            return [img1, img2]
        except Exception:
            print("buttons images don't exist")
            img1 = PhotoImage(file=self.DEFAULT_PILLAR_UP)
            img2 = PhotoImage(file=self.DEFAULT_PILLAR_DOWN)
            return [img1, img2]

    def get_buttons_images(self) -> tuple[PhotoImage, PhotoImage]:
        """
- returns the `PhotoImage` objects of `self.game_play_button_image` and `self.game_exit_button_image` as a list
- in case of an error, returns  the `PhotoImage` objects of `self.PLAY_BUTTON` and `self.EXIT_BUTTON`
        """
        try:
            img1 = PhotoImage(file=self.game_play_button_image)
            img2 = PhotoImage(file=self.game_exit_button_image)
        except Exception:
            print("buttons images don't exist")
            img1 = PhotoImage(file=self.PLAY_BUTTON)
            img2 = PhotoImage(file=self.EXIT_BUTTON)
        return img1, img2

    def get_logo_image(self):
        """
- returns the `PhotoImage` object of `self.game_logo_image`
- in case of an error, returns the `PhotoImage` object of `self.LOGO`
        """
        try:
            return PhotoImage(file=self.game_logo_image)
        except:
            return PhotoImage(file=self.LOGO)

    def get_help_image(self):
        """
- returns the `PhotoImage` object of `self.game_help_image`
- in case of an error, returns the `PhotoImage` object of `self.HELP`
        """
        try:
            return PhotoImage(file=self.game_help_image)
        except:
            return PhotoImage(file=self.HELP)
