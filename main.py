
from __future__ import annotations
from enum import Enum
from wrapper import fieldsize, shapes, shapesize
import pygame


class Field(Enum):
    EMTPY = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    NEW = 5


class Player:
    def __init__(self, color: int) -> None:
        self.color = color
        self.shapes: list[Field] = shapes
    
    @staticmethod
    def rotate(shape: str):
        # rotation from 0 to 3, so incrementing the integer by one results in 90° rotation
        old_shape: list[chr] = [list(x) for x in shape.split(" ")]
        updated_shape: list[chr] = [list(x) for x in shape.split(" ")]

        counter = shapesize - 1
        for index_1, bitarr in enumerate(old_shape):
            for index_2, bit in enumerate(bitarr):
                #print(index_1, index_2, "-- ", index_2, counter)
                updated_shape[index_2][counter] = bit
            counter -= 1
        return " ".join(["".join(x) for x in updated_shape])

    def legal(self, pos_x: int, pos_y: int, game: Game) -> bool: # this function can not be static in its current implementation, because of the color
        # is at least one notch connected to the other place
        if pos_x - 1 >= 0:
            if game.map[pos_x - 1][pos_y] == Field(self.color):
                return False
        if pos_x + 1 <= fieldsize - 1:
            if game.map[pos_x + 1][pos_y] == Field(self.color):
                return False
        if pos_y - 1 >= 0:
            if game.map[pos_x][pos_y - 1] == Field(self.color):
                return False
        if pos_y + 1 <= 0: 
            if game.map[pos_x][pos_y + 1] == Field(self.color):
                return False
        return True
    
    def clean_new(self, action: bool, game: Game):
        for x in range(fieldsize):
            for y in range(fieldsize):
                if game.map[x][y] == Field.NEW:
                    game.map[x][y] = Field(self.color) if action else Field(0)

    def place (self, game: Game,  position_x: int, position_y: int, rotation: int, start_x: int, start_y: int, shape: str) -> bool:
        if not shape in self.shapes:
            return False
        initial_shape = shape
        for x in range(rotation):
            shape = Player.rotate(shape)
        for index, place in enumerate(shape.replace(" ", "")):
            cur_x = int(index % shapesize)
            cur_y = int(index // shapesize)
            if int(place) == 1:
                if game.map[set_x := cur_x + position_x - start_x][set_y := cur_y + position_y - start_y] is Field.EMTPY:
                    game.map[set_x][set_y] = Field(5) # create a new field, so if something goes wrong it can be deleted easily later
                    if not self.legal(set_x, set_y, game):
                        self.clean_new(False, game)
                        return False
                else:
                    return False
        # set shape to true on the game field
        self.clean_new(True, game)         
        # every shape is only usable once
        self.shapes.remove(initial_shape)

    


class Game:
    def __init__(self, no_players: int):
        self.map: list[list[Field]] = [[Field(0) for x in range(0,fieldsize)] for y in range(0,fieldsize)]
        self.players: Player = [Player(1) for x in range(no_players)]
    
    def __repr__(self) -> str:
        ret = ""
        for x in range(fieldsize):
            for y in range(fieldsize):
                if self.map[x][y].value == 0:
                    ret += "- "
                elif self.map[x][y].value == 1:
                    ret += "r "
                elif self.map[x][y].value == 2:
                    ret += "b "
                elif self.map[x][y].value == 3:
                    ret += "g "
                elif self.map[x][y].value == 4:
                    ret += "y "
                else:
                    ret += "§"
            ret += "\n"
        return ret


g = Game(2)
player1 = Player(1)
while True:
    inp1 = int(input("shape:"))
    inp2 = int(input("x:"))
    inp3 = int(input("y:"))
    inp4 = int(input("rot:"))
    inp5 = int(input("finx:"))
    inp6 = int(input("finy:"))
    print(player1.place(g, inp2, inp3, inp4, inp5, inp6, shapes[int(inp1)]))
    print(g)