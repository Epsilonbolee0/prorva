# Epsilonbolee0
# Колонка с id всегда находится на нулевом столбце базы данных.

import sqlite3 as sql
import pickle


class Sqlite3DB(object):

    def __init__(self):

        self.database = 'sql/all_data.db'
        self.table = None
        self.connection = sql.connect(self.database)
        self.cursor = self.connection.cursor()

    def __del__(self):

        self.cursor.close()
        self.connection.close()

    def create_table(self, asset, table):

        self.table = table
        query = 'CREATE TABLE IF NOT EXISTS ' + self.table + ' (' + asset + ')'
        self.cursor.execute(query)
        self.connection.commit()

    def delete_table(self):

        query = 'DROP TABLE IF EXISTS ' + self.table
        self.cursor.execute(query)
        self.connection.commit()

    def delete_record(self, record_id):

        query = 'DELETE FROM ' + self.table + ' WHERE id = ' + record_id
        self.cursor.execute(query)
        self.connection.commit()

    def update_record_param(self, record_id, param_column, param_value):

        query = 'UPDATE ' + self.table + ' SET ' + str(param_column) + \
                ' = ' + "'" + str(param_value) + "'" + ' WHERE id = ' + str(record_id)

        self.cursor.execute(query)
        self.connection.commit()

    def update_record(self, data):

        record_id = data[0]

        for i in range(1, len(data)):
            self.update_record_param(record_id, self.cursor.description[i][0], data[i])

    def add_record(self, data):

        asset_string = ('?, ' * len(data))[:-2]
        query = 'INSERT INTO ' + self.table + ' VALUES(' + asset_string + ')'

        self.cursor.execute(query, data)
        self.connection.commit()

    def unique_add_record(self, data):

        record_id = data[0]
        query = 'SELECT * FROM ' + self.table + ' WHERE id = ' + str(record_id)
        self.cursor.execute(query)

        previous_row = self.cursor.fetchone()

        if previous_row is not None:
            self.delete_record(str(data[0]))
        self.add_record(data)

    def clear_table(self):

        query = 'DELETE FROM ' + self.table
        self.cursor.execute(query)
        self.connection.commit()

    def get_table_all(self):

        query = 'SELECT * FROM ' + self.table
        self.cursor.execute(query)
        matrix = list([line for line in self.cursor.fetchall()])

        return matrix

    def get_table_record(self, record_id):

        query = 'SELECT * FROM ' + self.table + ' WHERE id = ' + str(record_id)
        self.cursor.execute(query)
        array = self.cursor.fetchone()

        return array

    def get_table_param(self, record_id, param_column):

        query = 'SELECT ' + param_column + ' FROM ' + self.table + ' WHERE id = ' + str(record_id)
        self.cursor.execute(query)
        param = self.cursor.fetchone()

        return param

    def get_table_column(self, param_column):

        query = 'SELECT ' + param_column + ' FROM ' + self.table
        self.cursor.execute(query)
        column = [element for element in self.cursor.fetchall()]

        return column

        # Возвращает словарь {название колонки : значение}
        # для определённой записи}

    def get_dict(self, record_id):

        values = self.get_table_record(record_id)
        keys = [description[0] for description in self.cursor.description]
        record_dict = dict(zip(keys, values))

        return record_dict


# Входной для сохранения кортеж имеет следующий вид

# { id: string,
#   boat_blocks: matrix of blocks
#   boat_xml: string,
#   units: list(tuple) of units,
#   place: string,
#   done_quests: list(tuple) of quests
#   current_quest: quest
#   money: int
#   time: string
# }

# quest

# { id - int,
#   city - string
#   destination - string
#   time_left - int
#   bounty - list(tuple) of items
#   req_items - item
# }

# unit

# { name(id) - string,
#   current_health - float,
#   level - int,
#   (WIP)buffs - list of buffs
# }

# item

# { name(id) - string,
#   mass - int,
#   basic_cost int,
# }

# block

# { name(id) - string,
#   mass - int
#   cost - int
#   solidity - int
# }

# Вся эта информация требует сохранения при переходе между сценами, десу


class SaveDB(Sqlite3DB):

    def __init__(self):

        super().__init__()
        asset = 'id TEXT, boat_xml TEXT, blocks TEXT, units TEXT, money INT, items TEXT'
        self.table = 'saves'
        self.create_table(asset, self.table)

    def make_save(self, data_dict):

        record_id = data_dict['id']
        boat_xml = data_dict['boat_xml']
        blocks = data_dict['blocks']
        units = pickle.dumps(data_dict['units'], 2)
        money = data_dict['money']
        items = pickle.dumps(data_dict['items'], 2)

        db_blocks = BlocksDB()

        tileset_dict = db_blocks.get_tileset_dict()
        generator = XMLGenerator(boat_xml)
        generator.generate_tileset_xml(tileset_dict)
        generator.generate_xml(blocks)
        del db_blocks

        blocks = pickle.dumps(data_dict['blocks'], 2)

        save_data = [record_id, boat_xml, blocks, units, money, items]

        self.unique_add_record(save_data)

    def load_save(self, record_id):

        record = self.get_table_record(record_id)

        if record is None:
            raise FileNotFoundError

        keys = [key[0] for key in self.cursor.description]
        values = []

        pickle_list = [2, 3, 5]

        for i in range(len(record)):
            values.append(record[i] if i not in pickle_list else pickle.loads(record[i]))

        save = dict(zip(keys, values))

        return save


