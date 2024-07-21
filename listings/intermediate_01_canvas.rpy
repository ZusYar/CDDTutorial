init python:

    import random
    import pygame
    from math import sin

    # Various shapes
    class Example_1(renpy.Displayable):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            canvas = new_render.canvas()

            canvas.line('#ffd900ff', (0, 0), (1280, 720), width=2)
            canvas.lines(color='#ff0022ff', closed=False, pointlist=((600, 50), (650, 100), (550, 200), (700, 350), (500, 550)), width=1)

            color1 = pygame.Color(0x33, 0x22, 0x33)
            canvas.circle(color1, (200, 400), 200)
            color2 = color1 + color1
            canvas.circle(color2, (350, 400), 200, width=10)

            color3 = color2 + pygame.Color(0, 0, 0x11)
            canvas.rect(color3, (700, 20, 100, 600))
            color3.g = 255
            canvas.rect(color3, (650, 50, 500, 500), width=4)

            canvas.polygon('#5a21ddff', ((250, 50), (500, 100), (750, 500), (500, 700)), width=5)

            return new_render 

    # Interactive rectangles
    class Example_2(renpy.Displayable):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.data = []               # (color, rectangle) data storage
            self.max_count = 10          # we'll store last 10 rectangles
            self.start_point = None      # temporary

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            canvas = new_render.canvas()
            
            for color, rect in self.data:
                canvas.rect(color, rect)
            
            return new_render

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.start_point = (x, y) # memorize start point
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.add_rect(x, y)       # add new rectangle
            raise renpy.IgnoreEvent

        def add_rect(self, new_x, new_y):
            if not self.start_point:
                return
            
            # calculating rectangle
            old_x, old_y = self.start_point
            rect = (old_x, old_y, new_x-old_x, new_y-old_y)
            
            # random color
            color = pygame.Color(*[random.randint(0, 255) for _ in range(4)])
            # making sure the alpha is high enough. I don't want to create rectangles that are hard to notice.
            color.a = max(color.a, 128)
            
            while len(self.data) >= self.max_count:
                self.data.pop(0)
            self.data.append((color, rect))
            renpy.redraw(self, 0)

    # Colorpicker
    class Example_3(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = renpy.displayable(background)
            self.selected = None

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            new_render.place(self.background, 0, 0)

            if self.selected:
                color = self.selected
                canvas = new_render.canvas()
                canvas.rect(color, (500, 100, 212, 24))
                new_render.place(Text(f'RGBA = #{color.r:02x}{color.g:02x}{color.b:02x}{color.a:02x}'), 500, 100)

                h, s, l, a = color.hsla
                new_render.place(Text(f'Hue = {h:.3f}'), 500, 130)
                new_render.place(Text(f'Saturation = {s:.3f}'), 500, 160)
                new_render.place(Text(f'Lightness = {l:.3f}'), 500, 190)

            return new_render

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.selected = self.pick_color(x, y)
                renpy.redraw(self, 0)
            raise renpy.IgnoreEvent

        def pick_color(self, x, y):
            surf = renpy.load_surface(self.background)
            width, height = surf.get_size()
            if 0 <= x < width and 0 <= y < height:
                pixel = surf.get_at((x, y))
                return pixel

    # Hue rotation
    class Example_4(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = renpy.displayable(background)
            self.hue = 0

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            self.hue += 10

            surf = renpy.load_surface(self.background)
            width, height = surf.get_size()
            
            surf.lock()
            for x in range(width):
                for y in range(height):
                    color = surf.get_at((x, y))
                    h, s, l, a = color.hsla

                    h = (h + self.hue) % 360 # rotate hue

                    color.hsla = (h, s, l, a)
                    surf.set_at((x, y), color)
            surf.unlock()

            new_render.blit(surf, (0, 0))

            new_render.place(Text(f'{st:.03f}'), 300, 100)

            renpy.redraw(self, 0) # redraw CDD constantly
            return new_render 

screen test_screen_1():
    default game = Example_1()
    add game
    key 'dismiss' action Return()

screen test_screen_2():
    default game = Example_2()
    add game
    textbutton "CLOSE" action Return() xalign 1.0 yalign 0.05

screen test_screen_3():
    default game = Example_3('eileen concerned')
    add game
    textbutton "CLOSE" action Return() xalign 1.0 yalign 0.05

screen test_screen_4():
    default game = Example_4('eileen concerned')
    add game
    key 'dismiss' action Return()

label start:
    call screen test_screen_1()
    call screen test_screen_2()
    call screen test_screen_3()
    call screen test_screen_4()
    return
