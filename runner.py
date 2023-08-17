from logging import error
import chess, chess.pgn
import chessAI as ai
# import cProfile
# import pstats
import time
# from pstats import SortKey

DEPTH = 2

def main():
    # initiate classical chess board
    board = chess.Board()
    cvc(board)

def cvc(board: chess.Board):
    game = chess.pgn.Game()
    node = game
    game_start = time.time()
    tt = ai.TranspositionTable()
    while not board.is_game_over():
        move_start = time.time()
        move = ai.ai_move(board, DEPTH, tt)
        board.push(move)
        print(board.fen())
        node = node.add_variation(move)
        print(game)
        print(f'seconds taken: {time.time() - move_start}')
        print(f'eval: {ai.calc_eval(board)}\n')

    print(f'total time: {time.time() - game_start}')

    # when done print result
    print(board.result())


def pvc(board: chess.Board):
    game = chess.pgn.Game()
    node = game
    tt = ai.TranspositionTable()
    player_color = input("pick (white or black): ").lower()
    if player_color == "white":
            player_color = chess.WHITE
    elif player_color == "black":
            player_color = chess.BLACK
    else:
        print("Error: invalid choice")
        quit()
    while not board.is_game_over():
        print(f'eval: {ai.calc_eval(board)}\n')
        if board.turn == player_color:
            move = chess.Move.from_uci(input("your move: "))
            if move in board.legal_moves:
                board.push(move)
                node = node.add_variation(move)
        else:
            move = ai.ai_move(board, DEPTH, tt)
            board.push(move)
            node = node.add_variation(move)
            print("AI's move: " + chess.Move.uci(move))
    print(board.result())


# def runTime(function):

#     cProfile.run(f'{function}', 'output.dat')

#     with open('output_time.txt', 'w') as f:
#         p = pstats.Stats('output.dat', stream=f)
#         p.sort_stats('time').print_stats()

#     with open('output_calls.txt', 'w') as f:
#         p = pstats.Stats('output.dat', stream=f)
#         p.sort_stats('calls').print_stats()

if __name__ == "__main__":
    main()
