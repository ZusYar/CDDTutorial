init python:
    import pygame
    from math import sin

    class Example(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = ImageReference(background)
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            child_render = renpy.render(self.background, width, height, st, at)
    
            # size and half-size for convenience
            child_width, child_height = child_render.get_size()
            half_width, half_height = child_width // 2, child_height // 2

            # split the render into 4 rectangles
            lt = child_render.subsurface((0, 0, half_width, half_height))
            rt = child_render.subsurface((half_width, 0, half_width, half_height))
            lb = child_render.subsurface((0, half_height, half_width, half_height))
            rb = child_render.subsurface((half_width, half_height, half_width, half_height))

            max_distance = 100
            current_distance = abs(sin(st) * max_distance)
            
            # display the rectangles around the mouse pointer
            new_render.blit(lt, (self.x - half_width - current_distance, self.y - half_height - current_distance))
            new_render.blit(rt, (self.x + current_distance, self.y - half_height - current_distance))
            new_render.blit(lb, (self.x - half_width - current_distance, self.y + current_distance))
            new_render.blit(rb, (self.x + current_distance, self.y + current_distance))

            renpy.redraw(self, 0)
            return new_render 

        def event(self, ev, x, y, st):
            if x >= 0 and y >= 0:
                self.x, self.y = x, y
            raise renpy.IgnoreEvent

screen test_screen():
    default game = Example(background='eileen happy')
    add game

label start:
    call screen test_screen()
    return
