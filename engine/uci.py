import chess
import threading
from engine.search import find_best_move

board = chess.Board()

search_thread = None
stop_event = threading.Event()
best_move = None
searching = False


def search_worker(max_depth, movetime):
    global best_move, searching

    best_move = find_best_move(
        board,
        max_depth=max_depth,
        time_limit=movetime,
        stop_event=stop_event
    )

    searching = False

    # If search ended naturally (not stopped externally),
    # we must report the move now.
    if not stop_event.is_set():
        if best_move:
            print(f"bestmove {best_move.uci()}")
        else:
            print("bestmove 0000")


def main():
    global board, search_thread, stop_event, searching

    while True:
        try:
            command = input().strip()
        except EOFError:
            break

        if command == "uci":
            print("id name BotBreeze")
            print("id author Mateus")
            print("uciok")

        elif command == "isready":
            print("readyok")

        elif command.startswith("position"):
            parts = command.split()
            if "startpos" in parts:
                board = chess.Board()
                if "moves" in parts:
                    idx = parts.index("moves")
                    for move in parts[idx + 1:]:
                        board.push_uci(move)

        elif command.startswith("go"):
            stop_event.clear()
            searching = True

            # Defaults
            max_depth = None
            movetime = float("inf")

            parts = command.split()

            if "depth" in parts:
                max_depth = int(parts[parts.index("depth") + 1])

            if "movetime" in parts:
                movetime = int(parts[parts.index("movetime") + 1]) / 1000

            search_thread = threading.Thread(
                target=search_worker,
                args=(max_depth, movetime),
                daemon=True
            )
            search_thread.start()

        elif command == "stop":
            stop_event.set()
            if search_thread and search_thread.is_alive():
                search_thread.join()

            if best_move:
                print(f"bestmove {best_move.uci()}")
            else:
                print("bestmove 0000")

        elif command == "quit":
            stop_event.set()
            break