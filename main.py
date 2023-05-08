import random
import tkinter as tk
import backend


class App(tk.Tk):
    """
    This class contains the code of the GUI of the game Blappy Fird.
    I inherited from the Tk class instead of making a `self.root = tk.Tk()`
    object and using it throughout the class because I have no idea, it just looks cooler.

    Jokes apart, I did this so that the `App` class acts like a `tk.Tk` window itself.
    """
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
        """
- Calls the respective methods of the `Backend` class to get the
  `tk.PhotoImage` objects of the image paths defined in the `Backend` class

Defines these class attributes, each of them storing `tk.PhotoImage` objects
of all the currently used assets in the game
    - `self.background_image`
    - `self.player_icon_image`
    - `self.pillar_up_image` and `self.pillar_down_image`
    - `self.help_image`
    - `self.logo_image`

These attributes will be useful in drawing the widgets on the canvas later on
        """

        self.background_image = self.backend.get_current_bg_image()
        self.player_icon_image = self.backend.get_current_player_image()
        self.pillar_up_image, self.pillar_down_image = self.backend.get_current_pillar_images()

        self.play_button_image, self.exit_button_image = self.backend.get_buttons_images()
        self.help_image = self.backend.get_help_image()
        self.logo_image = self.backend.get_logo_image()

    def init_window(self):
        """
This method configures the game window:
    - Title set to "Blappy Fird"
    - Resizable property set to False
    - Title bar icon added

Class attributes that will be used later are defined:
    - `self.game_window_width`: 600
    - `self.game_window_height`: 500
    - `self.canvas`: a `tk.Canvas` widget placed in the window.
      It is stretched to fit the entire window and is the only widget
      present in the window. All the images will be drawn inside the canvas itself

Ensures the game window spawns in the center of the screen
    - Done by getting the user's screen dimensions and configuring
      `self.geometry` accordingly
        """

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
        """
- 3 background images placed side to side are drawn onto the canvas

`self.canvas_bg_images` is set to a list of those 3 canvas images' tags
    - Tags are basically unique integers assigned to all the drawn widgets on the canvas
    - These can be used to access the properties of any drawn canvas widget
      (text, image, shapes, etc)
    - `self.canvas.move(tag, x_increment, y_increment)` for example can be used
      to move a drawn widget by `x_increment` and `y_increment` pixels via its tag

- `self.scroll_background()` method is called
        """

        bg_img1 = self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)
        bg_img2 = self.canvas.create_image(self.game_window_width, 0, image=self.background_image, anchor=tk.NW)
        bg_img3 = self.canvas.create_image(self.game_window_width * 2, 0, image=self.background_image, anchor=tk.NW)

        self.canvas_bg_images = [bg_img1, bg_img2, bg_img3]
        self.update()
        self.scroll_background()

    def scroll_background(self):
        """
- This is a recursive method running in its own separate thread
  (using tkinter's `self.after(milliseconds, function_obj)` method)

- On each call, it iterates through the `self.canvas_bg_images`
  and moves each background image to the left by 2 pixels

- Calls the `self.shift_unseen_background()` method, explained below

- Runs every 50 milliseconds in a separate thread to not block the
  main thread events
        """
        for img in self.canvas_bg_images:
            self.canvas.move(img, -2, 0)

        self.shift_unseen_background()
        self.after(50, self.scroll_background)

    def shift_unseen_background(self):
        """
This method checks if the first background image has gone out of view
or not
    - Since the image and the window have a 600 pixel width, it checks
      if the top left corner of the first image is less than -602

If it is, the image is shifted to the right side of the third image,
basically by around (600*2) units, since that's the width of 2 images placed side to side
    - This shift is also done to the `self.canvas_bg_images` list
      so that it is in sync with the visual order of the images
        """

        x_coord_of_first_img, _ = self.canvas.coords(self.canvas_bg_images[0])

        if x_coord_of_first_img < -self.game_window_width-2:  # out of the screen
            increment = 2*self.game_window_width - 5
            # shift to the right side of the last background image

            self.canvas.move(self.canvas_bg_images[0], increment, 0)

            first_bg_img = self.canvas_bg_images.pop(0)
            self.canvas_bg_images.append(first_bg_img)

    # bird
    def init_bird(self):
        """
- Draws the bird image onto the canvas at the location 200, 200

- `self.bird_canvas_image`: the bird's canvas image tag is stored in this

Defines the properties required for the gravity effect on the bird:
    - `self.bird_velocity = 0`
    The current velocity of the bird (amount of pixels that the bird
    is moved everytime `self.make_bird_fall()` is called)

    - `self.terminal_velocity = 9.5`
    Maximum downwards velocity that the bird can reach

    - `self.gravity_acceleration = 0.6`
    The amount of pixels `self.bird_velocity` increases by every
    `self.gravity_interval` amount of milliseconds

    - `self.gravity_interval = 15`
    The amount of milliseconds after which the `self.make_brid_fall()`
    recursively calls itself (discussed later)

    - `self.bottom_death_limit = (self.game_window_height - 30)`
    Defines the coordinates of the false 'ground' in the bottom of
    the screen at which the bird should die if it reaches this

- Binds LEFT_CLICK and SPACEBAR to the `make_bird_hop()` method,
  which is basically the jump the bird makes when the user clicks

Defines some properties used by the `idle_bird_animation()` method
    - Enables a continuous up and down motion when the round hasn't
      started. This is the bird's idle animation
        """

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
        """
- A recursive method that runs in its own thread,
  running the idle animation of the bird when a round isn't going on

- Makes the bird move up or down by 1 pixel on every
  call and stores the pixels moved till now

- The way this animation works is, it keeps moving
  the bird up/down until it has been moved 30 pixels. Then it
  switches to the other direction and resets the pixel count
  to 0. Then counts till 30 again.

- This recursion is stopped by making the `self.idle_interrupt`
  boolean `True` while the thread is running

- Runs every 20 milliseconds
        """

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
        """
- A recursive method that run its own thread while the boolean
  `self.gravity_enabled` is `True`
- If `self.gravity_enabled` is set to `False`, the thread stops
  immediately

The logic of the gravity is pretty simple. when this function is called:
    - `self.bird_velocity` increases by `self.gravity_acceleration`
      amount of pixels
    - It is set to `self.terminal_velocity` in case it goes over
      the defined terminal velocity
    - Moves `self.bird_canvas_image` (the drawn bird image) in
      the y-direction by `self.bird_velocity` pixels
    - Calls itself after `self.gravity_interval` milliseconds
      in a separate thread using tkinter's `self.after(ms, func)` method

Basically, just like the real world, every moment the bird falls down
slightly more than the previous instant
    - At t=0ms, bird is at 200y, its velocity increases by 0.6 px
    - At t=15ms, bird will be at 200y + velocity = 200.6y, velocity
      increases by the same amount again and becomes 1.2px
    - At t=30ms, bird will be at 200.6y + velocity = 201.8y,
      velocity then becomes 1.2px + 0.6px = 1.8px
    - At t=45ms, bird will now be at 201.8y + velocity = 203.6y and so on...

- Runs every `self.gravity_interval` milliseconds
        """

        if not self.gravity_enabled:
            return

        self.bird_velocity += self.gravity_acceleration
        self.bird_velocity = min(self.bird_velocity, self.terminal_velocity)

        self.canvas.move(self.bird_canvas_image, 0, self.bird_velocity)
        # moves the bird in y direction by the current velocity amount of pixels

        self.after(self.gravity_interval, self.make_bird_fall)  # recursive call to continuously simulate gravity

    def make_bird_hop(self):
        """
- This method is called whenever the user clicks on the screen
  or presses spacebar to make the bird jump/hop
- The velocity is set to a fixed negative value -> -10.5
- This means a constant upwards velocity is assigned to the bird,
  leading to a "jump" effect since the gravity is still active
- If `self.main_menu_screen` is `True`, this function will not run,
  since the bird should not hop while the main menu is active
        """

        if self.main_menu_screen:
            return

        self.bird_velocity = -10.5
        # bird provided an upward velocity

    # main menu
    def init_mainmenu(self):
        """
This method draws the widgets present in the main menu and
stores their tags in class attributes:
    - `self.play_button_canvas_image`: play button image
    - `self.exit_button_canvas_image`: exit button image
    - `self.highscore_canvas_label`: shows the current
      highscore on the main menu
    - `self.logo_canvas_image`: the logo of the game
- Calls `init_help()` method which draws the help image
  on the canvas, which will show up on the pre round screen
- Binds mouse LEFT_CLICK event to button images to run
  their respective methods `self.new_game()` and `self.exit_game()`
        """

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
        """
Hides the drawn main-menu widgets which include:
  - The buttons, logo and the highscore label

- This is done by using the `state` property of canvas
  widgets which can changed to `'hidden'` to hide them
        """

        self.canvas.itemconfigure(self.play_button_canvas_image, state='hidden')
        self.canvas.itemconfigure(self.exit_button_canvas_image, state='hidden')
        self.canvas.itemconfigure(self.highscore_canvas_label, state='hidden')
        self.canvas.itemconfigure(self.logo_canvas_image, state='hidden')

    def show_mainmenu(self):
        """
- Shows the hidden main-menu widgets
- This is also done by using the `state` property of
  canvas widgets which can changed
- The widgets are also brought above all the background
  widgets to make them visible
        """

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
        """
- Draws the help image on the canvas, which will only
  be displayed on the pre round screen
- Stores the image tag in `self.help_canvas_image` and
  makes it hidden by default
- The help image indicates the user what can be used
  to play the game. In our case, left mouse click and spacebar
        """

        self.help_canvas_image = self.canvas.create_image(
            self.game_window_width/2, 420,
            image=self.help_image, state='hidden'
        )

    def show_help(self):
        """
- Changes the `state` property of `self.help_canvas_image`
  to `'normal'` to show the widget, which was previously hidden
        """

        self.canvas.itemconfigure(self.help_canvas_image, state='normal')

    def hide_help(self):
        """
- Hides the help image by changing the `state` property of `self.help_canvas_image`
  to `'hidden'` to hide the widget
        """

        self.canvas.itemconfigure(self.help_canvas_image, state='hidden')

