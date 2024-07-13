init python:
    import pygame

    class Example(renpy.Displayable):
    
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

screen test_screen():
    default game = Example('eileen happy')
    add game

label start:
    call screen test_screen()
    return
