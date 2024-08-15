label basic_01_first_cdd:
    scene background
    show nvl

    "So, {a=https://www.renpy.org/doc/html/cdd.html}CDD{/a}"
    extend " = Creator-Defined Displayables."
    "The main idea is to give you as much control over the image as possible."
    "Therefore, the developer himself will have to specify:"
    "1) What, where and when to display."
    "2) How the image reacts to external events: mouse and keyboard."
    "Once again: a single object on the screen is capable of drawing a collection of sprites, tracking projectiles, calculating collisions and responding to keyboard buttons."
    
    nvl clear

    show example basic_01_01a
       
    "The first step is to create a new image class that inherits from {a=https://www.renpy.org/doc/html/cdd.html#renpy-displayable}renpy.Displayable{/a}."

    show example basic_01_01b

    "A class is supposed to have a constructor."
    "For now it doesn't do anything other than run the parent constructor, passing all the arguments to it. (* kwargs = keyword arguments in python.)"

    show example basic_01_01c

    "But since it's supposed to be an image, let it have at least some kind of background image."
    "Note that this is now a required argument, and creating a class object will look like {b}Example(imagename){/b}."

    show example basic_01_01d

    "The only interesting thing here is {a=https://www.renpy.org/doc/html/cdd.html#renpy.displayable}renpy.displayable(){/a} function. It ensures that provided image is a displayable."
    
    hide example
    
    "Now it can be literally anything (within the limits of what renpy supports), such as {a=https://www.renpy.org/doc/html/layeredimage.html}layeredimage{/a}."

    nvl clear
    
    "Let's start displaying the CDD on the screen."

    show example basic_01_02a

    "CDD has a {a=https://www.renpy.org/doc/html/cdd.html#renpy.Displayable.render}def render(){/a} method for this."
    "Consider the arguments:"
    "{=green}width, height{/} - the amount of space available to this displayable, in pixels."
    "{=green}st{/} - a float, the shown timebase, in seconds."
    "{=green}at{/} - animation timebase. (This applies to displaying different pictures with the same tag, so it will not interest us in this context.)"

    nvl clear
    show example basic_01_02b

    "{a=https://www.renpy.org/doc/html/cdd.html#renpy-render}renpy.Render{/a} makes a new empty render."
    "For the sake of clarity in this lesson, let's call it {=green}new_render{/}."

    show example basic_01_02c

    "We will fill it with data, and when everything is ready, we will return it."

    nvl clear
    hide example
    
    "Now how do we fill the render with data?"

    show example basic_01_02d

    "Each render object has method {a=https://www.renpy.org/doc/html/cdd.html#renpy.Render.place}place(){/a}, and most interesting arguments are as follows:"
    "{=green}d{/} - a displayable to render. We will use {=green}self.background{/} for that."
    "{=green}x, y{/} - position to place the displayable. It's defaulted to 0, and we can provide it with something else."

    show example basic_01_02e

    "The method, called on our {=green}new_render{/} will automatically render {=green}self.background{/} inside {=green}new_render{/} (at the position x=150, y=25)."

    hide example
    nvl clear
    
    "Let's take a break :-)"
    "I understand that you want to get results as quickly as possible, so let’s imagine that everything has already been done."

    show example basic_01_03a large
    nvl clear

    "Indeed, this is a completely viable CDD that does little but it works."
    "The only thing left to do is somehow show it in the game, so let's make a test screen."

    hide example
    show example basic_01_03b small

    "Let Eileen be our placeholder :-)"
    
    hide example
    nvl clear

    call screen test_screen(
        obj = basic_01.Example('eileen happy'),
        desc = _("Hurray, it's working!")
    )
    
    call screen test_screen(
        obj = basic_01.Example('eileen_example'),
        desc = _("Note, that position indicate\nthe upper left corner of the\nimage, not its center.")
    )
    
    "All the listings can be found in the listings folder."

    return

############ DATA ##############

init python in basic_01:

    class Example(renpy.Displayable):
        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = renpy.displayable(background)
    
        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            new_render.place(self.background, 150, 25)
            return new_render 

image eileen_example = LayeredImage(attributes=[Solid('#69c6f177', xsize=320), Transform('eileen happy', matrixcolor=SaturationMatrix(0.0)), Text('x=150, y=25', style='note')])