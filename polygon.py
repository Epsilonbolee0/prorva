# Импорт библиотекimport cocos
from cocos.director import director
from cocos.layer import Layer
import cocos.collision_model as cm
import cocos.euclid as eu
from cocos import scene
from math import *
import random
import pyglet

# Импорт файлов
from units import *
from docks_logic import *
# from river_layer import *


class WaveGenerator(object):
    n_deviation = 0.2
    enemies = [Devil.name, Merman.name, Aspid.name]
    easy_waves = \
[{'duration': 1, 'pause': 30, Devil.name: 2, Merman.name: 5, Aspid.name: 0},
 {'duration': 4, 'pause': 3, Devil.name: 5, Merman.name: 5, Aspid.name: 0}]

    medium_waves = \
[{'duration': 20, 'pause': 3, Devil.name: 3, Merman.name: 7,  Aspid.name: 0},
 {'duration': 20, 'pause': 3, Devil.name: 3, Merman.name: 7, Aspid.name: 0},
 {'duration': 20, 'pause': 3, Devil.name: 3, Merman.name: 7, Aspid.name: 0},
 {'duration': 20, 'pause': 3, Devil.name: 3, Merman.name: 7, Aspid.name: 0}]

    hard_waves = \
[{'duration': 20, 'pause': 3, Devil.name: 3, Merman.name: 7, Aspid.name: 0},
 {'duration': 20, 'pause': 3, Devil.name: 3, Merman.name: 7, Aspid.name: 0},
 {'duration': 20, 'pause': 3, Devil.name: 3, Merman.name: 7, Aspid.name: 0},
 {'duration': 20, 'pause': 3, Devil.name: 3, Merman.name: 7, Aspid.name: 0},
 {'duration': 20, 'pause': 3, Devil.name: 3, Merman.name: 7, Aspid.name: 0},
 {'duration': 20, 'pause': 3, Devil.name: 3, Merman.name: 7, Aspid.name: 0}]

    def __init__(self, difficult='medium', start_duration=1):
        self.difficult = difficult

        self.temp_wave = -1
        self.is_done = False
        self.switch_time = start_duration
        self.time = 0
        self.spawn_time = {Devil.name: [],
                           Merman.name: [],
                           Aspid.name: []}

        if difficult == 'easy':
            self.waves = self.easy_waves
        elif difficult == 'hard':
            self.waves = self.hard_waves
        else:
            self.waves = self.medium_waves

    def update(self, dt):
        self.time += dt

        if self.time >= self.switch_time:
            self.temp_wave += 1
            self.time -= self.switch_time
            if self.temp_wave >= len(self.waves):
                self.is_done = True
            else:
                dur = self.waves[self.temp_wave]['duration']
                self.switch_time = dur + self.waves[self.temp_wave]['pause']

                for name in self.enemies:
                    n = self.waves[self.temp_wave][name]
                    self.spawn_time[name] = self.rand_time(dur, n)
        spawn_dict = {}
        for name in self.enemies:
            spawn_dict[name] = 0
            while (len(self.spawn_time[name]) > 0 and
                   self.spawn_time[name][0] < self.time):
                self.spawn_time[name].pop(0)
                spawn_dict[name] += 1
        return spawn_dict

    def rand_time(self, time, n):
        time_list = [0] * random.randint(round(n * (1 - self.n_deviation)),
                                         round(n * (1 + self.n_deviation)))
        for i in range(len(time_list)):
            time_list[i] = random.betavariate(2, 3) * time
        time_list.sort()
        return time_list


