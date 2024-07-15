define narrator = Character(None, kind=nvl)

style blue is text:
    color '#6453f7'
  
style red is text:
    color '#F00'

style green is text:
    color '#0F0'

style note is text:
    color '#eee'
    outlines [(1, '#070424dd', 1, 1)]

screen test_screen(obj, desc=None, close=None):

    default game = obj
    add game

    if desc:
        text desc xalign 0.5 yalign 0.05 style 'note'
    
    if close:
        textbutton "CLOSE" action Return() xalign 1.0 yalign 0.05
    else:
        key 'dismiss' action Return()

transform basic_05_transform_1:
    zoom 0.5
    parallel:
        ease 3.0 blur 4.0
        ease 3.0 blur 0.0
        repeat
    parallel:
        linear 1.0 alpha 0.1
        linear 1.0 alpha 1.0
        repeat
    parallel:
        linear 0.5 matrixcolor TintMatrix('#F00')
        linear 0.5 matrixcolor TintMatrix('#0F0')
        linear 0.5 matrixcolor TintMatrix('#00F')
        repeat
    parallel:
        rotate 0
        linear 3.5 rotate 360
        repeat

init python:
    renpy.add_to_all_stores('basic_05_transform_1', basic_05_transform_1)
