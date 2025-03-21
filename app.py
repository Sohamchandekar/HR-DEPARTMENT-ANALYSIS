from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import pandas as pd
from plotly.io import to_html
from datetime import datetime

from static.functions.Dashbaord_functions import read_excel_to_dict, totalActiveEmployeeCard, \
    employeeAverageGrowthRateCard, generate_professional_line_chart, generate_grouped_bar_chart, \
    employee_pie_chart, averageAttritionRateCard, activeEmployeeInDepartmentCard

app = Flask(__name__)
UPLOAD_FOLDER = 'D:/Projects/Rachna\'s Frontend/static/resources/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def validate_user(user_id, password):
    with open('D:/Projects/Rachna\'s Frontend/static/resources/user_credentials/login_credential.csv',
              mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['user_id'] == user_id and row['password'] == password:
                return row['access']
    return None


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    user_id = request.form['user_id']
    password = request.form['password']
    access = validate_user(user_id, password)
    if access == 'user':
        return redirect(url_for('home'))
    elif access == 'admin':
        return redirect(url_for('admin'))
    else:
        return "Invalid credentials", 401


@app.route('/home', methods=['GET', 'POST'])
def home():
    global data_dictionary

    excel_file_path = r"static/resources/uploads/hr-dashbaord-data.xlsx"
    data_dictionary = read_excel_to_dict(excel_file_path)

    default_month = pd.Timestamp('2025-02-01')  # Default month
    selected_month = default_month
    department_name = 'Sales BD'  # Default department

    if request.method == 'POST':
        selected_month_str = request.form.get('selected_month')
        department_name = request.form.get('department_name')

        if selected_month_str:
            try:
                selected_month = pd.Timestamp(selected_month_str)
            except ValueError:
                selected_month = default_month

    # Generate cards
    active_employee_card = totalActiveEmployeeCard(data_dictionary, selected_month)
    growth_rate_card = employeeAverageGrowthRateCard(data_dictionary, department_name)
    retention_rate_card = averageAttritionRateCard(data_dictionary, department_name)
    active_employee_in_department_card = activeEmployeeInDepartmentCard(data_dictionary, department_name, selected_month)

    department_names = list(data_dictionary.keys())
    months = sorted({month for dept_data in data_dictionary.values() for month in dept_data.keys()})

    # Generate line chart
    linechart = generate_professional_line_chart(data_dictionary, department_name)
    linechart_html = to_html(linechart, full_html= False)

    barchart = generate_grouped_bar_chart(data_dictionary, department_name)
    barchart_html = to_html(barchart, full_html=False)

    piechart = employee_pie_chart(data_dictionary, selected_month)
    piechart_html = to_html(piechart, full_html=False)


    return render_template('home.html',
                           active_employee_card=active_employee_card,
                           growth_rate_card=growth_rate_card,
                           retention_rate_card=retention_rate_card,
                           active_employee_in_department_card = active_employee_in_department_card,
                           selected_month=selected_month.strftime('%Y-%m-%d'),
                           department_name=department_name,
                           department_names=department_names,
                           months=months,
                           linechart_html = linechart_html,
                           barchart_html= barchart_html,
                           piechart_html = piechart_html)


# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return "No file part", 400
#         file = request.files['file']
#         if file.filename == '':
#             return "No selected file", 400
#         if file:
#             filename = file.filename
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], "hr-dashbaord-data.xlsx"))
#             return "File uploaded successfully", 200
#     return render_template('admin.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return render_template('admin.html', upload_success=False)

            file = request.files['file']
            if file.filename == '':
                return render_template('admin.html', upload_success=False)

            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], "hr-dashbaord-data.xlsx"))
                return render_template('admin.html', upload_success=True)
        except Exception as e:
            # Handle any exceptions that might occur during file saving
            print(f"Error uploading file: {e}")
            return render_template('admin.html', upload_success=False)

    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)