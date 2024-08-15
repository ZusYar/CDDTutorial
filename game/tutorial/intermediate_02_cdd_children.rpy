label intermediate_02_cdd_children:
    scene background
    show nvl

label .section_01:

    show example intermediate_02_01a large

    "Looking back at the lesson when we were using {=blue}blit(){/} to display multiple image parts, we can easily notice how fast the {=blue}render(){/} method can turn into so called spaghetti code, needlessly long with nearly identical copy-pasted lines doing approximately the same job."

    hide example

    "But who said that CDD has to do all the calculations? Why not delegate this responsibility to its child elements?"
    "Especially if the number of children will grow or if we'll need to reuse them elswhere."
    "In this lesson we'll develop another CDD with this new concept in mind."

    show example intermediate_02_02a small

    "We start simply enough with making this class."
    "As you can see, it only returns its rendered {=green}image{/}."

    nvl clear
    hide example
    show example intermediate_02_02b large

    "The biggest change I'm planing, is defining CDD children during its initialization time."
    "To do this, I render the image to detect the sizes."

    show example intermediate_02_02c

    "By the way, we can use ren'py transforms such as {=blue}Crop{/}, make them children of the CDD and store as {=green}self.children{/}."

    hide example
    show example intermediate_02_02d small

    "The only thing left to do is to place them onto our main CDD and it's easy to do in a simple loop."

    nvl clear
    hide example

    call screen test_screen(
        obj = intermediate_02_a.Example('eileen concerned'),
        desc = _("It kinda' works, but the children overlap.")
    )

label .section_02:

    "All the children are displayed in a single position on the screen."
    "We need to somehow tell the children their x/y offsets."
    "For example, we can change the way we organize {=green}self.children{/}."

    show example intermediate_02_03a small

    "Here's what we gonna do."

    show example intermediate_02_03b

    "And this is our new structure."

    show example intermediate_02_03c

    "Finally, we fix the loop placing the children."

    nvl clear
    hide example

    call screen test_screen(
        obj = intermediate_02_b.Example('eileen concerned'),
        desc = _("Looks like a single image for now.")
    )

label .section_03:

    "Another way to store the children offsets could be passing them as arguments to the constructor."
    "Actually, let's also pass the crop and construct the whole transform in the child's {=blue}render(){/}."

    show example intermediate_02_04a

    "In my opinion, it looks slightly better and easier to read now with named arguments."

    show example intermediate_02_04b

    "Should not forget to update the way we display the children too."

    nvl clear
    hide example
    show example intermediate_02_04c large

    "Our {=green}Example_Child{/} class will take and memorize the arguments."

    show example intermediate_02_04d

    "{=green}self.image{/} and {=green}self.crop{/} are then used to create Transform. I've also added zoom property changing over time."

    show example intermediate_02_04e

    "Note how the child must redraw itself now, while the parent CDD doesn't have to, because its children doing the job."

    nvl clear
    hide example

    call screen test_screen(
        obj = intermediate_02_c.Example('eileen concerned')
    )

label .section_04:

    "Before we end the lesson, let's get crazy and add more variations to the children."

    show example intermediate_02_05a large

    "In addition to already known arguments, here's a bunch of optional: {=green}rotation{/} speed, {=green}x/y shift{/} directions and max {=green}distance{/} to shift, and {=green}transform to apply{/}."
    "Initial offsets are there in order to shift the child relative to these coordinates."

    hide example
    show example intermediate_02_05b small

    "Yes, you can pass more transforms defined elsewhere, and to demostrate it I've added these two."

    hide example
    nvl clear
    show example intermediate_02_05c large

    "The 1st child definition will look like this."
    "It will shift to the left and up, at max distance = 100 pix."
    "There's also rotation speed = 15 and additional transform zoom_05."

    show example intermediate_02_05d

    "Let this be the whole children collection defined in the main CDD."

    hide example
    nvl clear
    show example intermediate_02_05e

    "Back to the child {=blue}render(){/}. If {=green}transform{/} is present, we can apply it. (Transforms are callable objects and here's the check)."

    show example intermediate_02_05f
    
    "Children should update their offset every time. For a change, I've made {=green}xoffset{/} moving with {b}sine{/b} function and {=green}yoffset{/} with {b}cosine{/b}."

    show example intermediate_02_05g

    "Finally redraw and return."
    extend " And it's time to see the result."

    nvl clear
    hide example

    call screen test_screen(
        obj = intermediate_02_d.Example('eileen concerned')
    )

    return

############ DATA ##############

