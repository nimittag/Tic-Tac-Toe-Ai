from project import make_move, move_isvalid, check_won, get_ai_move, check_tie

def test_make_move():
    empty_board = [["#"] * 3 for _ in range(3)]
    assert make_move(empty_board, "X", 0, 0) == [["X","#","#"], ["#","#","#"], ["#","#","#"]]


def test_move_isvalid():
    empty_board = [["#"] * 3 for _ in range(3)]
    non_empty_board = [["X","#","#"], ["#","#","#"], ["#","#","#"]]
    assert move_isvalid(non_empty_board, 0, 0) == False
    assert move_isvalid(empty_board, 0, 0) == True


def test_check_won():
    winning_board1 = [["X","X","X"], ["#","#","#"], ["#","#","#"]]
    winning_board2 = [["X","#","#"], ["X","#","#"], ["X","#","#"]]
    winning_board3 = [["X","#","#"], ["#","X","#"], ["#","#","X"]]
    winning_board4 = [["#","#","X"], ["#","X","#"], ["X","#","#"]]

    not_winning_board = [["X","#","X"], ["#","#","#"], ["#","#","#"]]

    assert check_won(winning_board1) == (True, "X")
    assert check_won(winning_board2) == (True, "X")
    assert check_won(winning_board3) == (True, "X")
    assert check_won(winning_board4) == (True, "X")
    assert check_won(not_winning_board) == (False, None)

def test_check_tie():
    tied_board = [["X","X","O"], ["O","O","X"], ["X","X","O"]]
    non_tied_board = [["X","X","O"], ["O","O","X"], ["X","X","#"]]

    assert check_tie(tied_board) == True
    assert check_tie(non_tied_board) == False


# AI-Tests-------------------------------------------

def test_randobot():
    l = 1
    almost_full_board = [["X","X","X"], ["X","#","X"], ["X","X","X"]]
    almost_empty_board = [["X","#","#"], ["#","#","#"], ["#","#","#"]]

    assert get_ai_move(almost_full_board, "O", l) == (1,1)
    assert get_ai_move(almost_empty_board, "O", l) != (0,0)

def test_winobot():
    l = 2
    almost_winning_board1 = [["O","O","#"], ["#","#","#"], ["#","#","#"]]
    almost_winning_board2 = [["O","#","#"], ["O","#","#"], ["#","#","#"]]
    almost_winning_board3 = [["O","#","#"], ["#","O","#"], ["#","#","#"]]
    almost_winning_board4 = [["#","#","O"], ["#","O","#"], ["#","#","#"]]

    assert get_ai_move(almost_winning_board1, "O", l) == (0,2)
    assert get_ai_move(almost_winning_board2, "O", l) == (2,0)
    assert get_ai_move(almost_winning_board3, "O", l) == (2,2)
    assert get_ai_move(almost_winning_board4, "O", l) == (2,0)

def test_defendobot():
    l = 3
    almost_losing_board1 = [["X","X","#"], ["#","#","#"], ["#","#","#"]]
    almost_losing_board2 = [["X","#","#"], ["X","#","#"], ["#","#","#"]]
    almost_losing_board3 = [["X","#","#"], ["#","X","#"], ["#","#","#"]]
    almost_losing_board4 = [["#","#","X"], ["#","X","#"], ["#","#","#"]]

    assert get_ai_move(almost_losing_board1, "O", l) == (0,2)
    assert get_ai_move(almost_losing_board2, "O", l) == (2,0)
    assert get_ai_move(almost_losing_board3, "O", l) == (2,2)
    assert get_ai_move(almost_losing_board4, "O", l) == (2,0)

def test_minimax():
    l = 4

    empty_board = [["#","#","#"], ["#","#","#"], ["#","#","#"]]
    assert get_ai_move(empty_board, "X", l) == (0,0)

    almost_winning_board = [["X","X","#"], ["#","#","#"], ["#","#","#"]]
    assert get_ai_move(almost_winning_board, "X", l) == (0,2)

    almost_losing_board = [["O","O","#"], ["#","#","#"], ["#","#","#"]]
    assert get_ai_move(almost_losing_board, "X", l) == (0,2)

    center_filled_board = [["#","#","#"], ["#","O","#"], ["#","#","#"]]
    move = get_ai_move(center_filled_board, "X", l)
    assert move in [(0,0),(0,2),(2,0),(2,2)]

    almost_full_board = [["X","#","X"], ["O","O","X"], ["O","X","O"]]
    move = get_ai_move(almost_full_board, "X", l)
    assert almost_full_board[move[0]][move[1]] == "#"

    bookmove_board = [["X","#","#"], ["#","O","#"], ["#","#","#"]]
    assert get_ai_move(bookmove_board, "X", l) == (2,2)
