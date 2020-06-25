import cocos
from cocos.actions import *
from cocos.director import director
import pyglet
# Импорт методов для красивох переходов сцен
from cocos.scenes.transitions import *
from cocos.sprite import Sprite
from cocos.layer import Layer
from cocos.scene import Scene
from collections import Counter


# Название игры, которое с периодом на экране уменьшается и увеличивается
class NameGame(cocos.layer.Layer):
    def __init__(self):
        super(NameGame, self).__init__()

        label = cocos.sprite.Sprite("src/arts/PRORVA.png")
        label.scale = 1
        size = director.get_window_size()
        label.position = size[0]/4.7, size[1] - size[1]/10
        self.add(label)



# Фон через спрайт
class SpriteVillage(cocos.sprite.Sprite):
    def __init__(self):
        super(SpriteVillage, self).__init__("src/arts/Village.jpeg")

        self.scale = 2/3
        size = cocos.director.director.get_window_size()
        self.position = size[0]/2, size[1]/2

# Таргеты
class TurgetSprite(cocos.sprite.Sprite):
    def __init__(self):
        super(TurgetSprite, self).__init__()


# Свиток, на котором расположены пункты меню
class ClothSprite(cocos.sprite.Sprite):
    def __init__(self):
        super(ClothSprite, self).__init__('src/fonts/main_menu_towel.png')
        size = cocos.director.director.get_window_size()
        self.scale = 0.535
        self.position = size[0]/5.5, size[1]/1.369 - size[1]/4.2

# Свиток, на котором расположены пункты меню
class ScrollSprite(cocos.sprite.Sprite):
    def __init__(self):
        super(ScrollSprite, self).__init__('src/fonts/scroll.png')
        size = cocos.director.director.get_window_size()
        self.scale = 0.535
        self.position = size[0]/2, size[1]/1.369 - size[1]/4.2

