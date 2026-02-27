import chess
from engine.config import piece_values
from engine.move_ordering import move_score

def king_attackers(board, king_square, enemy_color):
    attackers = len(board.attackers(enemy_color, king_square))
    return attackers

def is_endgame(board):
        total_material = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                total_material += piece_values[piece.piece_type]
        if total_material <= 2400 and not board.has_castling_rights(chess.WHITE) and not board.has_castling_rights(chess.BLACK):
            return True
        else:
            return False
        
def forcing(board):
    forcing_moves = []
    moves = list(board.legal_moves) #List legal moves
    if not board.is_check():
        for move in moves:
            if move.promotion or board.is_capture(move): #Check if a move is forcing
                forcing_moves.append(move) #Append the move to the list
                continue #Skip this iteration
    else:
        forcing_moves = moves
    
    
    #Order forcing moves
    forcing_moves.sort(key=lambda m: move_score(board, m), reverse=True)
    return forcing_moves

