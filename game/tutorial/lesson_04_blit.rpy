label lesson_04_blit:
    scene background
    show nvl

label .section_01:

    show example lesson_04_01a

    "In previous lessons we used {a=https://www.renpy.org/doc/html/cdd.html#renpy.Render.place}place(){/a} to fill the render."
    "This was convenient because the method automatically renders the image and places it at the specified coordinates."
    "But what if we first need to carry out some manipulations with the image?"
    "Then we must prepare the render ourselves, do everything we wanted and only after that display the result."
    "In this lesson we will look at methods that allow you to cope with this task."

    nvl clear
    show example lesson_04_01b

    "Now the most important thing is not to get confused. Compare these two commands."
    "{a=https://www.renpy.org/doc/html/cdd.html#renpy.Render}renpy.Render{/a} is the class we use to create a new render."
    "{a=https://www.renpy.org/doc/html/cdd.html#renpy.render}renpy.render(){/a} is a function that returns an instance of the renpy.Render class with the specified image inside."
    "{=green}new_render{/green} and {=green}child_render{/green} are both equivalent Render instances, so both have access to all methods of the {=blue}renpy.Render{/blue} class."
    "What can this class do? Let's look at the documentation and observe a few methods."

    nvl clear
    show example lesson_04_01c

    "{a=https://www.renpy.org/doc/html/cdd.html#renpy.Render.place}place(){/a} - A familiar method that places another (unrendered) image in it."

    show example lesson_04_01d

    "{a=https://www.renpy.org/doc/html/cdd.html#renpy.Render.get_size}get_size(){/a} - Returns a (width, height) tuple giving the size of this render."

    show example lesson_04_01e
    
    "{a=https://www.renpy.org/doc/html/cdd.html#renpy.Render.subsurface}subsurface(){/a} - Returns a render consisting of a rectangle cut out of this render."

    show example lesson_04_01f
    
    "{a=https://www.renpy.org/doc/html/cdd.html#renpy.Render.blit}blit(){/a} - Draws another render object into this render object."

    hide example
    
    "Let's get practical."

    nvl clear

label .section_02:

    show example lesson_04_02a

    "As our first step we'll render {=green}background{/green} as a {=green}child_render{/green}."

    show example lesson_04_02b

    "Now we can actually manipulate this new render. For example, we can crop her head (sorry, Eileen)"

    show example lesson_04_02c

    extend" and blit the head into the mouse position."
    "Note, that {=green}head{/green} is a Render object just as well."

    hide example
    nvl clear

    call screen lesson_test_screen(
        obj = lesson_04.Example_1('eileen concerned'),
        desc = _("Woooohooo")
    )

label .section_03:

    "Okay, this was too easy."
    "Let's correct the way we move the image and make its center match the mouse pointer position."

    show example lesson_04_03a

    "{a=https://www.renpy.org/doc/html/cdd.html#renpy.Render.get_size}get_size(){/a} will bring us the size of the image."

    show example lesson_04_03b

    "Then we could calculate half-size just for our convenience."

    show example lesson_04_03c

    "All we need to do now is simply offset the position by these values when we blit the {=green}child_render{/green}."
    "And we're ready to go."

    hide example
    nvl clear

    call screen lesson_test_screen(
        obj = lesson_04.Example_2('eileen concerned'),
        desc = _("Nice")
    )

label .section_04:

    "Still not satisfied?"
    "How about we split the image in 4 rectangles and make it explode around the mouse pointer? Does it sound like fun? Let's find out."

    nvl clear
    show example lesson_04_04a large

    "In addition to already mentioned steps, we simply make 4 new Render objects representing the 4 rectangles. We use half sizes for it."

    show example lesson_04_04b

    "Then we declare the maximum distance for the rectangles to move avay from mouse pointer."

    show example lesson_04_04c

    "Current distance can be calculated for example with use of {a=https://www.w3schools.com/python/ref_math_sin.asp}sine function{/a} from current {=green}st{/green} value, and we should import math library."

    nvl clear
    show example lesson_04_04d

    "Last chunk of maths for now, and we place the rectangles accordignly to their new positions."

    show example lesson_04_05a

    "Examine the listing and test the result. The lesson is over :D."

    hide example
    nvl clear

    call screen lesson_test_screen(
        obj = lesson_04.Example_3('eileen concerned'),
        desc = _("What the...")
    )
    
    return

############ DATA ##############

init python in lesson_04:
    from renpy.display.image import ImageReference
    import pygame
    from math import sin

    class Example_1(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = ImageReference(background)
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            child_render = renpy.render(self.background, width, height, st, at)
    
            head = child_render.subsurface((0, 0, 300, 280))
            new_render.blit(head, (self.x, self.y))

            renpy.redraw(self, 0)
            return new_render 

        def event(self, ev, x, y, st):
            if x >= 0 and y >= 0:
                self.x, self.y = x, y
            raise renpy.IgnoreEvent

    class Example_2(renpy.Displayable):

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

            # display the image with half-size offset
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
