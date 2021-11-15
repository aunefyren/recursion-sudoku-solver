import time as time
import copy as copy
import sys as sys


# Returns the number of cells that have unknown values.
def check_unplaced(board_input):
    amount = 0
    for y in range(board_ver):
        for x in range(board_hor):
            if board_input[y][x] == "?":
                amount += 1

    return amount


# Checks placed numbers in relation to other placed numbers, returning false if the board is invalid.
def check_board_logic():
    for y in range(board_ver):
        for x in range(board_hor):
            if board[y][x] != "?":
                works = check_rules(y, x, board[y][x])
                if not works:
                    return False

    return True


# A recursive method, calling itself repeatedly, saving valid solutions to an array.
def check_board_recursion():
    global recursions
    global board
    global board_solved
    global solutions
    global logging
    global solutions_wanted
    global board_solutions

    if solutions_wanted <= solutions and solutions_wanted != 0:
        return

    for y in range(board_hor):
        for x in range(board_ver):
            if board[y][x] == "?":
                for n in range(1, 10):
                    if check_rules(y, x, n):
                        board[y][x] = n
                        recursions = recursions + 1
                        check_board_recursion()
                        if solutions_wanted <= solutions and solutions_wanted != 0:
                            return
                        board[y][x] = "?"
                return

    if check_unplaced(board) == 0:
        board_solved = copy.deepcopy(board)
        board_solutions.append(board_solved)
        solutions = solutions + 1
        if logging:
            print("Found one solution")
    return


# The rule checking method. Based on the settings it can check if a number fits
# into a board based on row, column, region, knight's move and king's move.
def check_rules(y, x, num):
    global logging
    global king_check
    global knight_check

    if x <= 2:
        x_reg_min = 0
        x_reg_max = 2
    elif x <= 5:
        x_reg_min = 3
        x_reg_max = 5
    else:
        x_reg_min = 6
        x_reg_max = 8

    if y <= 2:
        y_reg_min = 0
        y_reg_max = 2
    elif y <= 5:
        y_reg_min = 3
        y_reg_max = 5
    else:
        y_reg_min = 6
        y_reg_max = 8

    #Check for num in region
    for j in range(y_reg_min, y_reg_max+1):
        for i in range(x_reg_min, x_reg_max+1):
            if board[j][i] == num and not (j == y and i == x):
                if logging:
                    print("Can't place {} at y: {}, x: {} because of region".format(num, y, x)) # debug line
                return False

    #Check for num in row
    for j in range(9):
        if board[y][j] == num and (j != x):
            if logging:
                print("Can't place {} at y: {}, x: {} because of row".format(num, y, x)) # debug line
            return False

    #Check for num in column
    for j in range(9):
        if board[j][x] == num and (j != y):
            if logging:
                print("Can't place {} at y: {}, x: {} because of column".format(num, y, x)) # debug line
            return False

    if knight_check:
        if x > 1:
            x_left = x-2
        elif x > 0:
            x_left = x-1
        else:
            x_left = x

        if x < 7:
            x_right = x+2
        elif x < 8:
            x_right = x+1
        else:
            x_right = x

        if y > 1:
            y_left = y-2
        elif y > 0:
            y_left = y-1
        else:
            y_left = y

        if y < 7:
            y_right = y+2
        elif y < 8:
            y_right = y+1
        else:
            y_right = y

        #Check for num in knight's move
        for j in range(y_left, y_right+1):
            for i in range(x_left, x_right+1):
                if board[j][i] == num and not (j == y and i == x) and \
                        ((j == y+2 and (i == x+1 or i == x-1)) or
                         (j == y-2 and (i == x+1 or i == x-1)) or
                         (i == x+2 and (j == y+1 or j == y-1)) or
                         (i == x-2 and (j == y+1 or j == y-1))):
                    if logging:
                        print("Can't place {} at y: {}, x: {} because of knight's move".format(num, y, x)) # debug line
                    return False

    if king_check:
        if x > 0:
            x_king_min = x-1
        else:
            x_king_min = 0

        if x < 8:
            x_king_max = x+1
        else:
            x_king_max = 8

        if y > 0:
            y_king_min = y-1
        else:
            y_king_min = 0

        if y < 8:
            y_king_max = y+1
        else:
            y_king_max = 8

        #Check for num in kingsmove
        for j in range(y_king_min, y_king_max+1):
            for i in range(x_king_min, x_king_max+1):
                if board[j][i] == num and not (j == y and i == x):
                    if logging:
                        print("Can't place {} at y: {}, x: {} because of king's move.".format(num, y, x)) # debug line
                    return False

    return True


