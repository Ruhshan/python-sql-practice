import sqlite3
import openpyxl

# Creating connection to a .sqlite3 db. This will create the file when the script runs for the first time
conn = sqlite3.connect('db_big.sqlite3')
# Taking the cursor
c = conn.cursor()

try:
    # This block will be executed if the table inspection exists
    c.execute("SELECT * FROM inspection")
except:
    # If the table inspection is not already created this will create the table
    c.execute('''CREATE TABLE inspection
             (activity_date DATE,
             employee_id VARCHAR(12),
             facility_address VARCHAR(50),
             facility_city CHARACTER(20),
             facility_id VARCHAR(12),
             facility_name VARCHAR(20),
             facility_state CHARACTER(5),
             facility_zip VARCHAR(15),
             grade CHARACTER(5),
             owner_id VARCHAR(15),
             owner_name VARCHAR(20),
             pe_description TEXT,
             program_element_pe INT,
             program_name VARCHAR(20),
             program_status CHARACTER(8),
             record_id VARCHAR(15),
             score INT,
             serial_number VARCHAR(15),
             service_code INT,
             service_description CHARACTER(50)
             )''')

try:
    # This block will be executed if the table violation exists
    c.execute("SELECT * FROM violation")
except:
    # This will create the table if it doesn't exists
    c.execute('''CREATE TABLE violation
              (
              points INT,
              serial_number VARCHAR(15),
              violation_code VARCHAR(10),
              violation_description text,
              violation_status CHARACTER(20)
              )''')

# This is trying to count how many rows are there in the inspection table
c.execute("SELECT COUNT(*) from inspection")
inspections = c.fetchone()[0]
# When inspections is 0 that means the table is not populated then this block will insert data rows into table
if inspections == 0:
    # Loading the excel
    book_inspection = openpyxl.load_workbook('inspections.xlsx')
    # Selecting the active workbook
    sheet = book_inspection.active
    # Referencing the rows
    rows = sheet.rows

    ct = 0
    # Template query for insertion which is used lated
    insert_into_inspection = '''INSERT INTO inspection VALUES ({})'''
    for row in rows:
        # Because first row is the titles of columns, so we are ignoring this
        if ct != 0:
            values = []
            for cell in row:
                cell_value = str(cell.value)
                cell_value = cell_value.replace('"', "'")

                values.append(' "{}" '.format(cell_value))
            values_for_query = ','.join(values)

            final_query = insert_into_inspection.format(values_for_query)
            try:
                c.execute(final_query)
            except:
                print(final_query)
                break
        ct=1
    # This will save the changes in the database
    conn.commit()

# This is trying to count how many rows are there in the violation table
c.execute("SELECT COUNT(*) from violation")
violations = c.fetchone()[0]

# When violations is 0 that means the table is not populated then this block will insert data rows into table
if violations == 0:
    book_violation = openpyxl.load_workbook("violations.xlsx")
    sheet = book_violation.active
    rows = sheet.rows
    ct = 0
    insert_into_violation = '''INSERT INTO violation VALUES ({})'''
    for row in rows:
        if ct != 0:
            values = []
            for cell in row:
                cell_value = str(cell.value)
                cell_value = cell_value.replace('"', "'")

                values.append(' "{}" '.format(cell_value))
            values_for_query = ','.join(values)

            final_query = insert_into_violation.format(values_for_query)

            c.execute(final_query)
        ct = 1
    conn.commit()
# closing connection to the database
c.close()

