label intermediate_03_shaders:

    scene background
    show nvl

label .section_00:

    "This is a tough topic, because shaders are special programs written in a language completely different from ren'py (and python), and understanding why and how to write them is a separate topic for a large discussion that goes far beyond the scope of this tutorial."
    "Well, at least we can try to learn how to use shaders inside {b}CDD{/b}, but it is highly recommended to read {a=https://www.renpy.org/doc/html/model.html}Model-Based Rendering{/a} page before going any further."
    "Luckily, ren'py comes with several shaders, so we don't have to code anything and can use them as our source material."

    nvl clear

    "So, what is the shader collection in ren'py? We can find it in {a=https://www.renpy.org/doc/html/model.html#default-shader-parts}Default Shader Parts{/a} (or the full code inside {=red}SDK/renpy/common/_shaders.rpym{/})."
    "And we need to, because in order to use a shader we must know its name and arguments it's operating."
    "For example {=green}\"renpy.blur\"{/} in addition to texture takes u_renpy_blur_log2, {=green}\"renpy.dissolve\"{/} takes 2 textures, u_lod_bias and u_renpy_dissolve etc."
    "Our first exercise will be making a CDD that has 2 images gradually dissolving into each other as we move mouse pointer to the left or to the right."
    "Shader {=green}\"renpy.dissolve\"{/} suits our needs, so let's simply provide it with 2 textures and u_renpy_dissolve, which is the amount of the dissolving process."
    "(u_lod_bias, where lod stands for {=green}level of details{/}, is optional, and we won't touch it.)"

    nvl clear
    show example intermediate_03_01a large

    "Without further ado, this is what the blank looks like. Example class takes 2 images (left and right), keeps track on x, y mouse position, renders and blits both images at (0, 0) of the CDD."
    "There's nothing particularly interesting here, so let's just focus on the {=blue}render{/} method."

    hide example
    nvl clear

    "It's about time to observe what else a {=blue}renpy.Render{/} object has in order to work with shaders."
    "{a=https://www.renpy.org/doc/html/cdd.html#renpy.Render.add_shader}add_shader(shader){/a} - This causes the shader part shader to be used when this Render or its children are drawn."
    "{a=https://www.renpy.org/doc/html/cdd.html#renpy.Render.add_uniform}add_uniform(name, value){/a} - Causes the uniform name to have value."
    "{a=https://www.renpy.org/doc/html/cdd.html#renpy.Render.add_property}add_property(name, value){/a} - Causes the GL property name to have value."
    "Last but not least, {a=https://www.renpy.org/doc/html/cdd.html#renpy.Render.mesh}mesh{/a} field, that enables model-based rendering for this Render."
    "Not all of them are needed at the same time, likewise explaining {a=https://www.renpy.org/doc/html/model.html#gl-properties}GL properties{/a}, {a=https://www.renpy.org/doc/html/model.html#Model}Model{/a} and {a=https://www.renpy.org/doc/html/model.html#transforms-and-model-based-rendering}mesh{/a} concepts lays beyond the tutorial."
    "But enough with theory."

label .section_01:

    nvl clear
    show example intermediate_03_01b

    "Finally, we add shader to our render and set {=green}mesh{/} to True in order to turn it into a {b}Model{/b} with {=green}left{/} / {=green}right{/} being tex0 / tex1."

    show example intermediate_03_01c

    "Then we have to provide {=green}u_renpy_dissolve{/g}, but what is the value?"

    show example intermediate_03_01d

    "Here I calculate it as a fraction of the mouse position {=green}x{/} compared to the image width (where {=blue}clamp{/} is a small helper function that limits the value to a range between 0 and 1)."

    nvl clear
    hide example

    call screen test_screen(
        obj = intermediate_03_shaders.Example_1('eileen happy', 'eileen vhappy'),
        desc = _("Move mouse left and right.")
    )

