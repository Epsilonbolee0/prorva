from database_interaction import *

class Quest(object):

    def __init__(self, id, state, city, head, story, req_items, bounty, gold):
        self.id = id
        self.state = state
        self.city = city
        self.head = head
        self.story = story
        self.req_items = req_items
        self.bounty = bounty
        self.gold = gold


class Item(object):

    def __init__(self, name, mass, basic_cost):

        self.name = name
        self.mass = mass
        self.basic_cost = basic_cost


class Unit(object):

    def __init__(self, name, current_health, level, *buffs):

        self.name = name
        self.current_health = current_health
        self.level = level
        self.buffs = buffs

class Block(object):

    def __init__(self, id, solidity, unit, prop=None):

        self.id = id
        self.solidity = solidity
        self.unit = unit
        self.prop = prop


class Hero(object):

    def __init__(self):

        save = SaveDB()
        record = save.load_save(0)

        self.inventory = record['items']
        self.quests = []
        self.units = record['units']
        self.gold = record['money']

        del save

    def check_quests(self):
        completed_quests = []
        for quest in self.quests:
            if quest.state == 1:
                if self.check(quest):
                    completed_quests.append(quest)
                    quest.state = 2
        return completed_quests

    def check(self, quest):
        req = set(quest.req_items)
        for item in req:
            pl = 0
            re = 0
            for have in self.inventory:
                if have.name == item.name: pl += 1
            for need in quest.req_items:
                if need.name == item.name: re += 1
            if pl < re:
                return 0
        for bounty in quest.bounty:
            if bounty.name == "gold": self.gold += 1
            else: self.add_item(bounty)
        for req in quest.req_items:
            if req.name == "gold": self.gold -= 1
            else: self.take_item(req)
        return 1

    def add_item(self, item):
        self.inventory.append(item)

    def take_item(self, item):
        self.inventory.remove(item)

    def __del__(self):

        save = SaveDB()
        record = save.load_save(0)

        record['units'] = pickle.dumps(self.units, 2)
        record['money'] = self.gold
        record['items'] = pickle.dumps(self.items, 2)

        save.make_save(record)

        del save


class Trader(object):
    def __init__(self, city, start_inv, greedy):

        self.city = city
        self.gold = 0
        self.inventory = start_inv
        self.greedy = greedy

    def refresh_inv(self, start_inv):
        self.inventory = start_inv

    def add_item(self, item):
        self.inventory.append(item)

    def take_item(self, item):
        self.inventory.remove(item)
