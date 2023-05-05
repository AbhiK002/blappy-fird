import random
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


        self.pillars_currently_visible = []
        self.init_pillars()

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
            # print("shifted")
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
        self.bird_canvas_image = self.canvas.create_image(200, 200, image=bird_img)
        self.canvas.moveto(self.bird_canvas_image, 200, 200)

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
            self.start_spawning_pillars()

    def init_buttons(self):
        self.playbutton, self.exitbutton = self.backend.get_buttons_images()

        self.playimage_button = self.canvas.create_image(300, 290, image=self.playbutton)
        self.exitimage_button = self.canvas.create_image(300, 350, image=self.exitbutton)

        self.canvas.tag_bind(self.playimage_button, '<Button-1>', lambda e: self.start_game())
        self.canvas.tag_bind(self.exitimage_button, '<Button-1>', lambda e: self.end_game())

    def hide_buttons(self):
        self.canvas.itemconfigure(self.playimage_button, state='hidden')
        self.canvas.itemconfigure(self.exitimage_button, state='hidden')

    def show_buttons(self):
        self.canvas.itemconfigure(self.playimage_button, state='normal')
        self.canvas.itemconfigure(self.exitimage_button, state='normal')
        self.canvas.lift(self.playimage_button)
        self.canvas.lift(self.exitimage_button)

    def game_over(self):
        self.ready_to_go = False
        self.main_menu_screen = True
        self.disable_gravity()
        self.after(200, self.show_buttons)
        self.canvas.lift(self.scoreboard)

    def start_game(self):
        self.hide_buttons()
        self.canvas.moveto(self.bird_canvas_image, 200, 200)
        self.ready_to_go = True
        self.main_menu_screen = False
        self.update_scoreboard(reset=True)
        self.canvas.itemconfigure(self.scoreboard, state='normal')
        self.despawn_all_pillars()

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

    def init_pillars(self):
        self.pillar_spawnpoint_x = 700
        self.pillar_distance = 300
        self.pillar_height = 400
        self.pillar_hole_gap = 165

        self.STANDARD_PILLAR_UP_Y = (self.game_window_height - self.pillar_hole_gap)/2 - self.pillar_height
        self.STANDARD_PILLAR_DOWN_Y = self.STANDARD_PILLAR_UP_Y + self.pillar_height + self.pillar_hole_gap

        self.pillar_up_image, self.pillar_down_image = self.backend.get_current_pillar_images()

    def spawn_pillars(self):
        for i in range(3):
            pillar_up_canvas = self.canvas.create_image(-200, 0, image=self.pillar_up_image)
            pillar_down_canvas = self.canvas.create_image(-200, 0, image=self.pillar_down_image)

            random_shift = random.randint(-10, 10) * 10

            self.canvas.moveto(pillar_up_canvas, self.pillar_spawnpoint_x + self.pillar_distance*i, self.STANDARD_PILLAR_UP_Y + random_shift)
            self.canvas.moveto(pillar_down_canvas, self.pillar_spawnpoint_x + self.pillar_distance*i, self.STANDARD_PILLAR_DOWN_Y + random_shift)

            self.pillars_currently_visible.append([pillar_up_canvas, pillar_down_canvas])

    def shift_unseen_pillar(self):
        first_pillar_up, first_pillar_down = self.pillars_currently_visible[0]
        xcoord_up, _ = self.canvas.coords(first_pillar_up)

        random_shift = random.randint(-10, 10) * 10

        self.canvas.moveto(first_pillar_up, self.pillar_spawnpoint_x, self.STANDARD_PILLAR_UP_Y + random_shift)
        self.canvas.moveto(first_pillar_down, self.pillar_spawnpoint_x, self.STANDARD_PILLAR_DOWN_Y + random_shift)
        temp = self.pillars_currently_visible.pop(0)
        self.pillars_currently_visible.append(temp)

        # print("shifted", self.pillars_currently_visible)

    def move_pillars(self):
        if self.main_menu_screen or self.ready_to_go:
            return

        for pillar_up, pillar_down in self.pillars_currently_visible:
            self.canvas.move(pillar_up, -3, 0)
            self.canvas.move(pillar_down, -3, 0)

        self.after(10, self.move_pillars)

    def keep_spawning_pillars(self):
        if self.main_menu_screen or self.ready_to_go:
            return

        last_pillar_up, last_pillar_down = self.pillars_currently_visible[-1]
        xcoord_up, _ = self.canvas.coords(last_pillar_up)

        if self.pillar_spawnpoint_x - xcoord_up >= self.pillar_distance - 50:
            # print("spawned", self.pillars_currently_visible)
            self.shift_unseen_pillar()

        self.after(50, self.keep_spawning_pillars)

    def start_spawning_pillars(self):
        self.move_pillars()
        self.keep_spawning_pillars()
        self.check_pillar_for_score()

    def despawn_all_pillars(self):
        for pilup, pildown in self.pillars_currently_visible:
            self.canvas.delete(pilup, pildown)

        self.pillars_currently_visible = []
        self.spawn_pillars()

    def check_pillar_for_score(self):
        pass


if __name__ == '__main__':
    App()
