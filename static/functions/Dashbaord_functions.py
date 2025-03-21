import pandas as pd
import plotly
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def read_excel_to_dict(file_path):
    # Create an empty dictionary to hold all department data
    all_departments_data = {}

    # Read the Excel file
    xls = pd.ExcelFile(file_path)

    # Iterate through each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # Create a dictionary for the current department
        department_data = {}

        # Iterate through the rows of the DataFrame
        for index, row in df.iterrows():
            # Assuming the first column is the month and the rest are values
            month = row[0]  # Change index if the month is in a different column
            values = row[1:].to_dict()  # Convert the rest of the row to a dictionary

            # Add the month and its corresponding values to the department data
            department_data[month] = values

        # Add the department data to the all departments dictionary
        all_departments_data[sheet_name] = department_data

    return all_departments_data


def totalActiveEmployeeCard(data_dictionary, selected_month):
    # Initialize total active employees count
    total_active_employees = 0

    # Iterate through each department in the data dictionary
    for department, monthly_data in data_dictionary.items():
        # Check if the selected month exists in the department's data
        if selected_month in monthly_data:
            # Get the active employee count for the selected month
            active_employee_count = monthly_data[selected_month].get('Active Employee', 0)
            # Add to the total count
            total_active_employees += active_employee_count
            total_active_employees = int(total_active_employees)

    # Create an HTML card with the total active employees
    html_card = f"""
    <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px; width: 200px;">
        <h3>Overall Total Active Employees</h3>
        <p>Month: {selected_month.strftime('%B %Y')}</p>
        <h2>{total_active_employees}</h2>
    </div>
    """

    return html_card


def employeeAverageGrowthRateCard(data_dictionary, department_name):
    # Initialize variables to calculate the average growth rate
    total_growth_rate = 0.0
    count = 0

    # If the user selects "All Departments"
    if department_name == "All Departments":
        total_average_growth_rate = 0.0
        department_count = 0

        # Iterate through each department in the data dictionary
        for dept, monthly_data in data_dictionary.items():
            dept_growth_rate = 0.0
            dept_count = 0

            # Iterate through each month's data for the current department
            for month, metrics in monthly_data.items():
                growth_rate = metrics.get('Growth Rate %:', np.nan)  # Use np.nan for missing values

                # Only consider valid growth rates (not NaN)
                if not pd.isna(growth_rate):
                    dept_growth_rate += growth_rate
                    dept_count += 1

            # Calculate the average growth rate for the current department
            if dept_count > 0:
                average_growth_rate = dept_growth_rate / dept_count
                total_average_growth_rate += average_growth_rate
                department_count += 1

        # Calculate the overall average growth rate across all departments
        average_growth_rate_all_departments = total_average_growth_rate / department_count if department_count > 0 else 0.0

        # Create an HTML card with the average growth rate for all departments
        html_card = f"""
        <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px; width: 250px;">
            <h3>Department wise Average Growth Rate</h3>
            <p>Department: {department_name}</p>
            <h2>{average_growth_rate_all_departments:.2f}%</h2>
        </div>
        """

    else:
        # Check if the department exists in the data dictionary
        if department_name in data_dictionary:
            monthly_data = data_dictionary[department_name]

            # Iterate through each month's data for the specified department
            for month, metrics in monthly_data.items():
                growth_rate = metrics.get('Growth Rate %:', np.nan)  # Use np.nan for missing values

                # Only consider valid growth rates (not NaN)
                if not pd.isna(growth_rate):
                    total_growth_rate += growth_rate
                    count += 1

            # Calculate the average growth rate
            average_growth_rate = total_growth_rate / count if count > 0 else 0.0

            # Create an HTML card with the average growth rate
            html_card = f"""
            <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px; width: 250px;">
                <h3>Department wise Average Growth Rate</h3>
                <p>Department: {department_name}</p>
                <h2>{average_growth_rate:.2f}%</h2>
            </div>
            """
        else:
            # If the department does not exist, return an error message
            html_card = f"""
            <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px; width: 250px;">
                <h3>Error</h3>
                <p>Department '{department_name}' not found.</p>
            </div>
            """

    return html_card


