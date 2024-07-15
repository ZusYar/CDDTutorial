init python:

    class Example(renpy.Displayable):
    
        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = renpy.displayable(background)
    
        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            new_render.place(self.background, 150, 25)
            return new_render 

screen test_screen():
    default game = Example('eileen happy')
    add game

label start:
    call screen test_screen()
    return