init python in intermediate_02_a:
    import pygame
    from store import Crop

    class Example_Child(renpy.Displayable):
        def __init__(self, image, **kwargs):
            super().__init__(**kwargs)
            self.image = image

        def render(self, width, height, st, at):
            return renpy.render(self.image, width, height, st, at)

    class Example(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.x, self.y = 0, 0
            
            image = renpy.displayable(background)
            child_render = renpy.render(image, 0, 0, 0, 0)
            width, height = child_render.get_size()
            half_width, half_height = int(width) // 2, int(height) // 2

            self.children = [
                Example_Child(Crop((0, 0, half_width, half_height), image)),
                Example_Child(Crop((half_width, 0, half_width, half_height), image)),
                Example_Child(Crop((0, half_height, half_width, half_height), image)),
                Example_Child(Crop((half_width, half_height, half_width, half_height), image))
            ]

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            for child in self.children:
                new_render.place(child, self.x, self.y)
            return new_render 

        def event(self, ev, x, y, st):
            if x >= 0 and y >= 0:
                self.x, self.y = x, y
                renpy.redraw(self, 0)
            raise renpy.IgnoreEvent

init python in intermediate_02_b:
    import pygame
    from store import Crop

    class Example_Child(renpy.Displayable):
        def __init__(self, image, **kwargs):
            super().__init__(**kwargs)
            self.image = image

        def render(self, width, height, st, at):
            return renpy.render(self.image, width, height, st, at)

    class Example(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.x, self.y = 0, 0
            
            image = renpy.displayable(background)
            child_render = renpy.render(image, 0, 0, 0, 0)
            width, height = child_render.get_size()
            half_width, half_height = int(width) // 2, int(height) // 2

            self.children = [
                (Example_Child(Crop((0, 0, half_width, half_height), image)), -half_width, -half_height),
                (Example_Child(Crop((half_width, 0, half_width, half_height), image)), 0, -half_height),
                (Example_Child(Crop((0, half_height, half_width, half_height), image)), -half_width, 0),
                (Example_Child(Crop((half_width, half_height, half_width, half_height), image)), 0, 0)
            ]

        def render(self, width, height, st, at):
            new_render = renpy.Render(width, height)
            for child, offset_x, offset_y in self.children:
                new_render.place(child, self.x + offset_x, self.y + offset_y)
            return new_render 

        def event(self, ev, x, y, st):
            if x >= 0 and y >= 0:
                self.x, self.y = x, y
                renpy.redraw(self, 0)
            raise renpy.IgnoreEvent

init python in intermediate_02_c:
    import pygame
    from math import sin
    from store import Transform

    class Example_Child(renpy.Displayable):
        def __init__(self, image, crop, xoffset, yoffset, **kwargs):
            super().__init__(**kwargs)
            self.image = image
            self.crop = crop
            self.xoffset, self.yoffset = xoffset, yoffset

        def render(self, width, height, st, at):
            img = Transform(self.image, crop=self.crop, zoom=abs(sin(st)))
            render = renpy.render(img, width, height, st, at)
            renpy.redraw(self, 0)
            return render

    class Example(renpy.Displayable):

        def __init__(self, background, **kwargs):
            super().__init__(**kwargs)
            self.x, self.y = 0, 0
            
            image = renpy.displayable(background)
            child_render = renpy.render(image, 0, 0, 0, 0)
            width, height = child_render.get_size()
            half_width, half_height = int(width) // 2, int(height) // 2

            self.children = [
                Example_Child(image, crop=(0, 0, half_width, half_height), xoffset=-half_width, yoffset=-half_height),
                Example_Child(image, crop=(half_width, 0, half_width, half_height), xoffset=0, yoffset=-half_height),
                Example_Child(image, crop=(0, half_height, half_width, half_height), xoffset=-half_width, yoffset=0),
                Example_Child(image, crop=(half_width, half_height, half_width, half_height), xoffset=0, yoffset=0),
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

init python in intermediate_02_d:
    import pygame
    from math import sin, cos
    from store import Transform

    class Example_Child(renpy.Displayable):
        def __init__(self, image, crop, xoffset, yoffset, xshift=0, yshift=0, distance=0, rotation=0, transform=None, **kwargs):
            super().__init__(**kwargs)
            self.image = image
            self.crop = crop
            self.xinitial, self.yinitial = xoffset, yoffset
            self.xoffset, self.yoffset = xoffset, yoffset
            self.xshift, self.yshift = xshift, yshift
            self.distance = distance
            self.rotation = rotation
            self.transform = transform

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

transform example_transform_tint_green:
    matrixcolor TintMatrix('#159357')

transform example_transform_zoom_05:
    zoom 0.5

init python:
    renpy.add_to_all_stores('tint_green', example_transform_tint_green)
    renpy.add_to_all_stores('zoom_05', example_transform_zoom_05)
