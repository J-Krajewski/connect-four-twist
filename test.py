def test_circular_horizontal():

    game = ConnectFourTwist()
    turn = random.randint(PLAYER, AI)
    board = game.get_board()

    game, turn = turn_drop_token(0, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)

    game, turn = turn_drop_token(1, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)

    game, turn = turn_drop_token(5, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)

def test_circular_lru_diagonal():

    game = ConnectFourTwist()
    turn = random.randint(PLAYER, AI)
    board = game.get_board()

    game, turn = turn_drop_token(5, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)

    game, turn = turn_drop_token(0, game, turn, AI_PIECE, board)
    game.score_position(board, AI_PIECE)
    game, turn = turn_drop_token(0, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)

    game, turn = turn_drop_token(1, game, turn, AI_PIECE, board)
    game.score_position(board, AI_PIECE)
    game, turn = turn_drop_token(1, game, turn, AI_PIECE, board)
    game.score_position(board, AI_PIECE)
    game, turn = turn_drop_token(1, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)

    game, turn = turn_drop_token(2, game, turn, AI_PIECE, board)
    game.score_position(board, AI_PIECE)
    game, turn = turn_drop_token(2, game, turn, AI_PIECE, board)
    game.score_position(board, AI_PIECE)
    game, turn = turn_drop_token(2, game, turn, AI_PIECE, board)
    game.score_position(board, AI_PIECE)
    game, turn = turn_drop_token(2, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)

def test_rotation():
    game = ConnectFourTwist()
    turn = random.randint(PLAYER, AI)
    board = game.get_board()

    game, turn = turn_drop_token(5, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)
    
    game, turn = turn_drop_token(5, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)
    game = turn_rotate_board(0, "left", game, board)

    game, turn = turn_drop_token(5, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)
    game = turn_rotate_board(0, "right", game, board)

    game, turn = turn_drop_token(5, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)
    game = turn_rotate_board(0, "right", game, board)

    game, turn = turn_drop_token(5, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)
    game = turn_rotate_board(0, "right", game, board)
    