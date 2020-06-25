# Импорт библиотек
import cocos
from cocos.sprite import Sprite
import cocos.collision_model as cm
import cocos.euclid as eu
from math import *
import pyglet

# Импорт файлов
from database_interaction import UnitsDB, AnimeDB
from behaviors import *

from cocos.audio.pygame.mixer import Sound
from cocos.audio.pygame import mixer

# Объекты для работы с БД
units_db = UnitsDB()
anime_db = AnimeDB()


# Класс следа мыши
class Ghost(Sprite):
    flash_n = 10

    def __init__(self, father, delay=0):
        # При инициализации создаётся невидимый спрайт
        super().__init__('src/blocks/grid.png')
        self.father = father
        self.visible = False
        self.in_process = False
        self.delay = delay
        self.target = None
        self.possible_move = [Bowman.name, Warrior.name, Priest.name,
                              Trader.name, Carpenter.name]

    def copy(self, target):
        self.target = target
        self.target.set_picked()
        super().__init__(self.target.default_img, target.position)
        self.opacity = 120
        self.scale = target.scale_const

    def disappear(self):
        self.in_process = False
        self.visible = False
        self.target = None

    def increase_opacity(self, n):
        if self.target is not None:
            if self.father.boat.is_block_exist(*self.position) is None:
                self.in_process = False
                self.disappear()
            else:
                self.opacity += n

    def is_movable(self, target):
        return target.name in self.possible_move


# Класс анимации
class Anime(object):
    def __init__(self, sprite, id):
        self.sprite = sprite
        self.time = 0
        # Считывание инфорации из БД в словарь
        data_dict = anime_db.get_dict(id)

        # Задание параметров юнита
        self.id = data_dict['id']
        self.name = data_dict['name']
        self.action = data_dict['action']
        self.frames = data_dict['frames']
        self.projectile_frame = data_dict['projectile_frame']
        self.duration = data_dict['duration']
        self.scale_const = data_dict['scale_const']
        self.is_loop = data_dict['is_loop']

        img_list = [0] * self.frames
        if self.frames == 1:
            img_list[0] = pyglet.image.load('src/{:}/{:}/{:}.jpg'. \
                                            format(sprite.type, sprite.name, self.name))
        else:
            temp_link = 'src/{:}/{:}/{:}/'.format(sprite.type, sprite.name,
                                                  self.action)
            for i in range(self.frames):
                img_list[i] = pyglet.image.load(
                    '{:}{:0>4d}.png'.format(temp_link, i))

        self.animation = pyglet.image.Animation.from_image_sequence(
            img_list, self.duration / self.frames, loop=self.is_loop)

    def stop(self):
        if not self.time:       return False
        self.sprite.image = pyglet.image.Animation.from_image_sequence(
            [pyglet.image.load(self.sprite.default_img)], 0)
        self.sprite.scale = self.sprite.scale_const
        self.time = 0

    def start(self):
        self.sprite.image = self.animation
        self.sprite.scale = self.scale_const
        self.time = self.duration

    def update(self, dt):
        self.time -= dt
        if self.time < 0:
            self.stop()

    def do_action(self):
        if self.time == 0:
            self.start()
        elif self.is_action():
            return True
        return False

    def is_action(self):
        return (self.duration - self.time >
                self.duration * (self.projectile_frame / self.frames))


