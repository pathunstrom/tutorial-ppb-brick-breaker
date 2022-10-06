import ppb


FONT = ppb.Font("RugenExpanded-DOKGE.otf", size=72)


class Ball(ppb.Sprite):
    image = ppb.Circle(220, 220, 220)
    velocity = ppb.directions.Up * 15
    position = ppb.Vector(0, -14)

    def on_update(self, event, signal):
        self.position += self.velocity * event.time_delta
        print(event.scene.main_camera.height, event.scene.main_camera.width)



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

    def on_button_released(self, event, signal):
        signal(ppb.events.StartScene(Game))


class Game(ppb.Scene):
    background_color = (25, 50, 25)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add(Ball())

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
