# Измененный файл библиотеки cocos'a

from __future__ import division, print_function, unicode_literals

__docformat__ = 'restructuredtext'

import cocos
from cocos.director import director
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene

import pyglet

from pyglet.gl import *

from cocos.menu import Menu
from cocos.menu import MenuItem

__pause_scene_generator__ = None


def get_pause_scene():
    return __pause_scene_generator__()


def set_pause_scene_generator(generator):
    global __pause_scene_generator__
    __pause_scene_generator__ = generator


def default_pause_scene():
    w, h = director.window.width, director.window.height
    texture = pyglet.image.Texture.create_for_size(
        GL_TEXTURE_2D, w, h, GL_RGBA)
    texture.blit_into(pyglet.image.get_buffer_manager().get_color_buffer(), 0, 0, 0)
    return PauseScene(texture.get_region(0, 0, w, h),
                      ColorLayer(25, 25, 25, 205), PauseLayer())
set_pause_scene_generator(default_pause_scene)


class PauseScene(Scene):
    """Pause Scene"""
    def __init__(self, background, *layers):
        super(PauseScene, self).__init__(*layers)
        self.bg = background
        self.width, self.height = director.get_window_size()

    def draw(self):
        self.bg.blit(0, 0, width=self.width, height=self.height)
        super(PauseScene, self).draw()


class PauseLayer(Layer):
    """Layer that shows the text 'PAUSED'
    """
    is_event_handler = True     #: enable pyglet's events

    def __init__(self):
        super(PauseLayer, self).__init__()

        x, y = director.get_window_size()

        ft = pyglet.font.load('Papyrus', 36)
        self.text = pyglet.font.Text(ft,
                                     'PAUSED',
                                     halign=pyglet.font.Text.CENTER)
        self.text.x = x // 2
        self.text.y = y // 1.1
        self.add(MenuPause())

    def draw(self):
        self.text.draw()


class MenuPause(Menu):
    def __init__(self):
        super(MenuPause, self).__init__()

        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (255, 255, 255, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'

        items = []

        items.append(cocos.menu.ToggleMenuItem('Show FPS:', self.on_show_fps, director.show_FPS))
        items.append(MenuItem("Back to game", self.unpaused))

        size = director.get_window_size()
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back(),
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                             [(size[0] / 2, size[1] / 10 * 4),
                              (size[0] / 2, size[1] / 10 * 3)]))

    def on_show_fps(self, value):
        director.show_FPS = value

    def unpaused(self):
        director.pop()
        return True

    def nothing(self):
        pass
