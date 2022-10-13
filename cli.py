# tetris olu!!

from os import system
from random import choice, randint
from getch import getch
from time import sleep
from math import cos, sin, radians, ceil

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
        this_block["o"] = tuple(map(int, b.pop(0).split(",")))
        this_block_coords = set()
        for y, row in enumerate(b):
            for x, col in enumerate(row):
               if col == "X":
                   this_block_coords.add((y, x))

        block_types[-1]["parts"] = this_block_coords

        block_types.append({"parts":[]})

    return block_types[:-1]


BLOCK_TYPES = create_block_types()

#####################################################

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
        self.center = b["o"]


    def __repr__(self):
        return "I am block: " + str(self.block_type)

    def get_components(self, condition="True", relative=None):
        """Return certain block components according to a condition (if given)"""

        if relative is None:
            y = self.top
            x = self.left
        else:
            y, x = relative


        return [(block[0] + y, block[1] + x) for block in self.block_type if eval(condition, {"block":block, "self":self})]

    def get_top(self):
        """Get top-most component parts"""
        x = self.get_components(condition="block[0] + self.top == self.top")
        return x

    def get_bottom(self):
        """Get bottom-most component parts"""
        return self.get_components(condition="block[0] + self.top == self.top + self.height - 1")

    def rotate(self):
        """Rotate block - tbc"""
        self.height, self.width = self.width, self.height
        new_parts = []
        q, p = self.center

        print("Parts were", self.block_type)
        a = radians(90)
        for part in self.block_type:
            y, x = part

            qx = p + cos(a) * (x - p) - sin(a) * (y - q)
            qy = q + sin(a) * (x - p) + cos(a) * (y - q)
            new_parts.append((ceil(qy), ceil(qx)))

        self.block_type = new_parts
        print("Parts are now", self.block_type)


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
                mine = self.get_components(relative=(y,x))
                #print(f"checking block {c} against my components {mine}")
                for my_comp in mine:
                    if my_comp == c:
                        #print(f"collsion at {my_comp}")
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

        new_bottom = self.top+self.height-1
    
        if d == "d" and self.left + self.width < WIDTH:
            if not self.collision(new_x+self.width-1, new_bottom, landed_blocks):
                self.left = new_x

        elif d == "a" and new_x >= 0:
            if not self.collision(new_x, new_bottom, landed_blocks):
                self.left = new_x

        elif d == "s":
            self.rotate()

        if self.top + self.height < (HEIGHT):
            for b in landed_blocks:
                if self.check_tesselate(b):
                    tesselate = True
                    break
            else:
                self.top += 1
        else:
            touch_bottom = True

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
    print("-" * WIDTH)

###############################################################

def play_game():

    do_getch = input("Enter a key for getch:")
    top_line = HEIGHT - 1

    blocks = []
    game_over = False
    landed = []

    while not game_over:

        current_block = Block()
        newly_landed = None

        while newly_landed is None:
            if do_getch:
                direction = getch()
            else:
                direction = choice([b'a', b'd', b's'])
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








