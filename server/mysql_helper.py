import mysql.connector
from mysql.connector import Error



def open_db():
    try:
        connection = mysql.connector.connect(host='35.247.140.36',
                                             database='ICT2101',
                                             user='root',
                                             password='felixthecat')

        if connection.is_connected():
                db_Info = connection.get_server_info()
                # print("Connection successful!")
                return connection

    except Error as e:
            print("Error while connecting to MySQL", e)

def close_db(connection):
    try:
        cursor = connection.cursor()
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")
    except Error as e:
            print("Error while closing MYSQL DB", e)

def select_statement(sql_statement):
    connection = open_db()
    try:
        cursor = connection.cursor()
        cursor.execute(sql_statement)
        records = cursor.fetchall()
        close_db(connection)
        return records
    except Error as e:
        print("error reading data from mysql table", e)
        return False



"""
Author:     Felix Wang
Purpose:    Perform INSERT, UPDATE or DELETE SQL Operations
Parameters: sql_statement: string, values ['values', 'values']
Returns:    If method work as expected:  True  
            If method fails to function: False
"""
def sql_operation(sql_statement, values):
    connection = open_db()
    try:
        cursor = connection.cursor()
        cursor.execute(sql_statement, values)
        connection.commit()
        close_db(connection)
        return True
    except Error as e:
        print("Error performing operation on from MySQL table", e)
        return False


def check_if_record_exist(sql_statement):
    connection = open_db()
    try:
        cursor = connection.cursor()
        cursor.execute(sql_statement)
        records = cursor.fetchall()
        close_db(connection)
        if len(records) > 0:
            return True
        else:
            return False
    except Error as e:
        print("error reading data from mysql table", e)
