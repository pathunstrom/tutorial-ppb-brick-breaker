Now that we have a window, we're going to want to do something with it! The
first thing I suggest we do is change the resolution of the window. The run
function passes any "extra" keyword arguments to the engine, who can pass them
to various subsystems, like the renderer. Breakout is generally played in a tall
game view, instead of a wide one. The default resolution is 800 pixels wide by
600 pixels tall. We're going reverse that so our window is tall:

```python
import ppb

ppb.run(resolution=(600, 800))
```

Next, we need to think about the structure of the game. I follow a method
another game dev helpfully refers to as the shell method:

We're going to make a "complete" (but bare) game, then slowly add to that.

We'll start by thinking through all the screens we need:

1. We'll want a title or menu screen.
2. We'll want a gameplay screen.
3. We'll want a game over screen.

In ppb, we call different parts of a game Scenes. (Side note: These three
screens can be models without scenes, but for this tutorial, this is a helpful
model.)

When you call `ppb.run()` it'll make an empty scene for you if you don't provide
one. We're now going to define a set of scenes and start wiring them up.

First, lets define our scenes:

```python
class TitleScreen(ppb.Scene):
    pass

class Game(ppb.Scene):
    pass

class GameOver(ppb.Scene):
    pass
```

Right now, none of these scenes is doing anything special, so let's do something
to make sure we know one is running.

Replace the `pass` in TitleScreen with `background_color = (0, 0, 0)`.

Then we're going to pass TitleScreen to the run function as the keyword argument
`starting_scene`

```python
import ppb


class TitleScreen(ppb.Scene):
    background_color = (0, 0, 0)

ppb.run(starting_scene=TitleScreen, resolution=(600, 800))
```

If this is working correctly, instead of a blue screen, you'll have a black one.

At this point, let's talk about color tuples: background_color and any other
color arguments we encounter take either individual red green and blue values or
a tuple of all three `(red, green, blue)`. The minimum value for any of these is
0, and the maximum is 255, and they should always be integers. (You may
recognize this as an 8 bit value.)

In the sample, all 0s is the color black. You can put in any RGB color value
here to customize your version of the game.

Back to wiring up our game.

Now that we have our title screen up, we're going to need a way to move to the
game scene. In order to do that, we're going to need events!

Let's respond to a user pressing _any_ mouse button or key by moving to the next
scene.

To respond to events in ppb, you need to write a method called
`on_the_name_of_the_event`. The name of the key events we care about are
KeyReleased and ButtonReleased so let's work through them.

```python
class TitleScreen(ppb.Scene):
    background_color = (0, 0, 0)
    
    def on_key_released(self, event, signal):
        pass
```

So this is what a key up handler looks like. The name of the function is
important, but always follows this pattern. The signature is always the same:
An instance of the event class and a signal function. We'll use the event
instance much more later, but we need the signal function right now.

```python
import ppb.events


def on_key_released(self, event, signal):
    signal(ppb.events.StartScene(Game))
```

StartScene is an event we like to call command events. They're a way to request
some part of the game performs an action. Their attributes are like parameters
if you called a function directly. In this case, we're telling ppb to add a new
scene to the scene stack. (Don't worry too much about this, I'll explain the
behavior as we go.) In this case, the Menu will get paused, and the Game scene
will get started and sit on top of the stack.

Let's try running this again. Notice when you press any keyboard key the color
changes. Now, we can add the same code for on_button_released to work with mouse
buttons.

Next, we're going to do the same basic process for Game, but we're going to use
a different command event.

```python
class Game(ppb.Scene):
    background_color = (25, 50, 25)
    
    def on_key_released(self, event, signal):
        signal(ppb.events.ReplaceScene(EndScreen))

    def on_button_released(self, event, signal):
        signal(ppb.events.ReplaceScene(EndScreen))
```

Notice I've changed the color of my game scene, so I know when it's active.
Instead of StartScene, we're using ReplaceScene. In this case, the engine is
going to stop and discard the Game scene, then replace it with our EndScreen.

Go ahead and test it, and we'll duplicate this process one more time on the
EndScreen, but replace ReplaceScene with StopScene and make sure to remove the
argument. In terms of what the engine
does, it's going to stop and discard the running EndScreen, but not replace it.

Because we left the Menu running earlier, the engine knows to step down the
stack and start using that already running scene. If we do StopScene with the
last running scene, the engine will gracefully quit.

```python
class EndScreen(ppb.Scene):
    background_color = (50, 25, 25)

    def on_key_released(self, event, signal):
        signal(ppb.events.StopScene())

    def on_button_released(self, event, signal):
        signal(ppb.events.StopScene())
```

Now, when we run our game, we can move from our black Title, to our Green Game,
to our Red End, which then goes back to the Black Title.

This is the entire structure for our game. Now, we need to add to it.
