import csv
from datetime import datetime


def csv_to_list(file_location):
    with open(file_location, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)


def display_list_simple(message, list_to_print):
    print('\t--- {} ---'.format(message))
    for i in list_to_print:
        print('\t\t{} {}: {} hours'.format(i['Last_Name'], i['First_Name'], i['Total_hours']))


def create_employee_hours_list(original_list):
    unpaid_lunch_break_time = 1.0
    employee_hours = list()
    for employee in original_list:
        first_name, last_name = employee['Name'].split(' ')
        # calculating the amount of total paid hours
        total_paid_hours = 0
        daily_hours = dict()
        for key, value in employee.items():
            if key in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
                if value != '':
                    starting_time, finish_time = value.split('-')
                    working_hours = datetime.strptime(finish_time, '%H:%M') - datetime.strptime(starting_time, '%H:%M')
                    # converting the result so hours
                    working_hours = working_hours.seconds/60/60 - unpaid_lunch_break_time
                    daily_hours['{}_hours'.format(key)] = working_hours
                    total_paid_hours += working_hours
                else:
                    daily_hours['{}_hours'.format(key)] = 0

        result = {'First_Name': first_name,
                  'Last_Name': last_name,
                  'Daily_hours': daily_hours,
                  'Total_hours': total_paid_hours
                  }
        employee_hours.append(result)

    return employee_hours


def create_under_40h_employee_list(employee_hours_list):
    under_40h_list = list()
    for employee in employee_hours_list:
        if employee['Total_hours'] < 40:
            under_40h_list.append({'First_Name': employee['First_Name'], 'Last_Name': employee['Last_Name'], 'Total_hours': employee['Total_hours'] })

    return under_40h_list


def calculate_weekend_hours(employee_hours_list):
    employee_weekend_hours = list()

    for employee in employee_hours_list:
        if employee['Daily_hours'].get('Saturday_hours') > 0 or employee['Daily_hours'].get('Sunday_hours') > 0:
            employee_weekend_hours.append({'First_Name': employee['First_Name'], 'Last_Name': employee['Last_Name'], 'Total_hours': employee['Daily_hours']['Saturday_hours'] + employee['Daily_hours']['Sunday_hours']})

    return employee_weekend_hours


def calculate_overtime(employee_hours_list):
    employee_overtime = list()

    for employee in employee_hours_list:
        _regular = 0
        _overtime = 0
        _double = 0
        for day, hours in employee['Daily_hours'].items():
            if 8 < hours <= 12:
                # overtime
                _overtime += hours - 8
            elif hours > 12:
                # double
                _double += hours -12
            else:
                # rehular
                _regular += hours

        employee_overtime.append({'First_Name': employee['First_Name'], 'Last_Name': employee['Last_Name'], 'Regular_hours': _regular, 'Overtime': _regular, 'Double': _double})

    return employee_overtime


def main():
    # reading the csv
    timesheet = csv_to_list('data/timesheet.csv')

    if timesheet is None:
        raise ("[Error] no timesheet object")

    employee_hours_list = create_employee_hours_list(timesheet)
    # sorting the list by Last name and First Name respectively
    # skipped 2nd sorting layer for First name due to time limitation
    employee_hours_list = sorted(employee_hours_list, key=lambda d: d['Last_Name'])

    # Task 1
    display_list_simple(message='List of all the employees and their total weekly working paid hours (lunch break time not included)', list_to_print=employee_hours_list)

    print('\n')
    # Task 2
    display_list_simple(message='List of all the employees that worked less than 40h in the week and total weekly working paid hours (lunch break time not included)', list_to_print=create_under_40h_employee_list(employee_hours_list))

    # Task 3
    employees_weekend = calculate_weekend_hours(employee_hours_list)
    print('\n')
    display_list_simple(message='List of all the employees that worked at the weekend and total weekend working paid hours (lunch break time not included)', list_to_print=employees_weekend)

    # Task 3
    employees_overtime = calculate_overtime(employee_hours_list)
    print('\n')
    # displaying the results with a separate display func


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
