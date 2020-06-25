from database_interaction import *
from entities import Block
from cocos.tiles import *
from pyglet.window.key import symbol_string
from cocos import layer
from components import *


shift = 8
blocks_db = BlocksDB()

p = blocks_db.get_table_record(0)
v = blocks_db.get_table_record(1)

platform = Block('platform', 100, 'NULL')
void = Block('void', 0, 'NULL')

class Boat(object):

    # Здесь мы загружаем карту из пути к ней и задаём пустые компоненты для корабля
    def __init__(self, boat_path):

        self.boat_path = boat_path
        boats = load('./xml/' + boat_path + '.xml')
        self.map = boats['boat']
        self.width = round(self.map.px_width / self.map.tw)
        self.height = round(self.map.px_height / self.map.th)
        self.solidity_components = [[[] for i in range(self.width)] for j in range(self.height)]
        self.blocks = [[[] for i in range(self.width)] for j in range(self.height)]

        self.units = [[self.map.get_cell(i, j)['unit'] if self.map.get_cell(i, j)['unit'] != 'NULL' else None\
         for i in range(self.width)] for j in range(self.height)]

        self.id = [[[] for i in range(self.width)] for j in range(self.height)]
        # Инициализируем каждый блок стандартными компонентами
        for i in range(self.width):
            for j in range(self.height):
                try:
                    self.solidity_components[i][j] = HasSolidity(self.map.get_cell(i, j)['solidity'])
                except KeyError:
                    self.solidity_components[i][j] = None

                self.map.set_cell_color(i + shift, j + shift, [255, 255, 255])
                self.id[i][j] = self.map.get_cell(i, j)['id']
                if self.id[i][j] == 'void':
                    self.blocks[j][i] = Block('platform', 0, 'NULL')
                    self.map.set_cell_opacity(j, i, 0)
                else:
                    self.blocks[j][i] = Block('platform', 100, 'NULL')

    def output_info(self):
        for i in range(self.width):
            for j in range(self.height):
                self.output_cell_info(i, j)

    def output_cell_info(self, i, j):

        i, j = i - shift, j - shift
        if not self.in_range(i, j):
            print("Out of range")
            return

        if self.solidity_components[i][j] is None:
            print("I have no solidity")
        else:
            self.solidity_components[i][j].output_info()

        print("My id is: " + self.id[i][j])
        print('----------\n')

    # Нанесение урона и получение ремонта, переправляющее запрос к компоненту
    def get_damage(self, i, j, damage, convert=True):
        if convert:
            i, j = self.map.get_key_at_pixel(i, j)
            i, j = i - shift, j - shift
        if not self.in_range(i, j):
            return
        if self.solidity_components[i][j] is None:
            return
        self.solidity_components[i][j].get_damage(damage)
        if self.solidity_components[i][j].get_solidity() < 0.75 * self.solidity_components[i][j].get_max_solidity():
            self.map.set_cell_opacity(i, j, 220)

        if self.solidity_components[i][j].get_solidity() < 0.5 * self.solidity_components[i][j].get_max_solidity():
            self.map.set_cell_opacity(i, j, 190)

        if self.solidity_components[i][j].get_solidity() < 0.25 * self.solidity_components[i][j].get_max_solidity():
            self.map.set_cell_opacity(i, j, 120)


        if self.solidity_components[i][j].get_solidity() == 0:
            self.destroy(i + shift, j + shift)

    def destroy(self, i, j):
        i, j = i - shift, j - shift
        if not self.in_range(i, j):
            return
        if self.id[i][j] == 'void':
            return

        self.solidity_components[i][j] = None
        self.map.set_cell_opacity(i, j, 0)
        self.id[i][j] = 'void'
        self.blocks[i][j] = Block('void', 0, 'NULL')
        if self.units[i][j] is not None:
            self.units[i][j].death()
            self.units[i][j] = None

    def place(self, i, j):

        i, j = i - shift, j - shift
        if not self.in_range(i, j):
            return
        if self.id[i][j] != 'void':
            return

        self.solidity_components[i][j] = HasSolidity(100)
        self.map.set_cell_opacity(i, j, 255)
        self.id[i][j] = 'platform'
        self.blocks[i][j] = Block('platform', 100, 'NULL')

    def get_repair(self, i, j, repair):
        i, j = self.map.get_key_at_pixel(i, j)

        i, j = i - shift, j - shift

        if not self.in_range(i, j):
            return

        if self.solidity_components[i][j] is not None:
            self.solidity_components[i][j].get_repair(repair)
            self.get_damage(i, j, 0, convert=False)

    def in_range(self, i, j):

        return  self.width > j >= 0 and self.height > i >= 0

    def is_block_busy(self, i, j, convert=True):
        if convert:
            i, j = self.map.get_key_at_pixel(i, j)
            i, j = i - shift, j - shift
        if not self.in_range(i, j) or self.blocks[i][j].id == 'void' or self.units[i][j] != None:
            return None
        return self.units[i][j] is not None

    def is_block_exist(self, i, j, convert=True):
        if convert:
            i, j = self.map.get_key_at_pixel(i, j)
            i, j = i - shift, j - shift
        if not self.in_range(i, j) or self.blocks[i][j].id == 'void':
            return None
        return self.units[i][j] is not None

    def del_unit(self, i, j):
        if self.is_block_busy(i, j):
            return False
        else:
            i, j = self.map.get_key_at_pixel(i, j)
            self.units[i - shift][j - shift] = None
            self.blocks[i - shift][j - shift].unit = None
            return True

    def del_unit_all(self, unit):
        for k in range(self.width):
            for l in range(self.height):
                if self.units[k][l] == unit:
                    self.units[k][l] = None
                    return True
        return False

    def set_unit(self, i, j, unit):
        if self.is_block_busy(i, j):
            return False
        else:
            i, j = self.map.get_key_at_pixel(i, j)
            i, j = i - shift, j - shift
            self.units[i][j] = unit
            self.blocks[i][j].unit = self.units[i][j].name
            return True

    def get_center(self, i, j, convert=True):
        if convert:
            i, j = self.map.get_key_at_pixel(i, j)
            i, j = i - shift, j - shift
        return [32 * shift + key for key in self.map.get_cell(i, j).center]

    def closest_block(self, i, j):

        i, j = self.map.get_key_at_pixel(i, j)

        """
        if not self.in_range(i, j) or self.blocks[i][j] != 'void':
            return None

        if self.blocks[i][j] != 'void':
            return (i, j)
        """

        min = 1500
        temp_i = None
        temp_j = None

        for k in range(self.width):
            for l in range(self.height):
                if self.blocks[k][l].id != 'void' and (i - k - shift) ** 2 + (j - l - shift) ** 2 < min:
                    min = (i - k - shift) ** 2 + (j - l - shift) ** 2
                    temp_i = k
                    temp_j = l

        if temp_i is None:
            return None
        else:
            return tuple([shift * 32 + key for key in self.map.get_cell(temp_i, temp_j).center])

    # x, y - координаты центра блока
    def is_near(self, x, y, i, j, buffer):

        k, l = self.map.get_key_at_pixel(x, y)

        inside_outer_x = self.map.get_cell(k, l).bottomleft[0] - buffer <= i <= self.map.get_cell(k, l).topright[0] + buffer
        inside_outer_y = self.map.get_cell(k, l).bottomleft[1] - buffer <= j <= self.map.get_cell(k, l).topright[1] + buffer

        inside_inner_x = self.map.get_cell(k, l).bottomleft[0] + buffer <= i <= self.map.get_cell(k, l).topright[0] - buffer
        inside_inner_y = self.map.get_cell(k, l).bottomleft[1] + buffer <= j <= self.map.get_cell(k, l).topright[1] - buffer

        check = (inside_outer_x and inside_outer_y) and not (inside_inner_x and inside_inner_y)

        return check


    def get_free_blocks(self):

        free_blocks = list()

        for i in range(self.width):
            for j in range(self.height):
                if self.units[i][j] is None and self.blocks[i][j].id != 'void':
                    free_blocks.append([key + shift * 32 for key in self.map.get_cell(i, j).center])

        return free_blocks

    def get_arranged_units(self):

        arranged_units = dict()

        for i in range(self.width):
            for j in range(self.height):
                temp = self.units[i][j]
                if temp is not None:
                    if temp not in arranged_units.keys():
                        arranged_units[temp] = list()
                    arranged_units[temp].append([key + shift * 32 for key in self.map.get_cell(i, j).center])

        return arranged_units

    def block_to_heal(self, x, y):

        min_hp = 100
        k, l = self.map.get_key_at_pixel(x, y)
        k, l = k - shift, l - shift
        temp_i = None
        temp_j = None

        for i in range(k - 1, k + 2):
            for j in range(l - 1, l + 2):
                if self.is_block_exist(i, j, convert=False) is not None:
                    if self.solidity_components[i][j].get_solidity() < min_hp:
                        min_hp = self.solidity_components[i][j].get_solidity()
                        temp_i, temp_j = i, j

        if temp_i is None:
            return None

        return tuple([shift * 32 + key for key in self.map.get_cell(temp_i, temp_j).center])

    def get_borders(self, buffer=0):

        found_bottom = False
        i = 0

        while (i < self.width and not found_bottom):
            for j in range(self.height):
                if self.is_block_exist(i, j, convert=False):
                    bottom_i = i
                    # bottom_j = j
                    found_bottom = True
            i += 1

        flag = False
        j = 0

        while (j < self.height and not flag):
            for i in range(self.width):
                if self.is_block_exist(i, j, convert=False):
                    # bottom_i = i
                    bottom_j = j
                    flag = True
            j += 1

        found_upper = False
        i = self.width - 1

        while (i >= 0 and not found_upper):
            for j in range(self.height - 1, -1, -1):
                if self.is_block_exist(i, j, convert=False):
                    upper_i = i
                    # upper_j = j
                    found_upper = True
            i -= 1

        flag = False
        j = self.height - 1

        while (j >= 0 and not flag):
            for i in range(self.width - 1, -1, -1):
                if self.is_block_exist(i, j, convert=False):
                    # upper_i = i
                    upper_j = j
                    flag = True
            j -= 1

        if bottom_i is None:
            return None

        return (tuple([shift * 32 - buffer + key for key in self.map.get_cell(bottom_i, bottom_j).center]),
        tuple([shift * 32 + buffer + key for key in self.map.get_cell(upper_i, upper_j).center]))

    def get_boat_center(self):
        return self.get_center(5, 5, convert=False)

    def neighbor_units(self, x, y):

        units = list()

        k, l = self.map.get_key_at_pixel(x, y)
        k, l = k - shift, l - shift


        for i in range(k - 1, k + 2):
            for j in range(l - 1, l + 2):
                if self.is_block_exist(i, j, convert=False) is not None:
                    if self.units[i][j] is not None:
                        units.append(self.units[i][j])

        return units



