"""
Compare agents performances
"""

from tkinter import W
from unicodedata import name
from pip import main
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from model.tictactoe import TicTacToeBoard
from game.game_handler import MCTS


def play_two_agents(rule_selection1, rule_selection2, size):
    game = TicTacToeBoard(
        size=size, rule_selection1=rule_selection1, rule_selection2=rule_selection2, sequence_length=sequence_length)
    mcts = MCTS()
    turn = 0
    while not game.is_win() and not game.is_draw():
        turn += 1
        if (turn % 2 == 0):
            game = game.game_turn_IA(mcts, game.rule_selection1)
        else:
            game = game.game_turn_IA(mcts, game.rule_selection2)
        if game.is_draw():
            return(0)
        elif game.is_win():
            if (turn % 2 == 0):  # last_player = rule_selection1
                return(1)
            else:  # last_player = rule_selection2
                return(-1)


# +
def agent_vs_agent(game_name, size, agent_to_test, agent_to_compare, begin, sequence_length):
    """
    game_name : 'tictactoe' or 'go'
    size : size of the board
    agent_to_test = 'IMED' or 'UCB'
    agent_to_compare = 'RANDOM'
    """
    if game_name == 'tictactoe':
        rule_selection1 = agent_to_test if begin else agent_to_compare
        rule_selection2 = agent_to_compare if begin else agent_to_test
        result = play_two_agents(
            rule_selection1, rule_selection2, size, sequence_length)
        return (result)


def performance_agent(game, size, agent_to_test, agent_to_compare, nb_simulations, begin, plot=False, throttle=1, sequence_length=3):
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
    with tqdm(total=nb_simulations, postfix=postfix) as pbar:
        for simulation in range(nb_simulations):
            result = agent_vs_agent(
                game, size, agent_to_test, agent_to_compare, begin, sequence_length)
            # ----

            stats[simulation] = result
            nb_draw += int(result == 0)
            nb_win += int(result == 1)

            postfix['draw'] = '{:.0%}'.format(nb_draw / (simulation + 1))
            postfix['wins'] = '{:.0%}'.format(nb_win / (simulation + 1))

            if simulation % throttle == 0:
                pbar.set_postfix(postfix)
                pbar.update(throttle)

    win_rate = nb_win/nb_simulations
    win_rate_int = int(round(win_rate, 2)*100)
    ecart_type = 1/np.sqrt(nb_simulations)
    interval = [win_rate - ecart_type, win_rate + ecart_type]
    if plot:
        plotstats(stats, win_rate_int)
    return(interval)


def plotstats(stats, win_rate):
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

    plt.text(0.90, 0.80, f'win rate {win_rate} %', horizontalalignment='right',
             verticalalignment='top', transform=ax.transAxes, fontsize=14, color='r')

    plt.tight_layout()
    plt.show()


def compare_agents(game, size, agents_to_test, agent_to_compare, nb_simulations, begin=True, plot=False, sequence_length=3):
    """
    game: TicTacToe / Go

    agents_to_test: list of Agent class ['imed_agent', 'ucb_agent']
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
                                                     agent_to_test, agent_to_compare, nb_simulations, begin, plot, sequence_length=sequence_length)
        win_rate = (intervals[agent_to_test][0] +
                    intervals[agent_to_test][1])/2
        win_rates[agent_to_test] = int(round(win_rate, 2)*100)

    print(f'The win_rates (%) of each agent are : {win_rates}')

    intervals = sorted(intervals.items(), key=lambda t: t[1])
    if intervals[0][1][1] <= intervals[1][1][0]:  # b1 < a2
        print(
            f'Best agent is {intervals[1]} and worst agent is {intervals[0]}')

    elif intervals[0][1][1] <= intervals[1][1][1]:  # b1 < b2 intervalles se recoupent
        intersection = abs(intervals[1][1][0] - intervals[0][1][1])
        intersection = int(round(intersection, 2)*100)  # b1 - a2
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
    agent_to_compare = ['random']
    game_name = 'tictactoe'
    size = 5
    sequence_length = 3
    compare_agents(game_name, size, agents_to_test, agent_to_compare,
                   nb_simulations=200, begin=False, plot=True, sequence_length=sequence_length)
    #performance_agent(game_name, size, 'IMED', 'UCB', 200, True, plot=True, throttle=1, sequence_length=sequence_length)
