"""Snake AI test"""

import pygame


class GameDrawer:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 255, 255)
    WIN_WIDTH = 800
    WIN_HEIGHT = 600
    pygame.init()
    game = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    def __init__(self, matrix_size, fps=20):
        self.mat_x, self.mat_y = matrix_size
        self.width, self.height = self.WIN_WIDTH / self.mat_x, self.WIN_HEIGHT / self.mat_y
        self.x_1 = 0
        self.x_2 = self.WIN_WIDTH - self.width
        self.fps = fps

    def draw_players(self, matrix):
        self.game.fill(self.BLACK)

        for ind_y, column in enumerate(matrix):
            y = ind_y * self.height
            for ind_x, row in enumerate(column):
                x = ind_x * self.width
                if row == 1:
                    pygame.draw.rect(self.game, self.BLUE, (self.x_1, y, self.width, self.height))

                elif row == 2:
                    pygame.draw.rect(self.game, self.BLUE, (self.x_2, y,
                                                            self.width, self.height))
                elif row == 3:
                    pygame.draw.rect(self.game, self.WHITE, (x, y, self.width, self.height))

        pygame.display.update()
        self.clock.tick(self.fps)

    def end_game(self):
        pygame.quit()
        return None


if __name__ == '__main__':
    from ping_pong import PongPin
    player = GameDrawer((20, 15), fps=20)

    pong = PongPin()

    run = True
    cnt = 0
    while run:
        run, reward = pong.play_game()
        player.draw_players(pong.matrix)
        cnt += 1
        if cnt >100:
            break
    print(cnt)
