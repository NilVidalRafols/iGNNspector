import random
import numpy as np
from sklearn.linear_model import *
from sklearn.metrics import mean_squared_error, median_absolute_error
import csv
from pathlib import Path

def get_data(paths, column):
    tables = []
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

def get_best_model(nodes, edges, times):
    randomize = list(zip(nodes, edges, times))
    random.shuffle(randomize)
    rand_nodes, rand_edges, rand_times =list(zip(*randomize))
    x = np.array(list(zip(np.log10(rand_nodes), np.log10(rand_edges))))
    y = np.array(np.log10(rand_times))

    # collection of regression methods
    models = {"OLS":LinearRegression(), 
            "R":Ridge(), 
            "BR":BayesianRidge(),
            "LL":LassoLars(alpha=.1),
            "L":Lasso(alpha=0.1),
            "EN":ElasticNet()}

    # collection of metrics for regression
    metrics = {"mse":mean_squared_error,
            "mae":median_absolute_error}

    # training
    scores = []
    for m in sorted(models):
        print("\n",m)
        models[m].fit(x,y)
        # metrics for comparison of regression methods
        for me in sorted(metrics):
            print("metric",me,metrics[me](y, models[m].predict(x)))
        scores.append((models[m], metrics['mse'](y, models[m].predict(x))))

    scores = [(model, mean_squared_error(y, model.predict(x))) for model in models.values()]
    best_model = min(scores, key=lambda x: x[1])[0]
    return best_model

def save_results(model, table, path):
    nodes, edges, times = table
    results = [['num_nodes', 'num_edges', 'real', 'pred']]
    x = np.array(list(zip(np.log10(nodes), np.log10(edges))))
    y = model.predict(x)
    pred_times = list(map(lambda y_i: pow(10, y_i), y))
    results += list(zip(nodes, edges, times, pred_times))

    out_path = 'experiments/sklearn/pred_' + path.stem + '.csv'
    with open(out_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerows(results)

if __name__ == '__main__':
    column = 'total'
    paths = list(Path('experiments/analysis/pyg').glob('times_all_*'))

    tables = get_data(paths, column)
    # tables = tables[:-1]
    x = []
    y = []
    z = []
    for table in tables:
        nodes, edges, times = table
        x += nodes
        y += edges
        z += times
    model = get_best_model(nodes, edges, times)

    for  table, path, in zip(tables, paths):
        save_results(model, table, path)