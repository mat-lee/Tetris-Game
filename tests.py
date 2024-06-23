from ai import Config, directory_path, get_interpreter, load_best_model, MCTS
from game import Game

from collections import namedtuple
import matplotlib.pyplot as plt

def test_dirichlet_noise():
    # Finding different values of dirichlet alpha affect piece decisions
    alpha_values = [1, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001, 0.0003, 0.0001]
    alpha_values = {alpha: {'n_same': 0, 'n_total': 0} for alpha in alpha_values}

    model = load_best_model()
    interpreter = get_interpreter(model)

    default_config = Config()

    for _ in range(100):
        game = Game()
        game.setup()

        for _ in range(10):
            default_move, _ = MCTS(default_config, game, interpreter, add_noise=False)

            for alpha_value in alpha_values:
                config = Config(DIRICHLET_ALPHA=alpha_value)
                move, _ = MCTS(config, game, interpreter, add_noise=True)

                if move == default_move:
                    alpha_values[alpha_value]['n_same'] += 1
                
                alpha_values[alpha_value]['n_total'] += 1

            # To change the board, make the default move
            game.make_move(default_move)

    percent_dict = {alpha: 100*alpha_values[alpha]['n_same']/alpha_values[alpha]['n_total'] for alpha in alpha_values}    

    fig, ax = plt.subplots()

    ax.bar(range(len(percent_dict)), list(percent_dict.values()), align='center')
    ax.set_xticks(range(len(percent_dict)), list(percent_dict.keys()))

    ax.set_xlabel("Dirichlet Alpha Values")
    ax.set_ylabel("% of moves that were the same as without noise")

    plt.savefig(f"{directory_path}/tst_alpha_vals")

    return percent_dict

test_dirichlet_noise()