label .section_02:

    "Let's practice some more and change the dissolve effect to pixellate."

    show example intermediate_03_02a

    "This time we won't need two images, instead we'll just have one widget and a max pixellation step, but everything else will remain untouched."

    nvl clear
    show example intermediate_03_02b

    "Renpy handles pixellation with \"{=green}renpy.texture{/}\" shader and {=green}u_lod_bias{/} = less details with lod growth (reasonable values are somewhere between 0 and 5)."

    show example intermediate_03_02c

    "Again, the calculation of the part is based on the mouse position on the x-axis, but in the range from 0 to the maximum step."

    nvl clear
    hide example

    call screen test_screen(
        obj = intermediate_03_shaders.Example_2('eileen happy', 5),
        desc = _("Alas, the picture becomes terribly blurry.")
    )

label .section_03:

    nvl clear
    show example intermediate_03_02d

    "To fix this situation, we need a GL property called \"{=green}texture_scaling{/}\"."

    nvl clear
    hide example

    call screen test_screen(
        obj = intermediate_03_shaders.Example_2('eileen happy', 5, good=True),
        desc = _("Perfect.")
    )

label .section_04:

    nvl clear

    "How about writing a simple shader?"

    show example intermediate_03_03a

    "This would be a distortion test example. It just does some artificial trigonometry."
    "It takes {=green}u_distort{/} and must change over time along with {a=https://www.renpy.org/doc/html/model.html#uniforms-and-attributes}u_time{/a}."

    show example intermediate_03_03b

    "Just passing in all the information it needs."

    nvl clear
    hide example

    call screen test_screen(
        obj = intermediate_03_shaders.Example_3('eileen happy'),
    )

label .section_05:

    nvl clear

    "As a side note, it doesn't have to be one shader at a time. We can apply several shaders at once, but there are a lot of nuances here: the shader parts priority, the naming of variables, and so on, making ren'py throw ShaderError exceptions, that aren't friendly at all. (though {a=https://www.renpy.org/doc/html/model.html#var-config.log_gl_shaders}config.log_gl_shaders{/a} might come in handy.)"
    "We won't delve too deeply into examining this topic and just limit ourselves with a funny example."
    "Let's say, I want to combine dissolving effect with pixellation and distortion."

    nvl clear
    show example intermediate_03_04a

    "This is a proposed CDD that accepts all required arguments "
    extend " and I'll tell you right away that nothing will work like this."

    show example intermediate_03_04b

    "For one thing, \"{=green}shader.distort{/}\" declares variable {=green}color0{/} which is already declared by \"{=green}renpy.dissolve{/}\"."
    "Secondly, both shaders take colors from supplied {=green}textures{/} not from one another, rewriting {=green}gl_FragColor{/}. It's a pity, but this was to be expected."

    hide example

    "In addition, because of the united scope or variables between shader parts, \"pixellation\" can be done without explicitly added \"{=green}renpy.texture{/}\"."
    "There is no choice but to fix all the issues and modify the custom shader."

    nvl clear
    show example intermediate_03_04c

    "Here is the modified shader. On a closer look, it only has 2 variables that are missing from previously added shaders, and {=green}color0{/} is used without declaring it."

    show example intermediate_03_04d

    "Fixed the render: removed unnecessary shader. Time to test our CDD again."

    nvl clear
    hide example

    call screen test_screen(
        obj = intermediate_03_shaders.Example_4('eileen happy', 'eileen vhappy', 2, 0.15),
        desc = _("Well, it almost does the job, but where's dissolve now?")
    )

    "Okay, let's remember {a=https://www.renpy.org/doc/html/model.html#var-config.log_gl_shaders}config.log_gl_shaders{/a} and use it to debug the result. (inspect logs)"

    show example intermediate_03_05a

    "There are problems there. The color from dissolve part is replaced in distort_mod part, thus making dissolve ineffective and pointless."
    "It's probably easier to just implement all the logic inside distort_mod, but hold on, I've got an idea."

    hide example
    show screen test_screen('eileen_heads_example')

    "Eileen's sprites are almost identical except for their top (face) part."
    "Nothing stops me from using any of the textures to make only her bottom part wiggle :P"

    nvl clear
    hide screen test_screen
    show example intermediate_03_05b

    "Now if you look at this new shader called \"{=green}shader.wiggle{/}\", it uses a single texture and it only works on data whose y coordinate is greater than 0.5."
    "Note that the upper part's color is still controlled by \"{=green}renpy.dissolve{/}\" shader. Rename the shader and enjoy the result."

    nvl clear
    hide example

    call screen test_screen(
        obj = intermediate_03_shaders.Example_5('eileen happy', 'eileen vhappy', 2, 0.15),
        desc = _("Smile and wiggle")
    )

