from pathlib import Path
import matplotlib.pyplot as plt
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
    column1 = plot['columns'][0]
    column2 = plot['columns'][1]
    paths = list(Path(settings['table_paths'][0]).glob(settings['table_paths'][1]))
    for path in paths:
        with open(path) as f:
            csv_reader = csv.reader(f, delimiter=',')
            x = []
            y = []
            header = next(csv_reader)
            index1 = header.index(column1)
            index2 = header.index(column2)
            for row in csv_reader:
                    s = row[index1]
                    x.append(int(s) if s.isnumeric() else float(s))
                    s = row[index2]
                    y.append(int(s) if s.isnumeric() else float(s))
        # add data to tables list
        tables.append((x,y))
    return tables

def generate_plot(tables, plot, settings):
    for table in tables:
        x, y = table
        plt.scatter(x, y, s=8)
        plt.plot(x, y)

    if settings['scale'] == 'log':
        plt.semilogy()


    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    plt.xlabel(plot['columns'][0])
    plt.ylabel(plot['columns'][1])

    plt.grid()

    path_out = plot['output_path']
    path_out += plot['columns'][1] + '-' + plot['columns'][0] + '.png'
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