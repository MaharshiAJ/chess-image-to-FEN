from enum import Enum


class Type(Enum):
    KING = 1
    QUEEN = 2
    BISHOP = 3
    KNIGHT = 4
    ROOK = 5
    PAWN = 6


class Color(Enum):
    WHITE = 1
    BLACK = 2

    def home_location(self) -> int:
        match self:
            case Color.WHITE:
                return 7
            case Color.BLACK:
                return 0


class Piece:
    def __init__(self, type: Type, color: Color, position=None) -> None:
        self.type = type
        self.color = color
        self.position = position
        self.available_moves = []
        self.previous_moves = []

    def notation(self) -> str:
        match self.type:
            case Type.KING:
                return "K" if self.color == Color.WHITE else "k"
            case Type.QUEEN:
                return "Q" if self.color == Color.WHITE else "q"
            case Type.BISHOP:
                return "B" if self.color == Color.WHITE else "b"
            case Type.KNIGHT:
                return "N" if self.color == Color.WHITE else "n"
            case Type.ROOK:
                return "R" if self.color == Color.WHITE else "r"
            case Type.PAWN:
                return "P" if self.color == Color.WHITE else "p"

    def image_path(self) -> str:
        match self.type:
            case Type.KING:
                return (
                    "./generator/Pieces/wk.png"
                    if self.color == Color.WHITE
                    else "./generator/Pieces/bk.png"
                )
            case Type.QUEEN:
                return (
                    "./generator/Pieces/wq.png"
                    if self.color == Color.WHITE
                    else "./generator/Pieces/bq.png"
                )
            case Type.BISHOP:
                return (
                    "./generator/Pieces/wb.png"
                    if self.color == Color.WHITE
                    else "./generator/Pieces/bb.png"
                )
            case Type.KNIGHT:
                return (
                    "./generator/Pieces/wn.png"
                    if self.color == Color.WHITE
                    else "./generator/Pieces/bn.png"
                )
            case Type.ROOK:
                return (
                    "./generator/Pieces/wr.png"
                    if self.color == Color.WHITE
                    else "./generator/Pieces/br.png"
                )
            case Type.PAWN:
                return (
                    "./generator/Pieces/wp.png"
                    if self.color == Color.WHITE
                    else "./generator/Pieces/bp.png"
                )
