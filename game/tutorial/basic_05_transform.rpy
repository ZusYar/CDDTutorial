label basic_05_transform:
    scene background
    show nvl

label .section_01:

    "So far we've been drawing and moving rectangles, but is it possible to do something more interesting than this?"
    "Yes there is! What if I remind you about such a powerful tool in ren'py as transform?"
    "That's right. The renderer can handle any displayable, including transform, giving access to the extensive capabilities of ren'py {a=https://www.renpy.org/doc/html/atl.html}Animation and Transformation Language{/a}."

    nvl clear
    show example basic_05_01a large

    "Let's take this example as a basis and change the size through {a=https://www.renpy.org/doc/html/atl.html#list-of-transform-properties}transform properties{/a}."

    show example basic_05_01b

    "We will of course focus only on the {=blue}render{/blue} method."
    
    nvl clear
    show example basic_05_01c

    "Zooming an image is an easy to test option, so why not start our experiments from zoom."

    show example basic_05_01d

    "We assume, that {=green}child_render{/green} will get the rendered image alright, without forcing us to change our calculations."

    hide example

    call screen test_screen(
        obj = basic_05.Example_1('eileen happy'),
        desc = _("And it works as expected.")
    )

label .section_02:

    show example basic_05_02a small

    "Just for fun, we can apply {a=https://www.renpy.org/doc/html/atl.html#transform-property-crop}crop{/a}, {a=https://www.renpy.org/doc/html/atl.html#transform-property-blur}blur{/a}, {a=https://www.renpy.org/doc/html/atl.html#transform-property-alpha}alpha{/a}, {a=https://www.renpy.org/doc/html/atl.html#transform-property-matrixcolor}matrixcolor{/a}. Beacuse why not?"

    hide example

    call screen test_screen(
        obj = basic_05.Example_2('eileen happy'),
        desc = _("Cool!")
    )

label .section_03:

    nvl clear

    "It is not necessary to program transforms inside the {=blue}render{/blue} itself."

    show example basic_05_03a small

    "You can design transform somewhere else."

    hide example
    show example basic_05_03b large

    "You can even get creative and include some animations."

    hide example
    show example basic_05_03c small

    "And then simply apply it as it is."

    show example basic_05_03d

    "Another way to apply transform is {a=https://www.renpy.org/doc/html/displayables.html#At}At{/a}, by the way."

    hide example
    nvl clear

    call screen test_screen(
        obj = basic_05.Example_3('eileen happy'),
        desc = _("Hm. Something's wrong. Where did our animations go?..")
    )

    show example basic_05_03d

    "Let's take a breath and think it over."
    "The thing is, there's a {=red}new{/red} transform created every time we render the CDD."

    hide example
    show example basic_05_03e large

    "In order to avoid it, we'll apply transform during CDD {=red}init{/red}, and then render it instead."

    hide example
    nvl clear

    call screen test_screen(
        obj = basic_05.Example_4('eileen concerned'),
        desc = _("...")
    )

    "Whew. We did it!"

    return
    
############ DATA ##############

init python in basic_05:
    import pygame
    from store import Transform, SaturationMatrix, At

    class Example_1(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = renpy.displayable(background)
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)

            image = Transform(self.background, zoom=0.5)
            child_render = renpy.render(image, width, height, st, at)
    
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

    class Example_2(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = renpy.displayable(background)
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)

            image = Transform(self.background, zoom=0.5, crop=(0.25, 0.0, 0.5, 1.0), alpha=0.75, blur=8.0, matrixcolor=SaturationMatrix(0.5))
            child_render = renpy.render(image, width, height, st, at)
    
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

    class Example_3(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = renpy.displayable(background)
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)

            image = At(self.background, basic_05_transform_1)
            child_render = renpy.render(image, width, height, st, at)
    
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

    class Example_4(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.image = At(renpy.displayable(background), basic_05_transform_1)
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

transform basic_05_transform_1:
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

init python:
    renpy.add_to_all_stores('basic_05_transform_1', basic_05_transform_1)
