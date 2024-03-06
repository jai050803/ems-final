import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Generate a synthetic dataset
np.random.seed(0)
X = np.random.rand(100, 2)  # 100 samples, 2 features
y = 3 * X[:, 0] + 2 * X[:, 1] + np.random.randn(100)  # Target variable with some noise

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the LinearRegression model
model = LinearRegression()

# Fit the model to the training data
model.fit(X_train, y_train)

# Make predictions using the testing set
y_pred = model.predict(X_test)

# Print model coefficients and intercept
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# Compare actual vs. predicted values (for the first few samples, as an example)
df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print(df.head())

# Optionally, plot actual vs. predicted values for visualization
plt.scatter(y_test, y_pred)
plt.xlabel('Actual values')
plt.ylabel('Predicted values')
plt.title('Actual vs. Predicted values')
plt.show()

# Calculate the model performance (e.g., R^2 score)
r2_score = model.score(X_test, y_test)
print(f"R^2 score: {r2_score}")
