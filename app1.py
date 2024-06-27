"""
This Flask web application provides personal finance management functionalities, including:
- User authentication using HTTP Basic Authentication.
- Expense tracking with visualization of expenses by category.
- Budget management, allowing users to set and track budget limits.
- Financial insights with summaries and visualizations of income vs expenses.
- Personalized financial advice using a machine learning model to predict future expenses.

Modules and Libraries:
- Flask: Web framework for building the web application.
- Flask-HTTPAuth: Library for adding basic authentication.
- pandas: Data manipulation and analysis library.
- matplotlib: Plotting library for generating visualizations.
- io and base64: Libraries for handling image conversion.
- scikit-learn: Machine learning library for training and predicting with a RandomForestRegressor.

Usage:
- Run the script to start the  web server.
- Navigate to the home page to access different functionalities.
- Authenticate using the username 'admin' and password '123'.
"""

from flask import Flask, render_template, request, Response
from flask_httpauth import HTTPBasicAuth
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

app = Flask(__name__)
auth = HTTPBasicAuth()

# Dummy user data
users = {
    "admin": "123"
}

@auth.verify_password
def verify_password(username, password):
    """
    Verify the password for a given username.

    Args:
        username (str): The username to verify.
        password (str): The password to verify.

    Returns:
        str or None: The username if the password is correct, None otherwise.
    """
    if username in users and users[username] == password:
        return username
    return None

# Load and clean the data
file_path = 'personal finance data 2.xlsx'  # Make sure the Excel file is in the same folder
data = pd.read_excel(file_path)
data['Date / Time'] = pd.to_datetime(data['Date / Time']) # Convert to datetime
data = data.dropna() # Drop rows with missing values

# Utility function to convert plots to base64
import io
import base64

def plot_to_img(plt):
    """
    Converts a matplotlib plot to a base64-encoded image URL.

    Parameters:
    plt (matplotlib.pyplot): The matplotlib plot object.

    Returns:
    str: The base64-encoded image URL.
    """
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

# Route for home page
@app.route('/')
@auth.login_required
def index():
    """
    Renders the index.html template.

    Returns:
        The rendered index.html template.
    """
    return render_template('index.html')

# Route for expense tracking
@app.route('/expenses')
@auth.login_required
def expenses():
    """
    Generate a summary of expenses by category and render it as a bar chart in the expenses.html template.

    Returns:
        str: The rendered HTML template with the bar chart.
    """
    # Group data by category and sum the expenses
    expense_summary = data[data['Income/Expense'] == 'Expense'].groupby('Category')['Debit/Credit'].sum()
    # Plot the data as a bar chart
    expense_summary.plot(kind='bar', figsize=(10, 6), title='Expenses by Category')
    # Convert the plot to an image URL
    plot_url = plot_to_img(plt)
    return render_template('expenses.html', plot_url=plot_url)

# Route for budgeting
@app.route('/budget', methods=['GET', 'POST'])
@auth.login_required
def budget():
    """
    Calculate the budget and expenses data for each month.

    Returns:
        A rendered HTML template with the over budget months data.
    """
    if request.method == 'POST':
        budget_limits = {
            'Food': float(request.form['Food']),
            'Household': float(request.form['Household']),
            'Transportation': float(request.form['Transportation']),
            'Entertainment': float(request.form['Entertainment'])
        }
    else:
        budget_limits = {'Food': 5000, 'Household': 10000, 'Transportation': 3000, 'Entertainment': 2000}

    # Group data by month and calculate total expenses
    monthly_expenses = data[data['Income/Expense'] == 'Expense'].groupby([data['Date / Time'].dt.to_period('M')])['Debit/Credit'].sum()

    # Create a DataFrame to store the budget data
    budget_data = pd.DataFrame(index=monthly_expenses.index)
    budget_data['Total Expenses'] = monthly_expenses
    budget_data['Budget'] = monthly_expenses.index.map(lambda period: sum(budget_limits.values()))
    budget_data['Over Budget'] = budget_data['Total Expenses'] > budget_data['Budget']

    # Print the data for debugging
    print("Monthly Expenses:\n", monthly_expenses)
    print("Budget Data:\n", budget_data)
    # Filter the months where expenses exceeded the budget
    over_budget_months = budget_data[budget_data['Over Budget']]

    return render_template('budget1.html', over_budget_months=over_budget_months.to_html())





# Route for financial insights
@app.route('/insights')
@auth.login_required
def insights():
    """
    Generates insights on income and expenses.

    Returns:
        render_template: The rendered template with the generated insights.
    """
    # Calculate total income, total expenses, and savings
    total_income = data[data['Income/Expense'] == 'Income']['Debit/Credit'].sum()
    # Calculate total expenses
    total_expenses = data[data['Income/Expense'] == 'Expense']['Debit/Credit'].sum()
    # Calculate savings
    savings = total_income - total_expenses
    # Group data by income and expenses and plot as a pie chart
    income_expense_summary = data.groupby('Income/Expense')['Debit/Credit'].sum()
    # Plot the data as a pie chart
    income_expense_summary.plot(kind='pie', autopct='%1.1f%%', startangle=90, figsize=(8, 8), title='Income vs Expenses')
    # Convert the plot to an image URL
    plot_url = plot_to_img(plt)
    return render_template('insights.html', plot_url=plot_url, total_income=total_income, total_expenses=total_expenses, savings=savings)

# Route for personalized advice
@app.route('/advice')
@auth.login_required
def advice():
    """
    Provides financial advice based on machine learning predictions.

    Returns:
        str: The rendered HTML template with the mean squared error (mse) and predicted expense.
    """
    # Prepare the data for machine learning
    data_ml = data.copy()
    # Convert the date to a string
    data_ml['Date'] = data_ml['Date / Time'].dt.to_period('M').astype(str)
    # One-hot encode the categorical columns
    data_ml = pd.get_dummies(data_ml, columns=['Category', 'Sub category', 'Mode', 'Income/Expense'])
    # Drop the date columns
    data_ml.drop(columns=['Date / Time', 'Date'], inplace=True)  # remove the date columns

    # Split the data into features and target
    X = data_ml.drop(columns=['Debit/Credit'])
    y = data_ml['Debit/Credit']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Random Forest Regressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)

    # Get an example input for prediction
    example_input = X_test.iloc[0]
    predicted_expense = model.predict([example_input])
    return render_template('advice.html', mse=mse, predicted_expense=predicted_expense[0])

if __name__ == '__main__':
    app.run(debug=True, port=5002)
