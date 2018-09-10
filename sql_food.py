import sqlite3

# Creating connection to a .sqlite3 db. This will create the file when the script runs for the first time
conn = sqlite3.connect('db_big.sqlite3')
# Taking the cursor
c = conn.cursor()

# This is a flag for checking existance of violations and inspection tables
run_this = 0
try:
    # This block will be executed if the table inspection exists
    c.execute("SELECT COUNT(activity_date) FROM inspection")
    run_this = 1
except:
    print("Please run db_create.py First")

# This block will only runnable if violations and inspection table exists
if run_this == 1:
    # Querying distinct business having at least 1 violation
    c.execute('''select distinct inspection.facility_name
              from inspection join  violation 
              on inspection.serial_number = violation.serial_number where violation.points >= 1;''')

    # Loading the query result in the facilities variable
    facilities = c.fetchall()
    ct = 1
    # Printing business names having at least 1 violation
    for f in facilities:
        ct += 1
        print(ct, f[0])

    try:
        # Checking if this script has been already run by evaluation the existance of Previous violation table
        c.execute('SELECT COUNT(*) from "Previous Violation"')
    except:
        # Creating Previous violation table as stated in instruction
        c.execute('''create table "Previous Violation" AS
                    select distinct inspection.facility_name,
                                    inspection.facility_address,
                                    inspection.facility_zip,
                                    inspection.facility_city
                    from inspection
                    join  violation on inspection.serial_number = violation.serial_number
                    where violation.points >= 1;
                  ''')
        # Saving changes to database
        conn.commit()

    # Querying businesses name and count of their violation
    c.execute('''select inspection.facility_name, sum(violation.points) as c
                from inspection join  violation on
                inspection.serial_number = violation.serial_number
                where violation.points >= 1 group by inspection.facility_name
                order by c desc ;
              ''')

    violation_counts = c.fetchall()
    # Printing the business name and their violation count
    for violation in violation_counts:
        print("Business: {}, Number of Violation: {}".format(violation[0], violation[1]))

c.close()