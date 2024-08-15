label intermediate_01_canvas:

    scene background
    show nvl

label .section_01:

    "In addition to loading physical image files, in a CDD you can access the canvas and directly draw primitives using methods listed in the {a=https://www.pygame.org/docs/ref/draw.html}pygame.draw{/a} documentation section."
    "Ren'py provides this functionality in a somewhat reduced form, and it is unlikely that many will find it useful anyway, but it will still not be superfluous to know about its existence."

    nvl clear

    "Let's look at the list of the methods:"
    "{=blue}line{/} - draw a straight line"
    "{=blue}lines{/} - draw multiple contiguous straight line segments"
    "{=blue}circle{/} - draw a circle"
    "{=blue}rect{/} - draw a rectangle"
    "{=blue}polygon{/} - draw a polygon"
    "{b}arc{/b} and {b}ellipse{/b} are not supported in ren'py."

    nvl clear

    "Before we draw the shapes, let's figure out how to specify colors, because you can't draw anything without it."
    "This could be a string like '#RGBA', a tuple of 3 or 4 elements of numbers from 0 to 255, or a {a=https://www.pygame.org/docs/ref/color.html}pygame.Color{/a} object."
    "Although a detailed analysis of pygame's capabilities is beyond the scope of this article, I will mention that the class provides named access to color fields, for example {=green}color.r{/}, {=green}color.g{/}"
    extend "; it allows you conversions to other color spaces such as {=green}HSLA{/}, {=green}CMY{/}"
    extend "; it even supports simple mathematical color manipulations such as +, -, *, //, \%, ~."
    "Example: {=green}'#10C010'{/} is equivalent to {=blue}pygame.Color(16, 192, 16){/}."
    "Example: (50, 50, 50) + (50, 50, 50) = (100, 100, 100)."

    nvl clear

    "Now we can draw. Let's start with straight lines."

    show example intermediate_01_01a large

    "First thing to do is accessing the canvas, and any {=blue}Render{/} object has the {a=https://www.renpy.org/doc/html/cdd.html#renpy.Render.canvas}canvas(){/a} method."

    show example intermediate_01_01b

    "With this code we draw a yellow line from (0, 0) to (1280, 720). Note that {=blue}line(){/} method takes an optional {=green}width{/} argument."

    nvl clear
    show example intermediate_01_01c

    "{=blue}lines(){/} method is a bit different. As you can see, its arguments are: {=green}color{/},{w} {=green}closed{/} - a bool signifying an additional line segment between the first and last points, {w} {=green}points{/} - a sequence of 2 or more (x, y) coordinates, {w} and {=green}width{/}, used for line thickness."

    show example intermediate_01_01d

    "(Unfortunately, ren'py doesn't fully match the pygame version, {=green}points{/} is {=green}pointlist{/} in ren'py, that is, if you want to name positional args.)"

    nvl clear
    show example intermediate_01_01e

    "Next, we'll easily add a couple of circles, but let's make {=blue}pygame.Color{/} instance this time."
    "Note, how we can draw only a circle's border with use of {=green}width{/}."

    nvl clear
    show example intermediate_01_01f

    "Next, we'll add a couple of rectangles: solid and border-only, experimenting with color."
    "As one would expect, rounded rectangle corners are not supported in ren'py."

    nvl clear
    show example intermediate_01_01g

    "To make the picture complete, we'll add a purple polygon shape."
    "Time to see if this is working at all."

    hide example
    nvl clear

    call screen test_screen(
        obj = intermediate_01_canvas.Example_1(),
        desc = _("Yes it is.")
    )

label .section_02:

    "As an excercise, let's look at this interactive CDD and figure out how it works."

    nvl clear

    call screen test_screen(
        obj = intermediate_01_canvas.Example_2(),
        desc = _("Click somewhere on the screen and release somewhere else do draw a rectangle of a random color."),
        close = True
    )

    show example intermediate_01_02a large

    "Let's agree that we will store data about the last 10 rectangles."

    show example intermediate_01_02b

    "Memorizing mouse pointer position on pressing left button"

    show example intermediate_01_02c

    extend " and appending rectangle on the button release."

    show example intermediate_01_02d

    "{=blue}render(){/} obviously enough displaying all the rectangles in a loop."
    
    nvl clear
    show example intermediate_01_02e

    "Finally, the method appending new rectangles."

label .section_03:

    nvl clear
    hide example

    "How about something slightly more practicle, for example a simple color picker?"
    "To access an image's color data, renpy has {a=https://www.renpy.org/doc/html/cdd.html#renpy.load_surface}renpy.load_surface(){/a} method."
    "The docs tell us, it \"loads the image manipulator and returns a pygame Surface.\""
    "{a=https://www.pygame.org/docs/ref/surface.html}Pygame Surface{/a} has its share of methods, some of them are implemented in ren'py, and we'll focus on the {=blue}get_at(){/} method specifically, which can get the color value at a single pixel."

    nvl clear
    show example intermediate_01_03a large

    "Omitting the obvious parts, we get something like this for {=blue}event(){/}."
    "The method's supposed to return the color under the mouse pointer and keep it as {=green}self.selected{/}."

    show example intermediate_01_03b

    "Because we can click outside of the image's dimensions, it's always good to check the boundaries."

    nvl clear
    show example intermediate_01_03c

    "Finally, to display the selected pixel's information, we return to the {=blue}render(){/}."

    nvl clear
    hide example

    call screen test_screen(
        obj = intermediate_01_canvas.Example_3('eileen concerned'),
        desc = _("Pick a color"),
        close = True
    )

label .section_04:

    nvl clear
    
    "Before we call it a day, I'd like to go back a few steps, and point at {=blue}get_at(){/} method."
    "As expected, you can manipulate pixels on the canvas with {=blue}set_at(){/} method."
    "Let's make our render perform hue rotation to the picture."

    nvl clear
    show example intermediate_01_04a large

    "{=green}self.hue{/} is our new variable memorizing the current hue shift value."

    show example intermediate_01_04b

    "It is updated every time, the {=blue}render(){/} triggers."
    "Also, we trigger next {=blue}renpy.redraw(){/} as soon as possible."

    nvl clear
    show example intermediate_01_04c

    "Next we add already familiar methods {=blue}load_surface(){/}, {=blue}get_size(){/}, {=blue}blit(){/}."

    show example intermediate_01_04d

    "Main loop goes like this. We take a pixel, break it down into H, S, L, A components, apply new hue and put it back."

    show example intermediate_01_04e

    "Code that reads or writes pixel values will need the surface to be locked."

    nvl clear
    show example intermediate_01_04f

    "One tiny detail, telling us the current render {=green}st{/} and we're ready to go."

    nvl clear
    hide example
    pause 0.5

    call screen test_screen(
        obj = intermediate_01_canvas.Example_4('eileen concerned'),
        desc = _("Note how long it takes to redraw."),
        close = True
    )

    "That said, the example is {=red}purely demonstrational{/} and you're not supposed to use it to actually manipulate the image data like this, preferring {a=https://www.renpy.org/doc/html/matrixcolor.html#matrixcolor}matrixcolor{/a} over canvas."

    return

############ DATA ##############

init python in intermediate_01_canvas:

    import random
    import pygame
    from store import Text
    from math import sin

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
