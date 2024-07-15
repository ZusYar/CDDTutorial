init python:
    import pygame

    class Example(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.image = At(renpy.displayable(background), basic_transform)
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)

            child_render = renpy.render(self.image, width, height, st, at)
    
            # size and half-size for convenience
            child_width, child_height = child_render.get_size()
            half_width, half_height = child_width // 2, child_height // 2
            new_render.blit(child_render, (self.x - half_width, self.y - half_height))

            renpy.redraw(self, 0)
            return new_render 

        def event(self, ev, x, y, st):
            if x >= 0 and y >= 0:
                self.x, self.y = x, y
            raise renpy.IgnoreEvent

transform basic_transform:
    zoom 0.5
    parallel:
        ease 3.0 blur 4.0
        ease 3.0 blur 0.0
        repeat
    parallel:
        linear 1.0 alpha 0.1
        linear 1.0 alpha 1.0
        repeat
    parallel:
        linear 0.5 matrixcolor TintMatrix('#F00')
        linear 0.5 matrixcolor TintMatrix('#0F0')
        linear 0.5 matrixcolor TintMatrix('#00F')
        repeat
    parallel:
        rotate 0
        linear 3.5 rotate 360
        repeat

screen test_screen():
    default game = Example(background='eileen concerned')
    add game

label start:
    call screen test_screen()
    return