class MouseLayer(layer.Layer):
    is_event_handler = True

    def __init__(self, boat_xml):
        super(MouseLayer, self).__init__()
        self.pos_x = 100
        self.pos_y = 240
        self.i, self.j = -1, -1
        self.boat = Boat(boat_xml)

    # При нажатии мышью на экран мы выбираем блок корабля, на который нажал пользователь


    def on_mouse_press(self, x, y, button, attributes):


        self.pos_x, self.pos_y = cocos.director.director.get_virtual_coordinates(x, y)
        self.i, self.j = self.boat.map.get_key_at_pixel(self.pos_x, self.pos_y)

    # При нажатии на '1' мы ударяем по блоку с уроном 10, при нажатии на '2' - чиним его на 10

    def on_key_press(self, key, modifiers ):

        key_code = symbol_string(key)

        if key_code == '_1':
            print(1)
            self.boat.destroy(self.i, self.j)

        if key_code == '_2':
            print(2)
            self.boat.place(self.i, self.j)


class Docks_Manager(object):

    def __init__(self):
        self.mouse_layer = None

    def load_ship(self, save_id):

        self.saves = SaveDB()
        data = self.saves.load_save(0)
        self.mouse_layer = MouseLayer(data['boat_xml'])

if __name__ == '__main__':
    window = cocos.director.director
    window.init(width=640, height=480, autoscale=False)

    docks = Docks_Manager()
    docks.load_ship(0)

    docks.mouse_layer.boat.map.set_view(-256, -256,
                                        docks.mouse_layer.boat.map.px_width + 256,
                                        docks.mouse_layer.boat.map.px_height + 256)
    boat_scene = cocos.scene.Scene(docks.mouse_layer.boat.map, docks.mouse_layer)
    window.run(boat_scene)