def averageAttritionRateCard(data, department_name):
    # Initialize variables to calculate the average retention rate
    total_attrition_rate = 0.0
    count = 0

    # Check if the specified department exists in the data dictionary
    if department_name in data:
        monthly_data = data[department_name]

        # Iterate through each month's data for the specified department
        for month, metrics in monthly_data.items():
            attrition_rate = metrics.get('Attrition Rate', np.nan)  # Use np.nan for missing values

            # Only consider valid retention rates (not NaN)
            if not pd.isna(attrition_rate):
                total_attrition_rate += attrition_rate
                count += 1

        # Calculate the average retention rate
        average_attrition_rate = total_attrition_rate / count if count > 0 else 0.0

        # Create an HTML card with the average retention rate
        html_card = f"""
        <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px; width: 250px;">
            <h3>Average Attrition Rate</h3>
            <p>Department: {department_name}</p>
            <h2>{average_attrition_rate:.2f}%</h2>
        </div>
        """
    else:
        # If the department does not exist, return an error message
        html_card = f"""
        <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px; width: 250px;">
            <h3>Error</h3>
            <p>Department '{department_name}' not found.</p>
        </div>
        """

    return html_card


def activeEmployeeInDepartmentCard(data, department, selected_month):
    # Check if the department exists in the data dictionary
    if department in data:
        # Get the monthly data for the department
        monthly_data = data[department]

        # Check if the selected month exists in the department's data
        if selected_month in monthly_data:
            # Get the active employee count for the selected month
            active_employee_count = monthly_data[selected_month].get('Active Employee', 0)
        else:
            active_employee_count = None
    else:
        active_employee_count = None

    # Create an HTML card with the active employee count
    if active_employee_count is not None:
        html_card = f"""
        <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px; width: 200px;">
            <h3>Department wise Active Employees</h3>
            <p>Department: {department}</p>
            <p>Month: {selected_month.strftime('%B %Y')}</p>
            <h2>{active_employee_count}</h2>
        </div>
        """
    else:
        html_card = f"""
        <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px; width: 200px;">
            <h3>Active Employees in {department} Department</h3>
            <p>Month: {selected_month.strftime('%B %Y')}</p>
            <h2>No data available</h2>
        </div>
        """

    return html_card


def generate_professional_line_chart(data, department):
    """
    Generates a professional-looking line chart comparing the 'Active Employee' count
    over time for the specified department using Plotly.

    Parameters:
    data (dict): The data dictionary containing department information.
    department (str): The department name for which the line chart is to be generated.

    Returns:
    fig: The plotly figure object that can be further customized or displayed
    """
    if department not in data:
        raise ValueError(f"Department '{department}' not found in data.")

    # Extract the relevant data for the specified department
    department_data = data[department]

    # Separate the timestamps and 'Active Employee' counts
    timestamps = list(department_data.keys())
    active_employee_counts = [department_data[ts].get('Active Employee', float('nan')) for ts in timestamps]

    # Filter out NaT values
    valid_data = [(ts, count) for ts, count in zip(timestamps, active_employee_counts) if pd.notna(count)]

    if not valid_data:
        raise ValueError(f"No valid data found for department '{department}'.")

    dates, active_employee_counts = zip(*valid_data)

    # Convert timestamps to pandas datetime
    dates = pd.to_datetime(dates)

    # Create a DataFrame for easier manipulation
    df = pd.DataFrame({
        'Date': dates,
        'Active Employees': active_employee_counts
    })

    # Calculate the trend line (3-month moving average)
    if len(df) >= 3:
        df['Trend'] = df['Active Employees'].rolling(window=3, min_periods=1).mean()
    else:
        df['Trend'] = df['Active Employees']

    # Create a professional color palette
    colors = {
        'main_line': '#1F77B4',  # Strong blue
        'trend_line': '#FF7F0E',  # Orange
        'background': '#F9F9F9',  # Light gray
        'grid': '#E0E0E0',  # Medium gray
        'title': '#2C3E50'  # Dark blue-gray
    }

    # Create the figure with custom theme
    fig = go.Figure()

    # Add the main data line
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Active Employees'],
        mode='lines+markers',
        name='Active Employees',
        line=dict(
            color=colors['main_line'],
            width=3
        ),
        marker=dict(
            size=8,
            line=dict(
                width=2,
                color=colors['main_line']
            )
        )
    ))

    # Add trend line
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Trend'],
        mode='lines',
        name='3-Month Trend',
        line=dict(
            color=colors['trend_line'],
            width=2,
            dash='dash'
        )
    ))

    # Add data points annotations if there are few points (optional)
    if len(df) <= 10:
        for i, row in df.iterrows():
            fig.add_annotation(
                x=row['Date'],
                y=row['Active Employees'],
                text=f"{int(row['Active Employees'])}",
                showarrow=False,
                yshift=15,
                font=dict(
                    size=11,
                    color="#303030"
                )
            )

    # Calculate min and max for y-axis with padding
    y_min = max(0, min(df['Active Employees']) - 1)
    y_max = max(df['Active Employees']) + 2

    # Update layout with professional styling
    fig.update_layout(
        title={
            'text': f'Active Employee Count Trends: {department}',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                family="Arial, sans-serif",
                size=21,
                color=colors['title']
            )
        },
        xaxis_title={
            'text': "",
            'font': dict(
                family="Arial, sans-serif",
                size=16,
                color="#606060"
            )
        },
        yaxis_title={
            'text': "Number of Active Employees",
            'font': dict(
                family="Arial, sans-serif",
                size=16,
                color="#606060"
            )
        },
        xaxis=dict(
            tickformat='%b %Y',
            tickangle=45,
            gridcolor=colors['grid'],
            showgrid=True,
            zeroline=False,
            showline=True,
            linecolor='#BEBEBE',
        ),
        yaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1 if (y_max - y_min) < 10 else None,
            gridcolor=colors['grid'],
            showgrid=True,
            zeroline=True,
            zerolinecolor='#BEBEBE',
            showline=True,
            linecolor='#BEBEBE',
            range=[y_min, y_max]
        ),
        legend=dict(
            x=0.78,
            y=1.2,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.8)',
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor='white',
        margin=dict(l=80, r=80, t=100, b=80),
        autosize=True,
        width=850,
        height=450,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial, sans-serif"
        )
    )

    # Add a subtle watermark/footer
    fig.add_annotation(
        xref='paper',
        yref='paper',
        x=0.5,
        y=-0.35,
        text=f"Graph Generated on {pd.Timestamp.now().strftime('%Y-%m-%d')}",
        showarrow=False,
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="gray"
        ),
        align='center',
    )

    # Disable Plotly's stock functionalities like panning and zooming
    fig.update_layout(
        dragmode=False,
        hovermode=False
    )

    return fig



