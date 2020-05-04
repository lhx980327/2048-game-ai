""" Used for training hyperparameters and running multiple simulations """
import time

from threading import Thread

import numpy as np

import game

test_cases = 100

count_512 = 0
count_1024 = 0
count_2048 = 0
count_4096 = 0
best_board = 0
best_score = 0
best_moves = 0
avg_score = 0
avg_moves = 0
prog = 0
g1 = game.Game()


def progress_bar():
    """ Increments the progress indicator """
    global prog
    prog += 1
    print(str((prog / test_cases) * 100) + "%")


def worker():
    """ Runs a simulation on a seprate thread and records statistics """
    global avg_moves, avg_score, best_board, best_score, best_moves,count_512,count_1024,count_2048,count_4096
    board, s, m = g1.run()
    if np.amax(board) == 512:
        count_512 += 1
    if np.amax(board) == 1024:
        count_1024 += 1
    if np.amax(board) == 2048:
        count_2048 += 1
    if np.amax(board) == 4096:
        count_4096 += 1
    avg_score += s
    avg_moves += m
    if s > best_score:
        best_board = board
        best_score = s
        best_moves = m
    if s == 4096:
        best_board = board
        best_score = s
        best_moves = m
    progress_bar()


def multi_simulate():
    """ Runs multiple simulation worker threads and reports results """
    start_time = time.process_time();
    workers = []
    print("0%")
    for i in range(0, test_cases):
        t = Thread(target=worker, args=())
        t.start()
        workers.append(t)

    """ Block until all threads finished """
    for w in workers:
        w.join()
    print("\nBest Score:", best_score, "Best Moves:", best_moves)
    g1.print_(best_board)
    print("\nAvg Score:", (avg_score / test_cases), "Avg Moves:", (avg_moves / test_cases))
    print("\n512-", count_512 / test_cases * 100, "%", " 1024-", count_1024 / test_cases * 100, "%", " 2048-",
          count_2048 / test_cases * 100, "%", " 4096-",
          count_4096 / test_cases * 100, "%")
    print("Time:", (time.process_time() - start_time), "seconds")


multi_simulate()
