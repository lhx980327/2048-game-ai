class TransparentGroup(pyglet.graphics.Group):
    def set_state(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def unset_state(self):
        glDisable(GL_BLEND)


SQ_SIZE = 58
SPACING = 10

BG_COLORS = {
    1: ('c3B', (238, 228, 219, 238, 228, 219, 238, 228, 219, 238, 228, 219)),
    2: ('c3B', (237, 224, 201, 237, 224, 201, 237, 224, 201, 237, 224, 201)),
    3: ('c3B', (241, 177, 125, 241, 177, 125, 241, 177, 125, 241, 177, 125)),
    4: ('c3B', (243, 149, 104, 243, 149, 104, 243, 149, 104, 243, 149, 104)),
    5: ('c3B', (243, 127, 100, 243, 127, 100, 243, 127, 100, 243, 127, 100)),
    6: ('c3B', (244, 96, 67, 244, 96, 67, 244, 96, 67, 244, 96, 67)),
    7: ('c3B', (236, 206, 120, 236, 206, 120, 236, 206, 120, 236, 206, 120)),
    8: ('c3B', (237, 204, 97, 237, 204, 97, 237, 204, 97, 237, 204, 97)),
    9: ('c3B', (237, 200, 80, 237, 200, 80, 237, 200, 80, 237, 200, 80)),
    10: ('c3B', (237, 197, 63, 237, 197, 63, 237, 197, 63, 237, 197, 63)),
    11: ('c3B', (237, 194, 46, 237, 194, 46, 237, 194, 46, 237, 194, 46)),
    12: ('c3B', (119, 110, 101, 119, 110, 101, 119, 110, 101, 119, 110, 101)),
    13: ('c3B', (119, 110, 101, 119, 110, 101, 119, 110, 101, 119, 110, 101)),
    14: ('c3B', (119, 110, 101, 119, 110, 101, 119, 110, 101, 119, 110, 101)),
}
TEXT_COLORS = {
    1: (119, 110, 101, 255),
    2: (255, 255, 255, 255),
}
LOST_SCREEN_COLOR = ('c4B', (238, 228, 219, 128,
                             238, 228, 219, 128,
                             238, 228, 219, 128,
                             238, 228, 219, 128))

WINDOW = pyglet.window.Window(280, 280)
BACKGROUND = pyglet.graphics.OrderedGroup(0)
FOREGROUND = pyglet.graphics.OrderedGroup(1)

BG = pyglet.image.load('assets/bg.png')
BG_SPRITE = pyglet.sprite.Sprite(BG)

FULL_SCREEN_VECTOR = ('v2f', (0, 0,
                              0, WINDOW.height,
                              WINDOW.width, 0,
                              WINDOW.width, WINDOW.height))

LOST_SCREEN = pyglet.graphics.Batch()
LOST_SCREEN.add_indexed(4, GL_TRIANGLE_STRIP,
                        TransparentGroup(), [0, 1, 2, 3],
                        FULL_SCREEN_VECTOR,
                        LOST_SCREEN_COLOR)
LOST_TEXT = pyglet.text.Label('Final Score: 0',
                              font_name='Arial',
                              font_size=18,
                              x=WINDOW.width//2, y=WINDOW.height//2,
                              anchor_x='center', anchor_y='center',
                              batch=LOST_SCREEN, group=FOREGROUND)


class Tile:
    def __init__(self, val, x, y):
        self.val = val
        self.x = x
        self.y = y
        self.merged_flag = False

    def move(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.val)+' at '+str(self.x)+', '+str(self.y)


class GraphicTile(Tile):
    def __init__(self, val, x, y):
        super().__init__(val, x, y)
        self.gx = lambda: self.x * (SQ_SIZE+SPACING) + SPACING
        self.gy = lambda: WINDOW.height - (self.y+1) * (SQ_SIZE+SPACING)  # 0, 0 is bottom-left
        self.batch = pyglet.graphics.Batch()
        self.v_list = self.batch.add_indexed(4, GL_TRIANGLE_STRIP,
                                             BACKGROUND, [0, 1, 2, 3],
                                             ('v2f', (self.gx(), self.gy(),
                                                      self.gx(), self.gy()+SQ_SIZE,
                                                      self.gx()+SQ_SIZE, self.gy(),
                                                      self.gx()+SQ_SIZE, self.gy()+SQ_SIZE)),
                                             BG_COLORS[1])
        self.label = pyglet.text.Label(str(2**val),
                                       font_name='Arial',
                                       bold=True,
                                       font_size=32,
                                       color=TEXT_COLORS[1],
                                       x=self.gx()+SQ_SIZE//2, y=self.gy()+SQ_SIZE//2,
                                       anchor_x='center', anchor_y='center',
                                       batch=self.batch, group=FOREGROUND)
        if self.val in BG_COLORS:
            self.v_list.colors = BG_COLORS[self.val][1]

    def move(self, x, y):
        super().move(x, y)
        self.v_list.vertices = [self.gx(), self.gy(),
                                self.gx(), self.gy()+SQ_SIZE,
                                self.gx()+SQ_SIZE, self.gy(),
                                self.gx()+SQ_SIZE, self.gy()+SQ_SIZE]
        self.label.x = self.gx()+SQ_SIZE//2
        self.label.y = self.gy()+SQ_SIZE//2
        self.label.text = str(2**self.val)

        if self.val in BG_COLORS:
            self.v_list.colors = BG_COLORS[self.val][1]

        if self.val > 9:
            self.label.font_size = 16
        elif self.val > 6:
            self.label.font_size = 24
        elif self.val > 2:
            self.label.color = TEXT_COLORS[2]


class Board:
    def __init__(self, graphic=False):
        self.graphic = graphic
        self.board = [[None for i in range(4)] for j in range(4)]
        self.score = 0
        self.lost = False

        self.spawn_tile()
        self.spawn_tile()

    def show(self):
        for i in range(0, 4):
            for j in range(0, 4):
                if self.board[i][j] is None:
                    print('_ ', end='')
                else:
                    print(str(self.board[i][j].val)+' ', end='')
            print()

    def inbounds(self, x, y):
        return 0 <= y and y < len(self.board) and 0 <= x and x < len(self.board[0])

    def exist(self, x, y):
        return self.inbounds(x, y) and self.board[y][x] is not None

    def get_empty_spots(self):
        empty_spots = []
        for y in range(0, 4):
            for x in range(0, 4):
                if self.board[y][x] is None:
                    empty_spots.append((x, y))
        return empty_spots

    def spawn_tile(self):
        empty_spots = self.get_empty_spots()
        if len(empty_spots) is 0:
            return False

        spot = random.choice(empty_spots)
        if not self.graphic:
            if random.random() < 0.90:
                self.board[spot[1]][spot[0]] = Tile(1, spot[0], spot[1])
            else:
                self.board[spot[1]][spot[0]] = Tile(2, spot[0], spot[1])
        else:
            if random.random() < 0.90:
                self.board[spot[1]][spot[0]] = GraphicTile(1, spot[0], spot[1])
            else:
                self.board[spot[1]][spot[0]] = GraphicTile(2, spot[0], spot[1])
        return True

    @staticmethod
    def mini_shift(tile_line):
        # Shift one row or column forward
        moved_flag = False
        points = 0
        for i in range(0, 3):
            r = 2-i
            if tile_line[r] is not None:
                z = r
                while z < 3:
                    if tile_line[z+1] is not None:
                        break
                    z += 1
                if tile_line[z] is None:
                    # If found a new empty spot, swap tiles
                    tile_line[z] = tile_line[r]
                    tile_line[r] = None
                    moved_flag = True
                # Check for merge
                if z < 3 and not tile_line[z+1].merged_flag and \
                   tile_line[z+1].val is tile_line[z].val:
                    tile_line[z+1].val += 1
                    points += 2**tile_line[z+1].val
                    tile_line[z+1].merged_flag = True
                    tile_line[z] = None
                    moved_flag = True
        return (tile_line, moved_flag, points)

    def shift(self, direction):
        moved_flag = False
        if direction is 'w' or direction is 's':
            for col in range(0, 4):
                tile_line = [self.board[row][col] for row in range(0, 4)]
                if direction is 'w':
                    tile_line.reverse()
                shifted_tiles, made_move, points = Board.mini_shift(tile_line)
                self.score += points
                moved_flag |= made_move
                if direction is 'w':
                    shifted_tiles.reverse()
                for row in range(0, 4):
                    self.board[row][col] = shifted_tiles[row]
        elif direction is 'a' or direction is 'd':
            for row in range(0, 4):
                tile_line = list(self.board[row])
                if direction is 'a':
                    tile_line.reverse()
                shifted_tiles, made_move, points = Board.mini_shift(tile_line)
                self.score += points
                moved_flag |= made_move
                if direction is 'a':
                    shifted_tiles.reverse()
                self.board[row] = shifted_tiles
        return moved_flag

    def check_loss(self):
        for y in range(0, 4):
            for x in range(0, 4):
                if self.board[y][x] is None or \
                   (self.exist(x-1, y) and self.board[y][x-1].val is self.board[y][x].val) or \
                   (self.exist(x+1, y) and self.board[y][x+1].val is self.board[y][x].val) or \
                   (self.exist(x, y-1) and self.board[y-1][x].val is self.board[y][x].val) or \
                   (self.exist(x, y+1) and self.board[y+1][x].val is self.board[y][x].val):
                    return False
        return True

    def computer_move(self):
        for row in range(0, 4):
            for col in range(0, 4):
                if self.board[row][col] is not None:
                    self.board[row][col].move(col, row)
                    self.board[row][col].merged_flag = False
        self.spawn_tile()
        self.lost |= self.check_loss()

    def hash(self):
        return hash(tuple(tuple(row) for row in self.board))


@WINDOW.event
def on_key_press(symbol, modifiers):
    moved_flag = False
    if symbol is key.UP or symbol is key.W:
        moved_flag = board.shift('w')
    elif symbol is key.RIGHT or symbol is key.D:
        moved_flag = board.shift('d')
    elif symbol is key.DOWN or symbol is key.S:
        moved_flag = board.shift('s')
    elif symbol is key.LEFT or symbol is key.A:
        moved_flag = board.shift('a')
    if moved_flag:
        board.computer_move()


@WINDOW.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    BG_SPRITE.y = WINDOW.height - BG_SPRITE.height
    BG_SPRITE.draw()

    for row in board.board:
        for tile in row:
            if tile is not None:
                tile.batch.draw()
    if board.lost:
        LOST_TEXT.text = "Final Score: "+str(board.score)
        LOST_SCREEN.draw()


def start(graphic=False, ai_solve=True):
    global board
    board = Board(graphic)

    if not ai_solve:
        pyglet.app.run()
    else:
        set_board(board)
        if graphic:
            # for _ in range(0, 20):
            #     smart_move(0)
            pyglet.clock.schedule_interval(smart_move, 1/120)
            pyglet.app.run()
        else:
            for i in range(0, 100):
                smart_move(0)
                if board.lost:
                    break
        board.show()
        print("Score:", board.score)


# start()

