import tkinter as tk
from backend import Backend


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.gravity_enabled = False

        self.main_menu_screen = True
        self.ready_to_go = False

        self.backend = Backend()
        self.init_window()

        self.update_used_assets()

        self.background_images : list[int] = []
        self.init_background()
        self.scroll_background()

        self.init_bird()
        self.init_buttons()

        self.score = 0
        self.init_scoreboard()

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
        self.canvas.moveto(self.bird_canvas_image, 150, 200)

        self.bird_velocity = 0
        self.gravity_acceleration = 0.6
        self.gravity_interval = 15

        self.bind("<Button-1>", lambda e: self.make_bird_jump())

        self.make_bird_fall()

    def make_bird_fall(self):
        if not self.gravity_enabled:
            return

        self.bird_velocity += self.gravity_acceleration
        if self.bird_velocity > 9:
            self.bird_velocity = 9

        self.canvas.move(self.bird_canvas_image, 0, self.bird_velocity)

        y_coords = self.canvas.coords(self.bird_canvas_image)[1]
        if y_coords >= 470:
            self.game_over()

        self.after(self.gravity_interval, self.make_bird_fall)

    def make_bird_jump(self):
        if self.main_menu_screen:  # user presses PLAY
            return

        if self.ready_to_go:
            self.ready_to_go = False  # game starts
            return

        self.bird_velocity = -10.5
        if not self.gravity_enabled:
            self.enable_gravity()

    def init_buttons(self):
        self.playbutton, self.exitbutton = self.backend.get_buttons_images()

        self.playimage_button = self.canvas.create_image(300, 260, image=self.playbutton)
        self.exitimage_button = self.canvas.create_image(300, 320, image=self.exitbutton)

        self.canvas.tag_bind(self.playimage_button, '<Button-1>', lambda e: self.start_game())
        self.canvas.tag_bind(self.exitimage_button, '<Button-1>', lambda e: self.end_game())

    def hide_buttons(self):
        self.canvas.itemconfigure(self.playimage_button, state='hidden')
        self.canvas.itemconfigure(self.exitimage_button, state='hidden')

    def show_buttons(self):
        self.canvas.itemconfigure(self.playimage_button, state='normal')
        self.canvas.itemconfigure(self.exitimage_button, state='normal')

    def game_over(self):
        self.ready_to_go = False
        self.main_menu_screen = True
        self.disable_gravity()
        self.show_buttons()

    def start_game(self):
        self.hide_buttons()
        self.canvas.moveto(self.bird_canvas_image, 150, 200)
        self.ready_to_go = True
        self.main_menu_screen = False
        self.update_scoreboard(reset=True)
        self.canvas.itemconfigure(self.scoreboard, state='normal')

    def end_game(self):
        self.canvas.delete(self.scoreboard)
        self.gravity_enabled = True
        self.make_bird_fall()
        self.after(800, self.destroy)

    def disable_gravity(self):
        self.gravity_enabled = False

    def enable_gravity(self):
        self.gravity_enabled = True
        self.make_bird_fall()

    def init_scoreboard(self):
        self.scoreboard = self.canvas.create_text(300, 50, text=f"{self.score}", font=("Calibri", 48, "bold"), state='hidden')

    def update_scoreboard(self, reset=False):
        self.score += 1
        if reset:
            self.score = 0

        self.canvas.itemconfigure(self.scoreboard, text=f'{self.score}')


if __name__ == '__main__':
    App()
