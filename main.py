from Kingdom import Kingdom
from Action import Action
from initializeGame import initialize
import importlib

class Game:
    def __init__(self, armycost=50, defenseup=3, wealthup=100, nomoves=1, maxmoves=100, botfile=None):
        self.ARMYCOST = armycost
        self.DEFENSEUP = defenseup
        self.WEALTHUP = wealthup
        self.NOMOVES = nomoves
        self.MAXMOVES = maxmoves

        self.initialization = True
        self.victory = False
        self.noTurns = 1
        self.players = []
        self.mode = 0

        if botfile is not None:
            self.mode = 1
            try:
                self.bot = importlib.import_module(botfile)
                self.botmove = getattr(self.bot, "botMove")
                self.botquantity = getattr(self.bot, "botQuantity")
            except:
                print botfile + ".py could not be located or " + botfile + ".py does not contain the 'botMove(player, enemy)' and 'botQuantity(player, enemy)' functions. Switching to mode 2..."
                self.mode = 2
        else:
            self.mode = 2

        while self.victory == False:
            if self.initialization:
                print "\n------- Welcome to Kingdoms! -------\n"
                print "Game settings:"
                print "The cost of an army is (" + str(self.ARMYCOST) + ")."
                print "Walls can be upgraded by (" + str(self.DEFENSEUP) + ") per turn."
                print "Trade will earn you (" + str(self.WEALTHUP) + ") per turn."
                print "Each player has (" + str(self.NOMOVES) + ") moves per turn.\n"

                try:
                    file = open("introduction.txt", "r")
                    intro = file.read()
                    print intro
                except:
                    pass

                player1 = raw_input("Player 1, name your kingdom: ")
                if botfile is None:
                    player2 = raw_input("Player 2, name your kingdom: ")
                elif self.mode == 2:
                    player2 = raw_input("Player 2, name your kingdom: ")
                else:
                    player2 = botfile

                kingdom1 = Kingdom(player1)
                kingdom2 = Kingdom(player2)
                self.players.append(kingdom1)
                self.players.append(kingdom2)
                self.initialization = False

            for player in self.players:
                for player2 in self.players:
                    if player2 == player:
                        pass
                    else:
                        enemy = player2
                self.doTurn(self.turn(player, enemy), player)
                self.noTurns += 1

                if self.victory == False:
                    pass
                else:
                    print str(player.name) + " is VICTORIOUS!"
                    break

    def perform(self, action, kingdom):
        if action.name == "attack":
            attacker = kingdom
            defender = action.info[0]
            attacksize = action.info[1]
            defense = defender.defense
            print "\n" + str(attacker.name) + " attacks " + str(defender.name) + "."
            if attacksize > defense:
                print str(attacker.name) + " has destroyed " + str(defender.name) + ".\n"
                self.victory = True
            else:
                print str(attacker.name) + " failed to destroy " + str(defender.name) + "."
                defender.defense -= attacksize
                attacker.army -= attacksize
                print str(defender.name) + " has (" + str(defender.defense) + ") defense left.\n"

        elif action.name == "defend":
            print "\ndefending " + str(action.info)
            kingdom.defense += action.info
            print "Your defeses have increased (" + str(kingdom.defense) + ").\n"

        elif action.name == "purchase":
            print "\npurchasing " + str(action.info)
            cost = action.info * self.ARMYCOST
            kingdom.army += action.info
            kingdom.wealth -= cost
            print "Your army has grown (" + str(kingdom.army) + ").\n"

        elif action.name == "trade":
            print "\ntrading"
            kingdom.wealth += self.WEALTHUP
            print "Your wealth has increased (" + str(kingdom.wealth) + ").\n"
        else:
            print "\nInvalid action\n"

    def doTurn(self, actionQ, kingdom):
        for action in actionQ:
            self.perform(action, kingdom)

    def actionGeneration(self, player, enemy):
        if self.mode == 1:
            if player.name == self.players[0].name:
                action = int(raw_input(str(player.name) + ", what would you like to do? Attack (1), defend (2), purchase (3), trade (4) or show kingdom information (0)? "))
            else:
                action = self.botmove(player, enemy)
                print player.name + " has selected action " + str(action) + "."

            return action

        elif self.mode == 2:
            action = int(raw_input(str(player.name) + ", what would you like to do? Attack (1), defend (2), purchase (3), trade (4) or show kingdom information (0)? "))

            return action

    def turn(self, player, enemy):
        actionQ = []
        moves = self.NOMOVES
        i = 0
        while (i < moves) and (moves <= self.MAXMOVES):
            try:
                action = self.actionGeneration(player, enemy)

                if action == 1:
                    if player.army == 0:
                        print "\nYou cannot attack because you don't have an army.\n"
                        moves += 1
                    else:
                        actionQ.append(Action("attack", [enemy, player.army]))
                elif action == 2:
                    actionQ.append(Action("defend", self.DEFENSEUP))
                elif action == 3:
                    if player.wealth >= self.ARMYCOST:
                        if self.mode == 1:
                            if player.name == self.players[0].name:
                                quantity = raw_input(str(player.name) + ", how much would you like to purchase? ")
                            else:
                                quantity = self.botquantity(player, enemy)
                        elif self.mode == 2:
                            quantity = raw_input(str(player.name) + ", how much would you like to purchase? ")

                        if quantity == "max":
                            limit = (player.wealth - (player.wealth % self.ARMYCOST)) / self.ARMYCOST
                            if limit == 0:
                                print "\nYou cannot do that.\n"
                                moves += 1
                            else:
                                actionQ.append(Action("purchase", limit))
                        elif int(quantity) > 0:
                            cost = int(quantity) * self.ARMYCOST
                            if player.wealth >= cost:
                                actionQ.append(Action("purchase", int(quantity)))
                            else:
                                print "\nNot enough wealth, my liege."
                                print "You have " + str(player.wealth) + "/" + str(cost) + ".\n"
                                moves += 1
                        else:
                            print "\nYou cannot do that.\n"
                            moves += 1
                    else:
                        print "\nNot enough wealth, my liege."
                        print "You need at least " + str(self.ARMYCOST) + " and you currently have " + str(player.wealth) + ".\n"
                        moves += 1
                elif action == 4:
                    actionQ.append(Action("trade", None))
                elif action == 0:
                    player.info()
                    enemy.info()
                    moves += 1
                else:
                    print "\nInvalid action!\n"
                    moves += 1
            except:
                moves += 1
            i += 1
        if moves > self.MAXMOVES:
            print "Out of moves!\n"
        else:
            return actionQ

mode = int(raw_input("What mode would you like to play? [Versus AI (1)] ### [Versus Human (2)]: "))
if mode == 1:
    bot = raw_input("\nWhat is the name of the file that contains your bot? ")
    try:
        settings = initialize()
        Kingdoms = Game(settings[0], settings[1], settings[2], settings[3], settings[4], bot)
    except:
        print "\nNo settings found. Starting default game...\n"
        Kingdoms = Game()
else:
    try:
        settings = initialize()
        Kingdoms = Game(settings[0], settings[1], settings[2], settings[3], settings[4])
    except:
        print "\nNo settings found. Starting default game...\n"
        Kingdoms = Game()


