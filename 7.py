import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# generate random data-set

np.random.seed(0)
x = np.random.rand(100, 1) #Generate a 2-D array with 100 rows, each row containing / random numbers:

y=2+3*x+np.random.rand(100, 1)

regression_model =  LinearRegression() # Model initialization

regression_model.fit(x, y) # Fit the data(train the model)

y_predicted = regression_model.predict(x) # Predict

#model evaluation

rmse =  mean_squared_error(y, y_predicted)

r2=r2_score(y, y_predicted)

#printing values

print('Slope:',regression_model.coef_)

print('Intercept:', regression_model.intercept_)

print('Root mean squared error: ', rmse)

print('R2 score:', r2)

#plotting values # data points

plt.scatter(x, y, s=10)

plt.xlabel('x-Values from 0-1')

plt.ylabel('y-values from 2-5')

#predicted values

plt.plot(x, y_predicted, color='r')

plt.show()