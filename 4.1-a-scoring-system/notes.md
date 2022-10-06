Now, let's add a scoring system to the game.

First, we need to write a ppb system.
A system is a way to extend the ppb engine to do more.

Let's create our scoring system:

```python
class Scoring(ppb.systemslib.System):

    def __init__(self, **kwargs):
        self.score = 0

    def on_scene_started(self, event, signal):
        if isinstance(event.scene, Game):
            self.score = 0
```

ppb systems are initialized by the engine and need to accept all the keywords.
Remember when we passed resolution to the run function?
That will end up passed to all the systems, but only the renderer cares about it.

Then we want to check when a Game scene starts using the `on_scene_started` handler.
We just reset the score if the new scene is a Game scene.

Let's add a new handler for an event that doesn't exist yet:
`on_brick_destroyed`:

```python
def on_brick_destroyed(self, event, signal):
    self.score += event.value
```

So, this is all the code we need to get what we want, but it helps us figure out the shape of the event:
We know the name of the class is BrickDestroyed based on the pattern of ppb's event handlers.
We know that it's going to have a value attribute.
It's also going to have a scene attribute because every event needs one.

Let's write that:

```python
@dataclass
class BrickDestroyed:
    value: int
    scene: ppb.Scene = None
```

The last step is to update our Bricks.

First, let's give each brick a value.
It'll default to 1, but when you instantiate it, you can change this value as before.
Then in the on_brick_struck, if the brick dies, we signal a BrickDestroyed with the brick's value.

```python
def on_brick_struck(self, event, signal):
    self.hits -= 1
    if self.hits <= 0:
        event.scene.remove(self)
        signal(BrickDestroyed(self.value))
```

Now we have a scoring system that is keeping track of our score.
The next step is to display it.
To do that, we need a sprite, let's call it Score.

```python

```

Then we will update the scoring system to get the engine,
which is always passed upon initialization.
To help us out, let's typehint `engine: ppb.Engine` in the class body.
```python
class Scoring(ppb.systemslib.System):
    engine: ppb.GameEngine
```

Then we'll write a function that takes an event, and adds a score to it.

```python
def set_score(self, event):
    event.score = self.score
```

And finally, in the `__init__` call self.engine.register,
pass it the PreRender event type, and our new set_score method.

Lastly, we wire everything up.

In the game, add the score sprite.

And to the run function we add `systems=[Scoring]`