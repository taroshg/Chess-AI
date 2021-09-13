import chess, chess.polyglot, chess.engine
# import random
import math

# largest number
MAX = math.inf

# piece values
piece_values = {chess.PAWN:100, chess.KNIGHT:320, chess.BISHOP:330, 
                chess.ROOK:500, chess.QUEEN:900, chess.KING:0}
# [pawn, knight, bishop, rook, queen, king] 
pieces_square_table = [
    [0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10,-20,-20, 10, 10,  5,
    5, -5,-10,  0,  0,-10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0,  0,  0,  0,  0,  0],


    [-50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50],

    [-20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20],

    [0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    5, 10, 10, 10, 10, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0],

    [-20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  5,  5,  5,  5,  5,  0,-10,
    0,  0,  5,  5,  5,  5,  0, -5,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20],

    [20, 30, 10,  0,  0, 10, 30, 20,
    20, 20,  0,  0,  0,  0, 20, 20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30]]
# king endgame square table
king_endgame =  [-50,-30,-30,-30,-30,-30,-30,-50,
                -30,-20,-10,  0,  0,-10,-20,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-30,  0,  0,  0,  0,-30,-30,
                -50,-40,-30,-20,-20,-30,-40,-50]

def get_opening_moves(board):
    """
    Returns list of moves from given opening book
    """
    moves = list()
    with chess.polyglot.open_reader("opening/performance.bin") as reader:
        for entry in reader.find_all(board):
            moves.append(entry.move)
    return moves


def find_best_move(board, depth):
    """
    Finds the best move given a position and depth of analysis
    """
    opening_moves = get_opening_moves(board)
    if len(opening_moves) != 0:
        return opening_moves[0]
    best_move = None

    if board.turn:
        best_v = -MAX
        for move in filtered_moves(board):
            pos = move_result(board, move)
            v = minimax(pos, depth, -MAX, MAX)
            if best_v < v:
                best_v = v
                best_move = move
    else:
        best_v = MAX
        for move in filtered_moves(board):
            pos = move_result(board, move)
            v = minimax(pos, depth, -MAX, MAX)
            if best_v > v:
                best_v = v
                best_move = move
    return best_move