class ActionLayer(Layer):
    is_event_handler = True
    menu_hide_opacity = 100
    merman_space = 1/4

    def __init__(self, boat, free_units={},
                 ghost_delay=0, is_menu=False, difficult='medium'):
        super().__init__()
        # Словарь всех юнитов
        self.units = {}
        self.fill_units_empty()
        self.free_units = free_units
        self.difficult = difficult
        self.is_finish = False
        self.is_menu = is_menu

        # Объект "следа"
        self.ghost = Ghost(self, ghost_delay)
        self.add(self.ghost)

        self.boat = boat

        self.col_status = cm.CollisionManagerBruteForce()
        self.to_clean_list = []

        temp_dict = self.boat.get_arranged_units()
        #temp_dict = {Bowman.name: [(176, 304), (16, 240)],
        #                Trader.name: [(176, 112)]}
        self.set_unit_from_save(temp_dict)

        self.schedule(self.update)
        if not is_menu:
            self.wave_generator = WaveGenerator(difficult=self.difficult)
            self.schedule(self.spawn_wave)
            self.schedule_interval(self.clear_out_of_screen, 3)

    def set_unit_from_save(self, temp_dict):
        for name in temp_dict.keys():
            for pos in temp_dict[name]:

                if self.boat.is_block_exist(*pos) is None:
                    continue

                temp_class = self.unit_class(name)
                temp = temp_class(self, position=pos)
                if not self.is_menu:
                    temp.set_attack()
                self.spawn_unit(temp)
                self.boat.set_unit(*pos, temp)
                self.ghost.disappear()

    # Действия на уровне при нажатии мыши
    def on_mouse_press(self, x, y, button, trash):
        if button == 1 and not(self.ghost.in_process):
            # Если юнит не выбран
            if self.ghost.target is None:
                self.pick_new_ghost(x, y)
            # Если юнит выбран
            else:
                self.put_ghost(x, y)

    def pick_new_ghost(self, x, y):
        # Поиск среди объектов этой точки подвижных юнитов
        for temp in self.col_status.objs_touching_point(x, y):
            if temp.copyable:
                if self.pick_from_menu(temp):
                    self.ghost.copy(temp)
                    return True
            elif self.ghost.is_movable(temp):
                self.ghost.copy(temp)
                return True
        return False

    def put_ghost(self, x, y):
        # Проверка на наличие в этой точке объекта меню,
        # совпадающим с выбранным юнитом
        for temp in self.col_status.objs_touching_point(x, y):
            if temp.copyable and self.ghost.target.name == temp.name:
                self.put_to_menu(temp)
                if not self.ghost.target.copyable:
                    self.boat.del_unit(*self.ghost.target.position)
                    self.ghost.target.death()
                self.ghost.disappear()
                return True

        if self.boat.is_block_busy(x, y) is None:
            return False

        # Перенос выбранного из меню юнита
        if self.ghost.target.copyable:
            x, y = self.boat.get_center(x, y)
            temp_class = self.unit_class(self.ghost.target.name)
            temp = temp_class(self, position=(x, y))
            if not self.is_menu:
                temp.set_attack()
            self.spawn_unit(temp)
            self.boat.set_unit(x, y, temp)
            self.ghost.disappear()

        # Передвижение с задержкой выбранного юнита
        else:
            x, y = self.boat.get_center(x, y)
            self.ghost.position = (x, y)
            flash_n = self.ghost.flash_n
            time = self.ghost.delay / self.ghost.target.move_speed
            dt = time / flash_n
            self.ghost.in_process = True
            self.waiting(time, dt, 135 / flash_n)

    def waiting(self, time, dt, dop):
        if self.ghost.target is not None:
            if time - dt > 0:
                self.do(Delay(dt) + CallFunc(
                    lambda: self.ghost.increase_opacity(dop)) +
                        CallFunc(lambda: self.waiting(time - dt, dt, dop)))
            else:
                self.delay_move(*self.ghost.position)

    def pick_from_menu(self, obj):
        if obj.name in self.free_units.keys() and self.free_units[obj.name] > 0:
            self.free_units[obj.name] -= 1
            if self.free_units[obj.name] == 0:
                obj.set_yellow_color()
                obj.opacity = self.menu_hide_opacity
            return True
        else:
            return False

    def put_to_menu(self, obj):
        if obj.name not in self.free_units.keys():
            self.free_units[obj.name] = 0
        self.free_units[obj.name] += 1
        if self.free_units[obj.name] == 1:
            obj.set_default_color()
            obj.opacity = 255

    def delay_move(self, x, y):
        if self.ghost.target is not None:
            self.boat.del_unit(*self.ghost.target.position)
            self.ghost.target.position = (x, y)
            self.ghost.target.move_hitbox(x, y)
            self.boat.set_unit(x, y, self.ghost.target)
        self.ghost.in_process = False
        self.ghost.disappear()

    # Действия на уровне при передвижении мыши
    def on_mouse_motion(self, x, y, dx, dy):
        if self.ghost.target is not None and not self.ghost.in_process:
            self.ghost.position = (x, y)

    def on_key_press(self, key, modifiers):
        key_code = symbol_string(key)
        if key_code == 'Q':
            if self.ghost.target is not None and self.ghost.target.copyable:
                self.put_to_menu(self.ghost.target)
            self.ghost.disappear()

    # Определение класса юнита по его имени
    def unit_class(self, name):
        for obj in Unit.subunits_list(Unit):
            if name == obj.name:
                return obj

    def fill_units_empty(self):
        for obj in Unit.subunits_list(Unit):
            self.units[obj.name] = []

    # Спавн пули
    def spawn_bullet(self, source, target):
        temp = Arrow(self, position=(source.x, source.y))
        temp.set_attack(target)
        self.spawn_unit(temp)

    def spawn_fireballs(self, pos, n=4):
        rand_angle = (2*pi / n) * random.random()
        for i in range(4):
            temp = Fireball(self, position=pos)
            temp.set_attack(rand_angle + (2*pi / n) * i)
            self.spawn_unit(temp)

    # Спавн юнита - добавление в словарь и на уровень
    def spawn_unit(self, new_unit):
        if new_unit.name not in self.units.keys():
            self.units[new_unit.name] = []
        self.units[new_unit.name].append(new_unit)
        self.add(self.units[new_unit.name][-1])
        self.col_status.add(new_unit)

    # Убийство юнита - удаление из словоря и уровня
    def kill_unit(self, obj):
        self.units[obj.name].remove(obj)
        self.to_clean_list.append(obj)
        self.boat.del_unit_all(obj)
        self.remove(obj)

        if obj.picked:
            self.ghost.disappear()

        if obj.name == Trader.name:
            self.game_over()

    # Обновление уровня
    def update(self, dt):
        # self.check_collisions()
        self.col_update()
        if self.is_finish:
            count = 0
            for name in [Devil.name, Merman.name, Aspid.name]:
                count += len(self.units[name])
            if count == 0:
                self.level_complete()

    def spawn_wave(self, dt):
        to_spawn = self.wave_generator.update(dt)

        if to_spawn[Devil.name]:
            free_blocks = self.boat.get_free_blocks()
            if len(free_blocks):
                for i in range(to_spawn[Devil.name]):
                    temp = Devil(self, position=random.choice(free_blocks))
                    temp.set_attack()
                    self.spawn_unit(temp)

        if to_spawn[Merman.name]:
            for i in range(to_spawn[Merman.name]):
                temp_y = \
