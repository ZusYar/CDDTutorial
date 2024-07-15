label basic_03_kb_events:
    scene background
    show nvl

label .section_1:

    "Let's take a closer look at working with the keyboard and write the first naive way to move an object using arrows."

    hide example
    show example basic_03_01a large

    "We have to program the {=blue}event{/blue} method so that it can react to the arrow keys."
    "When you press the corresponding button, it adds or subtracts 1 from the current {=green}x{/green} or {=green}y{/green} coordinate respectively."

    hide example
    nvl clear

    call screen test_screen(
        obj = basic_03.Example_1('eileen happy'),
        desc = _("Press the arrow keys to move."),
        close = True
    )

label .section_2:

    "It works, but the movement is rather slow."
    "The question arises: how much exactly should be added each time the method triggers?"
    "The second question is: at what speed does the event fire, because each time it will change the position of the object."

    show example basic_03_02a small

    "To formally solve the first problem, let's add {=green}speed{/green} to the arguments."

    show example basic_03_02b

    "Note that it's another required argument now."

    show example basic_03_02c
    nvl clear

    "Move on to the second problem, and here we pay attention that {=blue}event{/blue} method has the argument {=green}st{/green} (shown timebase)."
    "Thus, if we knew how much time passed between the previous method call and the current one, then it would be easy to calculate the distance that the object would travel during this time at a known speed."

    show example basic_03_02d

    "This is done in a simple way: we add a variable where we will store the old value of {=green}st{/green}, let's call it {=green}old_st{/green}."
    "The difference between {=green}st{/green} and {=green}old_st{/green} gives the desired value. All that remains is to multiply it by the {=green}speed{/green}."

    show example basic_03_02e

    "Let's also add {=green}horizontal_shift{/green} and {=green}vertical_shift{/green} which will indicate the directions we're moving."

    nvl clear
    hide example
    show example basic_03_03a

    "Now to update the values here's what we gonna do."
    "When you're holding {=green}K_UP{/green}, instead of directly subtracting 1 from {=green}y{/green} position, we set {=green}vertical_shift{/green} to -1, indicating the {=green}y{/green} value should decrease with movements."

    hide example
    show example basic_03_03b large
    
    "For another example, when you're holding {=green}K_RIGHT{/green} the {=green}horizontal_shift{/green} is set to 1, indicating X value increase."

    nvl clear
    show example basic_03_03c

    "And don't forget clearing {=green}horizontal_shift{/green} and {=green}vertical_shift{/green} when unholding the buttons :-)."

    nvl clear
    show example basic_03_03d

    "Finally we do some maths and calculate new position."
    "As you can see, there is delta, calculated every time the CDD renders itself."

    show example basic_03_03e

    "Accordingly to the plan, we multiply {=green}delta{/green}, {=green}shift{/green} and {=green}speed{/green}, adding it to {=green}x{/green} and {=green}y{/green} coordinates."

    hide example
    nvl clear

    call screen test_screen(
        obj = basic_03.Example_2('eileen happy', 200),
        desc = _("Press the arrow keys to move."),
        close = True
    )

    nvl clear

label .section_3:

    "This is more like it, but still, the control is a little bit wonky, especially if you keep using more than one button for long enough."
    "It's about time to mention, that checking {=green}ev.type{/green} and {=green}ev.key{/green} is not the only way to track buttons."

    show example basic_03_04a small

    "Luckily enough, there is {=blue}pygame.key.get_pressed(){/blue} which brings us the collection of pressed buttons."
    "Let's not hesitate to rewrite {=blue}event(){/blue} method entirely then :-]."
    
    hide example
    nvl clear
    show example basic_03_04b large

    "Note how instead of {=green}if ev.key == pygame.K_UP{/green}, it's now {=green}if keys[[pygame.K_UP]{/green}."

    show example basic_03_04c

    "Done. Observe the whole example class and test it in action."

    hide example
    nvl clear

    call screen test_screen(
        obj = basic_03.Example_3('eileen happy', 200),
        desc = _("Press the arrow keys to move."),
        close = True
    )

    return

############ DATA ##############

init python in basic_03:
    import pygame

    class Example_1(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = renpy.displayable(background)
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            new_render.place(self.background, self.x, self.y)
            renpy.redraw(self, 0)
            return new_render 

        def event(self, ev, x, y, st):
            if ev.type == pygame.KEYDOWN:
                
                if ev.key == pygame.K_UP:
                    self.y -= 1
                
                elif ev.key == pygame.K_RIGHT:
                    self.x += 1
                
                elif ev.key == pygame.K_DOWN:
                    self.y += 1
                
                elif ev.key == pygame.K_LEFT:
                    self.x -= 1
            
            raise renpy.IgnoreEvent

    class Example_2(renpy.Displayable):

        def __init__(self, background, speed, **kwargs):
            super().__init__(**kwargs)
            self.background = renpy.displayable(background)
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
            if ev.type == pygame.KEYDOWN:
                
                if ev.key == pygame.K_UP:
                    self.vertical_shift = -1
                
                elif ev.key == pygame.K_RIGHT:
                    self.horizontal_shift = 1
                
                elif ev.key == pygame.K_DOWN:
                    self.vertical_shift = 1
                
                elif ev.key == pygame.K_LEFT:
                    self.horizontal_shift = -1

            if ev.type == pygame.KEYUP:
                
                if ev.key == pygame.K_UP:
                    self.vertical_shift = 0
                
                elif ev.key == pygame.K_RIGHT:
                    self.horizontal_shift = 0
                
                elif ev.key == pygame.K_DOWN:
                    self.vertical_shift = 0
                
                elif ev.key == pygame.K_LEFT:
                    self.horizontal_shift = 0

            raise renpy.IgnoreEvent

    class Example_3(renpy.Displayable):

        def __init__(self, background, speed, **kwargs):
            super().__init__(**kwargs)
            self.background = renpy.displayable(background)
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
