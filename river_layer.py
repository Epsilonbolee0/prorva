import cocos
from cocos.actions import *
from cocos.layer import *
from cocos.sprite import Sprite
from random import choice
import pyglet

class WaterFlow(cocos.layer.Layer):
    def __init__(self):
        super(WaterFlow, self).__init__()

        river_anim = []
        
        for i in range(10):
            tmp = pyglet.resource.image(
                "src/blocks/river/animation/river_flow000" + str(i) + ".png")
            river_anim.append(tmp)
        for i in range(10, 31):
            tmp = pyglet.resource.image(
                "src/blocks/river/animation/river_flow00" + str(i) + ".png")
            river_anim.append(tmp)
        flow = pyglet.image.Animation.from_image_sequence(river_anim, 0.01,
                                                          loop=True)
        '''
        flow = pyglet.image.load_animation("src/blocks/river/animation/river_flow.gif")
        '''
        x, y = director.get_window_size()

        sprite = Sprite(flow)
        sprite.scale_y = y/1152
        sprite.scale_x = x/2048
        sprite.position = (x // 2, y // 2)

        self.add(sprite)
