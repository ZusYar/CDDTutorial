label basic_06_focus:

    scene background
    show nvl
    
label .section_01:

    "In this lesson we will discuss focus."
    "What might this be needed for?"

    show focus_illustration at truecenter

    "When a CDD is on screen, it captures all events, and we might want to restrict the area it's responding, while ignoring all the events outside of the given area."

    nvl clear
    hide focus_illustration
    show example basic_06_01a large

    "There's a method {=blue}add_focus{/} which does exactly that when applied to a render. It's not described anywhere in the docs, so here's what it says in the sources."
    "As far as I can assume, {=green}arg{/} is there to differentiate between instances of the same displayable, sort of like a tag."
    
    nvl clear

    "And since the rest of text doesn't look self-explanatory and consistent with the rest of args, {=green}x, y, w, h{/} represent the focus rectangle, {=green}mask{/g} can be used to implement focus_mask, with {=green}mx, my{/} being mask offset values."

    hide example

    "But before implementing the focus, let me demostrate something very quickly. I'll place a displayable somewhere away from the corner of the screen."

    call screen test_screen(
        obj = basic_06_focus.Example_0( Transform('eileen_rectangles', zoom=0.5), xpos=300, ypos=100),
        desc = 'CDD captures x/y position relative to its upper-left corner, not the screen corner.',
        close=True
    )

    nvl clear

    "This is usually helpful, but is it possible to retrieve the actual CDD position?"
    "There is no reliable way, unless you provide the required data yourself, for example passing args to its init method."
    "To automate the process, you can design your own {a=https://www.renpy.org/doc/html/screen_python.html#creator-defined-screen-language-statements}screen language displayable{/a} which will provide position through renpy style subsystem, but this takes us too far from the topic, and therefore remains as homework."

label .section_02:

    nvl clear
    show example basic_06_01b

    "Ok, now we will add a rectangular focus to our render."

    show example basic_06_01c

    "From now on the displayable takes part in ren'py focus mechanics, and filtering its events becomes as simple as checking {=blue}is_focused(){/}."
    
    hide example
    nvl clear

    call screen test_screen(
        obj = basic_06_focus.Example_1( Transform('eileen_rectangles', zoom=0.5), xpos=300, ypos=100),
        desc = 'Keeping mouse x, y position only when our CDD is focused',
        close=True
    )

label .section_03:

    "Let's create something useful now, for example, a button that imitates its pressed state."

    show button_skins at truecenter

    "These will be our idle, hovered and pressed images."
    
    show button_skins at truecenter, Transform(matrixcolor=SaturationMatrix(0.0))

    show example basic_06_02a small
    
    "Defining the displayable. Note, how xpos/ypos are there too, easily passable further to renpy.Displayable constructor."

    hide button_skins
    show example basic_06_02b

    "Another nuance will be cropping the original full-size images with a transform, passed to the CDD."

    nvl clear
    hide example
    show example basic_06_02c large

    "Standard init method, calling renpy.Displayable and memorizing arguments. One of not that obvious things is {=green}state{/}, set to idle by default, and another one is {=green}lmb_pressed{/}, supposed to indicate if the mouse button is pressed."

    show example basic_06_02d

    "We will update the {=green}lmb_pressed{/} variable on mouse button up / down events like this (remember, we're doing it only when the CDD is focused)."

    nvl clear
    show example basic_06_02e

    "The only lines added to the render are here: selecting the picture to show, depending on {=green}state{/} and {=green}lmb_pressed{/}, applying the {=green}transform{/} before rendering."
    "The last thing that is still obscure - swapping idle and hover, and it's time to introduce two more methods to implement."

    hide example
    show example basic_06_02f small
    
    "Focus and unfocus update {=green}state{/} accordingly."

    show example basic_06_02g

    "We will also clear {=green}lmb_pressed{/} in case we're leaving the focus area."

    nvl clear
    hide example
    show example basic_06_02h large

    "Full source to inspect one more time."

    nvl clear
    hide example

    call screen test_screen(
        obj = basic_06_focus.Example_2(
            idle='eileen concerned',
            hovered='eileen happy',
            pressed='eileen vhappy',
            transform=Transform(crop=(0, 0, 300, 300)),
            xpos=400, ypos=100
        ),
        desc='This button supports idle, hover and press',
        close=True
    )

