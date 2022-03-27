"""
Compare agents performances
"""

from unicodedata import name
from pip import main
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import random
from model.tictactoe import TicTacToeBoard
from game.game_handler import MCTS

# import operator

# agent_vs_agent_test : Fonction de test

# A remplacer par la fonciton qui fait s'affronter deux agents entre eux
# agent_vs_agent(game,agent_to_test, agent_to_compare, begin) :
# En paramètres :
# agent_to_test: Agent class (Specific rule selction agent)
# agent_to_compare: Agent class (Dummy Agent)
# begin : bool. If True, agent_to_test starts, if False agent_to_test doesn't start
# Returns :
# 1, 0,-1 if agent_to_test wins, draw, lose


def agent_vs_agent_test():
    list = [1, 0, -1]
    return(random.choice(list))


# def play_two_agent(agent1, agent2):


# +
def agent_vs_agent(game_name, size, agent_to_test, agent_to_compare, begin):
    """
    game_name : 'tictactoe' or 'go'
    size : size of the board
    agent_to_test = 'IMED' or 'UCB'
    agent_to_compare = 'random'
    """
    if game_name == 'tictactoe':
        size = 3
        mcts = MCTS()
        if begin:
            rule_selection1 = agent_to_test
            rule_selection2 = agent_to_compare

            model = TicTacToeBoard(
                                   size = size, rule_selection1 = rule_selection1, rule_selection2=rule_selection2)
            turn = 0
            while not model.is_win() and not model.is_draw():
                try:
                    if turn % 2 == 0:
                        model.game_turn_IA(
                            mcts, rule_selection1)
                    else:
                        model.game_turn_IA(
                            mcts, rule_selection2)
                    turn += 1
                    print('try')
                except Exception as e:
                    print(e)
                    break                
                
#             if turn % 2 == 0 : 
#                 last_player = rule_selection1
#             else : 
#                 last_player = rule_selection2
            if model.is_draw():
                print('is_draw')
                return(0)
            elif model.is_win():
                if (turn % 2 == 0):
                    print('win')
                    return(1)
                else:
                    print('lost')
                    return(-1)

#         else:
#             rule_selection1 = agent_to_compare
#             rule_selection2 = agent_to_test
#             model = TicTacToeBoard(board,
#                                    size, rule_selection1, rule_selection2)
#             turn = 0
#             while not model.is_win() and not model.is_draw():
#                 try:
#                     if turn % 2 == 0:
#                         model.game_turn_IA(
#                             mcts, rule_selection1)
#                     else:
#                         model.game_turn_IA(
#                             mcts, rule_selection2)
#                 except:
#                     print()
#             if model.is_win():
#                 return(-1)
#             elif model.is_draw():
#                 return(0)
#             else:
#                 return(1)

    # TODO : rajouter GO


# -

def performance_agent(game, size, agent_to_test, agent_to_compare, nb_simulations, begin, plot=False, throttle=1):
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
            # ----- Change the function to agent_vs_agent
            # uncomment when testing with real agents
            #result = agent_vs_agent(game,agent_to_test,agent_to_compare,begin)

            # test function agent_vs_agent_test
            result = agent_vs_agent(
                game, size, agent_to_test, agent_to_compare, begin)
            # ----
            print(result)

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
    # TODO : formule de l'intervale à 95%
    #interval_95 = [win_rate - 2*ecart_type, win_rate + 2*ecart_type]

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

    plt.text(0.5, 0.5, f'win rate {win_rate} %', horizontalalignment='left',
             verticalalignment='center', transform=ax.transAxes, fontsize=14, color='r')

    plt.tight_layout()
    plt.show()


def compare_agents(game, size, agents_to_test, agent_to_compare, nb_simulations, begin=True, plot=False):
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
                                                     agent_to_test, agent_to_compare, nb_simulations, begin, plot)
        win_rate = (intervals[agent_to_test][0] +
                    intervals[agent_to_test][1])/2
        win_rates[agent_to_test] = int(round(win_rate, 2)*100)

    print(f'The win_rates (%) of each agent are : {win_rates}')

    intervals = sorted(intervals.items(), key=lambda t: t[1])
    if intervals[0][1][1] <= intervals[1][1][0]:  # b1 < a2
        print(f'Best agent is {intervals[1]}')

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
    agent_to_test = 'random'
    agent_to_compare = 'imed'
    game = 'tictactoe'
    size = 3
#     compare_agents(game, size, agents_to_test, agent_to_compare,
#                    nb_simulations=20, begin=True, plot=True)

    performance_agent(game, size, agent_to_test, agent_to_compare, nb_simulations = 5, begin = True, plot = True)



