import random
import tkinter as tk
import backend


class App(tk.Tk):
    def __init__(self):
        super().__init__()  # creates a Tk window

        self.gravity_enabled = False
        self.main_menu_screen = True

        self.backend = backend.Backend()

        self.canvas_bg_images : list[int] = []
        self.canvas_pillar_images: list[list[int, int]] = []
        self.current_score = 0

        self.store_currently_used_assets()
        self.init_window()
        self.init_background()
        self.init_bird()
        self.init_mainmenu()
        self.init_pillars()
        self.init_scoreboard()

        self.mainloop()

    def store_currently_used_assets(self):
        self.background_image = self.backend.get_current_bg_image()
        self.player_icon_image = self.backend.get_current_player_image()
        self.pillar_up_image, self.pillar_down_image = self.backend.get_current_pillar_images()

        self.play_button_image, self.exit_button_image = self.backend.get_buttons_images()
        self.help_image = self.backend.get_help_image()
        self.logo_image = self.backend.get_logo_image()

    def init_window(self):
        self.title("Blappy Fird")
        self.resizable(False, False)
        self.iconphoto(True, self.backend.get_current_player_image())

        user_screen_width = self.winfo_screenwidth()
        user_screen_height = self.winfo_screenheight()

        self.game_window_width = 600
        self.game_window_height = 500

        pos_x = int((user_screen_width - self.game_window_width)/2)
        pos_y = int((user_screen_height - self.game_window_height)/2)

        self.geometry(f"{self.game_window_width}x{self.game_window_height}+{pos_x}+{pos_y}")
        self.canvas = tk.Canvas(self, height=self.game_window_height, width=self.game_window_width)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def init_background(self):
        bg_img1 = self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)
        bg_img2 = self.canvas.create_image(self.game_window_width, 0, image=self.background_image, anchor=tk.NW)
        bg_img3 = self.canvas.create_image(self.game_window_width * 2, 0, image=self.background_image, anchor=tk.NW)

        self.canvas_bg_images = [bg_img1, bg_img2, bg_img3]
        self.update()
        self.scroll_background()

    def scroll_background(self):
        for img in self.canvas_bg_images:
            self.canvas.move(img, -2, 0)

        self.shift_unseen_background()
        self.after(50, self.scroll_background)

    def shift_unseen_background(self):
        x_coord_of_first_img, _ = self.canvas.coords(self.canvas_bg_images[0])

        if x_coord_of_first_img < -self.game_window_width-2:  # out of the screen
            increment = 2*self.game_window_width - 5
            # shift to the right side of the last background image

            self.canvas.move(self.canvas_bg_images[0], increment, 0)

            first_bg_img = self.canvas_bg_images.pop(0)
            self.canvas_bg_images.append(first_bg_img)

    # bird
    def init_bird(self):
        bird_img = self.player_icon_image
        self.bird_canvas_image = self.canvas.create_image(0, 0, image=bird_img)
        self.canvas.moveto(self.bird_canvas_image, 200, 200)

        self.bird_velocity = 0
        self.terminal_velocity = 9.5  # maximum downwards velocity the bird can reach
        self.gravity_acceleration = 0.6   # pixels per gravity_interval that will be added to the bird's velocity
        self.gravity_interval = 15
        self.bottom_death_limit = self.game_window_height - 30  # coords below which the bird dies, for ground death

        self.bind("<Button-1>", lambda e: self.make_bird_hop())
        self.bind("<space>", lambda e: self.make_bird_hop())
        # left click and spacebar events binded to the game window

        self.idle_interrupt = False
        self.idle_animation_active = True
        self.idle_pixel_count = 0
        self.idle_increment = 1
        self.idle_bird_animation()

    def idle_bird_animation(self):
        if self.idle_interrupt:
            self.idle_interrupt = False
            self.idle_animation_active = False
            return

        self.idle_animation_active = True
        self.canvas.move(self.bird_canvas_image, 0, self.idle_increment)
        self.idle_pixel_count += 1

        if self.idle_pixel_count > 30:
            self.idle_increment *= -1
            self.idle_pixel_count = 0

        self.after(20, self.idle_bird_animation)

    def make_bird_fall(self):
        if not self.gravity_enabled:
            return

        self.bird_velocity += self.gravity_acceleration
        self.bird_velocity = min(self.bird_velocity, self.terminal_velocity)

        self.canvas.move(self.bird_canvas_image, 0, self.bird_velocity)
        # moves the bird in y direction by the current velocity amount of pixels

        self.after(self.gravity_interval, self.make_bird_fall)  # recursive call to continuously simulate gravity

    def make_bird_hop(self):
        if self.main_menu_screen:
            return

        self.bird_velocity = -10.5
        # bird provided an upward velocity

    # main menu
    def init_mainmenu(self):
        self.play_button_canvas_image = self.canvas.create_image(
            self.game_window_width/2, 310,
            image=self.play_button_image
        )
        self.exit_button_canvas_image = self.canvas.create_image(
            self.game_window_width/2, 370,
            image=self.exit_button_image
        )
        self.highscore_canvas_label = self.canvas.create_text(
            self.game_window_width/2, 430,
            text="Highscore: " + self.backend.get_current_highscore(),
            font=("Calibri", 18, "bold")
        )
        self.logo_canvas_image = self.canvas.create_image(
            self.game_window_width/2, 130,
            image=self.logo_image
        )

        self.init_help()

        self.canvas.tag_bind(self.play_button_canvas_image, '<Button-1>', lambda e: self.new_game())
        self.canvas.tag_bind(self.exit_button_canvas_image, '<ButtonRelease-1>', lambda e: self.exit_game())

    def hide_mainmenu(self):
        self.canvas.itemconfigure(self.play_button_canvas_image, state='hidden')
        self.canvas.itemconfigure(self.exit_button_canvas_image, state='hidden')
        self.canvas.itemconfigure(self.highscore_canvas_label, state='hidden')
        self.canvas.itemconfigure(self.logo_canvas_image, state='hidden')

    def show_mainmenu(self):
        self.canvas.itemconfigure(self.play_button_canvas_image, state='normal')
        self.canvas.itemconfigure(self.exit_button_canvas_image, state='normal')
        self.canvas.itemconfigure(self.highscore_canvas_label, state='normal', text="Highscore: " + self.backend.get_current_highscore())
        self.canvas.itemconfigure(self.logo_canvas_image, state='normal')
        self.canvas.lift(self.play_button_canvas_image)
        self.canvas.lift(self.exit_button_canvas_image)
        self.canvas.lift(self.highscore_canvas_label)
        self.canvas.lift(self.logo_canvas_image)

    # help
    def init_help(self):
        self.help_canvas_image = self.canvas.create_image(
            self.game_window_width/2, 420,
            image=self.help_image, state='hidden'
        )

    def show_help(self):
        self.canvas.itemconfigure(self.help_canvas_image, state='normal')

    def hide_help(self):
        self.canvas.itemconfigure(self.help_canvas_image, state='hidden')

