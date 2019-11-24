import mysql_helper
import math
from random import random
from twilio.rest import Client
import mysql_helper
from user import userClass


def getHeroAvailability(UserID):
    sql_statement = "SELECT isAvailable FROM myuser WHERE id = '" + str(UserID) + "';"
    response = mysql_helper.select_statement(sql_statement)
    if not response:
        return [1]
    return [0, response[0][0]]

def updateHToken(HToken, UserID, method):
    sql_statement = "SELECT hTokens FROM myuser WHERE id = '" + str(UserID) + "';"
    response = mysql_helper.select_statement(sql_statement)
    if not response:
        return 1
    current_HToken = int(response[0][0])

    # Add
    if method is 1:
        current_HToken += int(HToken)
    # Subtract
    if method is 0:
        current_HToken -= HToken

    # Update back into the database
    sql_statement = "UPDATE myuser set hTokens = %s WHERE id = %s;"
    mysql_helper.sql_operation(sql_statement, [str(current_HToken), str(UserID)])
    if not response:
        return 1
    return 0


"""
Author:     Felix Wang
Purpose:    Return a User Object
Returns:    User Object
Parameters: mobile_number : string
"""
def getUserObjMobile(mobile_number):
    sql_statement = "SELECT * FROM myuser WHERE contactNumber = '" + str(mobile_number) + "';"

    # self, id, username, fullName, contactNumber, email, age, equipment, powerLevel, hTokens, steps
    record = mysql_helper.select_statement(sql_statement)[0]
    user = userClass(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7],
                     record[8], record[9])
    return user

"""
Author:     Felix Wang
Purpose:    Return a User Object
Returns:    User Object
Parameters: User id : int
"""
def getUserObj(id):
    sql_statement = "SELECT * FROM myuser WHERE id = '" + str(id) + "';"

    # self, id, username, fullName, contactNumber, email, age, equipment, powerLevel, hTokens, steps
    record = mysql_helper.select_statement(sql_statement)[0]
    user = userClass(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7],
                     record[8], record[9])
    return user


def updateHeroPower(userID, powerLevel):
    sql_statement = "UPDATE myuser set powerLevel = %s WHERE id = %s ;"
    response = mysql_helper.sql_operation(sql_statement, [str(powerLevel), str(userID)])
    if not response:
        return 1
    return 0


def check_user_id(user_id):
    sql_statement = "SELECT id FROM myuser WHERE id = '" + str(user_id) + "';"
    if not mysql_helper.check_if_record_exist(sql_statement):
        print("ERROR: Invalid User ID")
        return False
    return True


def check_otp(mobile_number, OTP):
    sql_statement = "SELECT * FROM myotp WHERE phone_number = '" + mobile_number + "' AND OTP = '" + OTP + "';"
    if mysql_helper.check_if_record_exist(sql_statement):
        return 0
    else:
        return 11

def add_user(password, username, email_address, age, contact_number):
    sql_statement = "INSERT INTO myuser(username, contactNumber, emailAddress, age, password) " \
                    "VALUES(%s, %s, %s, %s, %s)"
    if mysql_helper.sql_operation(sql_statement, (username, contact_number, email_address, age, password)):
        sql_statement = "SELECT id FROM myuser WHERE username = '" + username + "';"
        sql_response = mysql_helper.select_statement(sql_statement)
        if not sql_response:         # If it doesnt work
            return 1
        else:
            print(sql_response[0][0])
            return 0, sql_response[0][0]
    else:
        return 1

def check_username_exist(username):
    sql_statement = "SELECT username FROM myuser WHERE username = '" + username + "';"
    if mysql_helper.check_if_record_exist(sql_statement):
        return 1
    else:
        return 0


def generateOTP(mobile_number):
    OTP = generateOTPCode()

    """ Check if details exists"""
    sql_statement = "SELECT * FROM myotp WHERE phone_number = '" + mobile_number + "';"
    if mysql_helper.check_if_record_exist(sql_statement):
        sql_statement = "UPDATE myotp SET OTP = %s WHERE phone_number = %s"
        data = (OTP,  mobile_number)
        if not mysql_helper.sql_operation(sql_statement, data):
            return 1
        print("Record Exists! Update instead!")

    else:
        sql_statement = "INSERT INTO myotp (phone_number, OTP) VALUES(%s, %s)"
        phone_data = (mobile_number, OTP)
        if not mysql_helper.sql_operation(sql_statement, phone_data):
            return 1
        print("Record Doesn't exist, Insert Record")

    if send_message(OTP, mobile_number):
        return 0
    else:
        return 2


def send_message(OTP, mobile_number):
    account_sid = 'AC57da2a42bd51adc49b3c60caf4748d1b'
    auth_token = '2dfef7e529081bc02666b9bc4a2d357d'
    client = Client(account_sid, auth_token)
    try:
        message = client.messages \
            .create(
            body="Your Gialey verification code is: " + OTP,
            from_='+12565783233',
            to="+65" + mobile_number
        )
        return True
    except:
        print("Send OTP Message Failed")
        return False

def generateOTPCode():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random() * 10)]
    return OTP

"""
Author:     Felix Wang
Params:     userDict {"emailAddress": "felixwrh13@gmail.com", "age": "22", "contactNumber" : None, "password" : None}
Purpose:    Update the user details
Return:     True

"""
def updateProfile(user_dict, userId):
    # Remove the keys in the dictionary that do not have a value.
    new_dict = {}
    for details in user_dict:
        if user_dict[details] is not None:
           new_dict[details] = user_dict[details]

    if len(new_dict) is 0:
        print("WARNING: No details to be updated. Exiting method now.")
        return True

    # Construct the SQL Statement
    sql_statement_first_half = "UPDATE myuser SET "
    sql_statement_next_half = " WHERE id = %s;"
    data_values = []

    counter = 1
    for details in new_dict:
        if len(new_dict) == counter:
            sql_statement_first_half += details + " = %s"
        else:
            sql_statement_first_half += details + " = %s, "
        data_values.append(new_dict[details])
        counter += 1

    # Update user profile into MYSql Database.
    data_values.append(str(userId))
    sql_statement = sql_statement_first_half + sql_statement_next_half
    mysql_helper.sql_operation(sql_statement, data_values)
    print("SUCCESS: User information updated successfully")
    return True


if __name__ == "__main__":
    # send_message("12345", "+6592233511")
    add_user('_Pass1234', 'kaixiangjiao', 'kx@gmail.com', 20, '92233522')

    # user_dict = {"emailAddress": "felixwrh13@gmail.com", "age": "22", "contactNumber" : None, "password" : '_Pass1234'}
    # updateProfile(user_dict, 1)
    # user_dict = {"emailAddress": None, "age": None, "contactNumber": None,
    #              "password": None}
    #
    # updateProfile(user_dict, 1)