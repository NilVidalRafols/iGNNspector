import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, BayesianRidge
from sklearn.metrics import mean_squared_error, median_absolute_error

x = [(1, 2), (1, 5), (1, 6), (2, 4), (2, 5), (2, 7), (3, 1), (3, 5), (3, 6)] 
y = [2.3,5.6,9.0,8.6,4.2,13.5,11.0,1.3,5.0]

x = np.array(x)
y = np.array(y)

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

