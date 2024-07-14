define narrator = Character(None, kind=nvl)

style blue is text:
    color '#6453f7'
  
style red is text:
    color '#F00'

style green is text:
    color '#0F0'

screen lesson_test_screen(obj, desc=None, close=None):

    if desc:
        text desc xalign 0.5 yalign 0.05
    
    default game = obj
    add game

    if close:
        textbutton "CLOSE" action Return() xalign 1.0 yalign 0.05
    else:
        key 'dismiss' action Return()
