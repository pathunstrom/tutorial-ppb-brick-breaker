So now we can get onto the fun stuff!
Set up an `__init__` in Game just like we did in the TitleScreen.

```python
def __init__(self, **kwargs):
    super().__init__(**kwargs)
```

We're going to use this in a moment, but now we're making a new class: Ball.

```python
class Ball(ppb.Sprite):
    pass
```

This is our next GameObject. A Sprite in the context of ppb is an object in the
play space. The default Sprite is square, has an image attribute, and has the
add/remove/get combo mentioned previously. You can also include event handlers
which is how we'll add behavior.

For now, let's leave it empty like this and see what we get.

```python
def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.add(Ball())
```

We'll run the program, click through the title screen and then we'll have a
simple square in the middle of the screen. You'll notice my square doesn't look
like yours: If you don't provide and image, Sprite will make an arbitrarily
colored square.

Since this is supposed to be a ball, let's use a circle instead:

```python
class Ball(ppb.Sprite):
    image = ppb.Circle(220, 220, 220)
```

Now run the game, and we have a white circle instead of our random colored
square.

Now let's make the ball move.

```python
import ppb


class Ball(ppb.Sprite):
    image = ppb.Circle(220, 220, 220)
    velocity = ppb.directions.Up * 3
    position = ppb.Vector(0, -15)

    def on_update(self, event: ppb.events.Update, signal):
        self.position += self.velocity * event.time_delta
```

First, we set a velocity. I need to cover a couple of theory bits to make sure
it's clear.
If you already know linear algebra, this is going to be a simplification.
ppb's 2d space uses a coordinate system in "game units".
If you've done any kind of mathematical graphing, this is a cartesian coordinate grid.
The origin of our grid defaults to the center of the screen.
(We won't be covering how to change this in this tutorial.)
A game unit is just an "arbitrary unit".
Our ball is 1 game unit in diameter.
The directions module is a set of unit vectors, or vectors that are 1 game unit long.
A vector in ppb is essentially a tuple of x, y pairs with some cool mathematical properties.
One of those properties is the ability to multiply them by a value to change their length.
The length of a vector is the length of the hypotenuse of a triangle using the two values as the size.
Here, we're essentially telling ppb that the velocity is a vector 3 units long.

Then we set the position of the ball. This is near the bottom of your screen.
The position is also a vector, and the arguments are x position and y position.
Then, we make a new event handler, probably the most used handler: The on_update.

In the event handler, we're using another one of those cool mathematical properties:
When you add two vectors together, you add each component separately.
So x 1 y 2 + x 3 y 4 = x 4 y 6

```python
Vector(1, 2) + Vector(3, 4) == Vector(4, 6)
```

Those of you who know a bit of physics will recognize this equation as a simple velocity integration.
The update event is one of the clock events ppb has, and provides a time_delta:
the amount of time from the last call to this call.
By multiplying velocity by the time_delta we get the amount of change in position since the last update.
Add that to the old position, and we have our new position.

(See what I mean by vectors having some cool features?)

So now, let's run our game and get to the game screen. Remember, don't click
once you're in the game screen! That'll take you to the end screen. The ball
should slide off the top of the screen.