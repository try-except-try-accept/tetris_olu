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
print(BLOCK_TYPES)

class Block:

    def __init__(self, test_block_data=None):
        if test_block_data:
            b = test_block_data
        else:
            b = BLOCK_TYPES[5] # choice(BLOCK_TYPES)
        self.left = WIDTH // 2
        self.top = 0
        self.landed = False

        self.id = randint(111, 999)

        self.block_type = b["parts"]
        self.width = b["w"]
        self.height = b["h"]


        print(self)
        print(f"w {self.width} h {self.height}")





    def __repr__(self):
        return "I am block: " + str(self.block_type)

    def get_components(self, condition="True"):

        return [(block[0] + self.top, block[1] + self.left) for block in self.block_type if eval(condition)]


    def get_top(self):
        #print("My top is", self.top)
        #print("My components are", self.get_components())

        x = self.get_components("block[0] + self.top == self.top")
        print("my top blocks are", x)
        return x


    def get_bottom(self):
        #print("My bottom is", self.top + self.height)
        #print("My components are", self.get_components())
        return self.get_components("block[0] + self.top == self.top + self.height - 1")


    def rotate(self):
        self.height, self.width = self.width, self.height


    def check_tesselate(self, block):



        ## if my bottom is one less than the other blocks top...

        #print("My bottom blocks are", self.get_bottom())
        #print("Their top blocks are", block.get_top())

        for my_comp in self.get_bottom():
            #print("Checking", my_comp, "against", block.get_components(), end=" ")
            for their_comp in block.get_components():
                #print("against", their_comp, end=" ")

                if my_comp[1] == their_comp[1]:  # horizontally aligned
                    if my_comp[0] == their_comp[0] - 1:  # vertically tesselating
                        return True


        return False

    def update(self, top_line, landed_blocks=None):
        if not landed_blocks:
            landed_blocks = []

        if self.top + 3 < top_line:
            return False
        
        for b in landed_blocks:             # improve in future.. BSP?
            if self.check_tesselate(b):
                return True


        return False

    def collision(self, x, y, blocks):

        for b in blocks:
            print("going to check new pos", y, x, "against", b.get_components())
            for c in b.get_components():
                if (y, x) == c:
                    print(f"COLLISION, because new x is {y, x} and this hits {c}")

                    return True
        return False


    def move(self, d, blocks, landed_blocks, top_line):
        d = d.decode()

        print(f"Block {self.id} is moving!")


        if ord(d) == 27:
            quit()

        touch_bottom = False
        
        new_x = self.left + (1 if d == "d" else -1)
        if self.top+self.height < (HEIGHT):
            self.top += 1
        else:
            touch_bottom = True
    
        if d == "d" and self.left + self.width < WIDTH:
            print("allowed to move right - did not hit edge")
            if not self.collision(new_x+self.width-1, self.top+self.height-1, landed_blocks):
                self.left = new_x

        elif d == "a" and new_x >= 0:
            if not self.collision(new_x, self.top+self.height-1, landed_blocks):
                self.left = new_x






        touch_top_line = self.update(top_line, landed_blocks)
        
        if touch_bottom:
            print("Stop because touch bottom")
        elif touch_top_line:
            print("stop because tesselate")

        print("End of move pos is ", self.get_components())

        return self if touch_bottom or touch_top_line else None

            

    


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




def play_game():

    do_getch = input("Enter a key for getch:")

    top_line = HEIGHT - 1


    blocks = []
    game_over = False
    landed = []
    while not game_over:

        current_block = Block()
        blocks = [current_block]

        newly_landed = None

        while newly_landed is None:
            if do_getch:
                direction = getch()
            else:
                direction = choice([b'a', b'd'])
                sleep(0.01)

            system("cls")
            newly_landed = current_block.move(direction, blocks, landed, top_line)

            if newly_landed:
                new_top = list(newly_landed.get_top())[0][0]
                if new_top < top_line:
                    top_line = new_top

            print_game(top_line, current_block, landed)
        landed.append(current_block)
        input()


if __name__ == "__main__":


    #block2 = Block({"parts":[[2,2], [1,2], [0,2], [1,1], [1,0]], "w":2, "h":3})

    #block1 = Block({"parts":[[0,1], [0,0]], "w":2, "h":1})


    #print(block1.check_tesselate(block2))




    play_game()







