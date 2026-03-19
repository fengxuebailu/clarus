"""
Go Board Utilities
Handles SGF parsing, coordinate conversion, and board manipulation
"""

from typing import List, Tuple, Optional
import re


class GoBoard:
    """
    Go Board representation and utilities

    Coordinates:
    - SGF: aa, ab, ..., ss (19x19, lowercase letters)
    - GTP: A1, B1, ..., T19 (skip 'I')
    - Internal: (x, y) zero-indexed
    """

    GTP_COLS = "ABCDEFGHJKLMNOPQRST"  # Skip 'I'

    def __init__(self, size: int = 19):
        self.size = size

    @staticmethod
    def sgf_to_gtp(sgf_coord: str) -> str:
        """
        Convert SGF coordinate to GTP coordinate

        Args:
            sgf_coord: SGF format like 'pd' (16,4)

        Returns:
            GTP format like 'Q16'
        """
        if len(sgf_coord) != 2:
            raise ValueError(f"Invalid SGF coordinate: {sgf_coord}")

        col = ord(sgf_coord[0]) - ord('a')
        row = ord(sgf_coord[1]) - ord('a')

        gtp_col = GoBoard.GTP_COLS[col]
        gtp_row = 19 - row  # Invert row

        return f"{gtp_col}{gtp_row}"

    @staticmethod
    def gtp_to_sgf(gtp_coord: str) -> str:
        """
        Convert GTP coordinate to SGF coordinate

        Args:
            gtp_coord: GTP format like 'Q16'

        Returns:
            SGF format like 'pd'
        """
        if len(gtp_coord) < 2:
            raise ValueError(f"Invalid GTP coordinate: {gtp_coord}")

        col_char = gtp_coord[0].upper()
        row_num = int(gtp_coord[1:])

        col = GoBoard.GTP_COLS.index(col_char)
        row = 19 - row_num

        sgf_col = chr(ord('a') + col)
        sgf_row = chr(ord('a') + row)

        return f"{sgf_col}{sgf_row}"

    @staticmethod
    def gtp_to_coords(gtp_coord: str) -> Tuple[int, int]:
        """
        Convert GTP coordinate to (x, y) tuple

        Args:
            gtp_coord: GTP format like 'Q16'

        Returns:
            (x, y) tuple (zero-indexed)
        """
        col_char = gtp_coord[0].upper()
        row_num = int(gtp_coord[1:])

        x = GoBoard.GTP_COLS.index(col_char)
        y = 19 - row_num

        return (x, y)

    @staticmethod
    def coords_to_gtp(x: int, y: int) -> str:
        """
        Convert (x, y) coordinates to GTP format

        Args:
            x: Column (0-18)
            y: Row (0-18)

        Returns:
            GTP format like 'Q16'
        """
        col = GoBoard.GTP_COLS[x]
        row = 19 - y

        return f"{col}{row}"


class SGFParser:
    """Parse SGF (Smart Game Format) files"""

    def __init__(self, sgf_string: str):
        self.sgf = sgf_string
        self.moves: List[Tuple[str, str]] = []
        self.board_size = 19
        self.komi = 7.5
        self.parse()

    def parse(self):
        """Parse SGF string and extract moves"""
        # Extract board size
        size_match = re.search(r'SZ\[(\d+)\]', self.sgf)
        if size_match:
            self.board_size = int(size_match.group(1))

        # Extract komi
        komi_match = re.search(r'KM\[([\d.]+)\]', self.sgf)
        if komi_match:
            self.komi = float(komi_match.group(1))

        # Extract moves
        # Black moves: ;B[pd]
        black_moves = re.findall(r';B\[([a-z]{2})\]', self.sgf)
        # White moves: ;W[pd]
        white_moves = re.findall(r';W\[([a-z]{2})\]', self.sgf)

        # Interleave moves in order
        # This is simplified - proper SGF parsing would track tree structure
        all_moves_pattern = re.findall(r';([BW])\[([a-z]{2})\]', self.sgf)

        for color, coord in all_moves_pattern:
            gtp_coord = GoBoard.sgf_to_gtp(coord)
            self.moves.append((color, gtp_coord))

    def get_moves(self) -> List[Tuple[str, str]]:
        """
        Get moves as list of (color, GTP coordinate) tuples

        Returns:
            List like [("B", "Q16"), ("W", "D4"), ...]
        """
        return self.moves

    def add_move(self, color: str, move: str) -> str:
        """
        Add a move to the SGF

        Args:
            color: "B" or "W"
            move: GTP coordinate like "Q16"

        Returns:
            Updated SGF string
        """
        sgf_coord = GoBoard.gtp_to_sgf(move)
        move_node = f";{color}[{sgf_coord}]"

        # Insert before final parenthesis
        if self.sgf.endswith(")"):
            updated_sgf = self.sgf[:-1] + move_node + ")"
        else:
            updated_sgf = self.sgf + move_node

        return updated_sgf


def parse_board_state(board_state: str, move_a: str, move_b: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    """
    Parse board state and create move sequences for KataGo analysis

    Args:
        board_state: SGF string or board representation
        move_a: Move A in GTP format (e.g., "Q16")
        move_b: Move B in GTP format (e.g., "D4")

    Returns:
        Two lists of moves: (moves_for_A, moves_for_B)
    """
    # Parse SGF to get existing moves
    if board_state.startswith("(;"):
        parser = SGFParser(board_state)
        base_moves = parser.get_moves()
    else:
        # Empty board
        base_moves = []

    # Determine whose turn it is
    if len(base_moves) == 0:
        next_color = "B"
    else:
        last_color = base_moves[-1][0]
        next_color = "W" if last_color == "B" else "B"

    # Create two sequences: base + move A, base + move B
    moves_a = base_moves + [(next_color, move_a)]
    moves_b = base_moves + [(next_color, move_b)]

    return moves_a, moves_b


def moves_to_sgf(moves: List[Tuple[str, str]], board_size: int = 19, komi: float = 7.5) -> str:
    """
    Convert move list to SGF string

    Args:
        moves: List of (color, GTP coordinate) tuples
        board_size: Board size
        komi: Komi value

    Returns:
        SGF string
    """
    sgf = f"(;GM[1]FF[4]SZ[{board_size}]KM[{komi}]"

    for color, gtp_coord in moves:
        sgf_coord = GoBoard.gtp_to_sgf(gtp_coord)
        sgf += f";{color}[{sgf_coord}]"

    sgf += ")"

    return sgf
