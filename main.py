import tkinter as tk
from backend import Backend


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bird_paused = True
        self.backend = Backend()
        self.init_window()

        self.update_used_assets()

        self.background_images : list[int] = []
        self.init_background()
        self.scroll_background()

        self.init_bird()

        self.mainloop()

    def init_window(self):
        self.title("Blappy Fird")
        self.resizable(False, False)
        self.iconphoto(True, self.backend.get_current_player_image())

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
        bg_img1 = self.canvas.create_image(0, 0, image=self.bg_img, anchor=tk.NW)
        bg_img2 = self.canvas.create_image(self.game_window_width, 0, image=self.bg_img, anchor=tk.NW)
        bg_img3 = self.canvas.create_image(self.game_window_width*2, 0, image=self.bg_img, anchor=tk.NW)

        self.background_images = [bg_img1, bg_img2, bg_img3]
        self.update()

    def shift_unseen_background(self):
        old_x_of_first_img = self.canvas.coords(self.background_images[0])[0]

        if old_x_of_first_img < -self.game_window_width-2:
            print("shifted")
            increment = 2*self.game_window_width - 5
            self.canvas.move(self.background_images[0], increment, 0)

            temp = self.background_images.pop(0)
            self.background_images.append(temp)

    def scroll_background(self):
        for i, img in enumerate(self.background_images):
            self.canvas.move(img, -2, 0)

        self.shift_unseen_background()
        self.after(50, self.scroll_background)

    def init_bird(self):
        bird_img = self.bird_img
        self.bird_canvas_image = self.canvas.create_image(150, 200, image=bird_img)

        self.bird_velocity = 0
        self.gravity_acceleration = 0.6
        self.gravity_interval = 15

        self.bind("<Button-1>", lambda e: self.make_bird_jump())

        self.make_bird_fall()

    def make_bird_fall(self):
        if self.bird_paused:
            return

        self.bird_velocity += self.gravity_acceleration
        if self.bird_velocity > 9:
            self.bird_velocity = 9

        self.canvas.move(self.bird_canvas_image, 0, self.bird_velocity)

        y_coords = self.canvas.coords(self.bird_canvas_image)[1]
        if y_coords >= 470:
            self.bird_paused = True
            self.game_over()

        self.after(self.gravity_interval, self.make_bird_fall)

    def make_bird_jump(self):
        self.bird_velocity = -12
        if self.bird_paused:
            self.bird_paused = False
            self.make_bird_fall()

    def game_over(self):
        pass


if __name__ == '__main__':
    App()
