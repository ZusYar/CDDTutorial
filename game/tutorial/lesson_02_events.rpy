label lesson_02_events:
    scene background
    show nvl

    "Let's talk about events."

    show example lesson_02_01a

    "CDD's {=blue}def event(){/blue} method is responsible for processing external events."
    "It's doing absolutely nothing at the moment."
    "Consider the arguments:"
    "ev is the event itself."
    "x, y - coordinates of the event that occurred, relative to the upper left corner of the CDD."
    "st - shown timebase."
    "We will only process the events we are interested in, so everything else should be ignored."

    show example lesson_02_01b

    "To do this, the event must throw a special exception {=red}renpy.IgnoreEvent{/red}."
    
    nvl clear
    hide example

    "It's time to find out what events exist."
    "According to the pygame documentation, this could be {=green}KEYDOWN, KEYUP{/green} for the keyboard,"
    "{=green}MOUSEBUTTONUP, MOUSEBUTTONDOWN{/green} for mouse"
    "{=green}JOYBUTTONUP, JOYBUTTONDOWN{/green}, etc. for the gamepad"
    "As well as others, including {=green}VIDEORESIZE{/green}."

    nvl clear
    show example lesson_02_01c

    "For example, this is how you can intercept a button press on the keyboard"

    show example lesson_02_01d

    "The pygame module will, of course, have to be imported first."

    show example lesson_02_01e

    "As a rule, it is also necessary to clarify which button was pressed, so in addition to the event type, the button code is checked."
    "Once an event has been identified, all that remains is to react to it."

    hide example
    nvl clear

    "But let's get back to our code."
    "As an exercise, have Eileen move around with the mouse pointer."
    extend "(I think this is the simplest thing you can think of)"
    "Note, that in CDD, you don't need to check the event type for this, because the coordinates {=green}x, y{/green} are already passed to {=blue}event{/blue} method."

    nvl clear
    show example lesson_02_02a

    "Let's add a starting position (0, 0) to the initialization method."

    show example lesson_02_02b

    "fix the render."

    show example lesson_02_02c

    "And let's force the {=blue}event{/blue} method to update this position."

    nvl clear
    show example lesson_02_03a large

    "Let's see how it works :-)"

    hide example
    nvl clear

    call screen lesson_02__test_screen_1()

    "As we have seen, if you move the cursor off the screen, the position is set to (-1, -1), which is not always appropriate."
    "Besides, there was no need to check the events, which makes the lesson rather pointless."

    show example lesson_02_02d small

    "Therefore, now we will correct the positioning, and in order not to overload the {=blue}event{/blue} method itself with unnecessary information, we will move the logic into a separate method."

    show example lesson_02_02e

    "And we will do this update only if you press the mouse button."
    "However, the wheel also counts, therefore we will limit ourselves to two mouse buttons: left and right."

    show example lesson_02_02f
    nvl clear

    "Unlike keyboard events, rather than checking {=green}ev.key{/green}, we will have to check {=green}ev.button{/green}."
    "Here's a little reference:\n1 - left click\n2 - middle click\n3 - right click\n4 - scroll up\n5 - scroll down."


    hide example
    nvl clear
    show example lesson_02_03b large

    "This is what happened in the end."
    "(Reminder: clicking on the screen moves Eileen.)"

    hide example

    call screen lesson_02__test_screen_2()

    return

############ DATA ##############

init python in lesson_02:
    from renpy.display.image import ImageReference
    import pygame

    class Example_1(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = ImageReference(background)
            self.pos = (0, 0)

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            child_render = renpy.render(self.background, width, height, st, at)
            new_render.blit(child_render, self.pos)
            renpy.redraw(self, 0)
            return new_render 

        def event(self, ev, x, y, st):
            self.pos = (x, y)
            raise renpy.IgnoreEvent
            
    class Example_2(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = ImageReference(background)
            self.pos = (0, 0)

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            child_render = renpy.render(self.background, width, height, st, at)
            new_render.blit(child_render, self.pos)
            renpy.redraw(self, 0)
            return new_render 

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONUP:
                if ev.button in (1, 3):
                    self.update_position(x, y)
            raise renpy.IgnoreEvent

        def update_position(self, x, y):
            if x >= 0 and y >= 0:
                self.pos = (x, y)

screen lesson_02__test_screen_1():
    default game = lesson_02.Example_1('eileen happy')
    add game
    dismiss action Return()

screen lesson_02__test_screen_2():
    default game = lesson_02.Example_2('eileen happy')
    add game
    textbutton "CLOSE" action Return() xalign 1.0