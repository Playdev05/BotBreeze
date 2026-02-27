import chess
from engine.config import piece_values, pst, STATS
from engine.utils import is_endgame, king_attackers

def evaluate_board(board):
    STATS.eval_calls += 1
    evaluation = 0
    total_material = 0
    king_safety_weight = 1.34
    king_safety_white = 0
    king_safety_black = 0

    if board.is_repetition(2):
        if board.turn == chess.WHITE:
            evaluation -= 8
        else:
            evaluation += 8

    #Simple material evaluation
    for piece_type, value in piece_values.items(): #Check for each square on the board
        for square in board.pieces(piece_type, chess.WHITE) | board.pieces(piece_type, chess.BLACK):
            piece = board.piece_at(square) #Get the piece at that square
            if piece: 
                value = piece_values[piece.piece_type] #Get the value of that piece
                if piece.piece_type != chess.KING: #Avoid king in endgame eval
                    total_material += value
                else:
                    #King safety evaluation
                    if piece.color == chess.WHITE:
                        king_safety_white = king_attackers(board, square, chess.BLACK)
                    else:
                        king_safety_black = king_attackers(board, square, chess.WHITE)

                if piece.color == chess.WHITE: 
                    evaluation += value 
                else: 
                    evaluation -= value 
                #PST bonus/malus
                _pst = {}
                if piece.color == chess.WHITE:
                    _pst = pst[piece.piece_type]
                    evaluation += _pst[square]
                else:
                    _pst = pst[piece.piece_type]
                    evaluation -= _pst[chess.square_mirror(square)]
                if piece.piece_type in (chess.KNIGHT, chess.BISHOP):
                    if piece.color == chess.WHITE and square in [chess.B1, chess.G1, chess.C1, chess.F1]:
                        evaluation -= 15

    #king safety evaluation
    if is_endgame(board):
        king_safety_weight = 0.46

    evaluation -= int(king_safety_black * king_safety_weight)
    evaluation += int(king_safety_white * king_safety_weight)

                
    return evaluation
        
    