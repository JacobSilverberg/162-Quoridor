# Author: Jacob Silverberg
# Date: 8/4/2021
# Description: A class recreating the board game Quoridor. Players take turns either moving their pawn or
# placing a one square fence. First player to move their pawn into their opponent's final row wins the game.
# Pawns move according to Quoridor rules.

class QuoridorGame:
    """
    Quoridor game class containing all of the necessary methods to play the classic tabletop game.
    Player 1 makes the first move.
    Initialize the class object and use the following methods to play:
    move_pawn(player, tuple of coordinates) to move a pawn
    place_fence(player, 'h' or 'v' for direction, tuple of coordinates) to place a fence
    is_winner(player) to see if a player has won the game.
    """
    def __init__(self):
        """
        Initialize the following:
        Game over boolean
        Player turn boolean
        Player fence count
        Player starting coordinates
        Empty horizontal and vertical fence lists
        Game board list of lists
        """
        self._game_over = False
        self._player1_move = True
        self._player2_move = False
        self._player1_fences = 10
        self._player2_fences = 10
        self._player1_coords = [4, 0]
        self._player2_coords = [4, 8]
        self._h_fences = []
        self._v_fences = []
        self._board = \
            [[0, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 2, 0, 0, 0, 0]]

    def is_winner(self, player):
        """
        Check for winning pawn placement, update game over boolean if there is a winner.
        Can be called to determine if a player has won the game.
        """
        # player 1 win condition check
        if player == 1:
            if 1 in self._board[8]:
                self._game_over = True
                return True
            else:
                return False

        # player 2 win condition check
        elif player == 2:
            if 2 in self._board[0]:
                self._game_over = True
                return True
            else:
                return False

        # invalid player input returns False
        else:
            return False

    def move_pawn(self, player, coords):
        """
        Method for coordinating necessary steps to check for move legality and eventual pawn move.
        """
        # set coord variables for branching comparisons
        new_x_coord, new_y_coord = coords
        if player == 1:
            old_x_coord, old_y_coord = self._player1_coords
        elif player == 2:
            old_x_coord, old_y_coord = self._player2_coords
        # invalid player input, return False
        else:
            return False

        # check for completed game state
        if self._game_over is True:
            return False

        # check for move to current pawn location
        elif new_x_coord == old_x_coord and new_y_coord == old_y_coord:
            return False

        # check for correct player turn
        elif self.player_turn_check(player) is True:

            # vertical move
            if (old_y_coord + 1 == new_y_coord or old_y_coord - 1 == new_y_coord) and old_x_coord == new_x_coord:
                if self.vertical_move_check(player, coords) is True:
                    self.complete_pawn_move(player, coords)
                    return True
                else:
                    return False

            # horizontal move
            elif (old_x_coord + 1 == new_x_coord or old_x_coord - 1 == new_x_coord) and old_y_coord == new_y_coord:
                if self.horizontal_move_check(player, coords) is True:
                    self.complete_pawn_move(player, coords)
                    return True
                else:
                    return False

            # vertical jump
            elif (old_y_coord + 2 == new_y_coord or old_y_coord - 2 == new_y_coord) and old_x_coord == new_x_coord:
                if self.jump_vert_move_check(player, coords) is True:
                    self.complete_pawn_move(player, coords)
                    return True
                else:
                    return False

            # horizontal jump
            elif (old_x_coord + 2 == new_x_coord or old_x_coord - 2 == new_x_coord) and old_y_coord == new_y_coord:
                if self.jump_horiz_move_check(player, coords) is True:
                    self.complete_pawn_move(player, coords)
                    return True
                else:
                    return False

            # diagonal move
            elif (old_x_coord - 1 == new_x_coord or old_x_coord + 1 == new_x_coord) and (old_y_coord + 1 == new_y_coord or old_y_coord - 1 == new_y_coord):
                if self.diag_move_check(player, coords) is True:
                    self.complete_pawn_move(player, coords)
                    return True
                else:
                    return False

        # incorrect player turn return
        else:
            return False

    def complete_pawn_move(self, player, coords):
        """
        Process after legal move.
        Updates board state, player coordinates, checks for winner and iterates player turn.
        """
        self.update_board(player, coords)
        self.set_player_coords(player, coords)
        self.is_winner(player)
        self.player_turn_change()

    def diag_move_check(self, player, coords):
        """Check for diagonal move legality"""
        # set coord variables for comparisons
        new_x_coord, new_y_coord = coords
        if player == 1:
            old_x_coord, old_y_coord = self._player1_coords
        elif player == 2:
            old_x_coord, old_y_coord = self._player2_coords
        # invalid player input, return False
        else:
            return False

        # up rightward move
        if new_x_coord > old_x_coord and new_y_coord < old_y_coord:
            # check for right block
            if self._board[old_y_coord][old_x_coord + 1] != 0:
                if (old_x_coord + 2, old_y_coord) in self._v_fences and (old_x_coord + 1, old_y_coord) not in self._h_fences:
                    return True
                else:
                    return False

            # check for up block
            elif self._board[old_y_coord - 1][old_x_coord] != 0:
                if (old_x_coord, old_y_coord - 1) in self._h_fences and (new_x_coord, new_y_coord) not in self._v_fences:
                    return True
                else:
                    return False

        # down rightward move
        elif new_x_coord > old_x_coord and new_y_coord > old_y_coord:
            # check for right block
            if self._board[old_y_coord][old_x_coord + 1] != 0:
                if (old_x_coord + 2, old_y_coord) in self._v_fences and (old_x_coord + 1, old_y_coord + 1) not in self._h_fences:
                    return True
                else:
                    return False

            # check for down block
            elif self._board[old_y_coord + 1][old_x_coord] != 0:
                if (old_x_coord, old_y_coord + 2) in self._h_fences and (new_x_coord, new_y_coord) not in self._v_fences:
                    return True
                else:
                    return False

        # down leftward move
        elif new_x_coord < old_x_coord and new_y_coord > old_y_coord:
            # check for left block
            if self._board[old_y_coord][old_x_coord - 1] != 0:
                if (old_x_coord - 1, old_y_coord) in self._v_fences and (new_x_coord + 1, new_y_coord) not in self._h_fences:
                    return True
                else:
                    return False

            # check for down block
            elif self._board[old_y_coord + 1][old_x_coord] != 0:
                if (old_x_coord, old_y_coord + 2) in self._h_fences and (old_x_coord, old_y_coord + 1) not in self._v_fences:
                    return True
                else:
                    return False

        # up leftward move
        elif new_x_coord < old_x_coord and new_y_coord < old_y_coord:
            # check for left block
            if self._board[old_y_coord][old_x_coord - 1] != 0:
                if (old_x_coord - 1, old_y_coord) in self._v_fences and (old_x_coord - 1, old_y_coord) not in self._h_fences:
                    return True
                else:
                    return False

            # check for down block
            elif self._board[old_y_coord - 1][old_x_coord] != 0:
                if (old_x_coord, old_y_coord - 2) in self._h_fences and (old_x_coord, old_y_coord - 1) not in self._v_fences:
                    return True
                else:
                    return False

        # invalid move input
        else:
            return False

    def jump_horiz_move_check(self, player, coords):
        """Check for horizontal jumping move legality"""
        # set coord variables for comparisons
        new_x_coord, new_y_coord = coords
        if player == 1:
            old_x_coord, old_y_coord = self._player1_coords
        elif player == 2:
            old_x_coord, old_y_coord = self._player2_coords
        # invalid player input, return False
        else:
            return False

        # rightward jump - check if empty space right
        if old_x_coord < new_x_coord:
            if self._board[old_y_coord][old_x_coord + 1] == 0:
                return False
            else:
                if (new_x_coord, new_y_coord) in self._v_fences:
                    return False
                else:
                    return True

        # leftward jump - check if empty space left
        elif old_x_coord > new_x_coord:
            if self._board[old_y_coord][old_x_coord - 1] == 0:
                return False
            else:
                if (old_x_coord - 1, old_y_coord) in self._v_fences:
                    return False
                else:
                    return True
        else:
            return False

    def jump_vert_move_check(self, player, coords):
        """Check for vertical jumping move legality"""
        # set coord variables for comparisons
        new_x_coord, new_y_coord = coords
        if player == 1:
            old_x_coord, old_y_coord = self._player1_coords
        elif player == 2:
            old_x_coord, old_y_coord = self._player2_coords
        # invalid player input, return False
        else:
            return False

        # downward jump - check if empty space below
        if old_y_coord < new_y_coord:
            if self._board[old_y_coord + 1][old_x_coord] == 0:
                return False
            else:
                # check for fence collision
                if (old_x_coord, old_y_coord + 1) in self._h_fences:
                    return False
                else:
                    return True

        # upward jump - check if empty space above
        elif old_y_coord > new_y_coord:
            if self._board[old_y_coord - 1][old_x_coord] == 0:
                return False
            else:
                # check for fence collision
                if (old_x_coord, old_y_coord - 1) in self._h_fences:
                    return False
                return True

    def horizontal_move_check(self, player, coords):
        """Checks for horizontal move legality"""
        # set coord variables for comparisons
        new_x_coord, new_y_coord = coords
        if player == 1:
            old_x_coord, old_y_coord = self._player1_coords
        elif player == 2:
            old_x_coord, old_y_coord = self._player2_coords
        # invalid player input, return False
        else:
            return False

        # check for left move fence collision
        if old_x_coord - 1 == new_x_coord and old_y_coord == new_y_coord:
            if (old_x_coord, old_y_coord) in self._v_fences:
                return False
            # check for other pawn
            elif self._board[new_y_coord][new_x_coord] != 0:
                return False
            else:
                return True

        # check for right move fence collision
        elif old_x_coord + 1 == new_x_coord and old_y_coord == new_y_coord:
            if (new_x_coord, new_y_coord) in self._v_fences:
                return False
            # check for other pawn
            elif self._board[new_y_coord][new_x_coord] != 0:
                return False
            else:
                return True

        # no vertical walls in way
        else:
            return True

    def vertical_move_check(self, player, coords):
        """Checks for vertical move legality"""
        # set coord variables for comparisons
        new_x_coord, new_y_coord = coords
        if player == 1:
            old_x_coord, old_y_coord = self._player1_coords
        elif player == 2:
            old_x_coord, old_y_coord = self._player2_coords
        # invalid player input, return False
        else:
            return False

        # check for up move fence collision
        if old_y_coord - 1 == new_y_coord and old_x_coord == new_x_coord:
            if (old_x_coord, old_y_coord) in self._h_fences:
                return False
            # check for other pawn on intended space
            elif self._board[new_y_coord][new_x_coord] != 0:
                return False
            else:
                return True

        # check for down move fence collision
        elif old_y_coord + 1 == new_y_coord and old_x_coord == new_x_coord:
            if (new_x_coord, new_y_coord) in self._h_fences:
                return False
            # check for other pawn on intended space
            elif self._board[new_y_coord][new_x_coord] != 0:
                return False
            else:
                return True

        # no horizontal walls in way
        else:
            return True

    def set_player_coords(self, player, coords):
        """Set method for player coordinates"""
        if player == 1:
            self._player1_coords = coords
            return
        elif player == 2:
            self._player2_coords = coords
            return
        else:
            return

    def update_board(self, player, coords):
        """Updates board to represent new legal pawn positions"""
        # set coord variables for update
        new_x_coord, new_y_coord = coords
        if player == 1:
            old_x_coord, old_y_coord = self._player1_coords
        elif player == 2:
            old_x_coord, old_y_coord = self._player2_coords
        # invalid player input, return False
        else:
            return False

        # set old position to 0, new position to correct payer's pawn
        self._board[old_y_coord][old_x_coord] = 0
        if player == 1:
            self._board[new_y_coord][new_x_coord] = 1
        elif player == 2:
            self._board[new_y_coord][new_x_coord] = 2
        return

    def place_fence(self, player, direction, coords):
        """Method for placing a vertical or horizontal fence on the game board."""
        # check for correct player turn, player has fences, not a duplicate fence placement and game is not over
        new_x_coord, new_y_coord = coords
        if self.player_turn_check(player) is True and \
        self.fence_count_check(player) is True and \
        self.fence_duplicate_check(direction, coords) is True and \
        self._game_over is False:

            # direction check
            if direction == 'v':
                # check for edge out outside board placement
                if new_x_coord < 1 or new_x_coord > 8:
                    return False
                else:
                    # place fence, decrement fence total, change player turn
                    self._v_fences.append(coords)
                    self.fence_decrement(player)
                    self.player_turn_change()
                    return True

            elif direction == 'h':
                # check for edge or outside board placement
                if new_y_coord < 1 or new_y_coord > 8:
                    return False
                else:
                    # place fence, decrement fence total, change player turn
                    self._h_fences.append(coords)
                    self.fence_decrement(player)
                    self.player_turn_change()
                    return True

            # invalid direction input
            else:
                return False

        # player turn incorrect, no more fences or duplicate fence resulting in False
        else:
            return False

    def fence_decrement(self, player):
        """Decrement fence count of given player"""
        if player == 1:
            self._player1_fences -= 1
        elif player == 2:
            self._player2_fences -= 1
        else:
            return

    def fence_count_check(self, player):
        """Checks for remaining player fences"""
        # player 1 has fences left
        if player == 1 and self._player1_fences > 0:
            return True
        # player 2 has fences left
        elif player == 2 and self._player2_fences > 0:
            return True
        # player does not have fences left
        else:
            return False

    def fence_duplicate_check(self, direction, coords):
        """Checks for duplicate fences already played"""
        if direction == 'h':
            if coords in self._h_fences:
                return False
            else:
                return True
        elif direction == 'v':
            if coords in self._v_fences:
                return False
            else:
                return True
        else:
            return False

    def player_turn_change(self):
        """Change player turn"""
        # if player 1 move, set to player 2 move
        if self._player1_move is True:
            self._player1_move = False
            self._player2_move = True
            return
        # if player 2 move, set to player 1 move
        else:
            self._player1_move = True
            self._player2_move = False
            return

    def player_turn_check(self, player):
        """Checks for correct player turn"""
        if player == 1 and self._player1_move is True:
            return True
        elif player == 2 and self._player2_move is True:
            return True
        else:
            return False

    def print_board(self):
        """Print board pieces.  No fences right now."""
        print(self._board[0])
        print(self._board[1])
        print(self._board[2])
        print(self._board[3])
        print(self._board[4])
        print(self._board[5])
        print(self._board[6])
        print(self._board[7])
        print(self._board[8])
        return

    def fence_list(self):
        """Method for returning currently placed fences"""
        print(self._h_fences, "horiz fences")
        print(self._v_fences, "vert fences")
