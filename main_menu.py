import cocos
from cocos.actions import *
from cocos.director import director
import pyglet
# Импорт методов для красивох переходов сцен
from cocos.scenes.transitions import *
from cocos.sprite import Sprite
from cocos.layer import Layer
import new_pause
from river_layer import *
from menu_components import *
from polygon import *
from entities import *
from market import Market
from pyglet.window import mouse

from cocos.audio.pygame.mixer import Sound
from cocos.audio.pygame import mixer

record_id = 0

# Меню настроек
class MenuSettings(cocos.menu.Menu):
    def __init__(self):
        super(MenuSettings, self).__init__('Settings')

        # Задание параметров загаловка. В этом случае это Settings
        self.font_title['font_size'] = 72
        self.font_title['color'] = (255, 255, 255, 255)
        self.font_title['font_name'] = 'Papyrus'

        # Задание параметров пунктов меню
        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (255, 255, 255, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'

        # Создание пунктов меню
        items = []
        items.append(cocos.menu.ToggleMenuItem('Show FPS:', self.on_show_fps, director.show_FPS))
        items.append(cocos.menu.MenuItem("Back to main menu", self.back_to_main_menu)) # Через self указывается функция,
                                                                        # которая выполняется при нажатии на пункт меню


        # Берем размеры текущего состояние окна
        size = director.get_window_size()

        # Располгаем пункты меню на экране
        # cocos.menu.shake() - функция анимации при наведении на пункт
        # cocos.menu.shake_back() - функции анимации при "убирании" наведения на пункт меню
        # layout_strategy=... задает координаты соответствующих пунтков меню
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back(),
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                            [(size[0]/4.5, 6*size[1]/10),
                             (size[0] / 3.5, 2 * size[1] / 10)]))

    def on_show_fps(self, value):
        director.show_FPS = value

    # Функция возвращения в главное меню
    def back_to_main_menu(self):
        director.replace(ZoomTransition(cocos.scene.Scene(FirstScene()), 1))


# При вызове cocos.scene.Scene(GameSettings()) у нас появится сцена состоящая из объектов, описанных в классе
# другими словами - это составляющие сцены настроек(фон и меню)
class GameSettings(cocos.layer.Layer):
    def __init__(self):
        super(GameSettings, self).__init__()
        self.add(SpriteVillage())
        self.add(WhiteSquare(0.54, 0.2, (290, 475)))
        self.add(WhiteSquare(0.54, 0.1, (370, 140)))
        self.add(MenuSettings())

# Главное меню
class MainMenu(cocos.menu.Menu):
    is_event_handler = True
    def __init__(self):
        super(MainMenu, self).__init__()

        # Задание параметров пунктов меню
        self.font_item['color'] = (0, 0, 0, 255)
        self.font_item_selected['color'] = (0, 0, 0, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'

        # Создание пунтков меню
        items = []
        items.append(cocos.menu.MenuItem("Start", self.new_game))
        items.append(cocos.menu.MenuItem("Loading", self.loading))
        items.append(cocos.menu.MenuItem("Settings", self.game_settings))
        items.append(cocos.menu.MenuItem("Captions", self.captions))
        items.append(cocos.menu.MenuItem("Quit", self.quit))

        size = director.get_window_size() # Текущий размер экрана

        # Создание меню смотри class MenuSettigs
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back(),
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                            [(size[0]/4.7, 7.1*size[1]/10), (size[0]/4.7, 6.1*size[1]/10),
                             (size[0]/4.7, 5.1*size[1]/10), (size[0]/4.7, 4.1*size[1]/10),
                             (size[0]/4.7, 3.1*size[1]/10)]))

    # Переход на сцену нового города
    def new_game(self):
        director.replace(ZoomTransition(cocos.scene.Scene(FirstCity()), 1))

    # Переход на сцену загрузок
    def loading(self):
        director.replace(ZoomTransition(cocos.scene.Scene(Loadings()), 1))

    # Переход на сцену настроек
    def game_settings(self):
        director.replace(ZoomTransition(cocos.scene.Scene(GameSettings()), 1))

    # Переход на сцену титров
    def captions(self):
        director.replace(ZoomTransition(cocos.scene.Scene(Captions()), 1))

    # Завершение программы
    def quit(self):
        director.window.close()


# Сцена главного меню
# Составляющие (фон, название игры, свиток, меню)
class FirstScene(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(FirstScene, self).__init__(155, 89, 182, 1000)
        self.add(SpriteVillage())
        self.add(NameGame())
        self.add(ClothSprite())
        #self.add(AnimationHolst())
        self.add(MainMenu())
        

# Меню титров
class MenuCaptions(cocos.menu.Menu):
    def __init__(self):
        super(MenuCaptions, self).__init__('Captions')
        
        # Параметры заголовка
        self.font_title['font_size'] = 72
        self.font_title['color'] = (200, 20, 20, 255)
        self.font_title['font_name'] = 'Papyrus'

        # Парампетры пунктов меню
        self.font_item['color'] = (0, 0, 0, 255)
        self.font_item_selected['color'] = (0, 0, 0, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'

        # Смотри class MenuSettigs
        items = []
        items.append(cocos.menu.MenuItem("Back to main menu", self.back_to_main_menu))

        size = director.get_window_size()
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back(),
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                            [(size[0]/3.5, 2*size[1]/10)]))

    # Вернуться в главное меню
    def back_to_main_menu(self):
        director.replace(ZoomTransition(cocos.scene.Scene(FirstScene()), 1))


# Сцена титров
# Составляющие(фон, меню, какой-то текст)
class Captions(cocos.layer.Layer):
    def __init__(self):
        super(Captions, self).__init__()
        
        self.add(SpriteVillage())
        self.add(WhiteSquare(0.55, 0.1, (360, 140)))
        self.add(WhiteSquare(0.75, 0.25, (645, 400)))
        self.add(MenuCaptions())

        text1 = "Главными особенностями игры "
        label1 = cocos.text.Label(text1, font_size=32,
                                  color=(0, 0, 0, 255))
        size = director.get_window_size()
        label1.position = size[0]/4, size[1]/2 + 100

        text2 = "являются - экономика и "
        label2 = cocos.text.Label(text2, font_size=32,
                                  color=(0, 0, 0, 255))
        label2.position = size[0] / 4, size[1] / 2.4 + 100

        text3 = "неповторимый славянский стиль"
        label3 = cocos.text.Label(text3, font_size = 32,
                                  color=(255, 255, 255, 255))
        label3.position = size[0]/4, size[1]/3 + 100
        label3 = cocos.text.Label(text3, font_size=32,
                                  color=(0, 0, 0, 255))
        label3.position = size[0] / 4, size[1] / 3 + 100

        self.add(label1)
        self.add(label2)
        self.add(label3)


