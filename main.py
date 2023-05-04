import tkinter as tk
from backend import Backend


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.backend = Backend()
        self.init_window()

        self.background_images : list[tk.Label] = []
        self.bg_img = self.backend.get_current_bg_image()
        self.bird_img = self.backend.get_current_player_image()
        # self.pillar_img = self.backend

        self.init_background()
        self.scroll_background()
        self.mainloop()

    def init_window(self):
        self.title("Flappy Bird")
        # self.resizable(False, False)

        self.user_screen_width = self.winfo_screenwidth()
        self.user_screen_height = self.winfo_screenheight()

        self.game_window_width = 600
        self.game_window_height = 500

        pos_y = int((self.user_screen_width - self.game_window_width)/2)
        pos_x = int((self.user_screen_height - self.game_window_height)/2)

        self.geometry(f"{self.game_window_width}x{self.game_window_height}+{pos_y}+{pos_x}")

    def init_background(self):
        bg_label = tk.Label(self, image=self.bg_img, borderwidth=0)
        bg_label.image = self.bg_img
        bg_label.place(x=-400, y=0)

        bg_label2 = tk.Label(self, image=self.bg_img, borderwidth=0)
        bg_label2.image = self.bg_img
        bg_label2.place(x=200, y=0)

        self.background_images.append(bg_label)
        self.background_images.append(bg_label2)
        self.update()

    def add_background(self):
        x_pos_of_last_bg_img = self.background_images[-1].winfo_x()

        if x_pos_of_last_bg_img < int(0.6*self.game_window_width):
            print("added")
            bg_label = tk.Label(self, image=self.bg_img, borderwidth=0)
            bg_label.image = self.bg_img

            new_coords = x_pos_of_last_bg_img + self.game_window_width - 5
            bg_label.place(x=new_coords, y=0)
            self.background_images.append(bg_label)

    def remove_unseen_background(self):
        x_pos_of_first_bg_img = self.background_images[0].winfo_x()

        if x_pos_of_first_bg_img < -self.game_window_width-2:
            print("removed")
            self.background_images.pop(0)

    def scroll_background(self):
        for i, label in enumerate(self.background_images):
            old_coords = label.winfo_x()
            label.place_configure(x=old_coords-2)

        self.add_background()
        self.remove_unseen_background()
        self.after(50, self.scroll_background)


if __name__ == '__main__':
    App()