# Классы юнитов
# Класс сущности
class Unit(Sprite):
    damage_time = 0.1
    heal_time = 0.1

    def __init_subclass__(cls):
        # Считывание инфорации из БД в словарь
        data_dict = units_db.get_dict(cls.id)

        # Задание параметров юнита
        cls.type = data_dict['type']
        cls.name = data_dict['name']
        cls.max_health = data_dict['max_health']
        cls.attack_damage = data_dict['attack_damage']
        cls.rotation_speed = data_dict['rotation_speed']
        cls.move_speed = data_dict['move_speed']
        cls.scale_const = data_dict['scale_const']
        cls.hitbox_size = data_dict['hitbox_size']
        cls.hitbox_type = data_dict['hitbox_type']

        cls.default_img = 'src/{:}/{:}/{:}.png'.format(cls.type, cls.name,
                                                       cls.name)

    # Задание параметров сущности при создании
    def __init__(self, father, position=(0, 0), action=None, copyable=False,
                 scale_by=1):
        super().__init__(self.default_img, position)
        self.father = father

        self.scale = self.scale_const
        self.health = self.max_health

        self.aim_list = []
        self.col_list = []

        self.alive = True
        self.active = False
        self.picked = False
        self.copyable = copyable
        self.action = action
        self.state = 'disabled'

        self.scale *= scale_by
        self.hitbox_size *= scale_by

        self.set_hitbox()

    def subunits_list(self):
        return self.__subclasses__()

    # Определение угла поворота
    def define_angle(self, obj):
        if type(obj) is tuple or type(obj) is list:
            dx = obj[0] - self.x
            dy = obj[1] - self.y
            dist = self.define_distance(obj)
            if not dist:
                return self.rotation
        else:
            dx = obj.x - self.x
            dy = obj.y - self.y
            dist = self.define_distance(obj)
            if not dist:
                return self.rotation

        ang = degrees(acos(dx / dist))
        if dy < 0:
            ang = 360 - ang
        return (-ang + 90) % 360

    # Расстояние до объекта
    def define_distance(self, obj):
        if type(obj) is tuple or type(obj) is list:
            return sqrt((self.x - obj[0]) ** 2 + (self.y - obj[1]) ** 2)

        else:
            return sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)

    def is_attack_target(self, obj):
        return obj.name in self.aim_list and obj.active

    def is_in_window(self):
        return self.father.is_in_window(self)

    # Смэрть
    def death(self):
        if not self.alive:
            return False
        self.alive = False
        self.active = False
        self.action = None
        self.health = 0
        self.father.kill_unit(self)

    # Ша! по лицу
    def take_damage(self, damage):
        if not self.alive: return False
        self.do(CallFunc(self.set_red_color) + Delay(self.damage_time) +
                CallFunc(self.set_default_color))
        self.health -= damage
        
        if self.health <= 0:
            self.death()

    def take_heal(self, heal):
        if not self.alive or self.health == self.max_health: return False
        self.do(CallFunc(self.set_green_color) + Delay(self.heal_time) +
                CallFunc(self.set_default_color))
        self.health = min(self.max_health, self.health + heal)

    # Передвижение хитбокса
    def move_hitbox(self, x, y):
        self.cshape.center = eu.Vector2(x, y)

    # Переключение состояний
    # Задание хитбокса
    def set_hitbox(self):
        if self.hitbox_type == 'CircleShape':
            self.cshape = cm.CircleShape(eu.Vector2(self.x, self.y),
                                         self.hitbox_size)

        elif self.hitbox_type == 'RectShape':
            pass

    # Атака
    def set_attack(self):
        self.state = 'attack'
        self.reset_to_disabled()
        self.active = True

    # Выбран мышкой
    def set_picked(self):
        self.picked = True

    # Бездействие
    def set_disabled(self):
        self.state = 'disabled'
        self.reset_to_disabled()

    def reset_to_disabled(self):
        self.active = False
        self.action = None
        self.picked = False

    def set_red_color(self):
        self.color = (248, 165, 194)

    def set_yellow_color(self):
        self.color = (255, 221, 89)

    def set_green_color(self):
        self.color = (123, 237, 159)

    def set_default_color(self):
        self.color = (255, 255, 255)


# Класс лучника
class Bowman(Unit):
    id = 0

    def __init__(self, father, position, copyable=False, scale_by=1):
        super().__init__(father, position, copyable=copyable, scale_by=scale_by)
        self.col_list = []
        self.aim_list = [Devil.name, Merman.name, Aspid.name]

        self.trigger_range = 300
        self.reload_time = 1

    def set_attack(self):
        super().set_attack()
        self.attack_animation = Anime(self, 0)
        self.action = self.do(BowmanAttack(range=self.trigger_range,
                                           reload=self.reload_time))
        self.action.init2(self.father.spawn_bullet, self.father.col_status,
                          self.attack_animation)


# Класс воина
class Warrior(Unit):
    id = 1

    def __init__(self, father, position, copyable=False, scale_by=1):
        super().__init__(father, position, copyable=copyable, scale_by=scale_by)
        self.col_list = []
        self.aim_list = [Devil.name, Merman.name]

        self.trigger_range = 100
        self.attack_range = 20 + self.hitbox_size
        self.reload_time = 1.5

    def set_attack(self):
        super().set_attack()
        self.attack_animation = Anime(self, 10)
        self.action = self.do(WarriorAttack(trigger_range=self.trigger_range,
                                            attack_range=self.attack_range,
                                            reload=self.reload_time))
        self.action.init2(self.father.col_status, self.attack_animation)


