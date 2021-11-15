import random as random
import time as time
import copy as copy


def brute_random(board_input, board_ver, board_hor, impossible, check_knight, check_king):
    for y in range(board_ver):
        for x in range(board_hor):
            if board_input[y][x] == "?":
                print("")
                num = [1,2,3,4,5,6,7,8,9]
                random.shuffle(num)
                works, num_int = check_rules(board_input, x, y, num, check_knight, check_king)
                if works != False:
                    board_input[y][x] = num_int
                else:
                    impossible = True
                    # print("{} at {}:{} didn't work".format(num_int, y, x)) # debug line
                    return board_input, impossible

    return board_input, impossible


def brute_check(board_input, board_ver, board_hor, tries, check_knight, check_king):
    finished = False
    impossible = False
    while not finished:
        check = False
        for y in range(board_ver):
            for x in range(board_hor):
                if board_input[y][x] == "?":
                    check = True
        if check:
            board_input, impossible = brute_random(board_input, board_ver, board_hor, impossible, check_knight, check_king)
        else:
            finished = True

        tries -= 1

        if tries < 1:
            break

        if impossible:
            # print("Board impossible...") # debug line
            return board_input

    return board_input


def check_done(board_input, board_ver, board_hor):
    finished = True
    for y in range(board_ver):
        for x in range(board_hor):
            if board_input[y][x] == "?":
                finished = False
                break

    return finished


def check_unplaced(board_input, board_ver, board_hor):
    amount = 0
    for y in range(board_ver):
        for x in range(board_hor):
            if board_input[y][x] == "?":
                amount += 1

    return amount


def check_board_logic(board_input, board_ver, board_hor, check_knight, check_king):
    for y in range(board_ver):
        for x in range(board_hor):
            if board_input[y][x] != "?":
                works, num_int = check_rules(board_input, x, y, [board_input[y][x]], check_knight, check_king)
                if not works:
                    return False

    return True


def check_rules(board_input, x, y, num, knight_check, king_check):
        for n in range(len(num)):
            block = True
            line = True
            knight = True
            king = True
            # print("For loop {}".format(num[n])) # debug line

            if x <= 2:
                x_block_min = 0
                x_block_max = 2
            elif x <= 5:
                x_block_min = 3
                x_block_max = 5
            else:
                x_block_min = 6
                x_block_max = 8

            if y <= 2:
                y_block_min = 0
                y_block_max = 2
            elif y <= 5:
                y_block_min = 3
                y_block_max = 5
            else:
                y_block_min = 6
                y_block_max = 8

            #Check for num in block
            for j in range(y_block_min, y_block_max+1):
                for i in range(x_block_min, x_block_max+1):
                    if board_input[j][i] == num[n] and not (j == y and i == x):
                        block = False
                        # print("{} found in block. ymin{} ymax{} xmin{} xmax{} j{} i{} x{} y{}".format(num[n], y_block_min, y_block_max, x_block_min, x_block_max, j, i, x ,y)) # debug line

            #Check for n in row
            for j in range(9):
                if board_input[y][j] == num[n] and (j != x):
                    line = False
                    # print("{} found in y line j{}".format(num[n], j)) # debug line

            for j in range(9):
                if board_input[j][x] == num[n] and (j != y):
                    line = False
                    # print("{} found in x line j{}".format(num[n], j)) # debug line

            if knight_check:
                x_knight_min = 0
                x_knight_max = 0
                y_knight_min = 0
                y_knight_max = 0

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
                        if board_input[j][i] == num[n] and not (j == y and i == x):
                            king = False
                            # print("{} found in block. ymin{} ymax{} xmin{} xmax{} j{} i{} x{} y{}".format(num[n], y_king_min, y_king_max, x_king_min, x_king_max, j, i, x ,y)) # debug line

            if block and line and knight and king:
                return True, num[n]

        return False, "Nothing"


def print_board(board_input, board_hor, board_ver):
    print("")
    for y in range(board_ver):
        for x in range(board_hor):
            print(board_input[y][x], end= "")
        print("")


runs = 0
lowest = 1000;
running = True
start_time = time.time()
logic = True;

size_h = 9
size_v = 9
board_orig = [
        [1,"?",4,"?","?","?","?",5,"?"],
        [6,"?",5,"?","?",9,"?","?",2],
        ["?","?","?","?","?","?","?",9,8],
        [8,"?","?",6,"?","?",9,"?","?"],
        [5,2,9,"?","?","?","?","?","?"],
        ["?","?","?",8,"?",7,"?",1,"?"],
        ["?",4,7,"?",6,"?","?","?",1],
        ["?","?","?","?",5,"?",3,8,"?"],
        [2,"?","?",7,1,"?","?","?","?"]
        ]


logic = check_board_logic(board_orig, 9, 9, False, False)
runs_max = 10000000
while running and logic and runs < runs_max:
    board = copy.deepcopy(board_orig)
    print("")
    print("Bruting from scratch... {}/{}".format(runs, runs_max))

    board = brute_check(board, 9, 9, 100000000, False, False)

    # print("NEW")
    # print_board(board, 9, 9) # Debug line

    unplaced = check_unplaced(board, 9, 9)
    print("Unplaced figures: {}.0".format(unplaced)) # debug line
    if unplaced < lowest:
        lowest = unplaced

    running = not check_done(board, 9, 9)
    runs += 1
    print("Lowest unplaced figures: {}".format(lowest)) # debug line


if not running:
    print_board(board, 9, 9)
    print("This solution works")
elif not logic:
    print("The sudoku is unsolvable...")
else:
    print("I gave up...")

s = time.time() - start_time
m, s = divmod(s, 60)
print("--- {} minutes {} seconds ---".format(m, s))

