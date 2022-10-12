## tetris olu!!

from os import system
from random import choice
from getch import getch, pause


WIDTH = 16
HEIGHT = 20


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
        self.right = max(b, key=lambda x: x[1])[1] + 1
        self.bottom = max(b, key=lambda x: x[0])[0] + 1
        self.block_type = b


    def update(self, landed_blocks):
        self.components = [[block[1] + self.left, block[0] + self.top] for block in self.block_type]
        for b in landed_blocks:
            for c in self.components:
                if c[0] == b.top-1 and c[1] == b.left:
                    return True

        return False
        

    def move(self, d, blocks, landed_blocks):
        touch_bottom = False
        
        new_x = self.left + (1 if d == "d" else -1)
        new_y = self.top + 1
    
        if d == "d" and new_x < WIDTH:
            self.left = new_x

        if d == "a" and new_x > 0:
            self.left = new_x

        if new_y < HEIGHT:
            self.top = new_y

        else:               
            touch_bottom = True

        touch_top_line = self.update(landed_blocks)


        return touch_bottom or touch_top_line

            

    


def print_game(blocks):

    
    for y in range(HEIGHT):
        print("|", end="")
        for x in range(WIDTH):
            char = " "
            for b in blocks:
                for c in b.components:
                    if c[0] == x and c[1] == y:
                        char = "X"
            print(char, end="")        

        print("|")



def play_game():

    blocks = []
    game_over = False
    
    while not game_over:

        touch = False       
        current_block = Block()
        blocks = [current_block]
        landed = []

        while not touch:
            
            direction = getch()
            system("cls")
            touch = current_block.move(direction, blocks, landed)
            print_game(blocks)
            
        landed.append(current_block)


if __name__ == "__main__":
    play_game()
