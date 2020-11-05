# This script pulls from a job website and stores positions into a database. If there is a new posting it notifies the user.
# CNA 330
# Michael Horton, Mahorton@student.rtc.edu, 206-930-5206
# With help from Zachary Rubin and Justin Ellis
# collaborated with Eric, Dillion, Igor, Vlado, Mohammad, 


import mysql.connector
import sys
import json
import urllib.request
import os
import time

# Connect to database
# You may need to edit the connect function based on your local settings.
def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='jobhunter')
    return conn

# Create the table structure
def create_tables(cursor, table):
    ## Add your code here. Starter code below
    cursor.execute('''CREATE TABLE IF NOT EXISTS Jobs_found (id INT PRIMARY KEY auto_increment,
                        Type varchar(10), Title varchar(100), Description TEXT CHARSET utf8a, Job_id varchar(36),
                        Created_at DATE, Company varchar(100), location varchar(50),
                        How_to_apply varchar(1000)); ''')
    return

# Query the database.
# You should not need to edit anything in this function
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor

# Add a new job
def add_new_job(cursor, jobdetails):
    ## Add your code here
    Type = jobdetails['Type']
    Title = jobdetails['Title']
    Description = jobdetails['Description']
    Job_ID = jobdetails['Job_ID']
    Created_At = jobdetails['Created_At']
    Company = jobdetails['Company']
    Location = jobdetails['Location']
    How_To_Apply = jobdetails['How_To_Apply']
    query = cursor.execute("INSERT INTO jobs(ID, Type, Title, Description, Job_ID, Created_at, Company, Location, How_to_apply" ")"
                           "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (Type, Title, Description, Job_ID, Created_At, Company, Location, How_To_Apply))

    return query_sql(cursor, query)

# Check if new job
def check_if_job_exists(cursor, jobdetails):
    ## Add your code here
    Job_ID = jobdetails['ID']
    query = "SELECT * FROM jobs WHERE Job_ID = \"%s\"" % Job_ID
    return query_sql(cursor, query)

def delete_job(cursor, jobdetails):
    ## Add your code here
    Job_ID = jobdetails['ID']
    query = "DELETE FROM jobs WHERE Job_ID = \"%s\"" % Job_ID
    return query_sql(cursor, query)

# Grab new jobs from a website
def fetch_new_jobs(arg_dict):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query = "https://jobs.github.com/positions.json?" + "location=remote" ## Add arguments here
    jsonpage = 0
    try:
        contents = urllib.request.urlopen(query)
        response = contents.read()
        jsonpage = json.loads(response)
    except:
        pass
    return jsonpage

# Load a text-based configuration file
def load_config_file(filename):
    argument_dictionary = 0
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/FileIO.py
    rel_path = os.path.abspath(os.path.dirname(__file__))
    file = 0
    file_contents = 0
    try:
        file = open(filename, "r")
        file_contents = file.read()
    except FileNotFoundError:
        print("File not found, it will be created.")
        file = open(filename, "w")
        file.write("")
        file.close()

    ## Add in information for argument dictionary
    return argument_dictionary

# Main area of the code.
def jobhunt(cursor, arg_dict):
    # Fetch jobs from website
    jobpage = fetch_new_jobs(arg_dict)
    # print (jobpage)
    add_or_delete_jobs(jobpage, cursor)
    ## Add your code here to parse the job page

    ## Add in your code here to check if the job already exists in the DB

    ## Add in your code here to notify the user of a new posting

    ## EXTRA CREDIT: Add your code to delete old entries

# Setup portion of the program. Take arguments and set up the script
# You should not need to edit anything here.
def add_or_delete_job(jobpage, cursor)

def main():
    # Connect to SQL and get cursor
    conn = connect_to_sql()
    cursor = conn.cursor()
    create_tables(cursor, "table")
    # Load text file and store arguments into dictionary
    arg_dict = 0
    while(1):
        jobhunt(cursor, arg_dict)
        conn.commit()
        time.sleep(3600) # Sleep for 1h

if __name__ == '__main__':
    main()
