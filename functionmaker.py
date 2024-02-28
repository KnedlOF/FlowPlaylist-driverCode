#for making function for volume knob, because it is not linear

import numpy as np
import matplotlib.pyplot as plt

# Provided data
x_data = np.array([1016, 995, 962, 940, 915, 875, 806, 840])
y_data = np.array([1, 10, 20, 30, 40, 50, 55, 53])
#x_data = np.array([690, 533, 322, 158, 4, 806])
#y_data = np.array([ 60, 70, 80, 90, 100, 55])

# Define the degree of the polynomial (adjust as needed)
degree = 3

# Fit the data with a polynomial of the specified degree
coefficients = np.polyfit(x_data, y_data, degree)

# Create a polynomial function based on the coefficients
poly_function = np.poly1d(coefficients)

# Generate data for the fitted curve
fit_x = np.linspace(min(x_data), max(x_data), 100)
fit_y = poly_function(fit_x)

# Print the coefficients of the fitted polynomial
print("Fitted Polynomial Coefficients:", coefficients)

# Plot the original data and the fitted curve
plt.scatter(x_data, y_data, label='Original Data')
plt.plot(fit_x, fit_y, 'r', label='Fitted Curve')
plt.xlabel('X Data')
plt.ylabel('Y Data')
plt.legend()
plt.show()
