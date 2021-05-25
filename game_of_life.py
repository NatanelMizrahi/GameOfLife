from scipy.signal import convolve2d
import matplotlib.pyplot as plt
import numpy as np
import re

# params
DEFAULT_SETTING = 'B2/S3'
N = 250  # board size
FRAMERATE = 0.001
MAX_T = 1000
SPARSITY = 7
MONOCHROME = False


def get_num_of_neighbors_matrix(m):
    """fancy shorthand way to get the sum of non-zero neighbours for each cell - in our case - number of neighbors"""
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    return np.asmatrix(convolve2d(m, kernel, 'same'))


def get_random_matrix(n):
    m = np.ones((n, n))
    for i in range(SPARSITY):
        m *= np.random.randint(2, size=(n, n))  # repetitive multiplication zeroes out more cells
    return m


def display_matrix(m):
    if MONOCHROME:
        plt.imshow(m, vmin=0, vmax=1, cmap=plt.cm.gray)
    else:
        plt.imshow(m)
    plt.axis('off')
    plt.pause(FRAMERATE)
    plt.close('all')


def get_next_generation(m, b, s):
    born = np.zeros(m.shape)
    survived = np.zeros(m.shape)
    num_of_neighbors_matrix = get_num_of_neighbors_matrix(m)
    indexes_of_born_cells = np.in1d(num_of_neighbors_matrix, b).reshape(m.shape)
    indexes_of_survived_cells = np.in1d(num_of_neighbors_matrix, s).reshape(m.shape)
    born[(m == 0) & indexes_of_born_cells] = 1
    survived[(m == 1) & indexes_of_survived_cells] = 1
    new_matrix = born + survived

    return new_matrix


def get_params_from_user():
    while True:
        try:
            user_input = input(f"Enter Born/Survive rules, default (Enter) is set to '{DEFAULT_SETTING}':")
            if user_input == "":
                user_input = DEFAULT_SETTING
            b_, s_ = re.search(r'B([0-8]+)/S([0-8]+)', user_input).groups()
            s = tuple(map(int, tuple(s_)))  # convert S... input to tuple
            b = tuple(map(int, tuple(b_)))  # convert B... input to tuple
            return b, s
        except AttributeError as e:
            raise SyntaxError('input must match "B<0-8>+/S<0-8>+')


def init():
    b, s = get_params_from_user()
    m = get_random_matrix(N)
    return m, b, s


def main_loop(m, b, s):
    for t in range(MAX_T):
        m = get_next_generation(m, b, s)
        display_matrix(m)


def game_of_life():
    m, b, s = init()
    main_loop(m, b, s)


game_of_life()
