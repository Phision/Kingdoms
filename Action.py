"""
--------------------------------------------------------------------------------------------------------------------------
Action name |   Action description                              |   Action form
--------------------------------------------------------------------------------------------------------------------------
attack      |   Kingdom A attacks the kingdom B with their army |   Action("attack", [kingdomB, kingdomA.army])
defend      |   Upgrade your walls to increase your defences    |   Action("defend", DEFENSEUP)
purchase    |   Purchase solders to increase your army size     |   Action("purchase", quantity)
trade       |   Trade goods to increase your wealth             |   Action("trade", None)
--------------------------------------------------------------------------------------------------------------------------
"""


class Action:
    def __init__(self, name, information):
        self.name = name
        self.info = information
