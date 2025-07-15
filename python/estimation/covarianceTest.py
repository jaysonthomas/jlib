import numpy as np

# Sample data
x = np.array([1, 2, 3, 4, 5])
y = np.array([5, 4, 3, 2, 1])

# Stack the data into a matrix
data = np.stack((x, y), axis=0)

covarianceMatrix = np.cov(data)

# Calculate the sample variances of x and y
xVar = np.var(x, ddof=1)
yVar = np.var(y, ddof=1)

print(f'Covariance matrix:\n {covarianceMatrix}')
print(f'Sample variances: {xVar}, {yVar}')