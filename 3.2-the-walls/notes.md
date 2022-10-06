So we have a ball that moves, but it goes off the screen.
Breakout takes place all on one screen, so let's set up keeping the ball inside.
There's a couple of strategies we could use for this.
One would be to check for the balls position against the various sides of the camera frame.
That's fairly simple, but I'd like the walls to be visible,
so we're going to use sprites to represent the walls.

First, let's fine out what the width and heigh of the play field is in game units.
We could calculate this by hand, but the camera keeps this information.
In the Title screen's button or key handler, add the following:

```python
def on_key_released(self, event, signal):
    signal(ppb.events.StartScene(Game))
    cam = event.scene.main_camera
    print(f"Width: {cam.width}, Height: {cam.height}")
```

Now run the game and use the input type you modified.
If you followed my lead, hit your spacebar.

You should see the following output:
`Width: 25.0, Height: 33.333333333333336`

So we know the game unit distance from left to right is 25 units,
and the top to bottom distance is 33 and 1/3.

We want our side walls taller than 33 units, and our top and bottom
walls should be wider than 25 units.

You'll notice that the event instance has the scene attached to it.
We'll be using this feature a lot,
but know that the engine will always put the current scene on an event.

Let's start a new class called Wall. It'll subclass RectangleSprite.

```python
import ppb


class Wall(ppb.RectangleSprite):
    def __init__(self, width=1, height=1, color=(220, 220, 220), **kwargs):
        super().__init__(width=width, height=height, color=color, **kwargs)
        self.image = ppb.Rectangle(*color, aspect_ratio=(width, height))
```

So I want our walls to be fairly easy to instantiate, but the Rectangle asset
for images needs to know its aspect ratio to work correctly. We cheat by just
sending width and height to the aspect ratio property and let the engine
calculate it for us. We don't need event handlers here, so let's put some walls
in our scene.

In the Game init:

```python
import ppb


def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.add(Ball())
    self.add(Wall(width=26, position=ppb.Vector(0, 16.5)))
    self.add(Wall(width=26, position=ppb.Vector(0, -16.5)))
    self.add(Wall(height=34, position=ppb.Vector(13, 0)))
    self.add(Wall(height=34, position=ppb.Vector(-13, 0)))
```

Run our game now, and we have white walls on each side of the screen.
Only. . . our ball goes right through them.
ppb doesn't handle collisions for you, so you have to write your own.
Let's add some details to our walls: A surface normal vector.
It's best practice to add this to the class as a default, even though we're going to be setting it
with the magic init.

```python
class Wall(ppb.RectangleSprite):
    normal = ppb.directions.Down
```

Now in our init, lets update our calls to Wall:

```python
import ppb.directions

self.add(Wall(width=26, position=ppb.Vector(0, 16.5)))
self.add(Wall(width=26, position=ppb.Vector(0, -16.5), ppb.directions.Up))
self.add(Wall(height=34, position=ppb.Vector(13, 0), ppb.directions.Left))
self.add(Wall(height=34, position=ppb.Vector(-13, 0), ppb.directions.Right))
```

So what's a surface normal?
It's a normal vector that is facing perpendicularly away from a surface.
Our walls represent surfaces, so we add these so that we can "bounce" the ball off them.
You'll notice I didn't pass one in for our top wall
(It uses the default)
and that the other three use the direction that is opposite their position.

Now, let's teach the ball how to bounce.

After we update our position, we're going to grab the scene from the update event
and get the walls.

```python
walls = event.scene.get(kind=Wall)
```

Next, let's write a helper function to see if the ball collides with another
object.

```python
def collides(self, other):
    combined_width = self.width + other.width
    combined_height = self.height + other.height
    max_vertical = max(self.top, other.top) - min(self.bottom, other.bottom)
    max_horizontal = max(self.right, other.right) - min(self.left, other.left)
    return max_vertical < combined_height and max_horizontal < combined_width
```

This has a lot going on, but it's a collision algorithm you'll use a lot in video games.
You should definitely spend some time later testing it either on graph paper or in ppb.
Just know that this will tell us if our bounding boxes (the edges of the sprites)
intersect.

Now back to our update function:

We're going to loop over the walls, and check if we've collided with them. If we
do, we reflect our velocity across the normal.

```python
def on_update(self, event, signal):
    self.position += self.velocity * event.time_delta
    walls = event.scene.get(kind=Wall)
    for wall in walls:
        if self.collides(wall):
            self.velocity = self.velocity.reflect(wall.normal)
```

If we run the program now, the ball should stay in bounds. But it's only going
straight up and down, so go ahead and pick a different direction like UpAndLeft
instead. 