from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Graph.html')

@app.route('/submit', methods=['POST'])
def submit():
    month = request.form['month']
    salary = float(request.form['salary'])

    # Get the number of expenditures
    num_expenditures = int(request.form['total_expenditures'])

    # Calculate total expenditure cost by summing the costs of all expenditures
    total_expenditure_cost = sum(float(request.form[f'expenditure_cost_{i}']) for i in range(num_expenditures))

    # Calculate total saving
    saving = salary - total_expenditure_cost

    # Create or load existing data
    try:
        data = pd.read_csv("monthly_data.csv")
    except FileNotFoundError:
        data = pd.DataFrame(columns=['Month', 'Salary', 'Total_Expenditure_Cost', 'Saving'])

    # Add new data
    new_row = {'Month': month, 'Salary': salary, 'Total_Expenditure_Cost': total_expenditure_cost, 'Saving': saving}
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

    # Save data to CSV
    data.to_csv("monthly_data.csv", index=False)

    # Plot the data
    months = data['Month']
    salary_values = data['Salary']
    expenditure_values = data['Total_Expenditure_Cost']
    saving_values = data['Saving']

    bar_width = 0.3
    index = np.arange(len(months))

    plt.figure(figsize=(10, 6))
    plt.bar(index, salary_values, bar_width, label='Salary')
    plt.bar(index + bar_width, expenditure_values, bar_width, label='Total Expenditure Cost')
    plt.bar(index + 2 * bar_width, saving_values, bar_width, label='Saving')

    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.title('Monthly Financial Analysis')
    plt.xticks(index + bar_width, months)
    plt.legend()
    plt.tight_layout()

    # Convert plot to base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return render_template('result.html', plot_data=plot_data)

if __name__ == '__main__':
    app.run(debug=True)
