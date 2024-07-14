init python:
    import pygame

    class Example(renpy.Displayable):

        def __init__(self, background, speed, **kwargs):
            super().__init__(**kwargs)
            self.background = ImageReference(background)
            self.x, self.y = 0, 0

            # variables related to motion            
            self.speed = speed
            self.old_st = None
            self.horizontal_shift, self.vertical_shift = 0, 0

        def render(self, width, height, st, at):
            # calculating new position from speed, time delta and directions
            if self.old_st is None:
                self.old_st = st
            delta = st - self.old_st
            self.old_st = st
            
            self.x += self.speed * delta * self.horizontal_shift
            self.y += self.speed * delta * self.vertical_shift
            
            # rendering
            new_render = renpy.Render(width, height)
            new_render.place(self.background, self.x, self.y)
            renpy.redraw(self, 0)
            return new_render 

        def event(self, ev, x, y, st):

            keys = pygame.key.get_pressed()
            self.horizontal_shift, self.vertical_shift = 0, 0

            if keys[pygame.K_UP]:
                self.vertical_shift -= 1
            
            if keys[pygame.K_RIGHT]:
                self.horizontal_shift += 1
            
            if keys[pygame.K_DOWN]:
                self.vertical_shift += 1
            
            if keys[pygame.K_LEFT]:
                self.horizontal_shift -= 1

            raise renpy.IgnoreEvent

screen test_screen():
    default game = Example(background='eileen happy', speed=200)
    add game

label start:
    call screen test_screen()
    return
