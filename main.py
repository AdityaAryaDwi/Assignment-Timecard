import pandas as pd
import sys
# Reading the CSV file into a DataFrame
file_path = "Assignment_Timecard.csv"
df = pd.read_csv(file_path)

# Convert the 'Time' and 'Time Out' columns to datetime objects with the specified format
df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %I:%M %p', errors='coerce')
df['Time Out'] = pd.to_datetime(df['Time Out'], format='%m/%d/%Y %I:%M %p', errors='coerce')

# Convert 'Timecard Hours (as Time)' to timedelta format, handling errors
df['Timecard Hours (as Time)'] = pd.to_timedelta(df['Timecard Hours (as Time)'], errors='coerce')

# Function to check if an employee worked for 7 consecutive days
def check_consecutive_days(employee_data):
    return employee_data['Time'].diff().dt.days.eq(1).sum() >= 6

# Function to check if an employee has less than 10 hours between shifts but greater than 1 hour
def check_time_between_shifts(employee_data):
    time_diff = employee_data['Time'].diff().dt.total_seconds()
    return any((time_diff > 3600) & (time_diff < 36000))

# Function to check if an employee has worked for more than 14 hours in a single shift
def check_long_shift(employee_data):
    return (employee_data['Time Out'] - employee_data['Time']).dt.total_seconds().max() > 50400

# Identify employees who have worked for 7 consecutive days
df['DaysDiff'] = df.groupby('Employee Name')['Time'].diff().dt.days
consecutive_days_employees = df[df['DaysDiff'] == 1]['Position ID'].unique()

# Identify employees with less than 10 hours between shifts but greater than 1 hour
df['TimeBetweenShifts'] = (df['Time'] - df['Time Out'].shift()).dt.total_seconds() / 3600
time_between_shifts_employees = df[(df['TimeBetweenShifts'] < 10) & (df['TimeBetweenShifts'] > 1)]['Position ID'].unique()

# Identify employees who have worked for more than 14 hours in a single shift
long_shift_employees = df[(df['Time Out'] - df['Time']).dt.total_seconds() / 3600 > 14]['Position ID'].unique()

# Print the results
print("Analysis Results:")

# Print employees who have worked for 7 consecutive days
print("\nEmployees who have worked for 7 consecutive days:")
for position_id in consecutive_days_employees:
    employees = df[df['Position ID'] == position_id]['Employee Name'].unique()
    print(f"{position_id}, {', '.join(employees)}")

# Print employees with less than 10 hours between shifts but greater than 1 hour
print("\nEmployees with less than 10 hours between shifts but greater than 1 hour:")
for position_id in time_between_shifts_employees:
    employees = df[df['Position ID'] == position_id]['Employee Name'].unique()
    print(f"{position_id}, {', '.join(employees)}")

# Print employees who have worked for more than 14 hours in a single shift
print("\nEmployees who have worked for more than 14 hours in a single shift:")
for position_id in long_shift_employees:
    employees = df[df['Position ID'] == position_id]['Employee Name'].unique()
    print(f"{position_id}, {', '.join(employees)}")

# Redirect console output to a file    
with open('output.txt', 'w') as f:
    sys.stdout = f

    # Your existing code for printing the results
    print("Analysis Results:")
    print("\nEmployees who have worked for 7 consecutive days:")
    for position_id in consecutive_days_employees:
        employees = df[df['Position ID'] == position_id]['Employee Name'].unique()
        print(f"{position_id}, {', '.join(employees)}")

    print("\nEmployees with less than 10 hours between shifts but greater than 1 hour:")
    for position_id in time_between_shifts_employees:
        employees = df[df['Position ID'] == position_id]['Employee Name'].unique()
        print(f"{position_id}, {', '.join(employees)}")

    print("\nEmployees who have worked for more than 14 hours in a single shift:")
    for position_id in long_shift_employees:
        employees = df[df['Position ID'] == position_id]['Employee Name'].unique()
        print(f"{position_id}, {', '.join(employees)}")

# Reset console output to its original state
sys.stdout = sys.__stdout__