label .section_06:

    "Are we done yet? Well... How about doing something practical. I swear, this will be the last part of the lesson :D"
    "Here's the idea. Eileen will hide somewhere and we'll search her behind the fog with a flashlight."

    show example intermediate_03_06a small

    "Proposed displayable arguments will be as follows:\nsolid color behind Eileen\n\"fog\" = foreground displayable\n80 pix = flashlight circle radius."

    hide example
    nvl clear
    show example intermediate_03_06b large

    "The init part is trivial, except for setting up the background."

    show example intermediate_03_06c

    "I randomize Eileen's position and her sprite size between 50\% and 90\%."

    show example intermediate_03_06d

    "Then, using the values, set Composite as the base image."

    nvl clear
    show example intermediate_03_06e

    "Once again, {=blue}event(){/} only memorizes mouse x/y position, triggering self redraw."

    show example intermediate_03_06f

    "{=blue}render(){/} applies \"{=green}shader.flashlight{/green}\" to the base and foreground."
    "Note that the {=green}u_pos{/} uniform is passed as a tuple, treated as vec2 type in GLSL."

    nvl clear
    show example intermediate_03_06g

    "Now of course the most interesting part is the shader."
    "It utilizes {=green}u_model_size{/} to calculate pixel distances, performing the effect with use of built-in GLSL functions, described in chapter 8 of {a=https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf}the manual{/a}."
    "Time to play hide and seek."

    hide example

    call screen test_screen(
        obj = intermediate_03_shaders.Example_6(
            widget = "eileen vhappy",
            background = Solid("#d8ddc1"),
            foreground = "fog",
            distance = 80),
        desc = _("Can you find her?")
    )

    nvl clear
    show example intermediate_03_06h small

    "Sure you can say, that it's not impossible to make such a mini game without going CDD + shaders, but just to briebly illustrate the possibilities, I'll reduce {=green}lod{/} closer to edges of the light circle, making it look like a blur. Can't do that without shaders :}"

    hide example

    call screen test_screen(
        obj = intermediate_03_shaders.Example_6(
            widget = "eileen happy",
            background = Solid("#d8ddc1"),
            foreground = "fog",
            distance = 100,
            shader = "shader.flashlight_mod"),
        desc = _("Find her again")
    )

    return

############ DATA ##############

