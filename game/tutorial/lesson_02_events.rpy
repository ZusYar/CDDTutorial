label lesson_02_events:
    scene background
    show nvl

label .section_1:

    "Let's talk about events."

    show example lesson_02_01a

    "CDD's {a=https://www.renpy.org/doc/html/cdd.html#renpy.Displayable.event}def event(){/a} method is responsible for processing external events. It's doing absolutely nothing at the moment."
    "Consider the arguments:"
    "{=green}ev{/green} - the event itself. More details available in {a=http://www.pygame.org/docs/ref/event.html}pygame{/a} docs."
    "{=green}x, y{/green} - coordinates of the event that occurred, relative to the upper left corner of the CDD."
    "{=green}st{/green} - a float, the shown timebase, in seconds."
    "We will only process the events we are interested in, so everything else should be ignored."

    show example lesson_02_01b

    "To do this, the event must throw a special exception {a=https://www.renpy.org/doc/html/cdd.html#renpy.IgnoreEvent}renpy.IgnoreEvent{/a}."
    
    nvl clear
    hide example

    "It's time to find out what events exist."
    "According to the {a=http://www.pygame.org/docs/ref/event.html}pygame documentation{/a}, this could be {=green}KEYDOWN, KEYUP{/green} for the keyboard,"
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

    show example lesson_02_01f

    "Note, that in CDD, you don't need to check the event type for this, because the coordinates {=green}x, y{/green} are already passed to {=blue}event{/blue} method."
    
    nvl clear
    show example lesson_02_02a

    "Let's initialize our CDD with starting {=green}x, y{/green} positions at 0 (upper left corner)."

    show example lesson_02_02b

    "Fix the {=blue}render{/blue} and let it actually utilize the object's {=green}x, y{/green}."

    show example lesson_02_02c

    "And don't forget to update the coordinates every time the {=blue}event{/blue} method triggers."

    hide example
    nvl clear
    show example lesson_02_03a large

    "Let's see if it's working."

    hide example
    nvl clear

    call screen lesson_test_screen(
        obj = lesson_02.Example_1('eileen happy'),
        desc = _("Sadly, it doesn't move. But why?")
    )

label .section_2:

    "The thing is that although we have updated the data inside the CDD, ren'py does not know when it needs to be redrawn."

    show example lesson_02_04a small

    "{a=https://www.renpy.org/doc/html/cdd.html#renpy.redraw}renpy.redraw{/a} function comes to the rescue."
    "It causes the displayable {=green}d{/green} to be redrawn when {=green}when{/green} seconds have elapsed."

    show example lesson_02_04b

    "We are going to use it from our CDD, which is a displayable, thus {=green}d{/green} will refer to {=green}self{/green}, and {=green}when{/green} should indicate \"we want it as soon as possible\", in other words - it's 0."

    nvl clear
    show example lesson_02_04c

    "Because we update {=green}x, y{/green} constantly, let's put it into the {=blue}render{/blue} method, making it refresh itself every time the displayable is rendered."

    hide example
    show example lesson_02_05a large

    "Is this enough yet? Let's run the code and find out."

    hide example
    nvl clear

    call screen lesson_test_screen(
        obj = lesson_02.Example_2('eileen happy'),
        desc = _("It's alive!")
    )

label .section_3:

    "As you might have noticed, if you move the cursor off the screen, the position is set to (-1, -1), which is not always appropriate."
    "Besides, there was no need to check the events, which makes the lesson rather pointless."

    show example lesson_02_06a small

    "Therefore, now we will correct the positioning, and in order not to overload the {=blue}event{/blue} method itself with unnecessary information, we will move the logic into a separate method."

    show example lesson_02_06b

    "And we will do this update only if you press the mouse button."
    "However, the wheel also counts, therefore we will limit ourselves to two mouse buttons: left and right."

    show example lesson_02_06c
    nvl clear

    "Unlike keyboard events, rather than checking {=green}ev.key{/green}, we will have to check {=green}ev.button{/green}."
    "Here's a little reference:\n1 - left click\n2 - middle click\n3 - right click\n4 - scroll up\n5 - scroll down."

    hide example
    nvl clear
    show example lesson_02_07a large

    "This is what happened in the end."

    show example lesson_02_07b

    "On the second thought, if we only move the picture when the mouse is clicked, it would be smart to tell ren'py to redraw it only when necessary, for the sake of performance."

    hide example
    nvl clear

    call screen lesson_test_screen(
        obj = lesson_02.Example_3('eileen happy'),
        desc = _("Clicking on the screen makes Eileen teleport."),
        close = True
    )

    return

############ DATA ##############

init python in lesson_02:
    from renpy.display.image import ImageReference
    import pygame

    class Example_1(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = ImageReference(background)
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            new_render.place(self.background, self.x, self.y)
            return new_render 

        def event(self, ev, x, y, st):
            self.x, self.y = x, y
            raise renpy.IgnoreEvent
            
    class Example_2(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = ImageReference(background)
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            new_render.place(self.background, self.x, self.y)
            renpy.redraw(self, 0)
            return new_render 

        def event(self, ev, x, y, st):
            self.x, self.y = x, y
            raise renpy.IgnoreEvent

    class Example_3(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = ImageReference(background)
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            new_render.place(self.background, self.x, self.y)
            return new_render 

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONUP:
                if ev.button in (1, 3):
                    self.update_position(x, y)
            raise renpy.IgnoreEvent

        def update_position(self, x, y):
            if x >= 0 and y >= 0:
                self.x, self.y = x, y
                renpy.redraw(self, 0)
