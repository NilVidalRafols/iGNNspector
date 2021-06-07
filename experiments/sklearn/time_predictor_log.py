import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, BayesianRidge
from sklearn.metrics import mean_squared_error, median_absolute_error
import csv

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

    x = []
    y = []
    z = []
    for table in tables:
        nodes, edges, times = table
        x += nodes
        y += edges
        z += times
    
    return np.log(x), np.log(y), np.log(z)

def get_model(nodes, edges, times):
    x = np.array(list(zip(nodes, edges)))
    y = np.array(times)

    # collection of regression methods
    models = {"OLS":LinearRegression(), 
            "R":Ridge(), 
            "BR":BayesianRidge()}

    # collection of metrics for regression
    metrics = {"mse":mean_squared_error,
            "mae":median_absolute_error}

    # training
    for m in sorted(models):
        print("\n",m)
        models[m].fit(x,y)
        # metrics for comparison of regression methods
        for me in sorted(metrics):
            print("metric",me,metrics[me](y, models[m].predict(x)))
    
    return models


if __name__ == '__main__':
    column = 'total'
    paths = [
    'experiments/analysis/PubMed/time_table_PubMed_2.csv',
    'experiments/analysis/CiteSeer/time_table_CiteSeer_2.csv',
    'experiments/analysis/ogbn-arxiv/time_table_ogbn-arxiv.csv',
    'experiments/analysis/ogbn-products/ogbn-products_times.csv'
    ]

    nodes, edges, times = get_data(paths, column)
    models = get_model(nodes, edges, times)

    