from C4T import ConnectFourTwist

def test_circular_horizontal():
    turn = random.randint(0, 1)
    game = ConnectFourTwist(turn)
    turn = random.randint(PLAYER, AI)
    board = game.get_board()

    game, turn = turn_drop_token(0, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)

    game, turn = turn_drop_token(1, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)

    game, turn = turn_drop_token(5, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)

    game, turn = turn_drop_token(4, game, turn, PLAYER_PIECE, board)
    game.score_position(board, PLAYER_PIECE)

    if game.winning_move(board, 1):
            game.set_game_over(True)
            game.set_winner("1")

    if game.get_game_over():
            print("GAME OVER")
            print(f"Winner is {game.get_winner()}")

def test_lru_win():
    turn = random.randint(0, 1)
    game = ConnectFourTwist(turn)

    board = game.get_board()

    game, turn = turn_drop_token(0, game, turn, 1, board)
    game, turn = turn_drop_token(1, game, turn, 2, board)
    game, turn = turn_drop_token(1, game, turn, 1, board)
    game, turn = turn_drop_token(2, game, turn, 2, board)
    game, turn = turn_drop_token(2, game, turn, 2, board)
    game, turn = turn_drop_token(2, game, turn, 1, board)
    game, turn = turn_drop_token(3, game, turn, 2, board)
    game, turn = turn_drop_token(3, game, turn, 2, board)
    game, turn = turn_drop_token(3, game, turn, 2, board)
    game, turn = turn_drop_token(3, game, turn, 1, board)

    if game.winning_move(board, 1):
            game.set_game_over(True)
            game.set_winner("1")

    if game.get_game_over():
            print("GAME OVER")
            print(f"Winner is {game.get_winner()}")

def test_lrd_win():
    turn = random.randint(0, 1)
    game = ConnectFourTwist(turn)

    board = game.get_board()

    game, turn = turn_drop_token(3, game, turn, 1, board)
    game, turn = turn_drop_token(2, game, turn, 2, board)
    game, turn = turn_drop_token(2, game, turn, 1, board)
    game, turn = turn_drop_token(1, game, turn, 2, board)
    game, turn = turn_drop_token(1, game, turn, 2, board)
    game, turn = turn_drop_token(1, game, turn, 1, board)
    game, turn = turn_drop_token(0, game, turn, 2, board)
    game, turn = turn_drop_token(0, game, turn, 2, board)
    game, turn = turn_drop_token(0, game, turn, 2, board)
    game, turn = turn_drop_token(0, game, turn, 1, board)