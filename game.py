import copy
import time

import pygame, random

pygame.init()


class Game:
    def __init__(self, board, piece, pieces_list, held_piece):
        self.board = board
        self.piece = piece
        self.pieces_list = pieces_list
        self.held_piece = held_piece
        self.next_pieces = [Piece(), Piece(), Piece()]

        self.swapped_pieces = False
        self.game_over = False
        self.level = 1
        self.scaling_threshold = 15
        self.counter = 0
        self.score = 0
        self.lines_cleared = 0

    def place_piece(self):
        for coor in self.piece.coordinates:
            if board[coor[1] + self.piece.y][coor[0] + self.piece.x] == 1:
                self.game_over = True

        for coor in self.piece.coordinates:
            self.board[coor[1] + self.piece.y][coor[0] + self.piece.x] = 1
        self.pieces_list.append(self.piece)
        self.piece = self.next_pieces.pop(0)
        game.next_pieces.append(Piece())
        self.swapped_pieces = False

    def update(self):
        self.piece.update()

        while self.piece.out_of_bounds_left():
            self.piece.x += 1

        while self.piece.out_of_bounds_right():
            self.piece.x -= 1

        while self.piece.out_of_bounds_bottom():
            self.piece.y -= 1

        self.counter += 1

        if self.counter >= self.scaling_threshold:
            if self.piece.is_touching_bottom() or self.is_colliding():
                self.place_piece()
            self.piece.y += 1
            self.counter = 0

        for piece in self.pieces_list:
            piece.draw()

        self.check_clear_row()

    def draw(self):
        try:
            window.blit(TITLE, (325, 15))
            window.blit(HOLD, (320, 190))
            window.blit(NEXT, (455, 190))
            if game.held_piece is not None:
                game.held_piece.draw_img(10, 7)

            y = 7
            for piece in game.next_pieces:
                piece.draw_img(15, y)
                y += 4
            window.blit(SCORE, (320, 320))
            window.blit(LEVEL, (320, 405))
            window.blit(LINES, (320, 490))
            pygame.display.set_icon(ICON)
            message(str(game.score), 25, (255, 255, 255), (340, 360))
            message(str(game.lines_cleared), 25, (255, 255, 255), (340, 530))
            message(str(game.level), 25, (255, 255, 255), (340, 445))
        except:
            message("TETRIS", 50, (255, 0, 0), (325, 15))
            message("HOLD", 25, (200, 200, 200), (320, 190))
            message("NEXT", 25, (200, 200, 200), (455, 190))

            if game.held_piece is not None:
                game.held_piece.draw_img(10, 7)
            y = 7
            for piece in game.next_pieces:
                piece.draw_img(15, y)
                y += 4

            message("SCORE", 25, (200, 200, 200), (320, 300))
            message("LEVEL", 25, (200, 200, 200), (320, 400))
            message("LINES", 25, (200, 200, 200), (320, 500))

            message(str(game.score), 25, (255, 255, 255), (340, 360))
            message(str(game.lines_cleared), 25, (255, 255, 255), (340, 530))
            message(str(game.level), 25, (255, 255, 255), (340, 445))

        draw_grid()
        pygame.display.flip()
        window.fill((0, 0, 0))
        game.piece.draw()

    def is_colliding(self):
        for coor in self.piece.coordinates:
            if board[coor[1] + self.piece.y + 1][coor[0] + self.piece.x] == 1:
                return True

    def check_clear_row(self):
        for r in range(ROWS):
            if is_full_row(game.board[r]):
                game.board[r] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                int = r
                while int >= 0:
                    for col in range(COLS):
                        if game.board[int][col] == 1:
                            game.board[int][col] = 0
                            game.board[int + 1][col] = 1
                    int -= 1

                for piece in game.pieces_list:
                    for coord in piece.coordinates:
                        if coord[1] + piece.y == r:
                            coord[1] = -10
                            coord[0] = -10
                        if coord[1] + piece.y <= r:
                            coord[1] += 1
                self.score += 100
                self.lines_cleared += 1
                if self.lines_cleared % 10 == 0:
                    self.level = 1 + self.lines_cleared / 10
                self.scaling_threshold = 18 - self.level * 3

    def is_overlap_rotation(self):
        rotated_coords = copy.deepcopy(self.piece.coordinates)
        for coord in rotated_coords:
            temp = coord[1]
            coord[1] = coord[0]
            coord[0] = 3 - temp

        for coor in rotated_coords:
            try:
                if self.board[coor[1] + self.piece.y][coor[0] + self.piece.x] == 1:
                    return True
            except:
                return False

    def is_overlap_right(self):
        for coor in self.piece.coordinates:
            try:
                if board[coor[1] + self.piece.y][coor[0] + self.piece.x + 1] == 1:
                    return True
            except:
                return False

    def is_overlap_left(self):
        for coor in self.piece.coordinates:
            try:
                if board[coor[1] + self.piece.y][coor[0] + self.piece.x - 1] == 1:
                    return True
            except:
                return False


