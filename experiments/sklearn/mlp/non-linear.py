import random
import numpy as np
from sklearn.linear_model import *
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, median_absolute_error
import csv
from pathlib import Path
import pickle

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

    sizes = [10*i for i in range(1,11)]
    sizes = sizes + [[10*i,10*i] for i in range(1,11)]
    mlp_model = MLPRegressor(activation='logistic',
                        max_iter=200,
                        solver='lbfgs',random_state=42)

    parameters= {'hidden_layer_sizes': sizes,
                'alpha':[0.01,0.1,0.001],
                'activation':['logistic','relu'],
                'solver':['lbfgs', 'sgd', 'adam']}

    mlp_model_CV = GridSearchCV(estimator=mlp_model,
                    scoring=['r2'],
                    param_grid={'hidden_layer_sizes': sizes},
                    cv=5,
                    return_train_score=True,
                    refit='r2')

    mlp_model_CV.fit(x, y)
    y_pred = mlp_model_CV.predict(x)
    print(mlp_model_CV.best_estimator_)
    r2_mlp = mlp_model_CV.score(x, y)
    print('Mean sqared error with validation data: {}'.format(mean_squared_error(y,y_pred)))
    print('R2 score with validation data: {}'.format(r2_mlp))
    # collection of metrics for regression
    metrics = {"mse":mean_squared_error,
            "mae":median_absolute_error}

    best_model = mlp_model_CV.best_estimator_
    return best_model

def save_results(model, table, path):
    nodes, edges, times = table
    results = [['num_nodes', 'num_edges', 'real', 'pred']]
    x = np.array(list(zip(np.log10(nodes), np.log10(edges))))
    y = model.predict(x)
    pred_times = list(map(lambda y_i: pow(10, y_i), y))
    results += list(zip(nodes, edges, times, pred_times))

    out_path = 'experiments/sklearn/non-linear/2/pred_' + path.stem + '.csv'
    with open(out_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerows(results)

def save_model(model, path):
    with open(path + 'time_model.pickle', 'wb') as f:
        pickle.dump(model, f)

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
    
    out_path = 'ignnspector/analysis/'
    save_model(model, out_path)