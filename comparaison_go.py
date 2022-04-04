"""
Compare agents performances
"""
import os
from multiprocessing import Process, Queue
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

from game.game_handler import MCTS
from model.go import GoBoard, Color


def play_two_agents(agent_to_test, other_agent, size, verbose=0):
    game = GoBoard(
        size=size, rule_selection1=agent_to_test, rule_selection2=other_agent)
    mcts = MCTS()
    turns = 0
    while not game.is_win() and not game.is_draw():
        if verbose:
            print(turns)
        game = game.game_turn_IA(mcts, game.rule_selection)
        game = game.game_turn_IA(mcts, game.rule_selection2)
        turns += 1

    prisonners = {}
    prisonners[game.player_1] = game.prisoners_player_1
    prisonners[game.player_2] = game.prisoners_player_2

    if prisonners[Color.BLACK] > prisonners[Color.WHITE]:
        if (verbose):
            print("Black wins")
        return 1

    elif prisonners[Color.BLACK] < prisonners[Color.WHITE]:
        if (verbose):
            print("White wins")
        return -1

    else:
        if (verbose):
            print("Draw")
        return 0


# +
def agent_vs_agent(game_name, size, agent_to_test, agent_to_compare, begin, queue, verbose=0):
    """
    game_name : 'tictactoe' or 'go'
    size : size of the board
    agent_to_test = 'IMED' or 'UCB'
    agent_to_compare = 'RANDOM'
    """
    rule_selection1 = agent_to_test if begin else agent_to_compare
    rule_selection2 = agent_to_compare if begin else agent_to_test
    queue.put(play_two_agents(rule_selection1, rule_selection2, size, verbose=verbose))


def performance_agent(game, size, agent_to_test, agent_to_compare, nb_simulations, begin, plot=False, throttle=1,
                      sequence_length=3):
    """
    game: TicTacToe / Go

    size : size of the board

    agent_to_test: Agent class (Specific rule selction agent)

    agent_to_compare: Agent class (Dummy Agent)

    begin : bool
    If True, agent_to_test starts, if False agent_to_test doesn't start

    nb_simulations : int
    Number of simulation

    throttle: int
    Throttle tqdm updates.

    plot: bool
    If True, plot stats instead of returning them.

    returns:
    -------
    interval : list [moyenne - ecart_type, moyenne + ecart_type] for agent1

    """
    stats = np.zeros(nb_simulations)

    nb_win = 0
    nb_draw = 0
    postfix = {
        'draw': 0.0,
        'wins': 0.0,
    }

    start_time = perf_counter()
    queue = Queue()

    processes = [Process(target=agent_vs_agent, args=(game, size, agent_to_test, agent_to_compare, begin, queue, 1 if _ == 0 else 0)) for
                 _ in range(nb_simulations)]
    [p.start() for p in processes]
    [p.join() for p in processes]


    results = []

    while not queue.empty():
        results.append(queue.get())
    print(results)

    for simulation, result in enumerate(results):
        stats[simulation] = result
        nb_draw += int(result == 0)
        nb_win += int(result == 1)
    end_time = perf_counter()
    elapsed_time = end_time - start_time
    print(f"Time elapsed {elapsed_time // 60:.0f}min {elapsed_time % 60:.0f}s")

    win_rate = nb_win / nb_simulations
    win_rate_int = int(round(win_rate, 2) * 100)
    ecart_type = 1 / np.sqrt(nb_simulations)
    interval = [win_rate - ecart_type, win_rate + ecart_type]

    if plot:
        name = f'{agent_to_test if begin else agent_to_compare}vs{agent_to_compare if begin else agent_to_test}'
        plotstats(stats, win_rate_int, name)
    return (interval)


def plotstats(stats, win_rate, name):
    draws = stats == 0
    agent_wins = stats == 1

    _, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(np.cumsum(agent_wins) / np.cumsum(np.ones(len(stats))),
            color='green', label='wins')
    ax.plot(np.cumsum(draws) / np.cumsum(np.ones(len(stats))),
            color='blue', label='draws')
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

    ax.set_xlabel('')
    ax.legend(loc='upper left')

    plt.text(0.5, 0.5, f'win rate {win_rate} %', horizontalalignment='left',
             verticalalignment='center', transform=ax.transAxes, fontsize=14, color='r')

    plt.tight_layout()
    if not os.path.exists('figures/'):
        os.makedirs('figures/')

    plt.savefig(f'figures/{name}.png')


def compare_agents(game, size, agents_to_test, agent_to_compare, nb_simulations, begin=True, plot=False, ):
    """
    game: TicTacToe / Go

    agents_to_test: list of Agent class ['IMED', 'UCB']
    First AI agent.

    agent_to_compare: Agent class (Dummy Agent)
    Second AI agent.

    begin : bool
    If True, agents_to_test start, if False agent_to_test doesn't start

    nb_simulations : int
    Number of simulation

    returns:
    -------
    Best Agent

    """
    intervals = {}
    win_rates = {}

    for agent_to_test in agents_to_test:
        intervals[agent_to_test] = performance_agent(game, size,
                                                     agent_to_test, agent_to_compare, nb_simulations, begin, plot,
                                                     )
        win_rate = (intervals[agent_to_test][0] +
                    intervals[agent_to_test][1]) / 2
        win_rates[agent_to_test] = int(round(win_rate, 2) * 100)

    print(f'The win_rates (%) of each agent are : {win_rates}')

    intervals = sorted(intervals.items(), key=lambda t: t[1])
    if intervals[0][1][1] <= intervals[1][1][0]:  # b1 < a2
        print(f'Best agent is {intervals[1]}')

    elif intervals[0][1][1] <= intervals[1][1][1]:  # b1 < b2 intervalles se recoupent
        intersection = abs(intervals[1][1][0] - intervals[0][1][1])
        intersection = int(round(intersection, 2) * 100)  # b1 - a2
        print(
            f'Cannot conclude : there is a probability of {intersection} % that agents have the same performance.')  # However, agent with highest winning rate is {intervals[1][0]}')

    # a1<a2 et b2<b1 intervalles incluent l'un dans l'autre
    elif (intervals[0][1][0] < intervals[1][1][0]) & (intervals[1][1][1] < intervals[0][1][1]):
        print(
            f'Cannot conclude : agents have very close winning rate.')  # Agent with highest winngin rate is {max(win_rates.iteritems(), key=operator.itemgetter(1))[0]}')

    elif (intervals[0][1][0] == intervals[1][1][0]) & (intervals[0][1][1] == intervals[1][1][1]):
        print('Agents have exactly same performance')

    else:
        print('Debug : Not supposed to be there')


if __name__ == '__main__':
    agents_to_test = ['IMED', 'UCB']
    agent_to_compare = 'random'
    game_name = 'tictactoe'
    size = 7
    nb_simulations = 222
    compare_agents(game_name, size, agents_to_test, agent_to_compare,
                   nb_simulations=nb_simulations, begin=False, plot=True)
    compare_agents(game_name, size, agents_to_test, agent_to_compare,
                   nb_simulations=nb_simulations, begin=True, plot=True)
    performance_agent(game_name, size, 'IMED', 'UCB', nb_simulations, True, plot=True)
    performance_agent(game_name, size, 'IMED', 'UCB', nb_simulations, False, plot=True)
