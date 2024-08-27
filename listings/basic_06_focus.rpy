init python:
    import pygame
    from math import sin

    class Example(renpy.Displayable):
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
        
        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)

            d = self.pressed if self.lmb_pressed else self.state
            if callable(self.transform):
                d = self.transform(d)

            child = renpy.render(d, width, height, st, at)
            w, h = child.get_size()
            rv.blit(child, (0, 0))
            
            rv.add_focus(self, None,
                0, 0, w, h,
                0, 0, rv)
 
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

screen test_screen(obj):
    default game = obj

    add game at transform:
        alpha 0.5
        on idle:
            linear 0.5 alpha 0.5
        on hover:
            linear 0.5 alpha 1.0

label start:
    call screen test_screen(
        obj = Example(
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
