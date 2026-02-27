import chess
import time
from engine.config import STATS, pst, piece_values
from engine.evaluation import evaluate_board
from engine.tt import TT
from engine.utils import is_endgame, forcing
from engine.move_ordering import move_score
import threading

def quiescence(board, alpha, beta, depth, stop_event):
    STATS.qnodes += 1
    if stop_event.is_set():
        return evaluate_board(board)

    stand_pat = evaluate_board(board)

    if stand_pat >= beta:
        STATS.cutoffs += 1
        return beta

    if stand_pat > alpha:
        alpha = stand_pat

    if depth == 0:
        return alpha

    for move in forcing(board):  # captures/checks only
        board.push(move)
        score = -quiescence(board, -beta, -alpha, depth - 1, stop_event)
        board.pop()

        if score > alpha:
            alpha = score
            if alpha >= beta:
                STATS.cutoffs += 1
                break

    return alpha

def negamax(board, depth, alpha, beta, stop_event):
    STATS.nodes += 1
    STATS.max_depth = max(STATS.max_depth, depth)

    if stop_event.is_set():
        return evaluate_board(board)

    MATE_SCORE = 100000
    R = 2
    null_move_margin = 150

    # Terminal positions
    if board.is_checkmate():
        return -MATE_SCORE + depth

    if (board.is_stalemate() or
        board.is_insufficient_material() or
        board.can_claim_fifty_moves() or
        board.can_claim_threefold_repetition()):
        return 0

    if depth == 0:
        return quiescence(board, alpha, beta, 4, stop_event)

    # Transposition table
    key = (board._transposition_key(), depth)
    STATS.tt_probes += 1
    if key in TT:
        STATS.tt_hits += 1
        return TT[key]

    static_eval = evaluate_board(board)

    # Null-move pruning (safe)
    if (depth >= R + 2 and
        not board.is_check() and
        not is_endgame(board) and
        static_eval >= beta + null_move_margin):

        board.push(chess.Move.null())
        score = -negamax(board, depth - 1 - R, -beta, -beta + 1, stop_event)
        board.pop()

        if score >= beta:
            return beta

    moves = list(board.legal_moves)
    moves.sort(key=lambda m: move_score(board, m), reverse=True)

    best = alpha

    for move in moves:
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -best, stop_event)
        board.pop()

        if score > best:
            best = score
            if best >= beta:
                STATS.cutoffs += 1
                break

    TT[key] = best
    return best

def find_best_move(board, max_depth, stop_event, debug=False, time_limit = float('inf')):
    STATS.start_time = time.perf_counter()

    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None

    best_move = legal_moves[0]
    last_completed_best = best_move
    last_score = 0

    current_depth = 1
    base_window = 35  # centipawns

    while time.perf_counter() - STATS.start_time < time_limit and not stop_event.is_set():

        #aspiration setup 
        if current_depth > 1:
            window = base_window
            alpha = last_score - window
            beta = last_score + window
        else:
            alpha = float("-inf")
            beta = float("inf")

        while True:  # retry loop for aspiration failures

            depth_best = legal_moves[0]
            depth_alpha = alpha
            depth_beta = beta

            for move in legal_moves:

                if time.perf_counter() - STATS.start_time >= time_limit:
                    return last_completed_best
                
                if stop_event.is_set():
                    return last_completed_best

                board.push(move)
                score = -negamax(board, current_depth - 1, -depth_beta, -depth_alpha, stop_event)
                board.pop()

                if score > depth_alpha:
                    depth_alpha = score
                    depth_best = move

            depth_score = depth_alpha

            #aspiration evaluation
            if depth_score <= alpha:          # fail-low
                alpha = float("-inf")
                beta = depth_score + base_window * 2
                continue

            elif depth_score >= beta:         # fail-high
                alpha = depth_score - base_window * 2
                beta = float("inf")
                continue

            else:
                # success inside window
                last_score = depth_score
                best_move = depth_best
                last_completed_best = best_move
                break

        current_depth += 1

        if max_depth and current_depth > max_depth:
            break
    

    return best_move