# Меню загрузок
class MenuLoading(cocos.menu.Menu):
    def __init__(self):
        super(MenuLoading, self).__init__('Select save')
        
        # Смотри class MenuSettigs
        self.font_title['font_size'] = 60
        self.font_title['color'] = (255, 255, 255, 255)
        self.font_title['font_name'] = 'Papyrus'

        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (255, 255, 255, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'

        items = []
        items.append(cocos.menu.MenuItem("Back to main menu", self.back_to_main_menu))

        items.append(cocos.menu.MenuItem("First", self.first_save))
        items.append(cocos.menu.MenuItem("Second", self.second_save))
        items.append(cocos.menu.MenuItem("Third", self.third_save))

        # (size[0]/2, 6*size[1]/10),

        size = director.get_window_size()
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back(),
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                            [(size[0]/3.5, 2*size[1]/10),
                             (size[0]/4.5, 7*size[1]/10),(size[0]/4.5, 6*size[1]/10),
                             (size[0]/4.5, 5*size[1]/10)]))

    def first_save(self):
        pass

    def second_save(self):
        pass

    def third_save(self):
        pass

    def back_to_main_menu(self):
        director.replace(ZoomTransition(cocos.scene.Scene(FirstScene()), 1))


# Сцена настроек
# Составляющие(фон, меню)
class Loadings(cocos.layer.Layer):
    def __init__(self):
        super(Loadings, self).__init__()
        
        self.add(SpriteVillage())
        self.add(WhiteSquare(0.3, 0.25, (280, 425)))
        self.add(WhiteSquare(0.54, 0.1, (370, 140)))
        self.add(MenuLoading())

# Меню города
class FirstCityMenu(cocos.menu.Menu):
    def __init__(self):
        super(FirstCityMenu, self).__init__()

        mixer.stop()

        sound = Sound("src/sounds/music/mischievous_beaters_eternal.ogg")
        sound.set_volume(0.1)
        sound.play(-1)
        '''
        self.font_item['color'] = (0, 0, 0, 255)
        self.font_item_selected['color'] = (0, 0, 0, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'
        '''

        self.font_item['font_size'] = 36
        self.font_item_selected['font_size'] = 36

        # Пункты меню теперь стали изображениями (ImageMenuItem)
        # Смотри class MenuSettigs
        items = []
        items.append(cocos.menu.ImageMenuItem("src/arts/temple_ladoga.png", self.go_to_temple))
        items.append(cocos.menu.ImageMenuItem("src/arts/barracks.png", self.go_to_barracks))
        items.append(cocos.menu.ImageMenuItem("src/arts/trading_house.png", self.go_to_fair))
        items.append(cocos.menu.ImageMenuItem("src/arts/doki.png", self.go_to_docks))
        items.append(cocos.menu.ImageMenuItem("src/fonts/back_butt_row.png", self.back_to_main_menu))


        items[0].scale = 9
        items[1].scale = 4
        items[2].scale = 3
        items[3].scale = 3

        size = director.get_window_size()
        self.create_menu(items, layout_strategy=cocos.menu.fixedPositionMenuLayout(
                             [(size[0] / 4.723, 7.5 * size[1] / 10), (size[0] / 1.93, size[1] / 1.73),
                               (size[0] / 4.9, 4.95 * size[1] / 10), (size[0] / 4.1, 3.4 * size[1] / 10),
                            (size[0] / 20 * 1.1, size[1] / 20 * 19.3)]))

    def go_to_temple(self):
        mixer.stop()

        sound = Sound("src/sounds/sound_temple.ogg")
        sound.set_volume(0.1)
        sound.play()
        director.replace(ZoomTransition(cocos.scene.Scene(TempleScene()), 1))

    def go_to_fair(self):
        mixer.stop()

        sound = Sound("src/sounds/fair.ogg")
        sound.set_volume(0.1)
        sound.play()
        director.replace(ZoomTransition(cocos.scene.Scene(FairLadogaLayer()), 1))

    def go_to_docks(self):
        director.replace(ZoomTransition(cocos.scene.Scene(DocksLadoga()), 1))

    def go_to_barracks(self):
        mixer.stop()

        sound = Sound("src/sounds/barracks.ogg")
        sound.set_volume(0.1)
        sound.play()
        director.replace(ZoomTransition(cocos.scene.Scene(BarracksLadogaLayer()), 1))

    def back_to_main_menu(self):
        mixer.stop()

        sound = Sound("src/sounds/morning_field_sounds.ogg")
        sound.set_volume(0.1)
        sound.play(-1)
        director.replace(ZoomTransition(cocos.scene.Scene(FirstScene()), 1))


# Сцена города
# Составляющие(фон, фон названия(флаг), название, меню)
class FirstCity(cocos.layer.Layer):
    def __init__(self):
        super(FirstCity, self).__init__()
        self.add(FirstSitySprite())
        self.add(LabelCity())
        self.add(NameFirstCity())
        self.add(TableArrow())
        self.add(FirstCityMenu())

        #mixer.stop()
        #bg_music = Sound("src/sounds/music/mischievous_beaters.ogg")
        #bg_music.set_volume(0.02)
        #bg_music.play(-1)


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

