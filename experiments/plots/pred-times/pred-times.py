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

def get_tables(settings, path):
    pred_table = []
    real_table = []
    column = settings['column'][0]
    with open(path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        x = []
        y_pred = []
        y_real = []
        header = next(csv_reader)
        index = header.index(column)
        for row in csv_reader:
                s = row[index]
                x.append(int(s) if s.isnumeric() else float(s))
                s = row[-1]
                y_pred.append(int(s) if s.isnumeric() else float(s))
                s = row[-2]
                y_real.append(int(s) if s.isnumeric() else float(s))
    # add data to tables list
    pred_table = (x, y_pred)
    real_table = (x, y_real)
    return [real_table, pred_table]

def generate_plot(tables, path, settings):
    for table in tables:
        x, y = table
        plt.scatter(x, y, s=8)
        plt.plot(x, y)

    if settings['scale'] == 'log':
        plt.semilogy()


    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    plt.xlabel(settings['column'][0])
    plt.ylabel('time (s)')
    plt.title(Path(settings['table_paths'][1]).stem)
    plt.legend(labels=['real_tame', 'predicted_time'])
    plt.grid()
    
    path_out = settings['output_path']
    path_out += settings['column'][0] + '_' + path.stem + '.png'
    plt.savefig(path_out)
    plt.close()

if __name__ == '__main__':
    # Get settings from yaml file
    settings_path = sys.argv[1]
    with open(settings_path, 'r') as f:
        settings = yaml.full_load(f)

    # generate the plots from settings
    paths = Path(settings['table_paths'][0]).glob(settings['table_paths'][1])
    for path in paths:
        # get tables from table paths
        tables = get_tables(settings, path)
        generate_plot(tables, path, settings)