# FinanceMasterApp

FinanceMasterApp is a personal finance management application that helps users track expenses, manage budgets, gain financial insights, and receive personalized financial advice. The application is built using Flask and provides an interactive web interface.

## Features

- **Expense Tracking**: Visualize your expenses by category.
- **Budgeting**: Monitor your spending against budget limits.
- **Financial Insights**: Get an overview of your income, expenses, and savings.
- **Personalized Financial Advice**: Receive tailored financial advice based on your spending patterns.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Authentication](#authentication)
- [License](#license)

## Installation

### Prerequisites

- Python 3.9
- pip (Python package installer)

### Steps

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/FinanceMasterApp.git
    cd FinanceMasterApp
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Ensure the data file is present:**
    - Place the `personal_finance_data_2.xlsx` file in the `FinanceMasterApp` directory.

## Usage

1. **Run the Flask application:**
    ```sh
    python app.py
    ```

2. **Open your web browser and navigate to:**
    ```
    http://127.0.0.1:5002/
    ```

3. **Log in with the credentials:**
    - Username: `admin`
    - Password: `123`

## Endpoints

- **Home Page**: `/`
    - Displays the main navigation page.
- **Expense Tracking**: `/expenses`
    - Shows a bar chart of expenses by category.
- **Budgeting**: `/budget`
    - Displays budget alerts for over-spending.
- **Financial Insights**: `/insights`
    - Provides a pie chart of income vs. expenses and key financial metrics.
- **Personalized Financial Advice**: `/advice`
    - Offers tailored financial advice based on user data.

## Authentication

This application uses basic HTTP authentication. To access the routes, you need to log in with valid credentials.

- **Username**: `admin`
- **Password**: `123`
