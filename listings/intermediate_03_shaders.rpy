init python:

    import random
    import pygame

    # Smile and wiggle example
    class Example_1(renpy.Displayable):

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

    # Hide and seek example
    class Example_2(renpy.Displayable):
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
            rv.add_shader("shader.flashlight")
            rv.add_uniform("u_pos", (self.x, self.y))
            rv.add_uniform("u_distance", self.distance)
            return rv 

init python hide:

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
        float base_lod = int(visibility_factor * 4);
        vec4 color0 = texture2D(tex0, coord, base_lod);
        vec4 color1 = texture2D(tex1, coord, u_lod_bias);
        gl_FragColor = mix(color0, color1, visibility_factor);
    """)

screen test_screen_1():
    default game = Example_1('eileen happy', 'eileen vhappy', 2, 0.15)
    add game
    key 'dismiss' action Return()

screen test_screen_2():
    default game = Example_2(widget = "eileen happy",
            background = Solid("#d8ddc1"),
            foreground = "fog",
            distance = 100)
    add game
    key 'dismiss' action Return()

label start:
    call screen test_screen_1()
    call screen test_screen_2()
    return
