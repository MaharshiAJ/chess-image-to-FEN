import pygame
import random
import json

piece_list = ["R", "N", "B", "Q", "P"]


def write_json(path_to_img, fen, filename="./dataset/mapping.json"):
    with open(filename, "r+") as file:
        file_data = json.load(file)
        file_data[path_to_img] = fen
        file.seek(0)
        json.dump(file_data, file, indent=4)


def place_kings(brd):
    while True:
        rank_white, file_white, rank_black, file_black = (
            random.randint(0, 7),
            random.randint(0, 7),
            random.randint(0, 7),
            random.randint(0, 7),
        )
        diff_list = [abs(rank_white - rank_black), abs(file_white - file_black)]
        if sum(diff_list) > 2 or set(diff_list) == set([0, 2]):
            brd[rank_white][file_white], brd[rank_black][file_black] = "K", "k"
            break


def populate_board(brd, wp, bp):
    for x in range(2):
        if x == 0:
            piece_amount = wp
            pieces = piece_list
        else:
            piece_amount = bp
            pieces = [s.lower() for s in piece_list]
        while piece_amount != 0:
            piece_rank, piece_file = random.randint(0, 7), random.randint(0, 7)
            piece = random.choice(pieces)
            if (
                brd[piece_rank][piece_file] == " "
                and pawn_on_promotion_square(piece, piece_rank) == False
            ):
                brd[piece_rank][piece_file] = piece
                piece_amount -= 1


def fen_from_board(brd):
    fen = ""
    for x in brd:
        n = 0
        for y in x:
            if y == " ":
                n += 1
            else:
                if n != 0:
                    fen += str(n)
                fen += y
                n = 0
        if n != 0:
            fen += str(n)
        fen += "/" if fen.count("/") < 7 else ""
    fen += " w - - 0 1\n"
    return fen


def pawn_on_promotion_square(pc, pr):
    if pc == "P" and pr == 0:
        return True
    elif pc == "p" and pr == 7:
        return True
    return False


PIECE_IMAGES = {
    "R": pygame.image.load("./generator/pieces/wr.png"),
    "N": pygame.image.load("./generator/pieces/wn.png"),
    "B": pygame.image.load("./generator/pieces/wb.png"),
    "Q": pygame.image.load("./generator/pieces/wq.png"),
    "K": pygame.image.load("./generator/pieces/wk.png"),
    "P": pygame.image.load("./generator/pieces/wp.png"),
    "r": pygame.image.load("./generator/pieces/br.png"),
    "n": pygame.image.load("./generator/pieces/bn.png"),
    "b": pygame.image.load("./generator/pieces/bb.png"),
    "q": pygame.image.load("./generator/pieces/bq.png"),
    "k": pygame.image.load("./generator/pieces/bk.png"),
    "p": pygame.image.load("./generator/pieces/bp.png"),
}

pygame.init()

BOARD_SIZE = 8
SQUARE_SIZE = 60
WHITE = (211, 211, 211)
BLACK = (128, 128, 128)

window_size = BOARD_SIZE * SQUARE_SIZE
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Chess Board")


def draw_chessboard(screen):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                ),
            )
            piece = board[row][col]
            if piece != " ":
                piece_img = PIECE_IMAGES[piece]
                screen.blit(piece_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            pygame.display.flip()


def main():
    for i in range(0, 1):
        piece_amount_white = 2
        piece_amount_black = 2
        place_kings(board)
        populate_board(board, piece_amount_white, piece_amount_black)

        screen = pygame.display.set_mode((window_size, window_size))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            draw_chessboard(screen)
            pygame.display.flip()

        pygame.image.save(screen, f"image{i}.png")
        write_json(f"image{i}.png", fen_from_board(board))

    pygame.quit()


if __name__ == "__main__":
    main()