label .section_04:

    "In the last section of the lesson we will additionally implement a couple of useful features."
    "Assume we need to apply focus_mask to our improvised button."

    show example basic_06_03a small

    "To do this, we can simply specify the same render object as a mask to itself. (Alternatively, you can provide and render any other picture)"
    "Don't forget setting {=green}mx / my{/} to 0."

    nvl clear
    hide example

    "Another useful trick is that displayables support {=blue}set_transform_event(){/} method. Basically this means you can tell it when to trigger {a=https://www.renpy.org/doc/html/screens.html#on}atl events{/a} like show, hide."

    show example basic_06_03b large

    "Note how simple this is to implement."

    show example basic_06_03c

    "Let's compose a quick test transform to our displayable."

    nvl clear
    show example basic_06_03d

    "We pass x/y coordinates as args to the button when calling the screen."

    show example basic_06_03e

    "Oh, it's a button, right? Let's give it a simple action."

    show example basic_06_03f

    "And make sure to call it when click is occured."

    nvl clear
    hide example

    call screen test_screen_basic_6(
        obj = basic_06_focus.Example_3(
            idle='eileen concerned',
            hovered='eileen happy',
            pressed='eileen vhappy',
            transform=Transform(crop=(0, 0, 300, 300)),
            xpos=400, ypos=100,
            action=Notify('click'),
            masked=True,
        )
    )

    return

############ DATA ##############

init python in basic_06_focus:

    import pygame
    from store import Text

    class Example_0(renpy.Displayable):
        def __init__(self, widget, **kwargs):
            super().__init__(**kwargs)
            self.widget = renpy.displayable(widget)
            self.x, self.y = 0, 0
        
        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            child = renpy.render(self.widget, width, height, st, at)
            w, h = child.get_size()
            rv.blit(child, (0, 0))
            rv.place(Text(f'position: x={self.x}, y={self.y}'), 0, 0)

            rv.add_focus(self, None,
                0, 0, w, h,
                None, None, None)

            return rv 
    
        def event(self, ev, x, y, st):
            self.x, self.y = x, y
            renpy.redraw(self, 0)
            raise renpy.IgnoreEvent

    class Example_1(Example_0):
        def event(self, ev, x, y, st):
            if not self.is_focused():
                return None

            self.x, self.y = x, y
            renpy.redraw(self, 0)
            raise renpy.IgnoreEvent

    class Example_2(renpy.Displayable):
        def __init__(self, idle, hovered, pressed, transform=None, action=None, **kwargs):
            super().__init__(**kwargs)
            self.idle = renpy.displayable(idle)
            self.hovered = renpy.displayable(hovered)
            self.pressed = renpy.displayable(pressed)
            self.transform = transform
            self.action = action

            self.x, self.y = 0, 0
            self.state = self.idle
            self.lmb_pressed = False
            self.masked = kwargs.get('masked')
        
        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            d = self.pressed if self.lmb_pressed else self.state
            if callable(self.transform):
                d = self.transform(d)
            child = renpy.render(d, width, height, st, at)
            w, h = child.get_size()
            rv.blit(child, (0, 0))
            
            mx, my, mask = None, None, None
            if self.masked:
                mx, my, mask = 0, 0, rv
            rv.add_focus(self, None,
                0, 0, w, h,
                mx, my, mask)
 
            return rv 
    
        def event(self, ev, x, y, st):
            if not self.is_focused():
                return None

            self.x, self.y = x, y
            if ev.type == pygame.MOUSEBUTTONDOWN:
                self.lmb_pressed = True
                renpy.redraw(self, 0)
            elif ev.type == pygame.MOUSEBUTTONUP:
                self.lmb_pressed = False
                renpy.redraw(self, 0)
                if callable(self.action):
                    self.action()
            raise renpy.IgnoreEvent

        def focus(self, default=False):
            super().focus(default)
            self.state = self.hovered

        def unfocus(self, default=False):
            super().unfocus(default)
            self.state = self.idle
            self.lmb_pressed = False

    class Example_3(Example_2):
        def focus(self, default=False):
            super().focus(default)
            self.state = self.hovered
            self.set_transform_event("hover")

        def unfocus(self, default=False):
            super().unfocus(default)
            self.state = self.idle
            self.lmb_pressed = False
            self.set_transform_event("idle")

image focus_illustration = Composite((400, 240),
    (0, 0), Transform(Solid('#e09bee'), size=(400, 240)),
    (200, 50), Transform(Solid('#55dd11'), size=(100, 80)),
    (8, 8), Text('ignore'),
    (208, 58), Text('capture'),
)

image button_skins = Composite((900, 300),
    (0, 0), Transform('eileen concerned', crop=(0, 0, 300, 300)),
    (300, 0), Transform('eileen happy', crop=(0, 0, 300, 300)),
    (600, 0), Transform('eileen vhappy', crop=(0, 0, 300, 300)),
    (0, 0), Text('idle'),
    (300, 0), Text('hovered'),
    (600, 0), Text('pressed'),
)

screen test_screen_basic_6(obj):
    default game = obj

    add game at transform:
        alpha 0.5
        on idle:
            linear 0.5 alpha 0.5
        on hover:
            linear 0.5 alpha 1.0

    textbutton "CLOSE" action Return() xalign 1.0 yalign 0.05