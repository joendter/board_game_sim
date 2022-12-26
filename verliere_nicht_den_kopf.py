from random import randint
import random
from copy import deepcopy
from time import time


def rep(x,n):
    out = []
    for i in range(n):
        out.append(x)
    return out


sidelength = 10
playernumber = 4
playerpieces = 4
#pos -1 means start
#neg position means target; -2 first one

class player:
    def __init__(self, pieces, home, ai):
        self.pieces = [-1]*pieces
        self.home = home
        self.piecenumber = pieces
        self.ai = ai

    def won(self):
        return max(self.pieces) < -1

    def three_rolls(self):
        if max(self.pieces) >= 0:
            return False

        #abspieces = [abs(p) for p in self.pieces]
        housepieces = []
        for p in self.pieces:
            if p < -1:
                housepieces.append(p)
        if len(housepieces) == 0:
            return True

        if min(housepieces) == - self.piecenumber - 1 and max(housepieces) == - self.piecenumber + len(housepieces) - 2:
            return True

        return False



class board:
    def __init__(self, sidelength, playernumber, playerpieces, *ais, debug = False):
        self.sidelength = sidelength
        self.playernumber = playernumber
        self.playerpieces = playerpieces
        self.size = sidelength*playernumber
        self.players = []
        self.playertargets = []
        self.winner = -1
        self.debug = debug
        #print(ais)
        for playerID in range(playernumber):
            self.players.append(player(playerpieces,playerID*sidelength, ais[playerID]))

    def play(self):
        while self.winner == -1:
            self.turn()
        return self.winner

    def turn(self):
        for playerID in range(playernumber):
            nturn = 1 + 2*self.players[playerID].three_rolls()
            while nturn > 0:
                nturn = nturn - 1
                if self.playerturn(playerID):
                    nturn = 1

            if self.winner != -1:
                break

    def playerturn(self, playerID):
        dicethrow = randint(1,6)
        move = self.players[playerID].ai(deepcopy(self),dicethrow,playerID)
        self.move(playerID,move,dicethrow)
        if self.players[playerID].won():
            print(f"Player {playerID} won")
            self.winner = playerID
        if self.debug:
            print(f"Player {playerID} moved piece {move} with diceroll {dicethrow}")
            print(f"Current positions of his pieces: {self.players[playerID].pieces}")
        if dicethrow == 6:
            return True
        return False

    def kill(self, playerID, square):
        if square < 0:
            return 0
        for player in range(self.playernumber):
            if player != playerID:
                for i in range(self.players[player].piecenumber):
                    if square == self.players[player].pieces[i]:
                        self.players[player].pieces[i] = -1
        return 1

    def kill_try(self, playerID, square):
        if square < 0:
            return 0
        for player in range(self.playernumber):
            if player != playerID:
                for i in range(self.players[player].piecenumber):
                    if square == self.players[player].pieces[i]:
                        return 1
        return 0

    def move(self, playerID, pieceID, dicethrow):
        player = self.players[playerID]
        comeout = False

        if player.won():
            return 1

        position = player.pieces[pieceID]
        house = position < 0

        if not house:
            new_position = (position + dicethrow) % self.size
        else:
            new_position = position - dicethrow

        if position == -1 and dicethrow != 6:
            return 0

        if position == -1 and dicethrow == 6:
            new_position = player.home
            comeout = True

        if dicethrow == 6 and player.home not in player.pieces and position != -1:
            return 0

        if new_position in player.pieces:
            return 0

        if player.home in player.pieces and position != player.home and not player.home + dicethrow in player.pieces:
            return 0

        if (position + dicethrow >= player.home > position or position + dicethrow >= player.home + self.size > position)\
                and not comeout:
            new_position = player.home - new_position - 2
            house = True

        if house:
            for piece in range(player.piecenumber):
                if piece != pieceID and position > player.pieces[piece] >= new_position:
                    return 0

            if new_position < -player.piecenumber - 1:
                return 0

        self.kill(playerID,new_position)
        self.players[playerID].pieces[pieceID] = new_position
        return 1

    def validmove(self, playerID, pieceID, dicethrow):
        player = self.players[playerID]
        comeout = False

        if player.won():
            return 1

        position = player.pieces[pieceID]
        house = position < 0

        if not house:
            new_position = (position + dicethrow) % self.size
        else:
            new_position = position - dicethrow

        if position == -1 and dicethrow != 6:
            return 0

        if position == -1 and dicethrow == 6:
            new_position = player.home
            comeout = True

        if dicethrow == 6 and player.home not in player.pieces and position != -1:
            return 0

        if new_position in player.pieces:
            return 0

        if player.home in player.pieces and position != player.home and not player.home + dicethrow in player.pieces:
            return 0

        if (position + dicethrow >= player.home > position or position + dicethrow >= player.home + self.size > position)\
                and not comeout:
            new_position = player.home - new_position - 2
            house = True

        if house:
            for piece in range(player.piecenumber):
                if piece != pieceID and position > player.pieces[piece] >= new_position:
                    return 0

            if new_position < -player.piecenumber - 1:
                return 0

        return 1

    def valid(self, dicethrow: int, playerID: int):
        v = []
        for i in range(self.players[playerID].piecenumber):
            if self.validmove(playerID, i, dicethrow):
                v.append(i)
        return v

def aiRandom(board: board, dicethrow: int, playerID: int):
    return randint(0,board.players[playerID].piecenumber-1)

def aiZero(board: board, dicethrow: int, playerID: int):
    return 0

def aiValidMin(board: board, dicethrow: int, playerID: int):
    valid = board.valid(dicethrow,playerID)
    if len(valid) > 0:
        return valid[0]
    return 0


def aiValidRandom(board: board, dicethrow: int, playerID: int):
    valid = board.valid(dicethrow, playerID)
    if len(valid) > 0:
        return valid[randint(0,len(valid)-1)]
    return 0




results = [0]*4

random.seed(42)

a = board(sidelength,playernumber,playerpieces,aiValidMin,aiZero,aiZero,aiZero, debug=True)
a.play()

t0 = time()
for i in range(1280):
    if i % 128 == 0:
        print(i)
        print(results)
        print(time() - t0)
    a = board(sidelength,playernumber,playerpieces,aiValidMin,aiValidMin,aiValidMin,aiValidMin)
    #print(a.players)
    a.play()
    results[a.winner] += 1

print(results)
print(time()-t0)