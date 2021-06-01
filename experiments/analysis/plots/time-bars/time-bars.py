import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
import yaml
import sys
from scipy import stats
from collections import Counter
import math
from random import randint

def get_tables(settings):
    with open(settings['table_path']) as f:
        csv_reader = csv.reader(f, delimiter=',')
        table = list(csv_reader)
    return table

def generate_plot(table, settings):
    if settings['scale'] == 'log':
        plt.semilogy()

    functions = table[0][2:-1]
    values = [list(map(float, row[2:-1])) for row in table[1:]]
    colors = ['#%06X' % randint(0, 0xFFFFFF) for _ in functions]
    x_axis = settings['column']
    x_index = table[0].index(x_axis)
    x = []
    [x.append(row[x_index]) for row in table[1:]]
    previous_y = [0.0] * len(x)
    for i in range(len(functions)):
        y = []
        [y.append(row[i]) for row in values]
        plt.bar(x=x, 
                height=y,  
                bottom=previous_y,
                color=colors[i])
        previous_y = [py_i + y_i for py_i,y_i in zip(previous_y,y)]

    plt.xticks(fontsize=8, rotation=45)
    # plt.xticks(range(0, x[-1], x[-1]//10))
    # # plt.yticks(np.arange(min(y), max(y)+1, step=100))
    # plt.xlabel('# nodes')
    # plt.ylabel('# edges')
    # plt.suptitle('node-edge-time correlation', y=0.98, fontsize=10, fontweight='bold')
    # title = plot['column']
    # plt.title(title, fontsize=9)
    plt.legend(labels=functions, 
               fontsize=8, 
               loc='best', 
               markerscale=2.0,
               )

    # plt.grid()

    path_out = settings['output_path'] + settings['column']
    if 'title' in settings:
        path_out += '_' + settings['title']
    path_out += '.png'
    plt.savefig(path_out)
    plt.close()


if __name__ == '__main__':
    # Get settings from yaml file
    settings_path = sys.argv[1]
    with open(settings_path, 'r') as f:
        settings = yaml.full_load(f)

    # generate the plots from settings
    table = get_tables(settings)
    generate_plot(table, settings)