# XMLGenerator генерирует файлы с карты и тайлсета с расширением .xml
# xml_path - путь к файлу с картой для того генератора
# (файл с tileset будет иметь вид xml_path + "_tiles.xml")
# Для генерации тайлсета нужно подать на вход базу данных с блоками

class XMLGenerator(object):

    def __init__(self, xml_path):

        self.xml_path = xml_path

    # path_dict - словарь вида {id: путь к картинке}
    # Для простоты обработки, укороченный id - первые две буквы id

    def generate_tileset_xml(self, path_dict):

        xml_file = open('xml/' + self.xml_path + '_tiles.xml', 'w')

        xml_file.write('<?xml version="1.0"?>\n')
        xml_file.write("<resource>\n")

        for ident in path_dict.keys():
            path = 'src/blocks/' + path_dict[ident] + '.png'
            string = '<image file="{}" id="{}"/>\n'.format(path, ident)
            xml_file.write(string)

        xml_file.write('<tileset>\n')

        for ident in path_dict.keys():
            string = '<tile id="{}"><image ref="{}"/></tile>\n'.format(path_dict[ident], ident)
            xml_file.write(string)

        xml_file.write('</tileset>\n')
        xml_file.write('</resource>\n')

        xml_file.close()

    # Один элемент вида blocks содержит поля
    # id - укороченный идентификатор
    # curr_solidity - нынешняя прочность
    # **prop - какие - либо именованные параметры

    def generate_xml(self, blocks):

        xml_file = open('xml/' + self.xml_path + '.xml', 'w')
        xml_file.write('<?xml version="1.0"?>\n')
        xml_file.write("<resource>\n")

        try:
            file = open('xml/' + self.xml_path + '_tiles.xml', 'r')

        except IOError:
            print("The tileset file doesn't exist!")
            return

        string = "\t<requires file='{}'/>".format(self.xml_path + '_tiles.xml') + '\n'
        xml_file.write(string)
        xml_file.write('\t<rectmap id="boat" origin="100,110,111" tile_size="32x32">\n')

        for j in range(len(blocks[0])):

                xml_file.write('\t<column>\n')
                for i in range(len(blocks)):
                    xml_file.write('\t\t<cell tile="{}">'.format(blocks[i][j].id) + '\n')
                    string = '\t\t<property type="int" name="solidity" value="{}"/>'.\
                        format(blocks[i][j].solidity) + '\n'
                    xml_file.write(string)
                    string = '\t\t<property type="unicode" name="id" value="{}"/>'. \
                                 format(blocks[i][j].id) + '\n'
                    xml_file.write(string)
                    string = '\t\t<property type="unicode" name="unit" value="{}"/>'. \
                                 format(blocks[i][j].unit if blocks[i][j].unit is not None else 'NULL') + '\n'
                    xml_file.write(string)

                    if blocks[i][j].prop is not None:
                        for param, value in blocks[i][j].prop.values():
                            string = '\t\t<property type="int" name="{}" value="{}"/>'.\
                                format(param, value) + '\n'
                            xml_file.write(string)

                    xml_file.write('\t\t</cell>\n')
                xml_file.write('\t</column>\n')

        xml_file.write("\t</rectmap>\n")
        xml_file.write("</resource>\n")

        xml_file.close()


class BlocksDB(Sqlite3DB):

    def __init__(self):

        super().__init__()
        self.table = 'blocks'
        asset = 'id TEXT, name TEXT, img_path TEXT, solidity INT, ' \
                'unit TEXT'
        self.create_table(asset, self.table)

    # Возвращает словарь {идентификатор: путь к картинке}
    # для использования генератором XML

    def get_tileset_dict(self):

        tileset_dict = dict()
        query = 'SELECT id, img_path FROM ' + self.table
        self.cursor.execute(query)

        for ident, img_path in self.cursor.fetchall():
            tileset_dict[ident] = img_path

        return tileset_dict

class AnimeDB(Sqlite3DB):

    def __init__(self):

        super().__init__()
        self.table = 'anime'
        asset = 'id TEXT, name TEXT, action TEXT, frames INT, \
        projectile_frame INT, duration REAL, scale_const REAL, is_loop INT'
        self.create_table(asset, self.table)


class UnitsDB(Sqlite3DB):

    def __init__(self):

        super().__init__()
        self.table = 'units'
        asset = ' id INT, type TEXT, name TEXT, max_health	REAL, attack_damage	REAL, rotation_speed REAL, \
        move_speed REAL, scale_const REAL, hitbox_size REAL, hitbox_type TEXT'

        self.create_table(asset, self.table)