class MenuDocks(cocos.menu.Menu):
    def __init__(self):
        super(MenuDocks, self).__init__()

        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (255, 255, 255, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'

        items = []
        items.append(cocos.menu.MenuItem('Save', self.broke))
        items.append(cocos.menu.MenuItem('Set sail', self.set_sail))
        items.append(cocos.menu.MenuItem('Back', self.back_to_city))

        size = director.get_window_size()
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back(),
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
            [(size[0] / 20 * 17, 8 * size[1] / 20),
            (size[0] / 20 * 17, 5 * size[1] / 20),
            (size[0] / 20 * 17, 2 * size[1] / 20)]))

    def broke(self):

        saves = SaveDB()
        record = saves.load_save(record_id)

        record["blocks"] = boat.blocks
        saves.make_save(record)

    def set_sail(self):
        director.replace(ZoomTransition(cocos.scene.Scene(Sail()), 1))

    def back_to_city(self):
        director.replace(ZoomTransition(cocos.scene.Scene(FirstCity()), 1))

# Сцена доков
class DocksLadoga(Layer):
    is_event_handler = True

    def __init__(self):
        global boat
        global me
        super(DocksLadoga, self).__init__()
        size = director.get_window_size()
        self.add(DocksSprite())
        self.add(SpriteMenuDocks())
        self.add(MenuDocks())

        self.add(cocos.text.Label(text="Units", position=(
        size[0] / 20 * 16.7, 19.2 * size[1] / 20 - 150),
                                  font_name='Papyrus', font_size=20,
                                  color=(255, 255, 255, 255)))

        self.add(cocos.text.Label(text="bowman", position=(
        size[0] / 20 * 16.9, 17.7 * size[1] / 20 - 150),
                                  font_name='Papyrus', font_size=12,
                                  color=(255, 255, 255, 255)))

        self.add(cocos.text.Label(text="warrior", position=(
        size[0] / 20 * 14.85, 17.7 * size[1] / 20 - 150),
                                  font_name='Papyrus', font_size=12,
                                  color=(255, 255, 255, 255)))

        self.add(cocos.text.Label(text="carpenter", position=(
        size[0] / 20 * 14.8, 15.5 * size[1] / 20 - 150),
                                  font_name='Papyrus', font_size=12,
                                  color=(255, 255, 255, 255)))

        self.add(cocos.text.Label(text="priest", position=(
        size[0] / 20 * 17, 15.5 * size[1] / 20 - 150),
                                  font_name='Papyrus', font_size=12,
                                  color=(255, 255, 255, 255)))

        self.add(cocos.text.Label(text="trader", position=(
        size[0] / 20 * 18.8, 16.5 * size[1] / 20 - 150),
                                  font_name='Papyrus', font_size=12,
                                  color=(255, 255, 255, 255)))

        docks = Docks_Manager()
        docks.load_ship(0)

        docks.mouse_layer.boat.map.set_view(-256, -256,
                                            docks.mouse_layer.boat.map.px_width + 256,
                                            docks.mouse_layer.boat.map.px_height + 256)

        boat = docks.mouse_layer.boat
        self.add(docks.mouse_layer.boat.map)
        self.add(docks.mouse_layer)

        archer = Unit('archer', 150, 1)

        free_units = {}

        self.add(DocksUnits(docks.mouse_layer.boat, free_units=free_units))


class Sail(cocos.layer.Layer):
     is_event_handler = True
     def __init__(self):
         global boat
         super(Sail, self).__init__()

         mixer.stop()

         sound = Sound("src/sounds/music/mischievous_beaters_blue.ogg")
         sound.set_volume(0.1)
         sound.play(-1)

         self.pause_label = cocos.text.Label(text="Pause", anchor_x="center", anchor_y="center",
                                        font_name='Papyrus', font_size=20, color=(0,0,0,255))
         self.size = director.get_window_size()
         self.pause_label.position = (self.size[0] / 21 , 24 * self.size[1] / 25)

         self.font_pause_label = Sprite("src/fonts/white_square.png", anchor=(0, 900))
         self.font_pause_label.scale_x = 0.08
         self.font_pause_label.scale_y = 0.04
         self.font_pause_label.position = self.size[0] / 50, 49 * self.size[1] / 50

         self.add(self.font_pause_label)

         self.add(WaterFlow())

         self.add(self.pause_label)

         docks = Docks_Manager()
         docks.load_ship(0)

         docks.mouse_layer.boat.map.set_view(-256, -256, docks.mouse_layer.boat.map.px_width + 256,
                                             docks.mouse_layer.boat.map.px_height + 256)

         boat = docks.mouse_layer.boat
         self.add(docks.mouse_layer.boat.map)

         self.add(BattleLayer(docks.mouse_layer.boat))

     def mouse_on_sprite(self, x, y):
         if x < self.font_pause_label.x + self.font_pause_label.width and x > self.font_pause_label.x and \
                y < self.font_pause_label.y and y > self.font_pause_label.y - self.font_pause_label.height:
             self.pause_label.color = (255, 0, 0, 255)
             return True
         return False

     def on_mouse_press(self, x, y, button, modifiers):
         if button & mouse.LEFT:
             if self.mouse_on_sprite(x, y):
                 pause_sc = new_pause.get_pause_scene()
                 if new_pause:
                     director.push(pause_sc)

     def on_mouse_motion(self, x, y, dx, dy):
         if self.mouse_on_sprite(x, y):
             self.pause_label.do(ScaleTo(1.1, 0))
         else:
             self.pause_label.do(ScaleTo(1, 0))


class BattleLayer(ActionLayer):

    def __init__(self, boat):

        super().__init__(boat, ghost_delay=100,
                         is_menu=False, difficult='easy')

    def game_over(self):
        super().game_over()
        director.replace(cocos.scene.Scene(Death()))

    def level_complete(self):
        super().level_complete()
        director.replace(cocos.scene.Scene(QuestVillage()))


class TempleScene(Layer):
    is_event_handler = True
    def __init__(self):
        super(TempleScene, self).__init__()
        global me
        self.me = me
        self.add(TempleBg((255,255,255)))
        self.add(WhiteSquare(0.4, 0.1, (360, 140)))
        for i in range(len(self.me.quests)):
            if self.me.quests[i].state == 1:
                self.add(QuestBlock(self.me.quests[i], me, i))
        self.add(TempleLadogaMenu())


