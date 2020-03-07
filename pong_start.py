"""Ping Pong AI test"""
import os
import pickle
from ping_pong_ai.ping_pong import PongPin
from ping_pong_ai.game_anim import GameDrawer
from ping_pong_ai.eval_pong import get_move


def run_game(pong, game_draw, controller):
    cnt = 0
    run = True
    while run:
        inputs = list(pong.ball) + pong.racquet_1 + [pong.ball_dir]
        action = controller.activate(inputs)
        force = get_move(action)
        pong.robot_play()
        pong.move(force)
        pong.collide()
        pong.ball_move()
        pong.render_matrix()
        run = pong.check_alive()
        cnt += 1
        game_draw.draw_players(pong.matrix)
        cnt += 1
        if cnt > 5000:
            run = False
            game_draw.end_game()


if __name__ == '__main__':
    pong = PongPin((15, 20))
    game_draw = GameDrawer((20, 15), fps=15)

    file = 'winner-feedforward'
    file_name = os.path.join(os.getcwd(), 'pkl', file)
    controller = pickle.load(open(file_name, 'rb'))

    run_game(pong, game_draw, controller)
