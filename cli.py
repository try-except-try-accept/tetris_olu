# tetris olu!!

from os import system
from random import choice
from getch import getch, pause
import numpy as np

WIDTH = 16
HEIGHT = 20
BLANK_LINE = "|" + (" " * WIDTH) + "|"

def create_block_types():
    blocks = '''X
X
X
X

XX
 X
 XX

XXX
  X
  X

XXX
X
X

 XX
XX

XX
XX

XXX
 X
 X'''.split("\n\n")

    block_types = [[]]
    for b in blocks:
        print(b)
        for y, row in enumerate(b.split("\n")):
            for x, col in enumerate(row):
               if col == "X":
                   block_types[-1].append([x, y])
        block_types.append([])

    return block_types


BLOCK_TYPES = create_block_types()

class Block:

    def __init__(self):

        b = choice(BLOCK_TYPES)
        self.left = WIDTH // 2
        self.top = 0
        self.landed = False

        self.block_type = b
        self.width = max(self.block_type, key=lambda x: x[1])[1] + 1
        self.height = max(self.block_type, key=lambda x: x[0])[0] + 1

        self.update()

    def get_components(self):

        return [[block[1] + self.left, block[0] + self.top] for block in self.block_type]


    def rotate(self):
        self.height, self.width = self.width, self.height


    def check_tesselate(self, block):
        return False

    def update(self, landed_blocks=None):
        if not landed_blocks:
            landed_blocks = []
        
        for b in landed_blocks:
            if self.check_tesselate(b):
                return True


        return False
        

    def move(self, d, blocks, landed_blocks):
        d = d.decode()


        if ord(d) == 27:
            quit()

        touch_bottom = False
        
        new_x = self.left + (1 if d == "d" else -1)
        new_y = self.top + 1
    
        if d == "d" and self.left + self.width < WIDTH:
            self.left = new_x

        if d == "a" and new_x >= 0:
            self.left = new_x

        if new_y + self.height <= HEIGHT:
            self.top = new_y

        else:               
            touch_bottom = True

        touch_top_line = self.update(landed_blocks)
        

        return self if touch_bottom or touch_top_line else None

            

    


def print_game(current_block, landed_blocks):

    print("landed", landed_blocks)
    
    
    empty = ((BLANK_LINE + "\n") * current_block.top)[:-1]
    print(empty)
    
    for y in range(current_block.top, HEIGHT):
        print("|", end="")
        for x in range(WIDTH):
            char = " "
            for b in landed_blocks + [current_block]:
                for c in b.get_components():
                    if c[0] == x and c[1] == y:
                        char = "X"
            print(char, end="")        

        print("|")




def play_game():

    try:

        blocks = []
        game_over = False
        landed = []
        while not game_over:

            current_block = Block()
            blocks = [current_block]

            newly_landed = None

            while newly_landed is None:

                direction = getch()

                system("cls")
                newly_landed = current_block.move(direction, blocks, landed)
                print_game(current_block, landed)
            landed.append(current_block)

    except Exception as e:
        print(e)
        input()

if __name__ == "__main__":
    play_game()
