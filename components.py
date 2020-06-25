# Класс HasSolidity - компонент получения урона тайлом и починки/баффа тайла, а также его разрушения
import cocos

class HasSolidity(object):

    def __init__(self, solidity):

        self.__max_solidity = solidity
        self.__solidity = solidity
        self.undefeated = True

    def get_damage(self, damage):

        if damage < 0:
            damage = 0

        if self.undefeated:

            self.__solidity = 0 if self.__solidity - damage < 0 else self.__solidity - damage
            self.__solidity = round(self.__solidity)

            if self.__solidity <= 0:
                self.undefeated = False
                self.defeat()

    def get_repair(self, repair):

        if repair < 0:
            repair = 0

        if self.undefeated:
            self.__solidity += repair
            self.__solidity = round(self.__solidity)

            if self.__solidity > self.__max_solidity:
                self.__solidity = self.__max_solidity

    def buff_solidity(self, buff):

        self.__max_solidity += buff
        self.__solidity = round(self.__solidity)

        if self.__max_solidity <= 0:
            self.__max_solidity = 1

    def buff_solidity_percent(self, buff):

        self.__max_solidity *= buff
        self.__max_solidity = round(self.__max_solidity)
        if self.__max_solidity <= 0:
            self.__max_solidity = 1

    def output_info(self):

        print("I am " + ("alive" if self.get_solidity() > 0 else "destroyed"))
        print("I have {} hitpoints".format(self.__solidity))
        print("My max hitpoints are {}".format(self.__max_solidity))

    def defeat(self):

        self.undefeated = False

    def get_solidity(self):
        return self.__solidity

    def get_max_solidity(self):
        return self.__max_solidity

# Класс HasMass - компонент уменьшения и увеличения, а также баффа массы тайла


class HasMass(object):

    def __init__(self, mass):

        self.__mass = mass
        self.__basic_mass = mass

    def buff_mass(self, buff):

        self.__mass += buff
        self.__mass = round(self.__mass)
        if self.__mass <= 0:
            self.__mass = 1

    def buff_mass_percent(self, buff):

        self.__mass *= buff
        self.__mass = round(self.__mass)

        if self.__mass <= 0:
            self.__mass = 1

    def output_info(self):
        print("My mass is {}".format(self.__mass))
        print("My basic mass is {}".format(self.__basic_mass))

    def get_mass(self):
        return self.__mass

    def get_basic_mass(self):
        return self.__basic_mass

# Класс HasCost -  компонент покупки и продажи тайла, а также изменения его цены


class HasCost(object):

    def __init__(self, cost):

        self.__cost = cost
        self.__basic_cost = cost

    def buff_cost(self, buff):

        self.__cost += buff
        self.__cost = round(self.__cost)
        if self.__cost < 0:
            self.__cost = 0

    def buff_cost_percent(self, buff):

        self.__cost *= buff
        self.__cost = round(self.__cost)
        if self.__cost < 0:
            self.__cost = 0

    def sell_tile(self):
        return round(self.__cost * 0.9)

    def buy_tile(self, id):
        pass

    def get_cost(self):
        return self.__cost

    def get_basic_cost(self):
        return self.__basic_cost

    def output_info(self):
        print("My cost is {}".format(self.__cost))
        print("My basic cost is {}".format(self.__basic_cost))