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
    # DEFAULT_PILLARS = resource_path()

    PLAY_BUTTON = resource_path(assets_directory / "play.png")
    EXIT_BUTTON = resource_path(assets_directory / "exit.png")

    def __init__(self):
        self.game_background_image = self.DEFAULT_BACKGROUND
        self.game_player_image = self.DEFAULT_BIRD
        self.game_pillar_image = None

        self.play_button = self.PLAY_BUTTON
        self.exit_button = self.EXIT_BUTTON

        self.user_has_windows = True if "win" in platform.system().lower() else False

        self.classic_game_mode = False
        # in case the game directory can't be accessed, the game will not allow customisations

        self.init_game_directory()

    def init_game_directory(self):
        if self.user_has_windows:
            current_root_directory = self.root_directory_for_windows
        else:
            current_root_directory = self.root_directory

        self.settings_directory = current_root_directory / self.creator_root_directory / self.game_directory
        try:
            self.settings_directory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.classic_game_mode = True

    def get_current_bg_image(self):
        try:
            img = PhotoImage(file=self.game_background_image)
            return img
        except Exception:
            print("bg image doesn't exist")
            return PhotoImage(file=self.DEFAULT_BACKGROUND)

    def get_current_player_image(self):
        try:
            img = PhotoImage(file=self.game_player_image)
            return img
        except Exception:
            print("player image doesn't exist")
            return PhotoImage(file=self.DEFAULT_BIRD)

    def get_buttons_images(self) -> list[PhotoImage] | None:
        try:
            img1 = PhotoImage(file=self.play_button)
            img2 = PhotoImage(file=self.exit_button)
            return [img1, img2]
        except Exception:
            print("buttons images don't exist")
            return None

