import ppb
from ppb import keycodes

FONT = ppb.Font("RugenExpanded-DOKGE.otf", size=72)


class Ball(ppb.Sprite):
    image = ppb.Circle(220, 220, 220)
    velocity: ppb.Vector = ppb.directions.DownAndRight * 13
    position = ppb.Vector(-3, -12)

    def on_update(self, event, signal):
        self.position += self.velocity * event.time_delta
        walls = event.scene.get(kind=Wall)
        for wall in walls:
            if self.collides(wall):
                self.velocity = self.velocity.reflect(wall.normal)
        paddle = next(event.scene.get(kind=Paddle))
        if self.collides(paddle):
            ball_x = self.position.x
            min_range = paddle.left
            max_range = paddle.right
            percent_from_left = (max(min(ball_x, max_range), min_range) - min_range) / (max_range - min_range)
            left_normal = ppb.directions.UpAndLeft
            right_normal = ppb.directions.UpAndRight
            vector = right_normal * percent_from_left + left_normal * (1 - percent_from_left)
            normal = vector.normalize()
            self.velocity = self.velocity.reflect(normal)

    def collides(self, other):
        combined_width = self.width + other.width
        combined_height = self.height + other.height
        max_vertical = max(self.top, other.top) - min(self.bottom, other.bottom)
        max_horizontal = max(self.right, other.right) - min(self.left, other.left)
        return max_vertical < combined_height and max_horizontal < combined_width


class Wall(ppb.RectangleSprite):
    normal = ppb.directions.Down

    def __init__(self, width=1, height=1, color=(220, 220, 220), **kwargs):
        super().__init__(width=width, height=height, color=color, **kwargs)
        self.image = ppb.Rectangle(*color, aspect_ratio=(width, height))


class Paddle(ppb.RectangleSprite):
    width = 3
    height = 0.5
    color = (175, 175, 255)

    MOUSE_CONTROLS = "mouse"
    KEYBOARD_CONTROLS = "keyboard"
    control_scheme = None
    control_left = False
    control_right = False
    mouse_vector = None

    speed = 7

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = ppb.Rectangle(*self.color, aspect_ratio=(self.width, self.height))

    def on_update(self, event: ppb.events.Update, signal):
        if self.control_scheme == self.KEYBOARD_CONTROLS:
            movement_vector = ppb.Vector(0, 0)
            if self.control_right:
                movement_vector += ppb.directions.Right
            if self.control_left:
                movement_vector += ppb.directions.Left
            if movement_vector:
                self.position += movement_vector.normalize() * self.speed * event.time_delta
        if self.control_scheme == self.MOUSE_CONTROLS:
            to_position = self.mouse_vector - self.position
            if to_position:
                movement_delta = to_position.normalize() * self.speed * event.time_delta
                if movement_delta.length > to_position.length:
                    movement_delta = to_position
                self.position += movement_delta

    def on_key_pressed(self, event: ppb.events.KeyPressed, signal):
        if event.key is keycodes.Left:
            self.control_left = True
            self.control_scheme = self.KEYBOARD_CONTROLS
        elif event.key is keycodes.Right:
            self.control_right = True
            self.control_scheme = self.KEYBOARD_CONTROLS

    def on_key_released(self, event: ppb.events.KeyReleased, signal):
        if event.key is keycodes.Left:
            self.control_left = False
        elif event.key is keycodes.Right:
            self.control_right = False

    def on_mouse_motion(self, event: ppb.events.MouseMotion, signal):
        self.mouse_vector = ppb.Vector(event.position.x, self.position.y)
        self.control_scheme = self.MOUSE_CONTROLS


class TitleScreen(ppb.Scene):
    background_color = (0, 0, 0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add(
            ppb.Sprite(
                image=ppb.Text("Brick Breaker", font=FONT, color=(220, 220, 220)),
                size=2
            )
        )

    def on_key_released(self, event, signal):
        signal(ppb.events.StartScene(Game))
        cam = event.scene.main_camera
        print(f"Width: {cam.width}, Height: {cam.height}")

    def on_button_released(self, event, signal):
        signal(ppb.events.StartScene(Game))


class Game(ppb.Scene):
    background_color = (25, 50, 25)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add(Ball())
        self.add(Wall(width=26, position=ppb.Vector(0, 16.5)))
        self.add(Wall(width=26, position=ppb.Vector(0, -16.5), normal=ppb.directions.Up))
        self.add(Wall(height=34, position=ppb.Vector(12, 0), normal=ppb.directions.Left))
        self.add(Wall(height=34, position=ppb.Vector(-12, 0), normal=ppb.directions.Right))
        self.add(Paddle(position=ppb.Vector(0, -14)))

class EndScreen(ppb.Scene):
    background_color = (50, 25, 25)

    def on_key_released(self, event, signal):
        signal(ppb.events.StopScene())

    def on_button_released(self, event, signal):
        signal(ppb.events.StopScene())


ppb.run(starting_scene=TitleScreen, resolution=(600, 800))
