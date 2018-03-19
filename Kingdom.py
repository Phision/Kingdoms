class Kingdom:
    def __init__(self, name, wealth=0, army=0, defense=100):
        self.name = name
        self.wealth = wealth
        self.army = army
        self.defense = defense

    def info(self):
        print "\nKingdom " + str(self.name) + " information:"
        print "Wealth: " + str(self.wealth)
        print "Army: " + str(self.army)
        print "Defense: " + str(self.defense) + "\n"