self.anchor_y * (self.merman_space + 2*random.randint(0, 1)*(1 - self.merman_space))
                while True:
                    pos = (random.randint(0, self.anchor_x * 2),
                           temp_y)
                    if self.boat.is_block_exist(*pos) is None:
                        break
                temp = Merman(self, position=pos)
                temp.set_attack()
                self.spawn_unit(temp)

        if to_spawn[Aspid.name]:
            temp = Aspid(self, position=(self.anchor_x*2 + 30,
                                         random.randint(0, self.anchor_y * 2)))
            temp.set_attack()
            self.spawn_unit(temp)

        if self.wave_generator.is_done:
            self.is_finish = True
            self.unschedule(self.spawn_wave)

    # Удаление вылетевших за экран юнитов (стрел)
    def clear_out_of_screen(self, dt):
        if Arrow.name in self.units.keys():
            for obj in self.units[Arrow.name]:
                if not obj.is_in_window():
                    obj.death()

        for obj in self.units[Fireball.name]:
            if not obj.is_in_window():
                obj.death()

    # Полное обновление менеджера столкновений
    def col_update(self):
        for obj in self.to_clean_list:
            self.col_status.remove_tricky(obj)
        self.to_clean_list = []

    # Проверка столкновений и исполнение действий, связанных с ними
    def check_collisions(self):
        # Просмотр каждого активного столкновения
        for i, j in self.col_status.iter_all_collisions():
            # Проверка действительности столкновения
            if (i.name in j.col_list or j.name in i.col_list) and i.active and j.active:
                # Нанесение урона
                i.take_damage(j.attack_damage)
                j.take_damage(i.attack_damage)

    # Проверка вылета объекта за экран (с заданным буфером)
    def is_in_window(self, obj, buffer=20):
        return (-buffer < obj.x < self.anchor_x * 2 + buffer and
                -buffer < obj.y < self.anchor_y * 2 + buffer)

    def clear_all_units(self):
        for name in self.units.keys():
            for obj in self.units[name]:
                obj.death()

    # Завершение игры (поражение)
    def game_over(self):
        self.unschedule(self.update)
        self.clear_all_units()

    # Успешное прохождение уровня
    def level_complete(self):
        self.unschedule(self.update)
        self.clear_all_units()