# Prints the given board with spacing and lines to represent a sudoku board.
def print_board(board_input):
    print("")
    for y in range(board_ver):
        print("_____________________________________")
        for x in range(board_hor):
            print("| {} ".format(board_input[y][x]), end= "")
        print("|")
    print("_____________________________________")


# Get the board from the user using input().
def get_board(board_input):
    global board_ver
    global board_hor

    for y in range(board_ver):
        for x in range(board_hor):
            current = False
            for j in range(board_ver):
                if current:
                    break
                print("_____________________________________")
                for i in range(board_hor):
                    if j == y and i == x:
                        current = True
                        break
                    print("| {} ".format(board_input[j][i]), end= "")
                print("|")
            print("_____________________________________")
            val = input("Enter the next value. Any number will be placed, 'x' exits the program, anything else will become an unknown value ('?')")

            if val == "x":
                exit();
            elif val.isnumeric():
                board_input[y][x] = int(val)
            else:
                board_input[y][x] = "?"
    return board_input


# The original board array
board_orig = [
    ["?","?","?","?","?","?","?","?","?"],
    ["?","?","?","?","?","?","?","?","?"],
    ["?","?","?","?","?","?","?","?","?"],
    ["?","?","?","?","?","?","?","?","?"],
    ["?","?","?","?","?","?","?","?","?"],
    ["?","?","?","?","?","?","?","?","?"],
    ["?","?","?","?","?","?","?","?","?"],
    ["?","?","?","?","?","?","?","?","?"],
    ["?","?","?","?","?","?","?","?","?"]
]

# Sudoku settings. Three settings are retrieved through input().
king = input("Using the king's move rule? y/n")
if king == "y":
    king_check = True
else:
    king_check = False

knight = input("Using the knight's move rule? y/n")
if knight == "y":
    knight_check = True
else:
    knight_check = False

wanted_solutions_string = input("How many solutions do you want if your sudoku is not complete? Any input but a number above 0 will provide all possible solutions.")
if wanted_solutions_string.isnumeric() and int(wanted_solutions_string) > 0:
    solutions_wanted = int(wanted_solutions_string)
else:
    solutions_wanted = 0

board_hor = 9
board_ver = 9
logging = False
stats = True


# Sudoku stats. Printed at the end if "stats" is enabled.
recursions = 0
start_time = time.time()
stop_time = time.time()
solutions = 0

# Sudoku logical varibales. These need to be declared for later use. The get_board() method is called here.
# Recursionlimit needed to be extended.
sys.setrecursionlimit(100000)
print("Please provide a sudoku:")
board_orig = get_board(board_orig)
board = copy.deepcopy(board_orig)
board_solved = copy.deepcopy(board_orig)
board_solutions = []

# Start the time for tracking recursion time.
start_time = time.time()

# The main execution of methods. First checks if the board is empty, then outputs results based on that.
if check_unplaced(board) > 0:
    if not check_board_logic():
        print_board(board)
        print("Unsolvable")
    else:
        print("Given sudoku break no rules. Solving sudoku...")
        check_board_recursion()
        if solutions < 1:
            print("Found no solutions...")
        else:
            for i in range(len(board_solutions)):
                print("")
                print("Solution {}:".format(i+1))
                print_board(board_solutions[i])
else:
    if check_board_logic():
        print_board(board)
        print("Solved correctly")
    else:
        print_board(board)
        print("Solved incorrectly")

# Stop tracking time.
stop_time = time.time()

# If stats are enabled these are printed.
if stats:
    print("")
    s = stop_time - start_time
    m, s = divmod(s, 60)
    print("Time: {} sec".format(s))
    print("Recursions: {}".format(recursions))
    print("Solutions wanted: {}".format(solutions_wanted))
    print("Solutions found: {}".format(solutions))
    print("King's move: {}".format(king_check))
    print("Knight's move: {}".format(knight_check))