# pillars and scores
    def init_scoreboard(self):
        self.scoreboard = self.canvas.create_text(300, 30, text=f"{self.current_score}", font=("Calibri", 48, "bold"), state='hidden')

    def update_scoreboard(self):
        self.canvas.itemconfigure(self.scoreboard, text=f'{self.current_score}')

    def increment_score(self):
        self.current_score += 1
        self.update_scoreboard()

    def reset_score(self):
        self.current_score = 0
        self.update_scoreboard()

    def init_pillars(self):
        self.pillar_spawnpoint_x = self.game_window_width + 100  # x coord of the first off-screen pillar in a new round
        self.pillar_distance = 300  # distance between 2 pillars' top left corners
        self.pillar_height = 400  # height of a pillar (image file)
        self.pillar_hole_gap = 170  # distance between bottom edge of top pillar and top edge of bottom pillar

        self.STANDARD_PILLAR_UP_Y = (self.game_window_height - self.pillar_hole_gap)/2 - self.pillar_height
        self.STANDARD_PILLAR_DOWN_Y = self.STANDARD_PILLAR_UP_Y + self.pillar_height + self.pillar_hole_gap
        # standard position of both the pillars, making the hole lie exactly in the center of the window height

        for i in range(3):
            pillar_up = self.canvas.create_image(0, 0, image=self.pillar_up_image)
            pillar_down = self.canvas.create_image(0, 0, image=self.pillar_down_image)

            self.canvas_pillar_images.append([pillar_up, pillar_down])

        self.reset_pillars_to_initial_position()

    def reset_pillars_to_initial_position(self):
        for i, [pillar_up, pillar_down] in enumerate(self.canvas_pillar_images):
            random_shift = random.randint(-10, 10) * 10

            self.canvas.moveto(
                pillar_up,
                self.pillar_spawnpoint_x + (self.pillar_distance * i),
                self.STANDARD_PILLAR_UP_Y + random_shift
            )
            self.canvas.moveto(
                pillar_down,
                self.pillar_spawnpoint_x + (self.pillar_distance * i),
                self.STANDARD_PILLAR_DOWN_Y + random_shift
            )

        self.initial_pillar_positions = self.canvas_pillar_images.copy()
        self.currently_tracking_index = 0

    def shift_unseen_pillar(self):
        first_pillar_up, first_pillar_down = self.canvas_pillar_images[0]

        random_shift = random.randint(-10, 10) * 10

        self.canvas.moveto(first_pillar_up, self.pillar_spawnpoint_x, self.STANDARD_PILLAR_UP_Y + random_shift)
        self.canvas.moveto(first_pillar_down, self.pillar_spawnpoint_x, self.STANDARD_PILLAR_DOWN_Y + random_shift)

        temp = self.canvas_pillar_images.pop(0)
        self.canvas_pillar_images.append(temp)

    def keep_moving_pillars(self):
        if self.main_menu_screen:
            return

        for pillar_up, pillar_down in self.canvas_pillar_images:
            self.canvas.move(pillar_up, -3, 0)
            self.canvas.move(pillar_down, -3, 0)

        self.after(10, self.keep_moving_pillars)

    def keep_shifting_pillars(self):
        if self.main_menu_screen:
            return

        last_pillar_up, last_pillar_down = self.canvas_pillar_images[-1]
        xcoord_up, _ = self.canvas.coords(last_pillar_up)

        if self.pillar_spawnpoint_x - xcoord_up >= self.pillar_distance - 50:
            # if the first pillar goes out of visual range
            # print("shifted", self.canvas_pillar_images)
            self.shift_unseen_pillar()

        self.after(50, self.keep_shifting_pillars)

    def lose_game(self):
        # print("lose game")
        self.main_menu_screen = True
        self.disable_gravity()
        self.backend.update_highscore_in_file(self.current_score)
        self.after(500, self.show_mainmenu)
        self.canvas.lift(self.scoreboard)
        self.bind("<Button-1>", lambda e: print(end=""))
        self.bind("<space>", lambda e: print(end=""))

    # game states
    def new_game(self):
        # print("new game")
        self.hide_mainmenu()
        self.main_menu_screen = False
        self.canvas.itemconfigure(self.scoreboard, state='normal')
        self.reset_score()
        self.reset_pillars_to_initial_position()
        self.show_help()
        self.after(50, lambda: [self.bind("<Button-1>", lambda e: self.start_game()), self.bind("<space>", lambda e: self.start_game())])
        if not self.idle_animation_active:
            self.canvas.moveto(self.bird_canvas_image, 200, 200)
            self.idle_bird_animation()

    def start_game(self):
        # print("started")
        self.hide_help()
        self.enable_gravity()
        self.keep_moving_pillars()
        self.keep_shifting_pillars()
        self.keep_checking_if_player_lost()
        self.make_bird_hop()
        self.bind("<Button-1>", lambda e: self.make_bird_hop())
        self.bind("<space>", lambda e: self.make_bird_hop())
        self.idle_interrupt = True

    def exit_game(self):
        self.canvas.delete(self.scoreboard)  # done to avoid a weird tkinter error when destroying game window
        self.after(200, self.destroy)

    def check_pillar_for_score(self):
        currently_tracking_pillars = self.initial_pillar_positions[self.currently_tracking_index]
        currently_tracking_pillar_up = currently_tracking_pillars[0]

        bird_coord_x, bird_coord_y = self.canvas.coords(self.bird_canvas_image)
        pilup_coord_x = self.canvas.coords(currently_tracking_pillar_up)[0]

        if pilup_coord_x < bird_coord_x:
            if bird_coord_y < 0:
                self.lose_game()
                return True

            self.increment_score()
            self.currently_tracking_index += 1
            self.currently_tracking_index %= len(self.initial_pillar_positions)

    def keep_checking_if_player_lost(self):
        above_upper_limit = self.check_pillar_for_score()
        if above_upper_limit is True:
            self.lose_game()
            return

        x1, y1, x2, y2 = self.canvas.bbox(self.bird_canvas_image)
        overlapping_objects_with_bird = self.canvas.find_overlapping(x1, y1+1, x2-1, y2-1)

        if sum(overlapping_objects_with_bird) > 10:
            self.lose_game()
            return

        _, y_coords = self.canvas.coords(self.bird_canvas_image)
        if y_coords >= self.bottom_death_limit:
            self.lose_game()
            return

        self.after(10, self.keep_checking_if_player_lost)

    def disable_gravity(self):
        self.gravity_enabled = False

    def enable_gravity(self):
        self.gravity_enabled = True
        self.make_bird_fall()


if __name__ == '__main__':
    App()
