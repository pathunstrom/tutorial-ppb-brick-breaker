Now we need the last element of our gameplay: the bricks we plan to break.

A lot of what we've built so far is going to be useful for our bricks, so let's
throw together our basic block:

```python
class Block(ppb.Sprite):
    hits = 3
    colors = [
        ppb.Square(200, 20, 20),
        ppb.Square(50, 150, 70),
        ppb.Square(10, 10, 100),
    ]
    image = colors[hits - 1]
```

This setup may look weird, but bear with me.
A ppb.Sprite defaults to 1 unit x 1 unit
(about the same size as our ball right now.)
We set a couple of ppb.Squares in various colors that we'll make the image attribute.
Then we set our image to the default square.

Next, we're going to give our block an event handler to respond to an event that the ball will throw when it hits.

```python
def on_brick_struck(self, event, signal):
    self.hits -= 1
    if self.hits <= 0:
        event.scene.remove(self)
```

This is a very simple handler:
If the brick gets a brick_struck event, it'll reduce its hits by 1.
Then, if the health is 0 or less, remove it.

Let's define the event, add an import: `from dataclasses import dataclass`

Then we'll define a dataclass as our event:

```python
@dataclass 
class BrickStruck:
    scene: ppb.Scene = None
```

We initialize this to `None` so we can make an event instance without providing the current scene.
Now, let's go back to the ball and have it check for collision against the Bricks.
This will look similar to how we check for the walls.
Get the bricks from the scene, then iterate.
Then we reflect off of a normal from the center of the brick to the ball position.

```python
bricks = event.scene.get(kind=Brick)
for brick in bricks:
    if self.collides(brick):
        normal = (self.position - brick.position).normalize()
        self.velocity = self.velocity.reflect(normal)
        signal(BrickStruck(), targets=[brick])
```

After that, we're going to use the signal function, but we're changing it up a little:
We send an empty BrickStruck() event, but we'll include a second keyword argument:
`targets` is an iterable that tells the engine which objects you want to send the message to.

What this means is each BrickStruck event will go to exactly 1 brick.
That way, the on_brick_struck only responds when the individual brick is struct,
and we don't decrement all the bricks when any individual gets  struck.

There's just one more thing we want to do, and that's change the image before the brick is rendered.
To do that, we'll set up an `on_pre_render` event.

```python
def on_pre_render(self, event, signal):
    self.image = self.colors[self.hits - 1]
```

We want to make this happen in the pre_render because it only matters when we render
which happens about 30 times per second, versus on each update which defaults to 60 times per second.
When you're doing presentational things,
like shifting the image,
or setting the position of ui elements,
it's best practice to do them during the pre_render.

The last step is to put our bricks in our scene.
Let's import product from itertools.
This lets us make a single loop for x, y grid versus nested loops.

In the game init:

```python
for x, y in product(range(-9, 12, 3), range(-4, 15, 3)):
    self.add(Brick(position=ppb.Vector(x, y)))
```

We're going to do one more thing before we end this section:

Let's add a lose condition:

When the ball hits the bottom of the screen, we're going to end the game scene.
First, add an attribute to our wall class: `deadly`.
Set the default to False.

```python
class Wall(ppb.RectangleSprite):
    normal = ppb.directions.Down
    deadly = False
```

Then in the game setup, pass deadly=True to the second wall
(that's the one with the normal of up)

```python
class Game(ppb.Scene):
    background_color = (25, 50, 25)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add(Ball())
        self.add(Wall(width=26, position=ppb.Vector(0, 16.5)))
        self.add(Wall(width=26, position=ppb.Vector(0, -16.5), normal=ppb.directions.Up, deadly=True))
        self.add(Wall(height=34, position=ppb.Vector(12, 0), normal=ppb.directions.Left))
```

Finally, in the ball update handler, where we check if a wall has collided
we check if the wall is deadly, then signal a replace scene to the end screen.

```python
def on_update(self, event, signal):
    self.position += self.velocity * event.time_delta
    walls = event.scene.get(kind=Wall)
    for wall in walls:
        if self.collides(wall):
            self.velocity = self.velocity.reflect(wall.normal)
            if wall.deadly:
                signal(ppb.events.ReplaceScene(EndScreen))
```

And now we have a fully functioning game!
With the knowledge you have from the title screen, you should be able to add a
message to the end screen.