def minimax(board, depth, alpha, beta):
    """
    Returns the best possible move
    """
    if depth == 0 or board.is_game_over():
        return evaluation(board)

    if board.turn:
        v = -MAX
        for move in filtered_moves(board):
            pos = move_result(board, move)
            v = max(v, minimax(pos, depth - 1, alpha, beta))
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v
    else:
        v = MAX
        for move in filtered_moves(board):
            pos = move_result(board, move)
            v = min(v, minimax(pos, depth - 1, alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v


def evaluation(board):
    """
    Returns the value of a given static position
    """
    if board.is_game_over():
        if board.result() == "1-0":
            return MAX
        elif board.result() == "0-1":
            return -MAX
        else:
            return 0

    v = 0

    piece_map = board.piece_map()

    filtered_piece_map = filtered_pieces(board, piece_map)

    white_piece_map = filtered_piece_map[0]
    black_piece_map = filtered_piece_map[1]
    tense_piece_map = filtered_piece_map[2]

    tense_pieces = set(tense_piece_map.keys())

    endgame = False
    if endgame == False:
        endgame = True if game_phase(board, piece_map) < 1 else False

    for s in piece_map:

        piece = piece_map[s]

        # White eval (+)
        if piece.color == chess.WHITE:

            v += piece_value(piece)
            v += piece_square_value(board, s, piece, endgame)

            # check for hanging pieces if any pieces  
            if s in tense_pieces:
                v -= hanging(board, s, piece, black_piece_map)

        # Black eval (-)
        else:

            v -= piece_value(piece)
            v -= piece_square_value(board, s, piece, endgame)

            # check for hanging pieces if any pieces 
            if s in tense_pieces:
                v += hanging(board, s, piece, black_piece_map)

    """
    WHITE
    """
    # -bouns if checked
    v -= 50 if board.is_check() else 0

    # bouns for mobility
    if not endgame:
        v += board.legal_moves.count()
    else:
        v += board.legal_moves.count() * 2
    
    # -bouns for number of doubled pawns
    v -= pawns_doubled(board, chess.WHITE) * 16

    """
    BLACK
    """   
    # -bouns if checked
    v += 50 if board.is_check() else 0

    # bouns for mobility
    if not endgame:
        v -= board.legal_moves.count()
    else:
        v -= board.legal_moves.count() * 2

    # -bouns for number of doubled pawns
    v += pawns_doubled(board, chess.BLACK) * 16

    return v


def piece_value(piece):
    """
    Given a piece this function returns its value
    """
    return piece_values[piece.piece_type]


def pawns_doubled(board, color):
    """
    Returns number of pawns that are doubled and open
    """
    last_pawn_rank = set(range(48, 56)) if color else set(range(8, 16))

    pawns = board.pieces(chess.PAWN, color)
    doubled = 0

    for s in pawns:
        cur_s = s
        while(cur_s not in last_pawn_rank):
            check_s = cur_s + 8 if color else cur_s - 8
            if check_s in pawns:
                doubled += 1
            cur_s = check_s

    return doubled


def hanging(board, square, piece, piece_map):
    """
    Returns value if piece is attacked and has no defenders
    """
    defender_squares = defenders(board, square, piece, piece_map)
    d_count = len(defender_squares)
    attacker_squares = board.attackers(not piece.color, square)
    a_count = len(attacker_squares)
    if d_count < a_count:
        a = 0
        d = 0
        for s in defender_squares:
            piece = board.piece_at(s)
            if piece.piece_type != chess.KING:
                d += 1 / piece_value(piece)
            else:
                d += 1 / 9000
        for s in attacker_squares:
            piece = board.piece_at(s)
            if piece.piece_type != chess.KING:
                a += 1 / piece_value(piece)
            else:
                a += 1 / 9000
    return 0


def defenders(board, square, piece, piece_map):
    """
    Returns square set of defenders to a given square
    """
    defenders = set()
    for s in piece_map:
        if piece_map[s].color == piece.color:
            piece_d_squares = board.attacks(s)
            if square in piece_d_squares:
                defenders.add(s)
    
    return defenders


def piece_square_value(board, square, piece, endgame):
    """
    Returns a value given the piece and square its on
    Square values range from (0 - 63) [a1 value, ..., h8 value]
    """
    v = 0

    piece_index = [chess.PAWN, chess.KNIGHT, chess.BISHOP, 
                    chess.ROOK, chess.QUEEN, chess.KING]

    i = piece_index.index(piece.piece_type)

    if piece.color:
        if piece.piece_type == chess.KING and endgame:
            return king_endgame[square]
        return pieces_square_table[i][square]
    else: 
        if piece.piece_type == chess.KING and endgame:
            return king_endgame[chess.square_mirror(square)]
        return pieces_square_table[i][chess.square_mirror(square)]

    return v


def game_phase(board, piece_map):
    """
    Returns a number according to the game phase, 0 being endgame
    """
    middle_game_limit = 15258 
    end_game_limit = 3915

    # non pawn material value
    npm = 0
    for s in piece_map:
        if piece_map[s].symbol() not in ['p', 'P']:
            npm += piece_value(piece_map[s])

    npm = max(end_game_limit, min(npm, middle_game_limit))

    return ((npm - end_game_limit) * 128) / (middle_game_limit - end_game_limit)


def filtered_pieces(board, piece_map):
    """
    Returns white, black and attacked pieces and their squares
    """
    tense = dict()
    white = dict()
    black = dict()
    for s in piece_map:
        piece = piece_map[s]
        if piece.color:
            white[s] = piece
        else:
            black[s] = piece
        if board.is_attacked_by(not piece.color, s):
            tense[s] = piece
    return [white, black, tense]


def filtered_moves(board):
    moves = set()
    for move in board.legal_moves:
        pos = move_result(board, move)

        piece_map = pos.piece_map()
        filtered_piece_map = filtered_pieces(pos, piece_map)
        tense_pieces = filtered_piece_map[2]

        any_hanging = False

        for s in piece_map:
            piece = piece_map[s]
            if piece.color == board.turn:
                if len(defenders(pos, s, piece, piece_map)) == 0 and pos.is_attacked_by(not piece.color, s):
                    any_hanging = True
                    break

        if not any_hanging:
            moves.add(move)

    return moves


def move_result(board, move):
    """
    Returns a board after a move is made
    """
    b = board.copy()
    b.push(move)
    return b