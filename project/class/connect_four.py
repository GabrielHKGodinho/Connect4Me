import random
import cv2

import opencv_function
import opencv_function as cv_f
import time
import math

import os

starter = 0

class Connect_Four():
    def __init__(self, log):
        self.log = log
        self.cv_object = cv_f.Opencv_Function()

    def new_board(self, board_width, board_height):
        return tuple(tuple(0 for _ in range(board_height)) for _ in range(board_width))

    def apply_move(self, board_state, move_x, side):
        move_y = 0
        for x in board_state[move_x]:
            if x == 0:
                break
            else:
                move_y += 1

        def get_tuples():
            for i in range(len(board_state)):
                if move_x == i:
                    temp = list(board_state[i])
                    temp[move_y] = side
                    yield tuple(temp)
                else:
                    yield board_state[i]

        return tuple(get_tuples())

    def available_moves(self, board_state):
        for x in range(len(board_state)):
            if any(y == 0 for y in board_state[x]):
                yield x

    def has_winning_line(self, line, winning_length):
        count = 0
        last_side = 0
        for x in line:
            if x == last_side:
                count += 1
                if count == winning_length:
                    return last_side
            else:
                count = 1
                last_side = x
        return 0

    def has_winner(self, board_state, winning_length):
        board_width = len(board_state)
        board_height = len(board_state[0])

        # Rows
        for x in range(board_width):
            winner = self.has_winning_line(board_state[x], winning_length)
            if winner != 0:
                return winner
        # Columns
        for y in range(board_height):
            winner = self.has_winning_line((i[y] for i in board_state), winning_length)
            if winner != 0:
                return winner

        # Diagonals
        diagonals_start = -(board_width - winning_length)
        diagonals_end = (board_width - winning_length)
        for d in range(diagonals_start, diagonals_end):
            winner = self.has_winning_line(
                (board_state[i][i + d] for i in range(max(-d, 0), min(board_width, board_height - d))),
                winning_length)
            if winner != 0:
                return winner
        for d in range(diagonals_start, diagonals_end):
            winner = self.has_winning_line(
                (board_state[i][board_height - i - d - 1] for i in range(max(-d, 0), min(board_width, board_height - d))),
                winning_length)
            if winner != 0:
                return winner

        return 0 

    def play_game(self, plus_player_function, minus_player_function, hard, board_width=7, board_height=6, winning_length=4, log = True):
        board_state = self.new_board(board_width, board_height)
        player_turn = 1

        p_bottom, cap = self.cv_object.prepare()

        if p_bottom == 1:
            countInitial = 0
            total = 0
            totalAux = 0
            board_state = [0] * 7
            #hard.stopMotores()
            for i in range(7):
                board_state[i] = [0] * 6
            while countInitial < 4:
                success, img = cap.read()
                contourimg = img.copy()
                if success:
                    x, y, w, h = self.cv_object.find_Board(img, contourimg)
                    positionsBlue = self.cv_object.find_Chess(img, contourimg, y, h, 0)
                    positionsYellow = self.cv_object.find_Chess(img, contourimg, y, h, 2)

                    for position in positionsBlue:
                        for i in range(0, 42):
                            if abs(position[0] - opencv_function.boardPositions[i][0]) <= 20 and abs(
                                    position[1] - opencv_function.boardPositions[i][1]) <= 20:
                                board_state[math.floor(i / 6)][5 - (i % 6)] = 1
                                total = total + 1

                    for position in positionsYellow:
                        for i in range(0, 42):
                            if abs(position[0] - opencv_function.boardPositions[i][0]) <= 20 and abs(
                                    position[1] - opencv_function.boardPositions[i][1]) <= 20:
                                board_state[math.floor(i / 6)][5 - (i % 6)] = -1
                                total = total + 1
                    print(str(total)+"  -  "+str(totalAux))
                    if total==totalAux:
                        countInitial = countInitial + 1
                    else:
                        countInitial = 0
                        totalAux = total
                    time.sleep(0.4)
                    total = 0

            if starter == 2:
                move = minus_player_function(board_state, -1)
                print("Coelho jogou na " + str(move))
                board_stateFic = self.apply_move(board_state, move, -1)
                #hard.startMotores()
                hard.jogada(move)
                #hard.stopMotores()
                winner = self.has_winner(board_stateFic, winning_length)
                if winner != 0:
                    print("COELHO TE HUMILHOU!")
                    return winner

            while True:
                success, img = cap.read()
                contourimg = img.copy()
                if success:
                    #cv2.imshow("Video", img)

                    x, y, w, h = self.cv_object.find_Board(img, contourimg)

                    positionsBlue = self.cv_object.find_Chess(img, contourimg, y, h, 0)

                    positionsYellow = self.cv_object.find_Chess(img, contourimg, y, h, 2)
                    # print(board_state)

                    pos = -2

                    quantidadeJogo = 0

                    for x in range(len(board_state)):
                        for y in range(len(board_state[0])):
                            if board_state[x][y] == 1:
                                quantidadeJogo = quantidadeJogo + 1

                    board_stateFic = [0] * 7
                    for i in range (7):
                        board_stateFic[i] = [0] * 6

                    # print("zerado")
                    # self.printboard(board_state)

                    quantidadeCam = 0

                    for position in positionsBlue:
                        for i in range (0,42):
                            if abs(position[0] - opencv_function.boardPositions[i][0]) <= 20 and abs(position[1] - opencv_function.boardPositions[i][1]) <= 20:
                                quantidadeCam = quantidadeCam + 1
                                board_stateFic[math.floor(i/6)][5-(i % 6)] = 1

                    for position in positionsYellow:
                        for i in range (0,42):
                            if abs(position[0] - opencv_function.boardPositions[i][0]) <= 20 and abs(position[1] - opencv_function.boardPositions[i][1]) <= 20:
                                board_stateFic[math.floor(i/6)][5-(i % 6)] = -1

                    # print(str(quantidadeJogo)+" + "+str(quantidadeCam))
                    if quantidadeCam > quantidadeJogo:
                        opencv_function.tests = opencv_function.tests + 1
                        if opencv_function.tests == 5:
                            pos = 1
                            board_state = board_stateFic
                    else:
                        opencv_function.tests = 0

                    time.sleep(0.4)

                    #cv2.imshow("Final", contourimg)

                    if pos == -2:
                        pass
                    else:
                        count = 0
                        time.sleep(2)
                        while count < 2:

                            # _avialable_moves = list(self.available_moves(board_state))
                            # if len(_avialable_moves) == 0:
                            #     if self.log:
                            #         print("No moves left, game ended a draw")
                            #     return 0.
                            if player_turn > 0:
                                # move = plus_player_function(board_state, 1, pos)
                                print("You played " )
                                count += 1
                                if self.log:
                                    self.printboard(board_state)
                                winner = self.has_winner(board_stateFic, winning_length)
                                if winner != 0:
                                    print("YOU WON!")
                                    return winner
                            else:
                                move = minus_player_function(board_state, -1)
                                print("Coelho jogou na "+str(move))
                                board_stateFic = self.apply_move(board_state, move, player_turn)
                                hard.jogada(move)
                                # time.sleep(2.0)
                                winner = self.has_winner(board_stateFic, winning_length)
                                if winner != 0:
                                    print("COELHO TE HUMILHOU!")
                                    return winner
                                count += 1

                            # if move not in _avialable_moves:
                            #     if self.log:
                            #         print("Illegal move ", move)
                            #     continue



                                # print("Can move position coordinate [O] : ", end = '')
                                # print(_avialable_moves)

                            # winner = self.has_winner(board_state, winning_length)
                            # if winner != 0:
                            #     if self.log:
                            #         if player_turn == 1:
                            #             print("We have a winner, side : O")
                            #         else:
                            #             print("We have a winner, side : X")
                            #
                            #     return winner
                            player_turn = -player_turn


                else:
                    break
                if cv2.waitKey(1) == ord('q'):
                    break
        else:
            pass

        cap.release()
        cv2.destroyAllWindows()

    def printboard(self, board_state):
        R_Max = 7
        C_Max = 6

        board = list(board_state)
        for i in range(R_Max):
            board[i] = list(board_state[i])
        
        for i in range(R_Max):
            for j in range(C_Max):
                if board[i][j] == 1:
                    board[i][j] = 'O'
                elif board[i][j] == -1:
                    board[i][j] = 'X'

        key1 = ''
        key2 = ''
        key3 = ''
        for x in range(0, R_Max):
            if x == R_Max - 1:
                key1 = "\n"
            print(" ---", end='{}'.format(str(key1)))
        for x in range(0, C_Max):
            key2 = ''
            key3 = ''
            print("|", end='')
            for y in range(0, R_Max):
                if board[y][C_Max - 1 - x] == 0:
                    print("  ", end = '')
                else:
                    print(" " + str(board[y][C_Max - 1 - x]), end='')
                if y == R_Max - 1:
                    key2 = "\n"
                print(" |", end='{}'.format(str(key2)))

            if x < R_Max:
                for y in range(0, R_Max):
                    if y == R_Max - 1:
                        key3 = "\n"
                    print(" ---", end='{}'.format(str(key3)))

    def real_player_opencv(self, board_state, _, pos):
        return pos

    def random_player(self, board_state, _):
        moves = list(self.available_moves(board_state))
        return random.choice(moves)

