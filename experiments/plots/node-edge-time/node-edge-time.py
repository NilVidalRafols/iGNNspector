from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import csv
import pandas as pd
import yaml
import sys
from scipy import stats
from collections import Counter
import math

from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

def get_tables(settings, plot):
    tables = []
    column = plot['column']
    paths = list(Path(settings['table_paths'][0]).glob(settings['table_paths'][1]))
    for path in paths:
        with open(path) as f:
            csv_reader = csv.reader(f, delimiter=',')
            nodes = []
            edges = []
            times = []
            header = next(csv_reader)
            column_index = header.index(column)
            for row in csv_reader:
                    nodes.append(int(row[0]))
                    edges.append(int(row[1]))
                    times.append(float(row[column_index]))
        # add data to tables list
        tables.append((nodes, edges, times))
    return tables

def generate_plot(tables, plot, settings):
    if settings['scale'] == 'log':
        plt.semilogy()

    x = []
    y = []
    z = []
    for table in tables:
        nodes, edges, times = table
        x += nodes
        y += edges
        z += times
    plt.scatter(x,y,s=15,c=z,cmap='rainbow')
    # sns.jointplot(x=x, y=y, hue=z, kind='reg')

    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    # plt.yticks(np.arange(min(y), max(y)+1, step=100))
    plt.xlabel('# nodes')
    plt.ylabel('# edges')
    plt.suptitle('node-edge-time correlation', y=0.98, fontsize=10, fontweight='bold')
    title = plot['column']
    plt.title(title, fontsize=9)
    # plt.legend(fontsize=8, loc='best', markerscale=2.0)

    cbar = plt.colorbar()
    # t = 5*round((len(x)//10)/5)
    # cbar.set_ticks(MultipleLocator(t))
    cbar.ax.tick_params(labelsize=8)
    cbar.ax.set_title('time (s)', fontsize=8)

    plt.grid()

    path_out = plot['output_path'] + plot['column']
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
    for plot in settings['plots']:
        # get tables from table paths
        tables = get_tables(settings, plot)
        generate_plot(tables, plot, settings)