# pillars and scores
    def init_scoreboard(self):
        """
- Draws the text widget displaying the current score at the top of
  the window
- Stores its tag in `self.scoreboard`
- It displays the current value of `self.current_score` variable,
  which is by default 0 on the opening of the game
        """

        self.scoreboard = self.canvas.create_text(300, 30, text=f"{self.current_score}", font=("Calibri", 48, "bold"), state='hidden')

    def update_scoreboard(self):
        """
- Changes the text of `self.scoreboard` to the current value
  of `self.current_score`
        """

        self.canvas.itemconfigure(self.scoreboard, text=f'{self.current_score}')

    def increment_score(self):
        """
- Increases the `self.current_score` by 1 and calls `self.update_scoreboard()`
        """

        self.current_score += 1
        self.update_scoreboard()

    def reset_score(self):
        """
- Sets `self.current_score` to 0 and calls `self.update_scoreboard()`
        """

        self.current_score = 0
        self.update_scoreboard()

    def init_pillars(self):
        """
Defines some properties related to the obstacles/pillars:
    - `self.pillar_spawnpoint_x`: x coordinate of the first
      off-screen pillar in a new round
    - `self.pillar_distance`: distance between 2 pillars' top
      left corners
    - `self.pillar_height`: height of the pillar (also the
      image file's height)
    - `self.pillar_hole_gap`: height of the gap between the
      top and bottom edges of 2 pillars through which the
      bird will pass
    - `self.STANDARD_PILLAR_UP_Y`: the default y coordinate
      of the upper pillar, making the pillar hole gap lie exactly in the center of the game window
    - `self.STANDARD_PILLAR_DOWN_Y`: the default y coordinate
      of the lower pillar, making the pillar hole gap lie exactly in the center of the game window

3 pairs of upper and lower pillars are spawned
    - These pairs are shifted to their positions by calling
      `self.reset_pillars_to_initial_position()`, discussed below
    - Each pair of the pillars' tags are stored together in
      `self.canvas_pillar_images` as a tuple like `[(7,8), (9,10), (10,11)]`
    - Note: `self.canvas_pillar_images` stores each pair of
      pillars as 1 element in the form of a tuple and I
      mentioned this again for no reason. Anyways.
        """

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
        """
- When a new round is about to start, this method resets
  the position of the pair of pillars to their initial positions
- Starting from the `self.pillar_spawnpoint_x` coordinate,
  these pairs are separated by `self.pillar_distance` pixels of distance

A random value from -100 to 100 in the factor of 10
(-100, -90, ... 90, 100) is added to their y-coordinate
    - This ensures randomness in the heights of hole
      gaps and makes the game challenging
        """

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
        """
Similar to `shift_unseen_background()`
    - It shifts the first pillar to `self.pillar_spawnpoint_x`
      and randomises the height again
    - This gives an illusion of infinitely spawning pillars
- The shift is also done to the `self.canvas_pillar_images`
  list where the first element is appended at the last
- Called by `self.keep_shifting_pillars()` whenever the
  first pillar goes off screen
        """

        first_pillar_up, first_pillar_down = self.canvas_pillar_images[0]

        random_shift = random.randint(-10, 10) * 10

        self.canvas.moveto(first_pillar_up, self.pillar_spawnpoint_x, self.STANDARD_PILLAR_UP_Y + random_shift)
        self.canvas.moveto(first_pillar_down, self.pillar_spawnpoint_x, self.STANDARD_PILLAR_DOWN_Y + random_shift)

        temp = self.canvas_pillar_images.pop(0)
        self.canvas_pillar_images.append(temp)

    def keep_moving_pillars(self):
        """
- Recursive method that runs in its own thread
- If `self.main_menu_screen` is `True`, this function
  will not run, since the obstacles should not move while
  the main menu is active
- When called, it moves all the pairs of pillars
  towards the left by 3 pixels
- Runs every 10 milliseconds
        """

        if self.main_menu_screen:
            return

        for pillar_up, pillar_down in self.canvas_pillar_images:
            self.canvas.move(pillar_up, -3, 0)
            self.canvas.move(pillar_down, -3, 0)

        self.after(10, self.keep_moving_pillars)

    def keep_shifting_pillars(self):
        """
- Recursive function that runs in its own thread
- If `self.main_menu_screen` is `True`, this function
  will not run, since the obstacles should not be shifted
  at all while the main menu is active

It checks whether the first pillar has gone off-screen or not
    - If it has, it calls `self.shift_unseen_pillar()` to
      shift the first pillar to the right end of the queue
      both visually and the `self.canvas_pillar_images` list,
      as explained before

- This method basically keeps shifting the pillars as soon
  as the first pillar goes out of vision to give an illusion
  of infinitely spawning pillars
- Since it uses the same 3 pillars drawn at the start of the
  program, there is no need for the canvas to keep drawing
  and deleting pillar images
- Runs every 50 milliseconds
        """

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
        """
- This method is called when the player loses due to
  collision of the bird with the ground, off screen
  pillar or the on screen pillar
- `self.main_menu_screen` is set to `True`

These methods are called:
    - `self.disable_gravity()`: switch off gravity on the bird
    - `self.backend.update_highscore_in_file(self.current_score)`: update highscore
      in the highscore text file, if applicable
    - `self.show_mainmenu()`: shows main menu

- The `self.scoreboard` canvas image is brought in front of
  all the other widgets
- Left click and spacebar events get disabled to disallow
  accidental bird hops
        """

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
        """
- Called when the player presses the PLAY button the main menu
- Represents the Pre-Round stage of the game
- `self.main_menu_screen` set to `False`
- When the user starts the game, the scoreboard is initially hidden.
  this method makes it visible and the scoreboard then remains visible until the game is closed

These methods are called:
    - `self.reset_score()`: set the score to 0
    - `self.reset_pillars_to_initial_position()`: reset the obstacles for a new round
    - `self.show_help()`: shows the image widget indicating the controls of the game, since this is pre-round
    - `self.idle_bird_animation()`: starts the idle bird animation

The left click and spacebar events are binded to `self.start_game()`
    - `self.bird_canvas_image` which is the drawn bird image, is moved to its initial position (200, 200)
        """

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
        """
- This method is called when the user starts the round via mouse
  click or spacebar in the pre round stage

These things happen here:
    - The help image is hidden
    - Switch on the gravity on the bird
    - Start moving the obstacles/pillars
    - Start the infinite obstacle effect
    - A recursive method that will be discussed later,
      checks if the bird collided anywhere
    - Since the left click and space bar events aren't
      binded to the bird_hop function yet, the trigger won't
      make the bird jump. Therefore this function is called
      manually to give the initial jump to the bird.

- Left click and keyboard events are again binded to `self.make_bird_hop()`
- `self.idle_interrupt` is set to `True` since the bird's
  idle animation is active during the pre round, which
  stops the `self.idle_bird_animation()` recursive thread
        """

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
        """
the scoreboard widget is deleted manually
    - This has been done to avoid a weird tkinter `alloc` error

- The game window is destroyed after 800 milliseconds

        """

        self.canvas.delete(self.scoreboard)  # done to avoid a weird tkinter error when destroying game window
        self.after(200, self.destroy)

    def check_pillar_for_score(self):
        """
- Checks if the bird has crossed a pillar

If it has, it will now check whether the bird is currently
flying higher than the game window
    If it is flying higher, this means the bird
    should collide with the offscreen upper pillar
         - Therefore it returns `True` (this will be used
           in `self.keep_checking_if_player_lost()`, discussed below)
    - Else, call `self.increment_scoreboard()` to increase the score
        """

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
        """
- This is a recursive method that run in its own thread

It has two purposes:
    - Check if player lost
    - Increase score if player passed a pillar

It first calls `self.check_pillar_for_score()` and keeps track of its return value in a local variable
    - If it returns `True` this means the player collided with an off screen pillar
    - Therefore, `self.lose_game()` is called and the thread ends here
    - Otherwise, nothing happens

Next, to see if the bird collided with any pillar, a method `find_overlapping(*args)` of class `tk.Canvas` is utilised
    - The coordinates of the top-left corner (x1, y1) and the bottom-right corner (x2, y2) of the rectangle
      surrounding the `self.bird_canvas_image` are stored

    - Using these coordinates, the coordinates of 2 smaller rectangles that
      cover the bird's visual body and beak are derived, for accurate deaths
      due to collision. This is done so that the bird doesn't die due to
      invisible collisions (where the bird doesn't touch the obstacle visually,
      but its rectangle does)

      ```
      rectangle_of_body = (x1+7, y1, x2-16, y2-1)  # 32x42 rectangle
      rectangle_of_beak = (x1+7+32, y1+18, x2, y2-1)  # 16x24 rectangle
      ```

    - The `tk.Canvas.find_overlapping(*args)` method returns a list of all the tags of the widgets
      that are currently coinciding with the passed rectangle coordinates
      (in this case, the rectangles we made)


    - In our case, the background images are always overlapping with the bird visually, so they should be ignored

    - The way I implemented this is:
      - If the sum of the tags (which are unique integers) is greater than 10,
        this implies the bird collided with any of the pillars, therefore `self.lose_game()`
        is called and the thread ends here
      - Otherwise, the bird is safe

    - The reason this works is that firstly, I noticed that the tags of
      the background images are always 2, 3 and 4 and the pillars go from 7 to 12.

    When the bird isn't colliding with the pillars, the possible list values returned are:
        - `[1, 2], [1, 3], [1, 4]` or sometimes rarely `[1, 2, 3], [1, 3, 4], [1, 4, 2]`
        - Notice, the sums of all these lists is always less than 10
        - Since the pillars' tags go from 7 to 12, if any one of them gets added to the returned list, the sum always exceeds 10

- This method runs every 10 milliseconds. Due to its superfast interval, I had to find a way which won't take up too much time or processing to see whether the bird collided with any pillars. This is why I adopted the easy `sum(tags_list) > 10` approach. Quick and efficient.
        """

        above_upper_limit = self.check_pillar_for_score()
        if above_upper_limit is True:
            self.lose_game()
            return

        x1, y1, x2, y2 = self.canvas.bbox(self.bird_canvas_image)  # main rectangle containing the entire bird image
        rectangle_of_body = (x1+7, y1, x2-16, y2-1)  # 32x42 rectangle
        rectangle_of_beak = (x1+7+32, y1+18, x2, y2-1)  # 16x24 rectangle

        overlapping_objects_with_body = self.canvas.find_overlapping(*rectangle_of_body)
        overlapping_objects_with_beak = self.canvas.find_overlapping(*rectangle_of_beak)

        if sum(set(overlapping_objects_with_body + overlapping_objects_with_beak)) > 10:
            self.lose_game()
            return

        _, y_coords = self.canvas.coords(self.bird_canvas_image)
        if y_coords >= self.bottom_death_limit:
            self.lose_game()
            return

        self.after(10, self.keep_checking_if_player_lost)

    def disable_gravity(self):
        """
- `self.gravity_enabled` is set to `False`
- This automatically stops the `self.make_bird_fall()` recursive thread if it's running currently
        """

        self.gravity_enabled = False

    def enable_gravity(self):
        """
- `self.gravity_enabled` is set to `True`
- `self.make_bird_fall()` is called, which starts a new thread controlling the bird's gravity
        """

        self.gravity_enabled = True
        self.make_bird_fall()


if __name__ == '__main__':
    App()
