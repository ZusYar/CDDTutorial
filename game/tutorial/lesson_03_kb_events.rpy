label lesson_03_kb_events:
    scene background
    show nvl

    "Let's take a closer look at working with the keyboard and write the first naive way to move an object using arrows."

    show example lesson_03_01a

    "Note that I separated {=green}x{/green} and {=green}y{/green} into their own variables for convenience."

    hide example
    nvl clear
    show example lesson_03_01b large

    "Next step would be programming {=blue}event{/blue} method to react to arrow keys."
    "When you press the corresponding button, it adds or subtracts 1 from the current x or y coordinate respectively."

    hide example
    nvl clear

    "Now press the arrow keys to move." (interact = False)

    call screen lesson_03__test_screen_1()

    "It works, but is rather slow."
    "The question arises: how much exactly should be added each time the method triggers?"
    "The second question is: at what speed does the event fire, because each time it will change the position of the object."

    show example lesson_03_02a small

    "To formally solve the first problem, let's add speed to the arguments."
    "Note that it's another required argument now."

    show example lesson_03_02b
    nvl clear

    "Move on to the second problem, and here we pay attention that we have the argument {=green}st{/green} (shown timebase)."
    "Thus, if we knew how much time passed between the previous method call and the current one, then it would be easy to calculate the distance that the object would travel during this time at a known speed."

    show example lesson_03_02c

    "This is done in a simple way: we add a variable where we will store the old value of st, let's call it {=green}old_st{/green}."
    "The difference between st and old_st gives the desired value. All that remains is to multiply it by the {=green}speed{/green}."

    show example lesson_03_02d

    "Let's also add {=green}horizontal_shift{/green} and {=green}vertical_shift{/green} which will indicate the directions we're moving."

    nvl clear
    hide example
    show example lesson_03_02e large

    "Now to update the values here's what we gonna do."
    "For example, when you're holding {=green}K_RIGHT{/green} the {=green}horizontal_shift{/green} is set to 1, indicating X value increase."
    "Holding {=green}K_LEFT{/green} on the other hand is setting it to -1, indicating X value decrease and so on."

    show example lesson_03_02f large
    nvl clear

    "And don't forget clearing the variables when unholding the buttons :-)."

    hide example
    show example lesson_03_02g small

    "Finally we have to do some maths and calculate new position."
    "As you can see, there is delta, calculated every time the CDD renders itself."

    show example lesson_03_02h

    "Accodingly to the plan, we multiply {=green}delta{/green}, {=green}shift{/green} and {=green}speed{/green}, adding it to {=green}x{/green} and {=green}y{/green} coordinates."

    hide example
    call screen lesson_03__test_screen_2()

    nvl clear

    "This is more like it, but still, the control is a little bit wonky, especially if you keep using more than one button for long enough."
    "It's about time to mention, that checking {=green}ev.type{/green} and {=green}ev.key{/green} is not the only way to track buttons."
    "Luckily enough, there is {=blue}pygame.key.get_pressed(){/blue} which brings us the collection of pressed buttons."
    
    nvl clear
    show example lesson_03_03a large
    
    "Let's not hesitate to rewrite {=blue}event(){/blue} method then."

    show example lesson_03_03b

    "Note how instead of {=green}if ev.key == pygame.K_UP{/green}, it's now {=green}if keys[[pygame.K_UP]{/green}."

    show example lesson_03_03c

    "Done. Observe the whole example class and test it in action."

    nvl clear
    hide example
    call screen lesson_03__test_screen_3()

    return

############ DATA ##############

init python in lesson_03:
    from renpy.display.image import ImageReference
    import pygame

    class Example_1(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.background = ImageReference(background)
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            child_render = renpy.render(self.background, width, height, st, at)
            new_render.blit(child_render, (self.x, self.y))
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
            child_render = renpy.render(self.background, width, height, st, at)
            new_render.blit(child_render, (self.x, self.y))
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
            child_render = renpy.render(self.background, width, height, st, at)
            new_render.blit(child_render, (self.x, self.y))
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

screen lesson_03__test_screen_1():
    default game = lesson_03.Example_1('eileen happy')
    add game
    key 'dismiss' action Return()

screen lesson_03__test_screen_2():
    text _("Move the picture with arrows.") xalign 0.5
    default game = lesson_03.Example_2('eileen happy', 200)
    add game
    key 'dismiss' action Return()

screen lesson_03__test_screen_3():
    text _("Move the picture with arrows.") xalign 0.5
    default game = lesson_03.Example_3('eileen happy', 200)
    add game
    key 'dismiss' action Return()
