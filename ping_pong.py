"""File contains main class with game logic"""

import numpy as np
import random


class PongPin:
    def __init__(self, matrix_size=(15, 20)):
        self.matrix_size = matrix_size
        self.direction = 0
        self.pl_size = 3
        self.racquet_1 = [0, 0 + self.matrix_size[0] // 2 - self.pl_size]
        self.racquet_2 = [-1, 0 + self.matrix_size[0] // 2 - self.pl_size]
        self.ball = [i // 2 for i in self.matrix_size]
        self.ball_dir = random.randint(0, 5)

        self.matrix = self.render_matrix()

    def render_matrix(self):
        """Fill matrix by positions of 2 rockets and ball
        racquet_1 :1
        racquet_2 :2
        ball :3
        """
        self.matrix = np.zeros(self.matrix_size)
        start = self.racquet_1[1]
        start_2 = self.racquet_2[1]
        self.matrix[start:start + self.pl_size, :1] = 1
        self.matrix[start_2:start_2 + self.pl_size, -1:] = 2
        self.matrix[self.ball[0]][self.ball[1]] = 3
        return self.matrix

    def move(self, direction: int, racquet=None):
        """Changes rocket position
        direction up: 0
        direction down: 1
        """
        if racquet is None:
            racquet = self.racquet_1

        # Move player up
        if direction == 0:
            if racquet[1] - 1 >= 0:
                racquet[1] -= 1
        # Move player down
        elif direction == 1:
            if racquet[1] + self.pl_size + 1 <= self.matrix_size[0]:
                racquet[1] += 1

    def robot_play(self, racquet=None):
        """Automatic move rocket closer to ball"""
        if racquet is None:
            racquet = self.racquet_2

        # Excludes the hit of the ball by the center of the racket every time
        center_player = random.randint(racquet[1], racquet[1] + self.pl_size - 1)

        if center_player < self.ball[0]:
            self.move(1, racquet)
        elif center_player > self.ball[0]:
            self.move(0, racquet)

    def ball_move(self):
        """Moves the ball in accordance with its direction"""

        ball_y, ball_x = self.ball
        matrix_y = self.matrix_size[0]
        # up right
        if self.ball_dir == 0:
            nex_pos = ball_y - 1, ball_x + 1
            if nex_pos[0] < 0:
                self.ball_dir = 1
                self.ball_move()
            else:
                self.ball = nex_pos

        # down right
        elif self.ball_dir == 1:
            nex_pos = ball_y + 1, ball_x + 1
            if nex_pos[0] >= matrix_y:
                self.ball_dir = 0
                self.ball_move()
            else:
                self.ball = nex_pos
        # up left
        elif self.ball_dir == 2:
            nex_pos = ball_y - 1, ball_x - 1
            if nex_pos[0] < 0:
                self.ball_dir = 3
                self.ball_move()
            else:
                self.ball = nex_pos
        # down left
        elif self.ball_dir == 3:
            nex_pos = ball_y + 1, ball_x - 1
            if nex_pos[0] >= matrix_y:
                self.ball_dir = 2
                self.ball_move()
            else:
                self.ball = nex_pos
        # right straight
        elif self.ball_dir == 4:
            self.ball = ball_y, ball_x + 1
        # left straight
        elif self.ball_dir == 5:
            self.ball = ball_y, ball_x - 1

    def collide(self):
        """Check collides ball with raquet and returns reward"""
        ball_y, ball_x = self.ball
        y1, y2, y3 = range(self.racquet_1[1], self.racquet_1[1] + self.pl_size)
        z1, z2, z3 = range(self.racquet_2[1], self.racquet_2[1] + self.pl_size)
        if ball_x == 1:
            if ball_y == y1:
                self.ball_dir = 0
                return 1
            elif ball_y == y2:
                self.ball_dir = 4
                return 1
            elif ball_y == y3:
                self.ball_dir = 1
                return 1
            else:
                return -10

        elif ball_x == self.matrix_size[1] - 2:
            if ball_y == z1:
                self.ball_dir = 2
            elif ball_y == z2:
                self.ball_dir = 5
            elif ball_y == z3:
                self.ball_dir = 3

        return 0

    def check_alive(self):
        ball_x = self.ball[1]
        if ball_x < 1 or ball_x >= self.matrix_size[1] - 1:
            return False
        return True

    def play_game(self):
        alive = self.check_alive()
        reward = 0
        if alive:
            self.robot_play()
            self.robot_play(self.racquet_1)
            reward = self.collide()
            self.ball_move()
            self.render_matrix()

        return alive, reward


if __name__ == '__main__':
    pong = PongPin((15, 20))
    run = True
    cnt = 0
    while run:
        run, reward = pong.play_game()
        print(pong.matrix, '\n')
        cnt += 1
        if cnt > 100:
            break
