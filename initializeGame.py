def initialize():
    file = open("settings.txt", "r")
    settings = file.read().split("\n")
    gameParameters = []
    for setting in settings:
        gameParameter = setting.split(" ")
        gameParameters.append(int(gameParameter[1]))
    return gameParameters
