screen main_menu():
    tag menu

    add gui.main_menu_background

    frame:
        style "main_menu_frame"

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"

    viewport:
        pos (16, 16)
        xysize (360, 670)
        scrollbars None

        vbox:
            xoffset 20
            yoffset 20
            label "Basics"
            textbutton 'Lesson 1 - First CDD' action Start('basic_01_first_cdd')
            textbutton 'Lesson 2 - Events (Mouse)' action Start('basic_02_events')
            textbutton 'Lesson 3 - Events (Keyboard)' action Start('basic_03_kb_events')
            textbutton 'Lesson 4 - Render methods' action Start('basic_04_blit')
            textbutton 'Lesson 5 - Transform' action Start('basic_05_transform')
            text "{space=200}???" style 'unavailable'
            
            label "Intermediate"
            textbutton 'Lesson 1 - Canvas' action Start('intermediate_01_canvas')
            textbutton 'Lesson 2 - CDD children' action Start('intermediate_02_cdd_children')
            textbutton 'Lesson 3 - Shaders' action Start('intermediate_03_shaders')
            text "{space=200}???" style 'unavailable'

            #label "Test feature"
            #textbutton 'Test Lesson' action Start('test_lesson')

    text "...to be continued?" style "main_menu_tbc"
    text "[gui.about]" style "main_menu_about"

style main_menu_frame is empty:
    xsize 400
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox is vbox:
    xalign 1.0
    xoffset -40
    xmaximum 800
    yalign 0.0
    yoffset 20

style main_menu_text is gui_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title is main_menu_text:
    properties gui.text_properties("title")

style main_menu_version is main_menu_text:
    properties gui.text_properties("version")

style main_menu_tbc:
    size 16
    color gui.idle_color
    yalign 1.0
    xoffset 160
    yoffset -20

style main_menu_about:
    color gui.idle_color
    xsize 800
    yalign 0.95
    xalign 1.0
    xoffset -40
    text_align 1.0
 
style unavailable is text:
    color gui.muted_color