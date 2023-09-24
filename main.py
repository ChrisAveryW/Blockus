
from __future__ import annotations
from enum import Enum
from wrapper import SIZE, shapes, shapesize




class Field(Enum):
    EMTPY = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4

class Player:
    def __init__(self, color: int) -> None:
        self.color = color
        self.shapes: list[Field] = shapes
    
    def place (self, game: Game,  position_x: int, position_y: int, rotation: int, start_x: int, start_y: int, shape: str) -> bool:
        if not shape in self.shapes:
            return False
        self.shapes.remove(shape)
        for index, place in enumerate(shape.replace(" ", "")):
            cur_x %= shapesize
            cur_y //= shapesize
            if shape[cur_x][cur_y] == 1 and game.map[set_x := cur_x + position_x - start_x][set_y := cur_y + position_y - start_y] is Field.EMTPY:
                game.map[set_x][set_y] = Field(self.color)
            else:
                return False



class Game:
    def __init__(self, no_players: int):
        self.map: list[list[Field]] = [[Field(0) for x in range(0,SIZE)] for y in range(0,SIZE)]
        self.players: Player = [Player(1) for x in range(no_players)]
    
    def __repr__(self) -> str:
        ret = ""
        for x in range(SIZE):
            for y in range(SIZE):
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
print(g)
player1 = Player(1)