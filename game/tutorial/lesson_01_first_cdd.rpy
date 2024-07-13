label lesson_01_first_cdd:
    scene background
    show nvl

    "So, {=blue}CDD{/blue}"
    extend " = Creator defined displayables."
    "The main idea is to give you as much control over the image as possible."
    "Therefore, the developer himself will have to specify:"
    "1) What, where and when to display."
    "2) How the image reacts to external events: mouse and keyboard."
    "Once again: a single object on the screen is capable of drawing a collection of sprites, tracking projectiles, calculating collisions and responding to keyboard buttons."
    
    hide sample_11
    nvl clear

    show example lesson_01_01a
       
    "The first step is to create a new image class that inherits from {=blue}renpy.Displayable{/blue}."

    show example lesson_01_01b

    "A class is supposed to have a constructor"
    "For now it doesn't do anything other than run the parent constructor, passing all the arguments to it."
    "* kwargs = keyword arguments in python."

    show example lesson_01_01c

    "But since it's supposed to be an image, let it have at least some kind of background image."
    "Note that this is now a required argument, and creating a class object will look like {b}Example(imagename){/b}."

    show example lesson_01_01d

    "The only interesting thing here is {=blue}ImageReference{/blue}. Since I'm going to use an automatically registered image, I wrap the background in an ImageReference."
    
    hide example
    
    "Now it can be literally anything (within the limits of what renpy supports), such as layeredimage."

    nvl clear
    
    "Let's start displaying the CDD on the screen."

    show example lesson_01_02a

    "CDD has a {=blue}def render(){/blue} method for this."
    "Consider the arguments:"
    "width, height - obviously"
    "st - shown timebase."
    "at - animation timebase. (This applies to displaying different pictures with the same tag, so it will not interest us in this context.)"

    nvl clear
    show example lesson_01_02b

    "{=red}renpy.Render{/red} makes a new empty render."
    "For the sake of clarity in this lesson, let's call it {b}new_render{/b}."

    show example lesson_01_02c

    "We will fill it with data, and when everything is ready, we will return it."

    show example lesson_01_02d

    "{=red}renpy.redraw(){/red} causes CDD to redraw itself on the screen."

    nvl clear
    
    "Now the main thing is not to get confused."

    show example lesson_01_02e

    "The {=red}renpy.render(){/red} function also returns a Render object, not empty this time, but with the currently needed image inside."
    "Let's call this render {b}child_render{/b}."
    "Assume that child_render needs to be rendered in the CDD at the top left corner - coordinates (0, 0)."
    "To do this, each render object has {=blue}def blit(){/blue} method, which we will use often."
    extend " Very often."

    show example lesson_01_02f

    "{=red}new_render.blit(){/red} renders something inside new_render at the specified position."
    
    hide example
    nvl clear
    
    "Let's take a break :-)"
    "I understand that you want to get results as quickly as possible, so let’s imagine that everything has already been done."

    show example lesson_01_03 large
    nvl clear

    "Indeed, this is a completely viable CDD that does little but it works."
    "The only thing left to do is somehow show it in the game, so let's make a test screen."

    nvl clear
    show example lesson_01_04 small

    "Let Eileen be the placeholder this time :-)"
    
    hide example
    show screen lesson_01__test_screen()
    
    "Hurray, it's working! The lesson listing can be found in the listings folder."

    return

############ DATA ##############

init python in lesson_01:
    from renpy.display.image import ImageReference

    class Example(renpy.Displayable):
        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = ImageReference(background)
    
        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            child_render = renpy.render(self.background, width, height, st, at)
            new_render.blit(child_render, (0, 0))
            renpy.redraw(self, 0)
            return new_render 

screen lesson_01__test_screen():
    default game = lesson_01.Example('eileen happy')
    add game
    dismiss action MainMenu(confirm=False)
