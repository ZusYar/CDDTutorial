init python:

    class Example(renpy.Displayable):
    
        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = ImageReference(background)
            self.width = width
            self.height = height
    
        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            child_render = renpy.render(self.background, width, height, st, at)
            new_render.blit(child_render, (0, 0))
            renpy.redraw(self, 0)
            return new_render 

screen test_screen():
    default game = Example('eileen happy')
    add game

label start:
    call screen test_screen()
    return