# Класс батюшки
class Priest(Unit):
    id = 2

    def __init__(self, father, position, copyable=False, scale_by=1):
        super().__init__(father, position, copyable=copyable, scale_by=scale_by)
        self.col_list = []
        self.aim_list = [Bowman.name, Warrior.name, Carpenter.name, Trader.name]

        self.heal_range = 100
        self.reload_time = 5

    def set_attack(self):
        super().set_attack()
        self.heal_animation = Anime(self, 3)
        self.action = self.do(PriestHealing(heal_range=self.heal_range,
                                            reload=self.reload_time))
        self.action.init2(self.father.col_status, self.heal_animation)


# Класс плотника
class Carpenter(Unit):
    id = 3

    def __init__(self, father, position, copyable=False, scale_by=1):
        super().__init__(father, position, copyable=copyable, scale_by=scale_by)

        self.reload_time = 5

    def set_attack(self):
        super().set_attack()
        self.animation = Anime(self, 4)
        self.action = self.do(CarpenterFix(reload=self.reload_time))
        self.action.init2(self.father.boat, self.animation)


# Класс купца (гг)
class Trader(Unit):
    id = 4

    def __init__(self, father, position, copyable=False, scale_by=1):
        super().__init__(father, position, copyable=copyable, scale_by=scale_by)


# Класс водяного
class Merman(Unit):
    id = 5

    def __init__(self, father, position, copyable=False, scale_by=1):
        super().__init__(father, position, copyable=copyable, scale_by=scale_by)
        self.attack_range = 10 + self.hitbox_size
        self.reload_time = 0.8

    def set_attack(self):
        super().set_attack()
        self.attack_animation = Anime(self, 7)
        self.move_animation = Anime(self, 9)
        self.action = self.do(MermanAttack(attack_range=self.attack_range,
                                           reload=self.reload_time))
        self.action.init2(self.father.boat, self.attack_animation,
                          self.move_animation)


# Класс чёрта
class Devil(Unit):
    id = 6

    def __init__(self, father, position, copyable=False, scale_by=1):
        super().__init__(father, position, copyable=copyable, scale_by=scale_by)
        self.col_list = [Arrow.name]
        self.aim_list = [Bowman.name, Warrior.name, Priest.name,
                         Carpenter.name, Trader.name]

        self.trigger_range = 500
        self.attack_range = 10 + self.hitbox_size
        self.reload_time = 0.8

    def set_attack(self):
        super().set_attack()
        self.attack_animation = Anime(self, 5)
        self.move_animation = Anime(self, 6)
        self.action = self.do(DevilAttack(trigger_range=self.trigger_range,
                                          attack_range=self.attack_range,
                                          reload=self.reload_time))
        self.action.init2(self.father.col_status, self.attack_animation,
                          self.move_animation)


# Класс аспида
class Aspid(Unit):
    id = 7

    def __init__(self, father, position, copyable=False, scale_by=1):
        super().__init__(father, position, copyable=copyable, scale_by=scale_by)
        self.attack_range = 300
        self.reload_time = 10

    def set_attack(self):
        super().set_attack()
        self.attack_animation = Anime(self, 1)
        self.move_animation = Anime(self, 2)
        self.action = self.do(AspidAttack(self.attack_range,self.reload_time))
        self.action.init2(self.father.boat, self.attack_animation,
                          self.move_animation, self.father.spawn_fireballs)


# Класс стрелы
class Arrow(Unit):
    id = 8

    def __init__(self, father, position, copyable=False):
        super().__init__(father, position, copyable=copyable)
        self.col_list = [Devil.name, Merman.name, Aspid.name]
        self.aim_list = [Devil.name, Merman.name, Aspid.name]

    def set_attack(self, target):
        super().set_attack()
        self.action = self.do(ArrowMove())
        self.action.init2(self.father.col_status, target)


class Fireball(Unit):
    id = 11

    def __init__(self, father, position, copyable=False):
        super().__init__(father, position, copyable=copyable)
        self.aim_list = [Bowman.name, Warrior.name, Priest.name,
                         Carpenter.name, Trader.name]

    def set_attack(self, angle=0):
        super().set_attack()
        self.action = self.do(FireballMove(angle))
        self.action.init2(self.father.boat)
