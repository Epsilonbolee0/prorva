class Market(object):
    def __init__(self, player, trader):
        self.player = player
        self.trader = trader
        self.mult = trader.greedy

    '''
        def show(self):
            for item in self.player.inventory:
                print(item)
            for item in self.trader.inventory:
                print(item)
            print(self.player.gold)
            print(self.trader.gold)
    '''

    def buy(self, item, amount):
        if item in self.trader.inventory:
            if self.player.gold >= item.basic_cost * self.mult * amount:
                for i in range(amount):
                    self.player.add_item(item)
                self.player.gold -= item.basic_cost * self.mult * amount
                for i in range(amount):
                    self.trader.take_item(item)
                self.trader.gold += item.basic_cost * self.mult * amount
                return 1
        return 0

    def sell(self, item, amount):
        if item in self.player.inventory:
            if self.trader.gold >= round(item.basic_cost / self.mult) * amount:
                for i in range(amount):
                    self.trader.add_item(item)
                self.trader.gold -= round(item.basic_cost / self.mult) * amount
                for i in range(amount):
                    self.player.take_item(item)
                self.player.gold += round(item.basic_cost / self.mult) * amount
                return 1
        return 0