init python in intermediate_03_shaders:
    import pygame
    import random
    from store import clamp, Transform, Solid, config, Composite

    class Example_1(renpy.Displayable):
        def __init__(self, left, right, **kwargs):
            super().__init__(**kwargs)
            self.left = renpy.displayable(left)
            self.right = renpy.displayable(right)
            self.x, self.y = 0, 0

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            left = renpy.render(self.left, width, height, st, at)
            right = renpy.render(self.right, width, height, st, at)
            w, h = left.get_size()

            rv.mesh = True
            rv.add_shader("renpy.dissolve")
            rv.add_uniform("u_renpy_dissolve", clamp(self.x / w)) 

            rv.blit(left, (0, 0))
            rv.blit(right, (0, 0))

            return rv 

        def event(self, ev, x, y, st):
            self.x, self.y = x, y
            renpy.redraw(self, 0)
            raise renpy.IgnoreEvent

    class Example_2(renpy.Displayable):
        def __init__(self, widget, steps, **kwargs):
            super().__init__(**kwargs)
            self.widget = renpy.displayable(widget)
            self.steps = steps
            self.x, self.y = 0, 0
            self.good = kwargs.get('good')

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            widget = renpy.render(self.widget, width, height, st, at)
            w, h = widget.get_size()

            quantum = w / (self.steps)
            step = clamp(self.x / quantum, 0, self.steps)

            rv.mesh = True
            rv.add_shader("renpy.texture")
            rv.add_uniform("u_lod_bias", step)

            if self.good:
                rv.add_property("texture_scaling", "nearest_mipmap_nearest")

            rv.blit(widget, (0, 0))

            return rv 

        def event(self, ev, x, y, st):
            self.x, self.y = x, y
            renpy.redraw(self, 0)
            raise renpy.IgnoreEvent

    class Example_3(renpy.Displayable):
        def __init__(self, widget, **kwargs):
            super().__init__(**kwargs)
            self.widget = renpy.displayable(widget)

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            widget = renpy.render(self.widget, width, height, st, at)
            rv.blit(widget, (0, 0))

            rv.add_shader("shader.distort")
            rv.add_uniform("u_distort", 0.02)

            renpy.redraw(self, 0)
            return rv 

    class Example_4(renpy.Displayable):

        def __init__(self, left, right, pixellation_level, distortion, **kwargs):
            super().__init__(**kwargs)
            self.left = renpy.displayable(left)
            self.right = renpy.displayable(right)
            self.pixellation_level = pixellation_level
            self.distortion = distortion
            self.x, self.y = 0, 0

        def event(self, ev, x, y, st):
            self.x, self.y = x, y
            raise renpy.IgnoreEvent

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            left = renpy.render(self.left, width, height, st, at)
            right = renpy.render(self.right, width, height, st, at)
            w, h = left.get_size()

            # dissolving
            rv.mesh = True
            rv.add_shader("renpy.dissolve")
            rv.add_uniform("u_renpy_dissolve", clamp(self.x / w)) 

            # applying lod and texture_scaling
            rv.add_uniform("u_lod_bias", self.pixellation_level)
            rv.add_property("texture_scaling", "nearest_mipmap_nearest")

            # adding our custom shader
            rv.add_shader("shader.distort_mod")
            rv.add_uniform("u_distort", self.distortion)

            rv.blit(left, (0, 0))
            rv.blit(right, (0, 0))
            renpy.redraw(self, 0)
            return rv 

    class Example_5(renpy.Displayable):

        def __init__(self, left, right, pixellation_level, distortion, **kwargs):
            super().__init__(**kwargs)
            self.left = renpy.displayable(left)
            self.right = renpy.displayable(right)
            self.pixellation_level = pixellation_level
            self.distortion = distortion
            self.x, self.y = 0, 0

        def event(self, ev, x, y, st):
            self.x, self.y = x, y
            raise renpy.IgnoreEvent

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            left = renpy.render(self.left, width, height, st, at)
            right = renpy.render(self.right, width, height, st, at)
            w, h = left.get_size()

            # dissolving
            rv.mesh = True
            rv.add_shader("renpy.dissolve")
            rv.add_uniform("u_renpy_dissolve", clamp(self.x / w)) 

            # applying lod and texture_scaling
            rv.add_uniform("u_lod_bias", self.pixellation_level)
            rv.add_property("texture_scaling", "nearest_mipmap_nearest")

            # adding our custom shader
            rv.add_shader("shader.wiggle")
            rv.add_uniform("u_distort", self.distortion)

            rv.blit(left, (0, 0))
            rv.blit(right, (0, 0))
            renpy.redraw(self, 0)
            return rv 

    class Example_6(renpy.Displayable):
        def __init__(self, widget, background, foreground, distance, **kwargs):
            super().__init__(**kwargs)

            # randomizing position
            w, h = config.screen_width, config.screen_height
            x, y = (random.randint(50, t) for t in (w - 100, h - 200))
            z = random.uniform(0.5, 0.9)

            self.base = Composite((w, h),
                (0, 0), renpy.displayable(background),
                (x, y), Transform(renpy.displayable(widget), zoom=z)
            )
            self.foreground = renpy.displayable(foreground)
            self.distance = distance
            self.x, self.y = 0, 0
            self.shader = kwargs.get('shader')

        def event(self, ev, x, y, st):
            if x > 0 and y > 0:
                self.x, self.y = x, y
                renpy.redraw(self, 0)
            raise renpy.IgnoreEvent

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            rv.place(self.base, 0, 0)
            rv.place(self.foreground, 0, 0)
  
            rv.mesh = True
            rv.add_shader(self.shader or "shader.flashlight")
            rv.add_uniform("u_pos", (self.x, self.y))
            rv.add_uniform("u_distance", self.distance)
            return rv 

