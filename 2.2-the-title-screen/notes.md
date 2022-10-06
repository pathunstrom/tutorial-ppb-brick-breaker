Let's focus on our Title screen.
We'll add a title.
The first thing we'll need to do is set up an `__init__` like so:

```python
def __init__(self, **kwargs):
    super().__init__(**kwargs)
```

This might seem odd, so let me explain the Game Object Model briefly:
Almost everything in ppb matches a protocol we call GameObjects.
So far, you've seen the engine run and written a couple of Scenes.
Later we'll be using Sprites and Systems.

The key things to know about game objects is:

* that they're all containers with add and remove methods
* all have a flexible `__init__` built in

The init only takes keyword arguments, but then sets attributes for each one.
So if you pass `color=(1, 2, 3)` to the constructor, it will set scene.color to (1, 2, 3)

We're going to add a child object to our scene. First, you should have a font
file (there's one in the resource folder). Put that in your project directory
and then at the top of your file, we'll add a FONT constant:

```python
import ppb

FONT = ppb.Font("RugenExpanded-DOKGE.otf", size=72)
```

ppb has an asset system that knows how to look up files on the python path.
Since we're keeping this font right next to our script, we can just reference it
by name. If you wanted, you could keep your assets organized in a resources
folder, you just need to include the name of that folder in the name string.

Now, in our init, we're going to add a sprite that can display our title:

```python
import ppb


def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.add(ppb.Sprite(
        image=ppb.Text("Block Breaker", font=FONT, color=(220, 220, 220)),
        size=2,
    ))
```

Now run your game again.

You'll notice the title appears at the middle of the screen. This is enough for
now, so let's move on to the next step.
