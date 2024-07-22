init python:
    import pygame
    from math import sin, cos

    class Example_Child(renpy.Displayable):
        def __init__(self, image, crop, xoffset, yoffset, rotation=0, xshift=0, yshift=0, distance=0, transform=None, **kwargs):
            super().__init__(**kwargs)
            self.image = image
            self.crop = crop
            self.xoffset, self.yoffset = xoffset, yoffset
    
            # optional
            self.rotation = rotation
            self.xshift, self.yshift = xshift, yshift
            self.distance = distance
            self.transform = transform
    
            # we need to keep the initial offsets as well
            self.xinitial, self.yinitial = xoffset, yoffset

        def render(self, width, height, st, at):
            img = Transform(self.image, crop=self.crop, rotate=(st*self.rotation)%360)
            if callable(self.transform):
                img = self.transform(img)
    
            self.xoffset = self.xinitial + sin(st) * self.distance * self.xshift
            self.yoffset = self.yinitial + cos(st) * self.distance * self.yshift
    
            renpy.redraw(self, 0)
            return renpy.render(img, width, height, st, at)

    class Example(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.x, self.y = 0, 0
            
            image = renpy.displayable(background)
            child_render = renpy.render(image, 0, 0, 0, 0)
            width, height = child_render.get_size()
            half_width, half_height = int(width) // 2, int(height) // 2

            self.children = [
                Example_Child(image, crop=(0, 0, half_width, half_height), xoffset=-half_width, yoffset=-half_height, xshift=-1, yshift=-1, distance=100, rotation=15, transform=zoom_05),
                Example_Child(image, crop=(half_width, 0, half_width, half_height), xoffset=0, yoffset=-half_height, xshift=1, yshift=-1, distance=80, rotation=30),
                Example_Child(image, crop=(0, half_height, half_width, half_height), xoffset=-half_width, yoffset=0, xshift=-1, yshift=1, distance=60, transform=tint_green),
                Example_Child(image, crop=(half_width, half_height, half_width, half_height), xoffset=0, yoffset=0, xshift=1, yshift=1, distance=40, rotation=-60),
            ]

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            for child in self.children:
                new_render.place(child, self.x + child.xoffset, self.y + child.yoffset)
            return new_render 

        def event(self, ev, x, y, st):
            if x >= 0 and y >= 0:
                self.x, self.y = x, y
            raise renpy.IgnoreEvent

transform tint_green:
    matrixcolor TintMatrix('#159357')

transform zoom_05:
    zoom 0.5

screen test_screen():
    default game = Example(background='eileen concerned')
    add game

label start:
    call screen test_screen()
    return
