from aocd import lines
from enum import Enum

# definitions
################
class RPS(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def _missing_(self, value):
        if value == 0:
            return self(3)
        if value == 4:
            return self(1)
        return value

class WLD(Enum):
    WIN = 1
    LOSE = 2
    DRAW = 3

dict_a = {"A": RPS.ROCK, "B": RPS.PAPER, "C": RPS.SCISSORS, "X": RPS.ROCK, "Y": RPS.PAPER, "Z": RPS.SCISSORS}
dict_b = {"A": RPS.ROCK, "B": RPS.PAPER, "C": RPS.SCISSORS, "X": WLD.LOSE, "Y": WLD.DRAW, "Z": WLD.WIN}

# part_a
################

def getScoreFromMoves(opponent: RPS, player: RPS):
    if opponent == player:
        return player.value + 3
    if opponent.value + 1 == player.value or (opponent.value == 3 and player.value == 1):
        return player.value + 6
    if player.value + 1 == opponent.value or (player.value == 3 and opponent.value == 1):
        return player.value

def playRPS_part_a(line):
    split = line.split()
    return getScoreFromMoves(dict_a.get(split[0]), dict_a.get(split[1]))

sum = 0
for line in lines:
    sum = sum + playRPS_part_a(line)

print("a:",sum)

# part_b
################

def getMove(opponent: RPS, desiredOutcome: WLD):
    if desiredOutcome == WLD.WIN:
        return RPS(opponent.value+1)
    if desiredOutcome == WLD.LOSE:
        return RPS(opponent.value-1)
    return opponent

def getScoreFromOutcomeAndMove(outcome: WLD, move: RPS):
    if outcome == WLD.WIN:
        return 6 + move.value
    if outcome == WLD.LOSE:
        return 0 + move.value
    return 3 + move.value
    
def playRPS_part_b(line):
    split = line.split()
    desiredOutcome = dict_b.get(split[1])
    move = getMove(dict_b.get(split[0]), desiredOutcome)
    return getScoreFromOutcomeAndMove(desiredOutcome, move)

sum = 0
for line in lines:
    sum = sum + playRPS_part_b(line)
print("b:",sum)