### SHADERS ###
#define config.log_gl_shaders = True

init python hide:
    renpy.register_shader("shader.distort"
    , variables="""
        uniform float u_lod_bias;
        uniform sampler2D tex0;
        uniform float u_distort;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        uniform float u_time;

    """, vertex_300="""
        v_tex_coord = a_tex_coord;

    """, fragment_300="""
        const float pi = 3.1415926;
        vec2 coord = v_tex_coord.st;

        float factor = sin(u_time * pi) * u_distort;
        coord.x += factor * cos(pi * coord.y);

        vec4 color0 = texture2D(tex0, coord, u_lod_bias);
        gl_FragColor = color0;
    """)

    renpy.register_shader("shader.distort_mod"
    , variables="""
        uniform float u_distort;
        uniform float u_time;

    """, fragment_300="""
        const float pi = 3.1415926;
        vec2 coord = v_tex_coord.st;

        float factor = sin(u_time * pi) * u_distort;
        coord.x += factor * cos(pi * coord.y);

        color0 = texture2D(tex0, coord, u_lod_bias);
        gl_FragColor = color0;
    """)

    renpy.register_shader("shader.wiggle"
    , variables="""
        uniform float u_distort;
        uniform float u_time;

    """, fragment_300="""
        const float pi = 3.1415926;
        vec2 coord = v_tex_coord.st;

        if (coord.y > 0.5) {
            float factor = sin(u_time * pi) * u_distort;
            coord.x += factor * cos(pi * coord.y);

            gl_FragColor = texture2D(tex0, coord, u_lod_bias);
        }
    """)

    renpy.register_shader("shader.flashlight"
    , variables="""
        uniform float u_lod_bias;
        uniform sampler2D tex0;
        uniform sampler2D tex1;
        uniform vec2 u_pos;
        uniform float u_distance;
        varying vec2 v_tex_coord;
        attribute vec2 a_tex_coord;
        uniform vec2 u_model_size;

    """, vertex_300=""" 
        v_tex_coord = a_tex_coord;

    """, fragment_300="""
        vec2 coord = v_tex_coord.st;
        vec2 cur = coord * u_model_size;

        float d = distance(u_pos, cur);
        float visibility_factor = smoothstep(u_distance / 2, u_distance, d);

        vec4 color0 = texture2D(tex0, coord, u_lod_bias);
        vec4 color1 = texture2D(tex1, coord, u_lod_bias);
        gl_FragColor = mix(color0, color1, visibility_factor);
    """)

    renpy.register_shader("shader.flashlight_mod"
    , variables="""
        uniform float u_lod_bias;
        uniform sampler2D tex0;
        uniform sampler2D tex1;
        uniform vec2 u_pos;
        uniform float u_distance;
        varying vec2 v_tex_coord;
        attribute vec2 a_tex_coord;
        uniform vec2 u_model_size;

    """, vertex_300=""" 
        v_tex_coord = a_tex_coord;

    """, fragment_300="""
        vec2 coord = v_tex_coord.st;
        vec2 cur = coord * u_model_size;

        float d = distance(u_pos, cur);
        float visibility_factor = smoothstep(u_distance / 2, u_distance, d);
        float base_lod = int(visibility_factor * 4);
        vec4 color0 = texture2D(tex0, coord, base_lod);
        vec4 color1 = texture2D(tex1, coord, u_lod_bias);
        gl_FragColor = mix(color0, color1, visibility_factor);
    """)

image eileen_heads_example = LayeredImage(attributes=[
    Solid('#69c6f177', xsize=300, ysize=180),
    Transform('eileen happy', crop=(0, 0, 300, 360), zoom=0.5),
    Transform(Text('happy', style='note'), xpos=4),
    Transform('eileen vhappy', crop=(0, 0, 300, 360), zoom=0.5, xpos=150),
    Transform(Text('vhappy', style='note'), xpos=212),
    Transform(Solid('#f1bb6977', xsize=300, ysize=180), ypos=180),
    Transform('eileen happy', crop=(0, 360, 300, 360), zoom=0.5, ypos=180, xpos=75),
    ])