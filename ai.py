import math
import random
import copy

from user import User
from slot import Slot


class AI(User):

    DEFAULT_MOVE_TIME = 400
    DEFAULT_DROP_TIME = 400
    DEFAULT_THINK_TIME = 400
    DEPTH = 5
    SCORE_DECAY_RATE = 0.5
    CENTER_WEIGHT = 0.75
    ENEMY_ONE_AWAY_WEIGHT = 1
    AI_ONE_AWAY_WEIGHT = 1.25
    WIN_WEIGHT = 25

    def __init__(self, game, color, win_color):
        User.__init__(self, game, color, win_color)
        
        self.move_time = self.DEFAULT_MOVE_TIME
        self.drop_time = self.DEFAULT_DROP_TIME
        self.think_time = self.DEFAULT_THINK_TIME
        
    def set_speed(self, speed):
        self.move_time = speed
        self.drop_time = speed
        self.think_time = speed
        
    def reset_speed(self):
        self.move_time = self.DEFAULT_MOVE_TIME
        self.drop_time = self.DEFAULT_DROP_TIME
        self.think_time = self.DEFAULT_THINK_TIME

    def get_piece_sequence_score(self, sequence):
        score = 0
        
        ai_piece_count = sequence.count(self.color)
        enemy_piece_count = sequence.count(self.game.get_other_color(self.color))
        empty_count = sequence.count(Slot.EMPTY_COLOR)
        
        highest_score = self.game.connect_amount * self.WIN_WEIGHT

        if ai_piece_count == self.game.connect_amount:
            score += highest_score

        ai_one_away_points = self.game.connect_amount * self.AI_ONE_AWAY_WEIGHT

        for check in range(1, self.game.connect_amount - 1):

            if ai_piece_count == self.game.connect_amount - check \
                    and empty_count == check:

                score += ai_one_away_points \
                         * self.SCORE_DECAY_RATE ** (check - 1)

        if enemy_piece_count == self.game.connect_amount - 1 \
                and empty_count == 1:
            score -= self.game.connect_amount * self.ENEMY_ONE_AWAY_WEIGHT

        return score

    def score_position(self, board):
        score = 0
        center_colors = []

        for start_row in range(board.rows - self.game.connect_amount + 1):
            center_column = board.center_column()
            last_row_ind = start_row + self.game.connect_amount

            for r in board.colors[start_row: last_row_ind]:
                center_colors.append(r[center_column])

                if board.columns % 2 == 0:
                    center_colors.append(r[center_column - 1])

        center_count = center_colors.count(self.color)
        score += center_count * self.game.connect_amount * self.CENTER_WEIGHT

        for r in range(board.rows):
            row_colors = board.colors[r]

            for c in range(board.columns - self.game.connect_amount + 1):
                sequence = row_colors[c: c + self.game.connect_amount]
                score += self.get_piece_sequence_score(sequence)

        for c in range(board.columns):
            column_colors = [board.colors[r][c] for r in range(board.rows)]

            for r in range(board.rows - self.game.connect_amount + 1):
                sequence = column_colors[r: r + self.game.connect_amount]
                score += self.get_piece_sequence_score(sequence)

        for r in range(board.rows - self.game.connect_amount + 1):

            for c in range(board.columns - self.game.connect_amount + 1):
                sequence = [board.colors[r + shift][c + shift]
                            for shift in range(self.game.connect_amount)]
                score += self.get_piece_sequence_score(sequence)

        for r in range(board.rows - self.game.connect_amount + 1):

            for c in range(board.columns - self.game.connect_amount + 1):
                sequence = [board.colors[r + self.game.connect_amount - 1 - shift]
                    [c + shift] for shift in range(self.game.connect_amount)]
                score += self.get_piece_sequence_score(sequence)

        return score

    def get_best_column(self, board, ai_score, enemy_score, is_self_turn, depth):
        open_columns = board.get_open_columns()

        if depth == 0:
            return None, self.score_position(board)

        if board.has_piece_been_played():
            game_has_been_won = board.has_last_move_won_game(
                self.game.connect_amount)

            if game_has_been_won and is_self_turn:
                return None, -math.inf

            if game_has_been_won and not is_self_turn:
                return None, math.inf

            if len(open_columns) == 0:
                return None, 0

        if is_self_turn:
            max_score = -math.inf
            chosen_column = random.choice(open_columns)

            for open_column in open_columns:
                board_copy = copy.deepcopy(board)
                board_copy.drop_piece_in_column(open_column, self.color)
                ai_score_from_column = self.get_best_column(
                    board_copy, ai_score, enemy_score, False, depth - 1)[1]

                if ai_score_from_column > max_score:
                    max_score = ai_score_from_column
                    chosen_column = open_column

                ai_score = max(ai_score, max_score)

                if ai_score >= enemy_score:
                    break

            return chosen_column, max_score

        else:
            min_score = math.inf
            chosen_column = random.choice(open_columns)

            for open_column in open_columns:
                board_copy = copy.deepcopy(board)
                board_copy.drop_piece_in_column(
                    open_column, self.game.get_other_color(self.color))
                enemy_score_from_column = self.get_best_column(
                    board_copy, ai_score, enemy_score, True, depth - 1)[1]
                
                if enemy_score_from_column < min_score:
                    min_score = enemy_score_from_column
                    chosen_column = open_column

                enemy_score = min(enemy_score, min_score)

                if ai_score >= enemy_score:
                    break

            return chosen_column, min_score

    def initiate_turn(self):
        self.game.disable_player_input()
        self.game.change_wait_symbol_state('normal')
        self.game.app.update()
        self.game.app.after(self.think_time, self.game.app.update_idletasks())
        column_played = self.get_best_column(
            self.game.board, -math.inf, math.inf, True, self.DEPTH)[0]
        self.game.change_wait_symbol_state('hidden')
        self.game.move_drop_piece_to_column(
            column_played, move_time=self.move_time)
        self.game.app.after(self.drop_time, self.game.drop_piece())
        self.game.app.update_idletasks()