class MenuCongratulation(cocos.menu.Menu):
    def __init__(self):
        super(MenuCongratulation, self).__init__("Congratulation!")
        # Параметры заголовка
        self.font_title['font_size'] = 72
        self.font_title['color'] = (200, 20, 20, 255)
        self.font_title['font_name'] = 'Papyrus'

        # Парампетры пунктов меню
        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (255, 255, 255, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'

        items = []
        items.append(cocos.menu.MenuItem("OK", self.back_to_main_menu))

        size = director.get_window_size()
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back(),
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                             [(size[0] / 2, 2 * size[1] / 10)]))

    def back_to_main_menu(self):
        director.replace(cocos.scene.Scene(TempleScene()))

class NewQuestMenu(cocos.menu.Menu):
    def __init__(self):
        super(NewQuestMenu, self).__init__("New quest!")
        # Параметры заголовка
        self.font_title['font_size'] = 72
        self.font_title['color'] = (200, 20, 20, 255)
        self.font_title['font_name'] = 'Papyrus'

        # Парампетры пунктов меню
        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (255, 255, 255, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'

        items = []
        items.append(cocos.menu.MenuItem("OK", self.back_to_main_menu))

        size = director.get_window_size()
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back(),
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                             [(size[0] / 2, 2 * size[1] / 10)]))

    def back_to_main_menu(self):
        director.replace(cocos.scene.Scene(TempleScene()))


class Congratulation(cocos.layer.ColorLayer):
    def __init__(self, quest):
        super(Congratulation, self).__init__(0, 0, 0, 230)
        self.add(TempleBg((100, 100, 100)))
        if sword in quest.bounty:
            print("a")
            self.add(NewQuestMenu())
            self.add(NewQuest(quest))

        else:
            self.add(QuestInfo(quest))
            self.add(MenuCongratulation())


class TempleLadogaMenu(cocos.menu.Menu):
    def __init__(self):
        super(TempleLadogaMenu, self).__init__('Temple')

        global me
        self.me = me
        # Параметры заголовка
        self.font_title['font_size'] = 72
        self.font_title['color'] = (255, 255, 255, 255)
        self.font_title['font_name'] = 'Papyrus'

        # Парампетры пунктов меню
        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (255, 255, 255, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'
        self.font_item['font_size'] = 20
        self.font_item_selected['font_size'] = 23

        items = []
        items.append(
            cocos.menu.MenuItem("Back to city", self.back_to_main_menu))
        items.append(
            cocos.menu.MenuItem("Get reward", self.first_reward))
        items.append(
            cocos.menu.MenuItem("Get reward", self.second_reward))



        size = director.get_window_size()
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back(),
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                            [(size[0]/3.5, 2*size[1]/10),
                             (size[0]/10*9, size[1]/10*5.5),
                             (size[0]/10*9, size[1]/10*1.5)]))

    # Вернуться в главное меню
    def back_to_main_menu(self):
        director.replace(ZoomTransition(cocos.scene.Scene(FirstCity()), 1))

    def first_reward(self):
        if self.me.check(self.me.quests[0]):
            director.replace(ZoomTransition(cocos.scene.Scene(Congratulation(self.me.quests[0])), 1))
    def second_reward(self):
        if self.me.check(self.me.quests[1]):
            director.replace(ZoomTransition(cocos.scene.Scene(Congratulation(self.me.quests[1])), 1))


