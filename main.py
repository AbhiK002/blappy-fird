import tkinter as tk
from backend import Backend


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.backend = Backend()
        self.init_window()

        self.background_images : list[tk.Label] = []
        self.update_used_assets()

        self.init_background()
        self.scroll_background()

        self.init_bird()

        self.mainloop()

    def init_window(self):
        self.title("Flappy Bird")
        self.resizable(False, False)

        self.user_screen_width = self.winfo_screenwidth()
        self.user_screen_height = self.winfo_screenheight()

        self.game_window_width = 600
        self.game_window_height = 500

        pos_y = int((self.user_screen_width - self.game_window_width)/2)
        pos_x = int((self.user_screen_height - self.game_window_height)/2)

        self.geometry(f"{self.game_window_width}x{self.game_window_height}+{pos_y}+{pos_x}")
        self.canvas = tk.Canvas(self, height=500, width=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def update_used_assets(self):
        self.bg_img = self.backend.get_current_bg_image()
        self.bird_img = self.backend.get_current_player_image()
        # self.pillar_img = self.backend

    def init_background(self):
        bg_label = tk.Label(self, image=self.bg_img, borderwidth=0)
        bg_label.image = self.bg_img
        bg_label.place(x=0, y=0)

        bg_label2 = tk.Label(self, image=self.bg_img, borderwidth=0)
        bg_label2.image = self.bg_img
        bg_label2.place(x=self.game_window_width, y=0)

        bg_label3 = tk.Label(self, image=self.bg_img, borderwidth=0)
        bg_label3.image = self.bg_img
        bg_label3.place(x=self.game_window_width*2, y=0)

        self.background_images = [bg_label, bg_label2, bg_label3]
        self.update()

    def shift_unseen_background(self):
        x_pos_of_first_bg_img = self.background_images[0].winfo_x()
        x_pos_of_last_bg_img = self.background_images[-1].winfo_x()

        if x_pos_of_first_bg_img < -self.game_window_width-2:
            print("shifted")
            new_coords = x_pos_of_last_bg_img + self.game_window_width - 5
            self.background_images[0].place_configure(x=new_coords, y=0)
            temp = self.background_images.pop(0)
            self.background_images.append(temp)

    def scroll_background(self):
        for i, label in enumerate(self.background_images):
            old_coords = label.winfo_x()
            label.place_configure(x=old_coords-2)

        self.shift_unseen_background()
        self.after(50, self.scroll_background)

    def init_bird(self):
        bird_img = self.bird_img
        bird_label = tk.Label(self, image=bird_img, borderwidth=0, bg='skyblue')
        bird_label.place(x=150, y=200)


if __name__ == '__main__':
    App()