class Piece:
    def __init__(self):
        self.grid = [[0] * 4 for x in range(4)]
        pair = copy.deepcopy(random.choice(list(TETROMINOS.items())))
        self.coordinates = pair[1]
        self.shape = pair[0]
        self.colour = COLOURS.get(pair[0])

        self.y = 0
        self.x = 3

    def update(self):
        for r in range(4):
            for c in range(4):
                self.grid[r][c] = 0

        for coord in self.coordinates:
            self.grid[coord[1]][coord[0]] = 1

    def draw(self):
        for coord in self.coordinates:
            pygame.draw.rect(window, self.colour,
                             pygame.Rect(coord[0] * TILE_SIZE + self.x * TILE_SIZE,
                                         coord[1] * TILE_SIZE + self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def draw_img(self, x, y):
        for coord in self.coordinates:
            pygame.draw.rect(window, self.colour,
                             pygame.Rect(coord[0] * TILE_SIZE + x * TILE_SIZE, coord[1] * TILE_SIZE + y * TILE_SIZE,
                                         TILE_SIZE, TILE_SIZE))

    def rotate(self):
        for coord in self.coordinates:
            temp = coord[1]
            coord[1] = coord[0]
            coord[0] = 3 - temp

    def out_of_bounds_right(self):
        for coor in self.coordinates:
            if coor[0] + self.x > COLS - 1:
                return True

    def out_of_bounds_left(self):
        for coor in self.coordinates:
            if coor[0] + self.x < 0:
                return True

    def out_of_bounds_bottom(self):
        for coor in self.coordinates:
            if coor[1] + self.y > 19:
                return True

    def is_touching_bottom(self):
        for coor in self.coordinates:
            if self.y + coor[1] == 19:
                return True


def is_full_row(row):
    for i in range(len(row)):
        if row[i] == 0:
            return False
    return True


def draw_grid():
    block_size = 30
    for x in range(0, 300, block_size):
        for y in range(0, SCREEN_HEIGHT, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(window, (200, 200, 200), rect, 1)


def message(msg, size, colour, loc):
    words = pygame.font.SysFont('comicsansms', size).render(msg, True, colour)
    window.blit(words, loc)


def check_events():
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_DOWN]:
        if not game.piece.out_of_bounds_bottom():
            game.counter += 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if not game.is_overlap_rotation():
                    game.piece.rotate()
            if event.key == pygame.K_RIGHT:
                if not game.is_overlap_right():
                    game.piece.x += 1
            if event.key == pygame.K_LEFT:
                if not game.is_overlap_left():
                    game.piece.x -= 1
            if event.key == pygame.K_c:
                if not game.swapped_pieces:
                    if game.held_piece is None:
                        game.held_piece = copy.deepcopy(game.piece)
                        game.piece = game.next_pieces.pop(0)
                        game.next_pieces.append(Piece())
                    else:
                        temp = copy.deepcopy(game.held_piece)
                        game.held_piece = copy.deepcopy(game.piece)
                        game.piece = temp
                    game.swapped_pieces = True
                    game.piece.y = 0
                    game.piece.x = 3
            if event.key == pygame.K_SPACE:
                while not game.is_colliding() or not game.piece.is_touching_bottom:
                    game.piece.y += 1
                    game.score += 2
                    if game.piece.is_touching_bottom() or game.is_colliding():
                        game.place_piece()
                        break
    if game.game_over:
        quit()

SCREEN_WIDTH, SCREEN_HEIGHT = 601, 601
TILE_SIZE = 30
COLS = 10
ROWS = 20
TETROMINOS = {
    "I": [[1, 0], [1, 1], [1, 2], [1, 3]],
    "J": [[2, 0], [2, 2], [1, 2], [2, 1]],
    "L": [[1, 0], [1, 1], [1, 2], [2, 2]],
    "O": [[1, 1], [1, 2], [2, 2], [2, 1]],
    "S": [[1, 2], [2, 2], [2, 1], [3, 1]],
    "Z": [[0, 1], [1, 1], [1, 2], [2, 2]],
    "T": [[0, 1], [1, 1], [2, 1], [1, 2]]
}
COLOURS = {
    "I": (0, 225, 255),
    "J": (3, 65, 190),
    "L": (255, 151, 28),
    "O": (255, 213, 0),
    "S": (114, 203, 59),
    "Z": (220, 50, 19),
    "T": (128, 0, 128)
}
TITLE = pygame.image.load(r"C:\Users\jonwu\Downloads\pixil-frame-0 (5).png")
HOLD = pygame.image.load(r"C:\Users\jonwu\Downloads\pixil-frame-0 (6).png")
NEXT = pygame.image.load(r"C:\Users\jonwu\Downloads\pixil-frame-0 (7).png") 
ICON = pygame.image.load(r"C:\Users\jonwu\Downloads\pixilart-drawing.png")
SCORE = pygame.image.load(r"C:\Users\jonwu\Downloads\score.png")
LEVEL = pygame.image.load(r"C:\Users\jonwu\Downloads\level.png")
LINES = pygame.image.load(r"C:\Users\jonwu\Downloads\lines.png")

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

board = [[0] * COLS for i in range(ROWS)]
piece = Piece()
pieces = []
held_piece = None
game = Game(board, piece, pieces, held_piece)

running = True

while running:
    check_events()
    game.update()
    game.draw()
    clock.tick(60)