def generate_grouped_bar_chart(data, department):
    """
    Generates a grouped bar chart comparing the 'Interview Scheduled' vs 'New Onboarded' counts over time for the specified department using Plotly.

    Parameters:
    data (dict): The data dictionary containing department information.
    department (str): The department name for which the grouped bar chart is to be generated.

    Returns:
    None
    """
    if department not in data:
        raise ValueError(f"Department '{department}' not found in data.")

    # Extract the relevant data for the specified department
    department_data = data[department]

    # Separate the timestamps, 'Interview Scheduled', and 'New Onboarded' counts
    timestamps = list(department_data.keys())
    interview_scheduled_counts = [department_data[ts].get('Interview Scheduled ', float('nan')) for ts in timestamps]
    new_onboarded_counts = [department_data[ts].get('New Onboarded', float('nan')) for ts in timestamps]

    # Filter out NaT values
    valid_data = [(ts, interview, onboarded) for ts, interview, onboarded in zip(timestamps, interview_scheduled_counts, new_onboarded_counts) if pd.notna(interview) and pd.notna(onboarded)]
    dates, interview_scheduled_counts, new_onboarded_counts = zip(*valid_data)

    # Convert timestamps to pandas datetime for better plotting
    dates = pd.to_datetime(dates)

    # Generate the grouped bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dates,
        y=interview_scheduled_counts,
        name='Interview Scheduled',
        marker_color='#5D8AA8'
    ))

    fig.add_trace(go.Bar(
        x=dates,
        y=new_onboarded_counts,
        name='New Onboarded',
        marker_color='#3CB371',  # Medium sea green
    ))

    fig.update_layout(
        title=dict(
            text=f'Interview Scheduled vs New Onboarded Over Time: {department}',
            x=0.5,  # Center the title horizontally
            y=0.95,  # Move the title down slightly
            xanchor='center',
            yanchor='top',
            font=dict(
                family="Arial, sans-serif",  # Set the font family
                size=21,  # Set the font size
                color="black"  # Set the font color (optional)
            )
        ),
        xaxis_title='Date',
        yaxis_title='Count',
        xaxis=dict(
            tickformat='%b%Y',
            dtick='M1',
            tickangle=45,
            tickmode='linear',
            tick0=0,
            tickvals=dates,
            ticktext=[d.strftime('%b%Y') for d in dates],
            tickfont=dict(size=12)
        ),
        barmode='group',
        legend=dict(
            x=0.75,
            y=1.2,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.5)',  # Optional: Add a semi-transparent background for the legend
            bordercolor='rgba(0, 0, 0, 0.5)',  # Optional: Add a semi-transparent border for the legend
        ),
        template='plotly',
        width=850,
        height=450
    )

    # Disable Plotly's default interactive features
    fig.update_layout(
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        dragmode=False,
    )

    return fig



