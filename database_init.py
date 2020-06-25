from database_interaction import *
from entities import *


class DBInit(object):

    def __init__(self):

        self.anime = AnimeDB()
        self.units = UnitsDB()
        self.blocks = BlocksDB()
        self.saves = SaveDB()
        self.flush()

        animations = [[0, 'archer',    'attack', 11, 10, 0.7, 0.25, 0],
                      [1, 'aspid',     'attack', 9, 8, 1, 1, 0],
                      [2, 'aspid',     'move', 8, 0, 1, 1, 0],
                      [3, 'priest',    'attack', 13, 12, 1, 0.3, 0],
                      [4, 'carpenter', 'act', 13, 12, 1, 0.3, 0],
                      [5, 'devil',     'attack', 12, 0, 1, 0.25, 0],
                      [6, 'devil',     'move', 15, 0, 1, 0.25, 1],
                      [7, 'merman',    'attack', 8, 7, 1, 0.25, 0],
                      [8, 'merman',    'move', 12, 0, 1, 0.25, 1],
                      [9, 'merman',    'swim', 7, 0, 1, 0.25, 1],
                      [10, 'warrior',  'attack', 12, 3, 1, 0.3, 0]]

        units = [[0,  'ally',       'archer',    150, 40,  180, 80,  0.3,  10, 'CircleShape'],
                 [1,  'ally',       'warrior',   300, 25,  120, 40,  0.3,  10, 'CircleShape'],
                 [2,  'ally',       'priest',    150, -35, 120, 50,  0.3,  9,  'CircleShape'],
                 [3,  'ally',       'carpenter', 150, 20,  180, 50,  0.3,  9,  'CircleShape'],
                 [4,  'ally',       'trader',    200, 15,  180, 70,  0.3,  9,  'CircleShape'],
                 [5,  'enemy',      'merman',    200, 10,  120, 20,  0.3,  9,  'CircleShape'],
                 [6,  'enemy',      'devil',     80,  35,  270, 15,  0.25, 9,  'CircleShape'],
                 [7,  'enemy',      'aspid',     450, 55,  180, 15,   1,    20, 'CircleShape'],
                 [8,  'projectile', 'arrow',     0.1, 30,  90,  200, 0.7,  7,  'CircleShape'],
                 [9,  'projectile', 'blessing',  0.1, -35, 90,  125, 0.3,  7,  'CircleShape'],
                 [10, 'projectile', 'buff',      0.1, 0,   90,  125, 0.1,  7,  'CircleShape'],
                 [11, 'projectile', 'fireball',  0.1, 55,  90,  175, 0.1,  10, 'CircleShape']]



        blocks = [[0, 'platform', 'platform', 100, 'NULL'],
                  [1, 'void', 'void', 0, 'NULL']]

        platform = Block('platform', 100, 'NULL')
        void = Block('void', 0, 'NULL')

        #raft = [[void, void, void, void if i != 5 else Block('platform', 100, 'trader'),
        #         void, void, void, void, void, void] for i in range(10)]

        raft = [[Block('platform', 100, 'archer') if i % 2 == 0 else platform,
                 Block('platform', 100, 'priest') if i % 3 == 0 else platform,
                 Block('platform', 100, 'warrior') if i % 2 == 0 else platform,
                 Block('platform', 100, 'carpenter') if i % 4 == 0 else platform
                    , platform if i != 5 else Block('platform', 100, 'trader') ,
                 platform, platform, platform, platform, platform] for i in range(10)]


        record = {'id': 0,
                  'boat_xml': 'autosave',
                  'blocks': raft,
                  'units': {},
                  'money': 250,
                  'items': []
                  }

        for animation in animations:
            self.anime.add_record(animation)

        for unit in units:
            self.units.add_record(unit)

        for block in blocks:
            self.blocks.add_record(block)

        self.saves.make_save(record)

    def flush(self):
        self.anime.clear_table()
        self.units.clear_table()
        self.blocks.clear_table()
        self.saves.clear_table()

test = DBInit()

