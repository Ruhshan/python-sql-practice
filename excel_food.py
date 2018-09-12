import sqlite3
from openpyxl import Workbook
# Creating connection to a .sqlite3 db. This will create the file when the script runs for the first time
conn = sqlite3.connect('db_big.sqlite3')
# Taking the cursor
c = conn.cursor()

# This is a flag for checking existance of violations and inspection tables
run_this = 0
try:
    # This block will be executed if the table inspection exists
    c.execute("SELECT COUNT(*) FROM violation")
    run_this = 1
except:
    print("Please run db_create.py First")

if run_this:
    # Querying database to retrieve required data
    c.execute('''select distinct violation_code, violation_description, count(violation_code) from violation group by violation_code;''')
    violations = c.fetchall()

    # Creating workbook
    wb = Workbook()
    ws = wb.active

    # Setting title of sheet
    ws.title = "Violations Types"

    # Creating first row
    ws.append(['Code','Description','Count'])

    # Adding other data rows
    for violation in violations:
        v = list(violation)
        ws.append(v)
    # Saving to file
    wb.save('ViolationTypes.xlsx')
    c.close()