class ScrollText(cocos.layer.Layer):
    def __init__(self, quest):
        super(ScrollText, self).__init__()
        size = cocos.director.director.get_window_size()

        head = cocos.text.Label(text=quest.head, font_size=30, align="center", color =(255,0,0,255), font_name="Papyrus")
        head.position = (size[0]/2-125, size[1]/1.369-50)
        self.add(head)

        reward = cocos.text.Label(text="Reward:", font_size=24, align="center", color =(0,0,0,255), font_name="Papyrus")
        reward.position = (size[0]/2-125, size[1]/1.369 - 100)
        self.add(reward)

        j = 0
        bounty = dict(Counter(quest.bounty))
        for item in bounty:
            if item.name == "sword":
                item_name = "src/items/" + item.name + ".png"
                self.add(Sprite(item_name, position=(
                    size[0] // 2 - 200 + j * 132, size[1] // 2), scale=0.15))
            else:
                item_name = "src/items/" + item.name + ".png"
                self.add(Sprite(item_name, position=(
                    size[0] // 2 - 50 + j * 128, size[1] // 2), scale=0.5))
            n = str(bounty[item])
            number = cocos.text.Label(text=n, font_size=30, font_name ="Papyrus",
                                      color=(0, 0, 0, 255))
            number.position = size[0] // 2 - 100 + j * 128, size[1] // 2 - 50
            self.add(number)
            j += 1


# Название первого города (текст)
class NameFirstCity(cocos.text.Label):
    def __init__(self):
        super(NameFirstCity, self).__init__("Ladoga", font_size=33, color=(0, 0, 0, 255),
                                            font_name = 'Papyrus')

        size = director.get_window_size()
        self.position = 7.73 * size[0] / 10, 1 * size[1] / 10

# Фон(флаг), на котором располагается текстовое название города
class LabelCity(cocos.sprite.Sprite):
    def __init__(self):
        super(LabelCity, self).__init__('src/fonts/city_label.png')
        self.scale = 1/2.8
        size = director.get_window_size()
        self.position = 8.4 * size[0] / 10, 1 * size[1] / 10

# Фон города
class FirstSitySprite(cocos.sprite.Sprite):
    def __init__(self):
        super(FirstSitySprite, self).__init__("src/arts/city_01_ladoga_clear.png")

        self.scale = 2/3
        size = cocos.director.director.get_window_size()
        self.position = size[0]/2, size[1]/2

class TableArrow(Sprite):
    def __init__(self):
        super(TableArrow, self).__init__('src/fonts/back_butt_bg.png')
        self.scale = 1
        size = cocos.director.director.get_window_size()
        self.position = size[0] / 20 * 1.3, size[1] / 20 * 18.5


# Фон доков
class DocksSprite(cocos.sprite.Sprite):
    def __init__(self):
        super(DocksSprite, self).__init__('src/arts/docks.png')
        self.scale = 2/3
        size = cocos.director.director.get_window_size()
        self.position = size[0]/2, size[1]/2

# Причал в доках(фон для меню)
class SpriteMenuDocks(Layer):
    def __init__(self):
        super(SpriteMenuDocks, self).__init__()
        sprite_menu_1 = Sprite('src/arts/in_game_menu_docks.png')
        sprite_menu_1.scale = 2 / 3
        size = cocos.director.director.get_window_size()
        self.add(sprite_menu_1)
        sprite_menu_1.position = size[0]*17/20, size[1]/2
        #sprite_menu_1.do(MoveTo((size[0]*19/20, size[1]/2), 0.7))

class WhiteSquare(Sprite):
    def __init__(self, scale_X, scale_Y, Position):
        super(WhiteSquare, self).__init__("src/fonts/background.png")
        self.scale_x = scale_X
        self.scale_y = scale_Y
        self.position = Position
        self.color = (200, 200, 200)
        self.opacity = 255


class WhiteSquareAlt(Sprite):
    def __init__(self, scale_X, scale_Y, Position, color):
        super(WhiteSquareAlt, self).__init__("src/fonts/background.png")
        self.scale_x = scale_X
        self.scale_y = scale_Y
        self.position = Position
        self.color = color
        self.opacity = 255


class TempleBg(Sprite):
    def __init__(self, Color):
        super(TempleBg, self).__init__("src/arts/temple_ladoga1.png")
        size = cocos.director.director.get_window_size()
        self.color = Color
        self.scale_x = 1.8
        self.scale_y = 1.5
        self.position = (size[0] // 2, size[1] // 2)


class QuestBlock(Layer):
    def __init__(self, quest, me, i):
        super(QuestBlock, self).__init__()
        self.me = me
        size = director.get_window_size()
        self.add(WhiteSquare(0.55, 0.3, (1000, size[1] - 275 - i * 300)))
        head_color = (255, 255, 255, 255)
        head = cocos.text.Label(quest.head, font_name="Papyrus", font_size=30, color=head_color)
        head.position = size[0] - 527, size[1] - 175 - i * 300
        self.add(head)
        label = cocos.text.Label(text=quest.story, font_name="Papyrus", font_size=20, width=490,
                                 color=head_color, multiline=True)
        label.position = size[0] - 527, size[1] - 210 - i * 300
        self.add(label)

        req = cocos.text.Label(text="Requirments: ", font_name="Papyrus", font_size=20,
                               color=head_color)
        req.position = size[0] - 527, size[1] - 300 - i * 300
        self.add(req)
        bounty = cocos.text.Label(text="Bounty: ", font_name="Papyrus", font_size=20,
                                  color=head_color)
        bounty.position = size[0] - 527, size[1] - 375 - i * 300
        self.add(bounty)

        num = dict(Counter(quest.req_items))
        have = dict(Counter(self.me.inventory))

        j = 0
        for item in num:
            #self.add(WhiteSquare(0.072, 0.075,(size[0] - 350 + j * 76,size[1] - 303 - i * 300)))
            if item.name == "sword":
                item_name = "src/items/" + item.name + ".png"
                self.add(Sprite(item_name, position=(
                    size[0] - 350 + j * 76, size[1] - 305 - i * 300),
                                scale=0.001))
            else:
                item_name = "src/items/" + item.name + ".png"
                self.add(Sprite(item_name, position=(
                    size[0] - 350 + j * 76, size[1] - 305 - i * 300), scale=0.4))
            h = 0
            if item in self.me.inventory:
                if item.name == "gold": h = str(self.me.gold)
                else: h = str(have[item])
            n = str(num[item])
            number = cocos.text.Label(text=str(h) + '/' + str(n), font_size=14,
                                      color=(255, 255, 255, 255))
            number.position = size[0] - 383 + j*76, size[1] - 337 - i*300
            self.add(number)
            j += 1

        j = 0
        num = dict(Counter(quest.bounty))
        for item in num:
            # self.add(WhiteSquare(0.072, 0.075,(size[0] - 350 + j * 76,size[1] - 372 - i * 300)))
            if item.name == "sword":
                item_name = "src/items/" + item.name + ".png"
                self.add(Sprite(item_name, position=(
                    size[0] - 350 + j * 76, size[1] - 372 - i * 300),
                                scale=0.12))
            else:
                item_name = "src/items/" + item.name + ".png"
                self.add(Sprite(item_name, position=(
                    size[0] - 350 + j * 76, size[1] - 372 - i * 300), scale=0.4))

            n = str(num[item])
            number = cocos.text.Label(text=n, font_size=14,
                                      color=(255, 255, 255, 255))
            number.position = size[0] - 383 + j * 76, size[1] - 402 - i * 300
            self.add(number)
            j += 1


class BarracksBg(Sprite):
    def __init__(self):
        super(BarracksBg, self).__init__("src/arts/barracks_ladoga.png")
        size = cocos.director.director.get_window_size()
        self.scale_x = 1.8
        self.scale_y = 1.5
        self.position = (size[0] // 2, size[1] // 2)


class FairBg(Sprite):
    def __init__(self):
        super(FairBg, self).__init__("src/arts/fair_ladoga1.png")
        size = cocos.director.director.get_window_size()
        self.scale_x = 0.7
        self.scale_y = 0.7
        self.position = (size[0] // 2, size[1] // 2)