# Отладочный уровень
class TestLayer(ActionLayer):
    def __init__(self, boat):
        # free_units - словарь свободных юнитов, подаётся извне
        temp_free_units = {Bowman.name: 10,
                           Warrior.name: 10,
                           Priest.name: 3,
                           Carpenter.name: 3}
        super().__init__(boat, ghost_delay=100, free_units=temp_free_units,
                         is_menu=False, difficult='medium')
        self.set_menu()

    # Установление меню
    def set_menu(self):
        obj_list = [Bowman, Warrior, Priest, Carpenter]
        for i in range(len(obj_list)):
            temp = obj_list[i](self, position=(30 + 60 * i, 430),
                               copyable=True, scale_by=1.5)
            if temp.name not in self.free_units.keys() or self.free_units[temp.name] == 0:
                temp.set_yellow_color()
                temp.opacity = self.menu_hide_opacity

            self.spawn_unit(temp)

    def game_over(self):
        super().game_over()
        print('Game over, Borislav if dead')

    def level_complete(self):
        super().level_complete()
        print('Level done')


# Юниты в меню доков
class DocksUnits(ActionLayer):
    def __init__(self, boat, free_units={}):
        super().__init__(boat, ghost_delay=0.2, free_units=free_units,
                         is_menu=True)
        self.set_menu()

    # Установление меню
    def set_menu(self):
        size = director.get_window_size()
        obj_list = [Bowman, Warrior, Priest, Carpenter]
        positions = [(size[0] / 20 * 17.4, 18.5 * size[1] / 20 - 150),
                     (size[0] / 20 * 15.3, 18.5 * size[1] / 20 - 150),
                     (size[0] / 20 * 17.4, 16.3 * size[1] / 20 - 150),
                     (size[0] / 20 * 15.4, 16.3 * size[1] / 20 - 150)]

        for i in range(len(obj_list)):
            temp = obj_list[i](self, positions[i],
                               copyable=True, scale_by=1.5)
            free_units_names = []
            for unit in self.free_units:
                free_units_names.append(unit.name)

            if temp.name not in free_units_names or self.free_units[temp] == 0:
                temp.set_yellow_color()
                temp.opacity = self.menu_hide_opacity
            else:
                temp.set_green_color()
                temp.opacity = self.menu_hide_opacity

            self.spawn_unit(temp)


def generator_test(flag):
    if flag:
        gena = WaveGenerator('easy')
        while not (gena.is_done):
            temp = gena.update(1)
            print(temp)
            print(gena.time, gena.spawn_time)
            print('\n_-_-_-_-_-_-_-_-_-_-_-_-\n')


# Запуск окна приложения (только для запуска этого файла)
if __name__ == '__main__':
    generator_test(False)
    # Окно приложения
    window = director
    # Инициализация окна
    window.init()
    window.show_FPS = True

    docks = Docks_Manager()
    docks.load_ship(0)
    docks.mouse_layer.boat.map.set_view(-256, -256,
                                        docks.mouse_layer.boat.map.px_width + 256 ,
                                        docks.mouse_layer.boat.map.px_height + 256)

    # Создание уровня объектов
    action_layer = TestLayer(docks.mouse_layer.boat)
    # Создание сцены
    # WaterFlow(), Coast()
    main_scene = scene.Scene(docks.mouse_layer.boat.map, docks.mouse_layer, action_layer)
    # Запуск приложения
    window.run(main_scene)

