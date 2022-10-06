import ppb


FONT = ppb.Font("RugenExpanded-DOKGE.otf", size=72)


class Ball(ppb.Sprite):
    image = ppb.Circle(220, 220, 220)
    velocity: ppb.Vector = ppb.directions.UpAndRight * 15
    position = ppb.Vector(0, -14)

    def on_update(self, event, signal):
        self.position += self.velocity * event.time_delta
        walls = event.scene.get(kind=Wall)
        for wall in walls:
            if self.collides(wall):
                self.velocity = self.velocity.reflect(wall.normal)

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

    def on_key_released(self, event, signal):
        signal(ppb.events.ReplaceScene(EndScreen))

    def on_button_released(self, event, signal):
        signal(ppb.events.ReplaceScene(EndScreen))


class EndScreen(ppb.Scene):
    background_color = (50, 25, 25)

    def on_key_released(self, event, signal):
        signal(ppb.events.StopScene())

    def on_button_released(self, event, signal):
        signal(ppb.events.StopScene())


ppb.run(starting_scene=TitleScreen, resolution=(600, 800))
