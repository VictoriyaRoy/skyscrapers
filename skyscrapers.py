'''
Solve the problem of skyscrapers game
github: https://github.com/VictoriyaRoy/skyscrapers
'''

def read_input(path: str) -> list:
    """
    Read game board file from path.
    Return list of str.
    """
    with open(path, mode = 'r', encoding = 'utf-8') as file:
        board = file.read().split('\n')
    return board


def left_to_right_check(input_line: str, pivot: int) -> bool:
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    check_number = input_line[pivot]
    for element in input_line[1:pivot]:
        if element >= check_number:
            return False
    return True


def check_not_finished_board(board: list) -> bool:
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', \
        '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', \
        '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', \
        '*35214*', '*41532*', '*2*1***'])
    False
    """
    for line in board:
        if '?' in line:
            return False
    return True


def check_uniqueness_in_rows(board: list) -> bool:
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', \
        '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', \
        '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', \
        '*35214*', '*41532*', '*2*1***'])
    False
    """
    for line in board[1:-1]:
        if len(set(line[1:-1])) != len(line[1:-1]):
            return False
    return True


def check_horizontal_visibility(board: list) -> bool:
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', \
        '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', \
        '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', \
        '*35214*', '*41532*', '*2*1***'])
    False
    """
    for line in board[1:-1]:
        check = line[0]
        if check != '*':
            count = 0
            for element in line[1:-1]:
                if left_to_right_check(line, int(element)):
                    count += 1
            if count != int(check):
                return False

        check = line[-1]
        if check != '*':
            count = 0
            for element in line[1:-1]:
                if left_to_right_check(line[::-1], int(element)):
                    count += 1
            if count != int(check):
                return False
    return True


def check_columns(board: list) -> bool:
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height)
    and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    length = len(board)
    new_board = ['' for i in range(length)]
    for line in board:
        for index, element in enumerate(line):
            new_board[index] += element
    return check_horizontal_visibility(new_board) and check_uniqueness_in_rows(new_board)


def check_skyscrapers(input_path: str) -> bool:
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.
    """
    board = read_input(input_path)
    if check_not_finished_board(board) and check_uniqueness_in_rows(board):
        if check_horizontal_visibility(board) and check_columns(board):
            return True
    return False


if __name__ == "__main__":
    print(check_skyscrapers('check.txt'))
