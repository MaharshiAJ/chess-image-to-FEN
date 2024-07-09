from PIL import Image, ImageDraw

from piece import Piece, Type, Color


class Board:
    def __init__(self) -> None:
        # Initalize an empty board
        self.board = [[None for x in range(8)] for y in range(8)]
        self.white_pieces: list[Piece] = []
        self.black_pieces: list[Piece] = []

    def can_castle(self, color: Color) -> tuple[bool]:
        queenside, kingside = False, False
        if (
            self.board[color.home_location()][0] is not None
            and self.board[color.home_location()][0].type == Type.ROOK
            and not self.board[color.home_location()][0].previous_moves
        ) and (
            self.board[color.home_location()][4] is not None
            and self.board[color.home_location()][4].type == Type.KING
            and not self.board[color.home_location()][4].previous_moves
        ):
            queenside = True

        if (
            self.board[color.home_location()][7] is not None
            and self.board[color.home_location()][7].type == Type.ROOK
            and not self.board[color.home_location()][7].previous_moves
        ) and (
            self.board[color.home_location()][4] is not None
            and self.board[color.home_location()][4].type == Type.KING
            and not self.board[color.home_location()][4].previous_moves
        ):
            kingside = True

        return (queenside, kingside)

    def inital_position(self) -> None:
        self.white_pieces.append(
            Piece(Type.KING, Color.WHITE, position=(Color.WHITE.home_location(), 4))
        )
        self.white_pieces.append(
            Piece(Type.QUEEN, Color.WHITE, position=(Color.WHITE.home_location(), 3))
        )
        self.white_pieces.append(
            Piece(Type.BISHOP, Color.WHITE, position=(Color.WHITE.home_location(), 2))
        )
        self.white_pieces.append(
            Piece(Type.BISHOP, Color.WHITE, position=(Color.WHITE.home_location(), 5))
        )
        self.white_pieces.append(
            Piece(Type.KNIGHT, Color.WHITE, position=(Color.WHITE.home_location(), 1))
        )
        self.white_pieces.append(
            Piece(Type.KNIGHT, Color.WHITE, position=(Color.WHITE.home_location(), 6))
        )
        self.white_pieces.append(
            Piece(Type.ROOK, Color.WHITE, position=(Color.WHITE.home_location(), 0))
        )
        self.white_pieces.append(
            Piece(Type.ROOK, Color.WHITE, position=(Color.WHITE.home_location(), 7))
        )

        self.black_pieces.append(
            Piece(Type.KING, Color.BLACK, position=(Color.BLACK.home_location(), 4))
        )
        self.black_pieces.append(
            Piece(Type.QUEEN, Color.BLACK, position=(Color.BLACK.home_location(), 3))
        )
        self.black_pieces.append(
            Piece(Type.BISHOP, Color.BLACK, position=(Color.BLACK.home_location(), 2))
        )
        self.black_pieces.append(
            Piece(Type.BISHOP, Color.BLACK, position=(Color.BLACK.home_location(), 5))
        )
        self.black_pieces.append(
            Piece(Type.KNIGHT, Color.BLACK, position=(Color.BLACK.home_location(), 1))
        )
        self.black_pieces.append(
            Piece(Type.KNIGHT, Color.BLACK, position=(Color.BLACK.home_location(), 6))
        )
        self.black_pieces.append(
            Piece(Type.ROOK, Color.BLACK, position=(Color.BLACK.home_location(), 0))
        )
        self.black_pieces.append(
            Piece(Type.ROOK, Color.BLACK, position=(Color.BLACK.home_location(), 7))
        )

        for i in range(8):
            self.white_pieces.append(Piece(Type.PAWN, Color.WHITE, position=(6, i)))
            self.black_pieces.append(Piece(Type.PAWN, Color.BLACK, position=(1, i)))

        for piece in self.white_pieces:
            self.board[piece.position[0]][piece.position[1]] = piece

        for piece in self.black_pieces:
            self.board[piece.position[0]][piece.position[1]] = piece

    # TODO:
    def random_position(self) -> None:
        pass

    def print(self) -> None:
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None:
                    print(self.board[i][j].notation(), end=" ")

            print("")

    def to_image(self):
        square_size = 60
        board_size = square_size * 8
        image = Image.new("RGB", (board_size, board_size))
        draw = ImageDraw.Draw(image)

        light_square_color = (211, 211, 211)
        dark_square_color = (128, 128, 128)

        for i in range(8):
            for j in range(8):
                square_color = (
                    light_square_color if (i + j) % 2 == 0 else dark_square_color
                )
                draw.rectangle(
                    [
                        j * square_size,
                        i * square_size,
                        (j + 1) * square_size,
                        (i + 1) * square_size,
                    ],
                    fill=square_color,
                )

        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None:
                    piece_img_path = piece.image_path()
                    piece_img = Image.open(piece_img_path).resize(
                        (square_size, square_size)
                    )
                    image.paste(
                        piece_img, (j * square_size, i * square_size), piece_img
                    )

        return image

    def to_fen(self, to_move: Color = Color.WHITE) -> str:
        fen = ""

        for i in range(8):
            count = 0
            for j in range(8):
                if self.board[i][j] is not None:
                    if count != 0:
                        fen += str(count)
                        count = 0

                    fen += self.board[i][j].notation()
                else:
                    count += 1

            if count != 0:
                fen += str(count)
                count = 0

            fen += "/" if i < 7 else ""

        fen += " w " if to_move == Color.WHITE else " b "

        white_castling_rights = self.can_castle(Color.WHITE)
        black_castling_rights = self.can_castle(Color.BLACK)

        if white_castling_rights[1] == True:
            fen += "K"

        if white_castling_rights[0] == True:
            fen += "Q"

        if black_castling_rights[1] == True:
            fen += "k"

        if black_castling_rights[0] == True:
            fen += "q"

        if (
            white_castling_rights[1] == False
            and white_castling_rights[0] == False
            and black_castling_rights[1] == False
            and black_castling_rights[0] == False
        ):
            fen += "-"

        # In order: En Passant, Halfmove clock, Full move clock
        fen += " - 0 1"

        return fen
