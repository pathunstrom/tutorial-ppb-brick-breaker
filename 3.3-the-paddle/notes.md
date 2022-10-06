The next step is going to be setting up our paddle.
This is the step where our interactions get more interesting!
Because play input uses the mouse and keyboard, let's delete the event handlers on Game.

```python
class Game(ppb.Scene):
    background_color = (25, 50, 25)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add(Ball())
        self.add(Wall(width=26, position=ppb.Vector(0, 16.5)))
        self.add(Wall(width=26, position=ppb.Vector(0, -16.5), normal=ppb.directions.Up))
        self.add(Wall(height=34, position=ppb.Vector(12, 0), normal=ppb.directions.Left))
        self.add(Wall(height=34, position=ppb.Vector(-12, 0), normal=ppb.directions.Right))


class EndScreen(ppb.Scene):
```

Note this means we can't see our End screen anymore, but that's okay, we'll add a lose condition in a bit.

Let's start by setting up our Paddle class.
Just like Wall, it's a RectangleSprite and we'll use the same cheat to make the rendered rectangle work.

```python
class Paddle(ppb.RectangleSprite):
    width = 3
    height = 0.5
    color = (175, 175, 255)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = ppb.Rectangle(*self.color, aspect_ratio=(self.width, self.height))
```

Next, let's add it to the Game when it starts up:

```python
def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.add(Ball())
    self.add(Wall(width=26, position=ppb.Vector(0, 16.5)))
    self.add(Wall(width=26, position=ppb.Vector(0, -16.5), normal=ppb.directions.Up))
    self.add(Wall(height=34, position=ppb.Vector(12, 0), normal=ppb.directions.Left))
    self.add(Wall(height=34, position=ppb.Vector(-12, 0), normal=ppb.directions.Right))
    self.add(Paddle(position=ppb.Vector(0, -14)))
```

The paddle doesn't move, and the ball actually goes through it, but now you can see where it'll start.
If you don't like the size or position, go ahead and try some other values for
the width, height, and the y component of the position.

Next step, let's make the ball collide with it.
We'll use the same idea before and reuse that collision function, but we'll select the normal in a new way.

```python
paddle = next(event.scene.get(kind=Paddle))
```

First, we need to get the paddle from the scene.
We can use `next` here because we only have one paddle and it's sure to exist.
If it didn't we'd have a host of other problems on our hands.

Then we check if the ball has collided with the paddle.
To find out normal, first we'll get the x position of the ball, and the left and right sides of the paddle.
Then we calculate the percentage distance from left to right that the ball is when it hits the paddle.
The calculation you see here is a normalization function for numbers.
It's a little gnarly, but it's worth keeping around since it's the basis of a lot of tricks in game dev.
After that, we pick two vectors to represent the normal at the extreme left and extreme right of our range.
In this case, I'm using UpAndLeft for the left and UpAndRight for the right.
You could use Left and Right or some other vector for each, but make sure they're reflections of each other.
Then we blend both vectors using the percentage we calculated before and its inverse by subtracting it from one.

This is a lot, so I'm going to leave the code up for you for a bit. Are there any questions?

```python
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
```

Now that we have a ball bouncing on the paddle, we want to add the controls.
We want to provide both mouse and keyboard controls, but we also don't want them to stumble over each other.
Let's set two class constants that are magical strings of "mouse" and "keyboard".
Then have control_scheme and set it to None.

Then let's set two controls: left and right.
Finally, we need a mouse_vector, set also to None.

```python
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
```
With all the state we'll need defined, let's add our event handlers.

For keyboard, we need both key released and key pressed.
They'll look very similar, but let's walk through key_pressed.

First, we'll add a new import to the top of our file: `from ppb import keycodes`
This isn't necessary, but it will make your development environment happier.

Then we make a key_pressed handler that takes a KeyPressed event parameter and a signal.
In that function, we check the key parameter of the KeyPressed event.
We only want the Left and Right arrows, so we grab those keycodes to compare against.
Then we set either the left or right control to true, and then switch to KEYBOARD_CONTROLS.

```python
def on_key_pressed(self, event: ppb.events.KeyPressed, signal):
    if event.key is keycodes.Left:
        self.control_left = True
        self.control_scheme = self.KEYBOARD_CONTROLS
    elif event.key is keycodes.Right:
        self.control_right = True
        self.control_scheme = self.KEYBOARD_CONTROLS
```

The mouse handler is very similar, but we don't need the if structure.
We'll use the mouse motion event for this step:
The event parameter is a MouseMotion.

We are going to make a vector using the mouse x component and the paddle y component.
This will make our update logic easier.
Then we switch our control_scheme to MOUSE_CONTROLS.

```python
def on_mouse_motion(self, event: ppb.events.MouseMotion, signal):
    self.mouse_vector = ppb.Vector(event.position, self.position.y)
    self.control_scheme = self.MOUSE_CONTROLS
```

Our last control step is the inverse of the mouse pressed.
When we let go of our keyboard controls, we want to turn off the left and right controls.

```python
def on_key_released(self, event: ppb.events.KeyReleased, signal):
    if event.key is keycodes.Left:
        self.control_left = False
    elif event.key is keycodes.Right:
        self.control_right = False
```

Now let's get to the update function. First, we'll add a speed attribute to our class

```python
class Paddle(ppb.RectangleSprite):
    width = 3
    height = 0.5
    color = (175, 175, 255)

    MOUSE_CONTROLS = "mouse"
    ...
    mouse_vector = None
    
    speed = 7
```

Then we set up a an on_update handler and we'll have two branches here, one for
the KEYBOARD_CONTROLS and one for the MOUSE_CONTROLS

In the keyboard control side, we make a movement zero vector.
Then we see if Left is pressed and add a Left vector to movement.
Do the opposite for Right.
Then, if the movement vector is non-zero, we update position just like we did the ball.

```python
def on_update(self, event: ppb.events.Update, signal):
    if self.control_scheme == self.KEYBOARD_CONTROLS:
        movement_vector = ppb.Vector(0, 0)
        if self.control_right:
            movement_vector += ppb.directions.Right
        if self.control_left:
            movement_vector += ppb.directions.Left
        if movement_vector:
            self.position += movement_vector.normalize() * self.speed * event.time_delta
```

For the Mouse control half, we get the to_position by subtracting the paddle position from our mouse_vector.
If that's non-zero, we create a movement_delta by normalizing our to_position, by speed and time_delta like before.
Then if that vector is longer than the total distance to_position, we replace the calculated delta with the to_position vector.
And then we update the position by that movement_delta.

And now, you should be able to control the paddle with either your mouse or keyboard!