class QuestInfo(Layer):
    def __init__(self, completed_quest):
        super(QuestInfo, self).__init__()
        size = cocos.director.director.get_window_size()
        self.add(WhiteSquare(0.7, 0.4, (size[0] // 2, size[1] // 2)))
        label = cocos.text.Label(
            text="You done " + completed_quest.head + " and got", font_name="Papyrus",
            font_size=30, align="center", width=640,
            color=(255, 0, 0, 255), multiline=True)
        label.position   = size[0] // 2 - 300, size[1] // 2 + 145
        self.add(label)
        j = 0
        bounty = dict(Counter(completed_quest.bounty))
        for item in bounty:
            item_name = "src/items/" + item.name + ".png"
            self.add(Sprite(item_name, position=(size[0] // 2 - 200 + j*132, size[1] // 2)))
            n = str(bounty[item])
            number = cocos.text.Label(text=n, font_size=30, font_name="Papyrus",
                                      color=(255, 255, 255, 255))
            number.position = size[0] // 2 - 290 + j * 170, size[1] // 2 - 75
            self.add(number)
            j += 1

class NewQuest(Layer):
    def __init__(self, completed_quest):
        super(NewQuest, self).__init__()
        size = cocos.director.director.get_window_size()
        self.add(WhiteSquare(0.7, 0.4, (size[0] // 2, size[1] // 2)))
        label = cocos.text.Label(
            text="You got swords, deliver them and get reward",
            font_name="Papyrus",
            font_size=30, align="center", width=640,
            color=(255, 0, 0, 255), multiline=True)
        label.position = size[0] // 2 - 300, size[1] // 2 + 145
        self.add(label)
        j = 0
        bounty = dict(Counter(completed_quest.bounty))
        for item in bounty:
            item_name = "src/items/" + item.name + ".png"
            self.add(Sprite(item_name, position=(
            size[0] // 2 - 200 + j * 132, size[1] // 2), scale=0.1))
            n = str(bounty[item])
            number = cocos.text.Label(text=n, font_size=30,
                                      font_name="Papyrus",
                                      color=(255, 255, 255, 255))
            number.position = size[0] // 2 - 290 + j * 170, size[1] // 2 - 75
            self.add(number)
            j += 1

class BarracksInfo(cocos.layer.Layer):
    def __init__(self, me):
        super(BarracksInfo, self).__init__()

        size = cocos.director.director.get_window_size()
        costs = cocos.text.Label(text='Costs:', font_name="Papyrus", font_size=30, color=(255, 255, 255, 255), position=(size[0] / 25+ 50, size[1] // 2 - 100))
        cost_archer = cocos.text.Label(text='50', font_name="Papyrus", font_size=30, color=(255, 255, 255, 255), position=(size[0] // 2 - 420+ 150, size[1] // 2 - 100))
        cost_carpenter = cocos.text.Label(text='20', font_name="Papyrus",font_size=30,color=(255, 255, 255, 255), position=(size[0] // 2 - 215+ 150, size[1] // 2 - 100))
        cost_priest = cocos.text.Label(text='35', font_name="Papyrus",
                                       font_size=30,
                                       color=(255, 255, 255, 255), position=(size[0] // 2 - 20+ 150, size[1] // 2 - 100))
        cost_warrior = cocos.text.Label(text='25', font_name="Papyrus",
                                       font_size=30,
                                       color=(255, 255, 255, 255), position=(size[0] // 2 + 180+ 150, size[1] // 2 - 100))
        self.add(costs)
        self.add(cost_archer)
        self.add(cost_carpenter)
        self.add(cost_priest)
        self.add(cost_warrior)
        self.add(cocos.sprite.Sprite("src/items/gold.png", position=(size[0]//2 + 450, size[1]//2-250), scale=0.5))
        self.add(cocos.text.Label(text=str(round(me.gold)), font_name="Papyrus",color=(255, 255, 255, 255), font_size=30
                                  ,position=(size[0]//2 + 480, size[1]//2-265)))

        have = cocos.text.Label(text='You have:', font_name="Papyrus",
                                 font_size=30, color=(255, 255, 255, 255),
                                 position=(size[0] / 30 + 30, size[1] // 2 + 100))
        have_archer = cocos.text.Label(text=str(me.units[archer]), font_name="Papyrus",
                                       font_size=30,
                                       color=(255, 255, 255, 255), position=(
            size[0] // 2 - 420+ 150, size[1] // 2 + 100))
        have_carpenter = cocos.text.Label(text=str(me.units[carpenter]), font_name="Papyrus",
                                          font_size=30,
                                          color=(255, 255, 255, 255),
                                          position=(size[0] // 2 - 215+ 150,
                                                    size[1] // 2 + 100))
        have_priest = cocos.text.Label(text=str(me.units[priest]), font_name="Papyrus",
                                       font_size=30,
                                       color=(255, 255, 255, 255), position=(
            size[0] // 2 - 20+ 150, size[1] // 2 + 100))
        have_warrior = cocos.text.Label(text=str(me.units[warrior]), font_name="Papyrus",
                                        font_size=30,
                                        color=(255, 255, 255, 255), position=(
            size[0] // 2 + 180+ 150, size[1] // 2 + 100))
        self.add(have)
        self.add(have_archer)
        self.add(have_carpenter)
        self.add(have_priest)
        self.add(have_warrior)


class BarracksBuy(cocos.menu.Menu):
    def __init__(self, me, trader):
        super(BarracksBuy, self).__init__("Barracks")
        size = cocos.director.director.get_window_size()

        self.player = me
        self.trader = trader

        # Параметры заголовка
        self.font_title['font_size'] = 72
        self.font_title['color'] = (200, 20, 20, 255)
        self.font_title['font_name'] = 'Papyrus'

        # Парампетры пунктов меню
        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (255, 255, 255, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'

        self.font_item['font_size'] = 36
        self.font_item_selected['font_size'] = 42

        positions = []
        positions.append((size[0] / 3.5, 2 * size[1] / 10))
        positions.append((size[0] // 2 - 400+ 150, size[1] // 2))
        positions.append((size[0] // 2 - 200+ 150, size[1] // 2))
        positions.append((size[0] // 2+ 150, size[1] // 2))
        positions.append((size[0] // 2 + 200+ 150, size[1] // 2))

        items = []

        items.append(cocos.menu.MenuItem("Back to city", self.back_to_main_menu))

        name = "archer"
        unit_image = "src/ally/" + name + "/" + name + ".png"
        items.append(cocos.menu.ImageMenuItem(unit_image, lambda: self.buy_unit(trader.inventory[0])))
        items[1].scale = 12

        name = "carpenter"
        unit_image = "src/ally/" + name + "/" + name + ".png"
        items.append(cocos.menu.ImageMenuItem(unit_image, lambda: self.buy_unit(trader.inventory[1])))
        items[2].scale = 7

        name = "priest"
        unit_image = "src/ally/" + name + "/" + name + ".png"
        items.append(cocos.menu.ImageMenuItem(unit_image, lambda: self.buy_unit(trader.inventory[2])))
        items[3].scale = 9

        name = "warrior"
        unit_image = "src/ally/" + name + "/" + name + ".png"
        items.append(cocos.menu.ImageMenuItem(unit_image, lambda: self.buy_unit(trader.inventory[3])))
        items[4].scale = 9.5



        self.create_menu(items, layout_strategy=cocos.menu.fixedPositionMenuLayout(positions))


        # Вернуться в главное меню

    def back_to_main_menu(self):
        director.replace(ZoomTransition(cocos.scene.Scene(FirstCity()), 1))


    def buy_unit(self, item):
        if self.player.gold >= item.basic_cost * self.trader.greedy:
            self.player.units[item] += 1
            self.player.gold -= item.basic_cost * self.trader.greedy
            director.replace(cocos.scene.Scene(BarracksLadogaLayer()))



class BarracksLadogaLayer(Layer):
    def __init__(self):
        super(BarracksLadogaLayer, self).__init__()
        global me
        global archer
        global priest
        global carpenter
        global warrior
        units = [archer, carpenter, priest, warrior]
        trader = Trader("Ladoga", units, 1)
        self.add(BarracksBg())
        self.add(WhiteSquare(0.55, 0.1, (360, 140)))
        self.add(BarracksInfo(me))
        self.add(BarracksBuy(me, trader))

class FairLadogaInfo(Layer):
    def __init__(self, me, trader, available_items):
        super(FairLadogaInfo, self).__init__()
        size = cocos.director.director.get_window_size()
        self.i_h = dict(Counter(me.inventory))
        self.h_h = dict(Counter(trader.inventory))
        for item in available_items:
            if item not in trader.inventory:
                self.h_h[item] = 0
        for item in available_items:
            if item not in me.inventory:
                self.i_h[item] = 0
        white = (255, 255, 255, 255)
        nme = str(self.h_h[available_items[0]])
        nbr = str(self.h_h[available_items[1]])
        nbe = str(self.h_h[available_items[2]])
        npo = str(self.h_h[available_items[3]])
        nbl = str(self.h_h[available_items[4]])

        # Отрисовка задника для ярмарки
        bg_buildings = cocos.sprite.Sprite("src/fonts/bg_buildings.png", scale=1.1, position=(size[0] / 20 * 9.2, size[1] / 1.95))
        bg_buildings.scale_x = 1.4
        self.add(bg_buildings)

        # показывает количество для покупки
        self.add(cocos.text.Label(text=nme, font_name="Papyrus", font_size=30, color=white, position=(size[0]/20 * 2.5, size[1]/10*3.2)))
        self.add(cocos.text.Label(text=nbr,font_name="Papyrus", font_size=30,color=white, position=(size[0] / 20 * 5.5, size[1] / 10 * 3.2)))
        self.add(cocos.text.Label(text=nbe,font_name="Papyrus", font_size=30,color=white, position=(size[0] / 20 * 8.5, size[1] / 10 * 3.2)))
        self.add(cocos.text.Label(text=npo,font_name="Papyrus", font_size=30,color=white, position=(size[0] / 20 * 11.5, size[1] / 10 * 3.2)))
        self.add(cocos.text.Label(text=nbl, font_name="Papyrus", font_size=30,color=white, position=(size[0] / 20 * 14.5, size[1] / 10 * 3.2)))

        # Показывает цену для покупки
        self.add(cocos.text.Label(text=str(round(available_items[0].basic_cost*trader.greedy)), font_name="Papyrus", font_size=30,
                                  color=white, position=(
            size[0] / 20 * 2.5, size[1] / 10 * 2.8)))
        self.add(cocos.text.Label(text=str(round(available_items[1].basic_cost*trader.greedy)), font_name="Papyrus", font_size=30,
                                  color=white, position=(
            size[0] / 20 * 5.5, size[1] / 10 * 2.8)))
        self.add(cocos.text.Label(text=str(round(available_items[2].basic_cost*trader.greedy)), font_name="Papyrus", font_size=30,
                                  color=white, position=(
            size[0] / 20 * 8.5, size[1] / 10 * 2.8)))
        self.add(cocos.text.Label(text=str(round(available_items[3].basic_cost*trader.greedy)), font_name="Papyrus", font_size=30,
                                  color=white, position=(
            size[0] / 20 * 11.5, size[1] / 10 * 2.8)))
        self.add(cocos.text.Label(text=str(round(available_items[4].basic_cost*trader.greedy)), font_name="Papyrus", font_size=30,
                                  color=white, position=(
            size[0] / 20 * 14.5, size[1] / 10 * 2.8)))

        nme = str(self.i_h[available_items[0]])
        nbr = str(self.i_h[available_items[1]])
        nbe = str(self.i_h[available_items[2]])
        npo = str(self.i_h[available_items[3]])
        nbl = str(me.units[block])

        # показывает количество для продажи
        self.add(cocos.text.Label(text=nme, font_name="Papyrus", font_size=30,
                                  color=white, position=(size[0] / 20*2.5, size[1] / 10 * 6.5)))
        self.add(cocos.text.Label(text=nbr, font_name="Papyrus", font_size=30,
                                  color=white, position=(size[0] / 20 * 5.5, size[1] / 10 * 6.5)))
        self.add(cocos.text.Label(text=nbe, font_name="Papyrus", font_size=30,
                                  color=white, position=(size[0] / 20 * 8.5, size[1] / 10 * 6.5)))
        self.add(cocos.text.Label(text=npo, font_name="Papyrus", font_size=30,
                                  color=white, position=(size[0] / 20 * 11.5, size[1] / 10 * 6.5)))
        self.add(cocos.text.Label(text=nbl, font_name="Papyrus", font_size=30,
                                  color=white, position=(size[0] / 20 * 14.5, size[1] / 10 * 6.5)))

        # Показывает цену для продажи
        self.add(cocos.text.Label(text=str(round(available_items[0].basic_cost/trader.greedy)), font_name="Papyrus", font_size=30,
                                  color=white, position=(size[0] / 20 * 2.5, size[1] / 10 * 6.9)))
        self.add(cocos.text.Label(text=str(round(available_items[1].basic_cost/trader.greedy)), font_name="Papyrus", font_size=30,
                                  color=white, position=(size[0] / 20 * 5.5, size[1] / 10 * 6.9)))
        self.add(cocos.text.Label(text=str(round(available_items[2].basic_cost/trader.greedy)), font_name="Papyrus", font_size=30,
                                  color=white, position=(size[0] / 20 * 8.5, size[1] / 10 * 6.9)))
        self.add(cocos.text.Label(text=str(round(available_items[3].basic_cost/trader.greedy)), font_name="Papyrus", font_size=30,
                                  color=white, position=(size[0] / 20 * 11.5, size[1] / 10 * 6.9)))
        self.add(cocos.text.Label(text=str(round(available_items[4].basic_cost/trader.greedy)), font_name="Papyrus", font_size=30,
                                  color=white, position=(size[0] / 20 * 14.5, size[1] / 10 * 6.9)))

        # ЖЕЛТЫЕ КВАДРАТЫ
        self.add(WhiteSquareAlt(0.12,0.06,(size[0]/20*3, size[1]/10*4), (255,255,0)))
        self.add(WhiteSquareAlt(0.12, 0.06, (size[0] / 20 * 6, size[1] / 10 * 4),
                                (255, 255, 0)))
        self.add(WhiteSquareAlt(0.12,0.06, (size[0] / 20 * 9, size[1] / 10 * 4),
                                (255, 255, 0)))
        self.add(WhiteSquareAlt(0.12,0.06, (size[0] / 20 * 12, size[1] / 10 * 4),
                                (255, 255, 0)))
        self.add(WhiteSquareAlt(0.12,0.06, (size[0] / 20 * 15, size[1] / 10 * 4),
                                (255, 255, 0)))


        self.add(WhiteSquareAlt(0.12,0.06, (size[0] / 20 * 3, size[1] / 10 * 6),
                                (255, 255, 0)))
        self.add(WhiteSquareAlt(0.12,0.06, (size[0] / 20 * 6, size[1] / 10 * 6),
                                (255, 255, 0)))
        self.add(WhiteSquareAlt(0.12,0.06, (size[0] / 20 * 9, size[1] / 10 * 6),
                                (255, 255, 0)))
        self.add(WhiteSquareAlt(0.12,0.06, (size[0] / 20 * 12, size[1] / 10 * 6),
                           (255, 255, 0)))
        self.add(WhiteSquareAlt(0.12,0.06, (size[0] / 20 * 15, size[1] / 10 * 6),
                           (255, 255, 0)))


        self.add(WhiteSquareAlt(0.12, 0.10, (size[0] / 20 * 3, size[1] / 2),
                           (255, 255, 0)))
        self.add(WhiteSquareAlt(0.12, 0.1, (size[0] / 20 * 6, size[1] / 2),
                           (255, 255, 0)))
        self.add(WhiteSquareAlt(0.12, 0.1, (size[0] / 20 * 9, size[1] / 2),
                           (255, 255, 0)))
        self.add(WhiteSquareAlt(0.12, 0.1, (size[0] / 20 * 12, size[1] / 2),
                           (255, 255, 0)))
        self.add(WhiteSquareAlt(0.12, 0.1, (size[0] / 20 * 15, size[1] / 2),
                           (255, 255, 0)))

        self.add(cocos.sprite.Sprite("src/items/meat.png", scale=0.5,
                                     position=(size[0] / 20 * 3, size[1] / 2)))
        self.add(cocos.sprite.Sprite("src/items/bread.png", scale=0.5,
                                     position=(size[0] / 20 * 6, size[1] / 2)))
        self.add(cocos.sprite.Sprite("src/items/beer.png", scale=0.5,
                                     position=(size[0] / 20 * 9, size[1] / 2)))
        self.add(cocos.sprite.Sprite("src/items/porridge.png", scale=0.5,
                                     position=(
                                     size[0] / 20 * 12, size[1] / 2)))
        self.add(cocos.sprite.Sprite("src/blocks/platform.png", scale=2,
                                     position=(
                                     size[0] / 20 * 15, size[1] / 2)))

        bg_buildings_money = cocos.sprite.Sprite("src/fonts/bg_buildings.png", scale=1.1, position=(size[0]/20*15,size[1]/12))
        bg_buildings_money.scale_x = 0.5
        bg_buildings_money.scale_y = 0.5
        self.add(bg_buildings_money)
        #self.add(WhiteSquareAlt(0.3, 0.2, (size[0]/20*15,size[1]/10), (255,255,0)))

        self.add(cocos.text.Label(text="You have:", font_size=23, color=white, font_name="Papyrus", position=(size[0]/20*12.8, size[1]/16)))
        self.add(cocos.text.Label(text=str(round(me.gold)), font_size=25, color=white, font_name="Papyrus", position=(size[0]/20*15, size[1]/16)))
        self.add(cocos.sprite.Sprite("src/items/gold.png", scale=0.2, position=(size[0] / 20 * 16.4, size[1] / 14)))

        self.add(cocos.text.Label(text="Seller has:", font_size=24, color=white, font_name="Papyrus", position=(size[0] / 20 * 12.5, size[1] / 10*1.2)))
        self.add(cocos.text.Label(text=str(round(trader.gold)), font_size=25, font_name="Papyrus", color=white,position=(size[0] / 20 * 15, size[1] / 10*1.2)))
        self.add(cocos.sprite.Sprite("src/items/gold.png", scale=0.2, position=(size[0] / 20 * 16.4, size[1] / 7)))


class FairLadogaBuy(cocos.menu.Menu):
    def __init__(self, me, seller, available_items):
        super(FairLadogaBuy, self).__init__()
        self.seller = seller
        self.me = me
        self.market = Market(me, seller)
        size = cocos.director.director.get_window_size()

        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (255, 255, 255, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'


        items = [cocos.menu.MenuItem("buy", lambda: self.buy(available_items[0])),
                 cocos.menu.MenuItem("buy",lambda: self.buy(available_items[1])),
                 cocos.menu.MenuItem("buy",lambda: self.buy(available_items[2])),
                 cocos.menu.MenuItem("buy",lambda: self.buy(available_items[3])),
                 cocos.menu.MenuItem("buy",lambda: self.buy(available_items[4])),
                 cocos.menu.MenuItem("sell",
                                     lambda: self.sell(available_items[0])),
                 cocos.menu.MenuItem("sell",
                                     lambda: self.sell(available_items[1])),
                 cocos.menu.MenuItem("sell",
                                     lambda: self.sell(available_items[2])),
                 cocos.menu.MenuItem("sell",
                                     lambda: self.sell(available_items[3])),
                 cocos.menu.MenuItem("sell",
                                     lambda: self.sell(available_items[4])),
                 ]

        pos = [(size[0]/20*3, size[1]/10*4),
               (size[0] / 20 * 6, size[1] / 10 * 4),
               (size[0] / 20 * 9, size[1] / 10 * 4),
               (size[0] / 20 * 12, size[1] / 10 * 4),
               (size[0] / 20 * 15, size[1] / 10 * 4),
               (size[0] / 20 * 3, size[1] / 10 * 6),
               (size[0] / 20 * 6, size[1] / 10 * 6),
               (size[0] / 20 * 9, size[1] / 10 * 6),
               (size[0] / 20 * 12, size[1] / 10 * 6),
               (size[0] / 20 * 15, size[1] / 10 * 6),
               ]


        self.create_menu(items, layout_strategy=cocos.menu.fixedPositionMenuLayout(pos))

    def buy(self, item):
        if item == block:
            if (block.basic_cost * self.seller.greedy <= self.me.gold) and (item in self.seller.inventory):
                self.me.units[block] += 1
                self.seller.inventory.remove(item)
                self.me.gold -= block.basic_cost * self.seller.greedy
                self.seller.gold += block.basic_cost * self.seller.greedy
                director.replace(cocos.scene.Scene(FairLadogaLayer()))
            else:
                pass
        elif self.market.buy(item, 1):
            director.replace(cocos.scene.Scene(FairLadogaLayer()))
        else:
            pass

    def sell(self, item):
        if item == block:
            if (block.basic_cost / self.seller.greedy <= self.seller.gold) and (self.me.units[block] > 0):
                self.me.units[block] -= 1
                self.seller.inventory.append(item)
                self.me.gold += block.basic_cost * self.seller.greedy
                self.seller.gold -= block.basic_cost * self.seller.greedy
                director.replace(cocos.scene.Scene(FairLadogaLayer()))
            else:
                pass
        elif self.market.sell(item, 1):
            director.replace(cocos.scene.Scene(FairLadogaLayer()))
        else:
            pass


class FairLadogaLayer(Layer):
    def __init__(self):
        super(FairLadogaLayer, self).__init__()
        global me
        global seller
        global meat, beer, bread, porridge, block
        self.add(FairBg())
        self.add(WhiteSquare(0.55, 0.1, (360, 67)))
        self.add(FairLadogaInfo(me, seller, [meat, beer, bread, porridge, block]))
        self.add(FairLadogaBuy(me, seller,[meat,beer,bread,porridge,block]))
        self.add(FairLadogaMenu())

class FairLadogaMenu(cocos.menu.Menu):
    def __init__(self):
        super(FairLadogaMenu, self).__init__('Fair')

        # Параметры заголовка
        self.font_title['font_size'] = 72
        self.font_title['color'] = (0, 0, 0, 255)
        self.font_title['font_name'] = 'Papyrus'

        # Парампетры пунктов меню
        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (255, 255, 255, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'

        items = []
        items.append(cocos.menu.MenuItem("Back to city", self.back_to_main_menu))

        size = director.get_window_size()
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back(),
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                            [(size[0]/3.5, size[1]/10)]))

    # Вернуться в главное меню
    def back_to_main_menu(self):
        director.replace(ZoomTransition(cocos.scene.Scene(FirstCity()), 1))


class QuestVillage(cocos.layer.Layer):
    def __init__(self):
        super(QuestVillage, self).__init__()
        global quest_v2, me
        if me.check(quest_v2):
            self.add(ScrollSprite())
            self.add(ScrollText(quest_v2))
        else:
            self.add(ScrollSprite())
            size = cocos.director.director.get_window_size()
            head = cocos.text.Label(text="You didn't brought swords!", font_size=30,
                                    align="center", color=(255, 0, 0, 255),width=330,
                                    font_name="Papyrus", multiline=True)
            head.position = (size[0] / 2 - 160, size[1] / 1.369 - 50)
            self.add(head)

        self.add(MenuQuestVillage())


class MenuQuestVillage(cocos.menu.Menu):
    def __init__(self):
        super(MenuQuestVillage, self).__init__()
        # Парампетры пунктов меню
        self.font_item['color'] = (0, 0, 0, 255)
        self.font_item_selected['color'] = (0, 0, 0, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'

        items = []
        items.append(cocos.menu.MenuItem("Ok", self.back_to_main_menu))

        size = director.get_window_size()
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back(),
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                             [(size[0] / 2, 4 * size[1] / 10)]))

        # Вернуться в главное меню

    def back_to_main_menu(self):
        director.replace(ZoomTransition(cocos.scene.Scene(FirstCity()), 1))


class Death(cocos.layer.Layer):
    def __init__(self):
        super(Death, self).__init__()
        self.add(DeathMenu())


class DeathMenu(cocos.menu.Menu):
    def __init__(self):
        super(DeathMenu, self).__init__("Borislav is dead!:....(")
        # Параметры заголовка
        self.font_title['font_size'] = 60
        self.font_title['color'] = (200, 20, 20, 255)
        self.font_title['font_name'] = 'Papyrus'

        # Парампетры пунктов меню
        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (255, 255, 255, 255)
        self.font_item['font_name'] = 'Papyrus'
        self.font_item_selected['font_name'] = 'Papyrus'

        items = []
        items.append(cocos.menu.MenuItem("Ok", self.back_to_main_menu))

        size = director.get_window_size()
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back(),
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                             [(size[0] / 2, 2 * size[1] / 10)]))

        # Вернуться в главное меню

    def back_to_main_menu(self):
        director.replace(ZoomTransition(cocos.scene.Scene(FirstCity()), 1))




me = Hero()
gold = Item("gold", 0, 1)
beer = Item("beer", 0, 25)
meat = Item("meat", 0, 55)
bread = Item("bread", 0, 60)
porridge = Item("prrodge", 5, 35)
block = Item("platform", 0, 10)
sword = Item("sword", 0, 0)

me.inventory = [gold, gold, gold, meat, meat, beer]
quest1 = Quest(0, 1, "Ladoga", "We need MORE gold",
               "One of the close villages need some gold and meet",
               [gold, gold, gold, meat], [beer], 30)
quest2 = Quest(1, 1, "Ladoga", "GIFTS", "Gifts gifts gifts", [],[meat, beer],30)
me.quests.append(quest1)
me.quests.append(quest2)

carpenter = Item("carpenter", 0, 20)
warrior = Item("warrior", 0, 25)
archer = Item("archer", 0, 50)
priest = Item("priest", 0, 35)

quest_v1 = Quest(0, 1, "Novolugovoe", "Novolugovoe", "Nearby village need a lot of swords to deffend from devils",
                 [], [sword for i in range(10)], 0)
quest_v2 = Quest(0, 1, "Novolugovoe", "Novolugovoe", "Thanks a lot", [sword for i in range(10)], [beer, beer, beer, beer, beer, meat, meat], 100)
me.quests.append(quest_v1)



me.units = {carpenter:0, warrior:0, archer:0, priest:0, block:0}

start_inv = [beer, meat, beer, meat, meat, meat, block, block, block, block, block, block, block]
seller = Trader("Ladoga", start_inv, 1.1)


window = cocos.director.director
window.init(width=1280, height=720, caption="ProrvaEnterprise", fullscreen=True)
cocos.director.director.window.pop_handlers()  # Метод который убирает стандартные бинды клавиш(полноэкранный режим,

                                                # показать PFS и другие )

mixer.init()

sound = Sound("src/sounds/morning_field_sounds.ogg")
sound.set_volume(0.1)
sound.play(-1)

director.run(cocos.scene.Scene(FirstScene()))


