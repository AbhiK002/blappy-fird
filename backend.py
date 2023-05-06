from pathlib import Path
from tkinter import PhotoImage
import os
import platform
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Backend:
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

    def __init__(self):
        self.game_background_image = self.DEFAULT_BACKGROUND
        self.game_player_image = self.DEFAULT_BIRD
        self.game_pillar_up_image = self.DEFAULT_PILLAR_UP
        self.game_pillar_down_image = self.DEFAULT_PILLAR_DOWN

        self.play_button = self.PLAY_BUTTON
        self.exit_button = self.EXIT_BUTTON

        self.user_has_windows = True if "win" in platform.system().lower() else False

        self.classic_game_mode = False
        # in case the game directory can't be accessed, the game will not allow customisations

        self.init_game_directory()

        self.current_highscore_in_file = "0"
        self.highscore_file = self.settings_directory / "highscore.txt"
        self.create_highscore_file_if_not_exists()
        self.get_highscore_from_file()

    def init_game_directory(self):
        if self.user_has_windows:
            current_root_directory = self.root_directory_for_windows
        else:
            current_root_directory = self.root_directory

        self.settings_directory = current_root_directory / self.creator_root_directory / self.game_directory
        self.check_game_directory()

    def check_game_directory(self):
        try:
            self.settings_directory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.classic_game_mode = True

    def create_highscore_file_if_not_exists(self):
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
        self.create_highscore_file_if_not_exists()
        with open(self.highscore_file, "r") as file:
            content = file.read().strip()
            if not content.isdecimal():
                with open(self.highscore_file, "w") as file:
                    file.write("0")

            else:
                if int(content) >= 1500:
                    self.current_highscore_in_file = "GOD???"
                elif int(content) >= 100000:
                    self.current_highscore_in_file = "CHEATER"
                else:
                    self.current_highscore_in_file = content

    def update_highscore_in_file(self, score: int):
        if self.current_highscore_in_file in ("GOD???", "CHEATER"):
            return

        if score <= int(self.current_highscore_in_file):
            return

        self.check_game_directory()
        with open(self.highscore_file, "w") as file:
            file.write(str(score))

        self.current_highscore_in_file = str(score)

    def get_current_highscore(self):
        return self.current_highscore_in_file

    def get_current_bg_image(self):
        try:
            return PhotoImage(file=self.game_background_image)
        except Exception:
            print("bg image doesn't exist")
            return PhotoImage(file=self.DEFAULT_BACKGROUND)

    def get_current_player_image(self):
        try:
            return PhotoImage(file=self.game_player_image)
        except Exception:
            print("player image doesn't exist")
            return PhotoImage(file=self.DEFAULT_BIRD)

    def get_current_pillar_images(self) -> list[PhotoImage]:
        try:
            img1 = PhotoImage(file=self.game_pillar_up_image)
            img2 = PhotoImage(file=self.game_pillar_down_image)
            return [img1, img2]
        except Exception:
            print("buttons images don't exist")
            img1 = PhotoImage(file=self.DEFAULT_PILLAR_UP)
            img2 = PhotoImage(file=self.DEFAULT_PILLAR_DOWN)
            return [img1, img2]

    def get_buttons_images(self) -> list[PhotoImage] | None:
        try:
            img1 = PhotoImage(file=self.play_button)
            img2 = PhotoImage(file=self.exit_button)
            return [img1, img2]
        except Exception:
            print("buttons images don't exist")
            return None

