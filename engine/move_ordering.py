import chess
from engine.config import pst, piece_values

def move_score(board, move):
    score = 0
    if board.is_capture(move):
        attacker = board.piece_at(move.from_square)
        victim = board.piece_at(move.to_square)
        # Handle en passant where victim is not on destination square
        if victim is None and board.is_en_passant(move):
            victim = chess.Piece(chess.PAWN, not board.turn)
        if victim:
            score += (piece_values[victim.piece_type] * 10) - piece_values[attacker.piece_type]
    if move.promotion:
        score += 200
    return score