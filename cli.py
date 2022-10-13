# tetris olu!!

from os import system
from random import choice, randint
from getch import getch, pause
import numpy as np
from time import sleep

WIDTH = 16
HEIGHT = 20
BLANK_LINE = "|" + (" " * WIDTH) + "|"

def create_block_types():
    """Load tetris block varieties from file"""

    with open("blocks.txt") as f:
        blocks = f.read().split("\n\n")

    block_types = [{"parts":[]}]

    for b in blocks:
        b = b.splitlines()
        this_block = block_types[-1]
        this_block["w"] = int(b.pop(0))
        this_block["h"] = int(b.pop(0))
        this_block_coords = set()
        for y, row in enumerate(b):
            for x, col in enumerate(row):
               if col == "X":
                   this_block_coords.add((y, x))

        block_types[-1]["parts"] = this_block_coords

        block_types.append({"parts":[]})

    return block_types[:-1]


BLOCK_TYPES = create_block_types()


class Block:
    """Object representation of a tetris block"""

    def __init__(self, test_block_data=None):
        if test_block_data:
            b = test_block_data
            self.left = 0
        else:
            b = choice(BLOCK_TYPES)
            self.left = WIDTH // 2
        self.top = 0
        self.landed = False
        self.id = randint(111, 999)
        self.block_type = b["parts"]
        self.width = b["w"]
        self.height = b["h"]

    def __repr__(self):
        return "I am block: " + str(self.block_type)

    def get_components(self, condition="True"):
        """Return certain block components according to a condition (if given)"""
        return [(block[0] + self.top, block[1] + self.left) for block in self.block_type if eval(condition)]

    def get_top(self):
        """Get top-most component parts"""
        x = self.get_components("block[0] + self.top == self.top")
        return x

    def get_bottom(self):
        """Get bottom-most component parts"""
        return self.get_components("block[0] + self.top == self.top + self.height - 1")

    def rotate(self):
        """Rotate block - tbc"""
        self.height, self.width = self.width, self.height

    def check_tesselate(self, block):
        """Check for tesselation with another block"""
        for my_comp in self.get_components():
            for their_comp in block.get_components():

                if my_comp[1] == their_comp[1]:  # horizontally aligned
                    if my_comp[0] + 1 == their_comp[0]:  # vertically tesselating
                        return True
        return False

    def collision(self, x, y, blocks):
        """Check if left/right movement would cause a collision"""

        for b in blocks:
            for c in b.get_components():
                if (y, x) == c:
                    return True
        return False

    def move(self, d, landed_blocks, top_line):
        """Move block according to direction d, return None if can still move after, or itself if not."""
        d = d.decode()

        if ord(d) == 27:
            quit()

        touch_bottom = False
        tesselate = False
        
        new_x = self.left + (1 if d == "d" else -1)
        if self.top+self.height < (HEIGHT):
            for b in landed_blocks:
                if self.check_tesselate(b):
                    tesselate = True
                    break
            else:
                self.top += 1
        else:
            touch_bottom = True

        new_bottom = self.top+self.height-1
    
        if d == "d" and self.left + self.width < WIDTH:
            if not self.collision(new_x+self.width-1, new_bottom, landed_blocks):
                self.left = new_x

        elif d == "a" and new_x >= 0:
            if not self.collision(new_x, new_bottom, landed_blocks):
                self.left = new_x

        return self if touch_bottom or tesselate else None

###############################################################

def print_game(top_line, current_block, landed_blocks):

    buffer = min(top_line, current_block.top)
    
    empty = ((BLANK_LINE + "\n") * current_block.top)[:-1]
    print(empty)
    
    for y in range(buffer, HEIGHT):
        print("|", end="")
        for x in range(WIDTH):
            char = " "
            for b in landed_blocks + [current_block]:
                for c in b.get_components():
                    if c[1] == x and c[0] == y:
                        char = "X"
            print(char, end="")        

        print("|")

###############################################################

def play_game():

    do_getch = input("Enter a key for getch:")
    top_line = HEIGHT - 1

    blocks = []
    game_over = False
    landed = [Block({'parts': [(18, 0), (18, 1), (18, 2), (18, 3), (18, 4), (18, 5), (18, 6), (18, 7), (18, 8), (18, 9), (18, 11), (18, 12), (18, 13), (18, 14), (18, 15), (19, 0), (19, 1), (19, 2), (19, 3), (19, 4), (19, 5), (19, 6), (19, 7), (19, 8), (19, 9), (19, 10), (19, 11), (19, 12), (19, 13), (19, 14), (19, 15)], 'w': 16, 'h': 2})]

    while not game_over:

        current_block = Block()
        newly_landed = None

        while newly_landed is None:
            if do_getch:
                direction = getch()
            else:
                direction = choice([b'a', b'd'])
                sleep(0.01)

            system("cls")
            newly_landed = current_block.move(direction, landed, top_line)

            if newly_landed:
                new_top = list(newly_landed.get_top())[0][0]
                if new_top < top_line:
                    top_line = new_top

            print_game(top_line, current_block, landed)
        landed.append(current_block)



if __name__ == "__main__":


    #block2 = Block({"parts":[[2,2], [1,2], [0,2], [1,1], [1,0]], "w":2, "h":3})

    #block1 = Block({"parts":[[0,1], [0,0]], "w":2, "h":1})


    #print(block1.check_tesselate(block2))




    play_game()