def employee_pie_chart(data, month):
    """
    Creates a professional pie chart showing the distribution of active employees
    across different departments for a specified month using Plotly with an enhanced color palette.

    Parameters:
    - data: Dictionary containing department data with timestamps.
    - month: String in the format 'YYYY-MM-DD' representing the month for which
             the pie chart should be generated.

    Returns:
    - fig: Plotly figure object that can be displayed or further customized
    """
    # Convert the input month string to a Timestamp
    selected_month = pd.Timestamp(month)

    # Extract active employees data for the specified month
    active_employee_data = {}
    for department, records in data.items():
        if selected_month in records and 'Active Employee' in records[selected_month]:
            active_employee_data[department] = records[selected_month]['Active Employee']

    # Filter out departments with NaN values or zero active employees
    active_employee_data = {k: v for k, v in active_employee_data.items() if pd.notna(v) and v > 0}

    # Check if there is data to plot
    if not active_employee_data:
        print(f"No data available for the month: {month}")
        return None

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame({
        'Department': list(active_employee_data.keys()),
        'Employees': list(active_employee_data.values())
    })

    # Sort by number of employees (descending)
    df = df.sort_values('Employees', ascending=False)

    # Calculate total employees
    total_employees = df['Employees'].sum()

    # Calculate percentages
    df['Percentage'] = df['Employees'] / total_employees * 100

    # Custom rich color palette options - choose one of these
    # Vibrant professional palette
    color_palette2 = ['#2E5EAA', '#5E87B8', '#97A2C7', '#A4C2A5', '#5FAD56', '#F2C14E', '#F78154', '#B4436C', '#8F5DB3',
                      '#3D3B8E']

    # Choose which palette to use (you can easily switch between them)
    selected_palette = color_palette2

    # If we have more departments than colors, cycle through the colors
    if len(df) > len(selected_palette):
        selected_palette = selected_palette * (len(df) // len(selected_palette) + 1)
    colors = selected_palette[:len(df)]

    # Create the figure with subplots - one for pie chart, one for legend/stats
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "domain"}, {"type": "table"}]],
        column_widths=[0.6, 0.4]
    )

    # Add pie chart
    fig.add_trace(
        go.Pie(
            labels=df['Department'],
            values=df['Employees'],
            hole=0.4,  # Create a donut chart
            marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1.5)),
            textinfo='label+percent',
            hoverinfo='label+value+percent',
            textfont=dict(size=10, color='black', family="Arial, sans-serif"),  # Reduced font size
            insidetextorientation='radial',
            pull=[0.05 if i == 0 else 0 for i in range(len(df))],  # Pull out largest segment
        ),
        row=1, col=1
    )

    # Add table with department breakdown
    fig.add_trace(
        go.Table(
            header=dict(
                values=['Department', 'Employees'],
                fill_color=selected_palette[0],  # Use first color from palette for header
                align='left',
                font=dict(size=14, color='white', family="Arial, sans-serif")
            ),
            cells=dict(
                values=[
                    df['Department'],
                    df['Employees']
                ],
                fill_color=[['#F9F9F9'] * len(df)] * 2,
                align=['left', 'center'],
                font=dict(size=14, color='#333333', family="Arial, sans-serif"),
                height=28
            )
        ),
        row=1, col=2
    )

    # Add a gradient background to the chart
    fig.update_layout(
        title={
            'text': f'Active Employee Distribution: {selected_month.strftime("%B %Y")}',
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(family="Arial, sans-serif", size=22, color="#333333")
        },
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="right",
            x=0.98,
            font=dict(size=6, color="#333333", family="Arial, sans-serif")
        ),
        margin=dict(l=20, r=20, t=70, b=20),
        paper_bgcolor='white',
        plot_bgcolor='white',
        width=1000,
        height=600,
        annotations=[
            dict(
                text=f"<b>Total<br>{total_employees}</b>",
                x=0.21,
                y=0.5,
                font=dict(size=16, color='#333333', family="Arial, sans-serif"),
                showarrow=False
            ),
            dict(
                text=f"Data as of {selected_month.strftime('%d %b %Y')}",
                x=0.5,
                y=-0.05,
                xref="paper",
                yref="paper",
                font=dict(size=10, color='#777777', family="Arial, sans-serif"),
                showarrow=False
            )
        ],
        showlegend=False  # Hide legend since we're using table for details
    )

    # Add department count info
    fig.add_annotation(
        text=f"{len(df)} Departments",
        x=0.21,
        y=0.42,
        font=dict(size=12, color='#777777', family="Arial, sans-serif"),
        showarrow=False
    )

    return fig