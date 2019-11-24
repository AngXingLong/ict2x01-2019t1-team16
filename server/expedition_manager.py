import mysql_helper
from expedition import expeditionClass
import user_manager
import datetime
import random
import unittest

"""
Send in a User Object
"""



"""
Author:     Felix Wang
Purpose:    Returns a list of Expedition Objects
Returns:    List of Expedition Objects
Parameters: hero_power_level : int
"""
def getExpeditionByID(expedition_id):

    sql_statement = "SELECT * FROM myexpedition WHERE expeditionID = '" + expedition_id + "';"
    try:
        ex = mysql_helper.select_statement(sql_statement)[0]
    except IndexError:
        print("ERROR: Expedition ID does not exist.")
        return [1]

    expedition = expeditionClass(ex[0], ex[1], ex[2], ex[3], ex[4], ex[5], ex[6], 'Y')
    return [0, expedition]


"""
Author:     Felix Wang
Purpose:    Returns a list of Expedition Objects
Returns:    List of Expedition Objects
Parameters: User_OBJ
"""
def getExpeditions(User):
    expeditionObjList = []
    sql_statement = "SELECT * FROM myexpedition"
    expeditionList = mysql_helper.select_statement(sql_statement)
    for ex in expeditionList:
        expedition = expeditionClass(ex[0], ex[1], ex[2], ex[3], ex[4], ex[5], ex[6], checkEligibleExpedition(ex[1], User.PowerLevel))
        expeditionObjList.append(expedition)
    return expeditionObjList

"""
Author:     Felix Wang 
Purpose:    Checks if user is eligible for expedition
Returns:    True (Eligible) / False (Illegible)
Parameter:  required_power_level : int, hero_power_level: int
"""
def checkEligibleExpedition(required_power_level, hero_power_level):
    if required_power_level <= hero_power_level:
        return True
    else:
        return False

"""
Author:     Felix Wang
Purpose:    Start Expedition - Set the start and end time of the expedition
"""

"** TESTING **"
def startExpedition(userID, expeditionID):

    # Get the Expedition ID.
    response = getExpeditionByID(expeditionID)
    if not response[0] == 0:
        print("ERROR: Expedition ID does not exist.")
        return False

    expedition_obj = response[1]
    # Get the start and end timings (start_timing, end_timing)
    timings = getTiming(expedition_obj.TimeTaken)

    # Get a randomized HToken value. +50 or -50)
    randomizedHToken = randomizeHToken(expedition_obj.HToken)

    # Insert record into myUserExpedition table.
    values = [userID, 'Y', expeditionID, timings[0], timings[1], randomizedHToken]
    sql_statement = "INSERT INTO myuserexpedition (userId, isOngoing, expeditionId, startTime, endTime, hTokens) " \
                    "VALUES (%s, %s, %s, %s, %s, %s)"

    response = mysql_helper.sql_operation(sql_statement, values)
    if not response:
        return 1
    print("Insertion into myUserExpedition successful")

    # Need to disable user expedition status by updating the table to 'N'
    sql_statement = "UPDATE myuser SET isAvailable = %s WHERE id = %s"
    values = ['N', userID]
    response = mysql_helper.sql_operation(sql_statement, values)
    if not response:
        return 1
    print("User availability updated to 'N'")
    return 0

"""
Author:     Felix Wang 
Purpose:    Checks if user is eligible for expedition
Returns:    True (Eligible) / False (Illegible)
Parameter:  required_power_level : int, hero_power_level: int
"""
def randomizeHToken(HToken):
    return HToken + random.randint(-50, 50)

"""
Author:     Felix Wang 
Purpose:    Checks if user is eligible for expedition
Returns:    True (Eligible) / False (Illegible)
Parameter:  required_power_level : int, hero_power_level: int
"""
def getTiming(timeTaken):
    start_timestamp = datetime.datetime.now()
    end_timestamp = datetime.datetime.now() + datetime.timedelta(minutes = timeTaken)
    return start_timestamp, end_timestamp


"""
Gets ongoing expeditions and returns it.
"""
def get_ongoing_expeditions(userID):
    sql_statement = "SELECT * FROM myuserexpedition as ue INNER JOIN myexpedition as e on ue.expeditionId = e.expeditionId WHERE ue.userId = '" + str(userID) + "' AND ue.isOngoing = 'Y';"
    response = mysql_helper.select_statement(sql_statement)
    if not response:
        return [1]
    return [0, {"USER_ID": response[0][0],
                "IS_ONGOING": response[0][1],
                "EXPEDITION_ID": response[0][2],
                "START_TIME": response[0][3],
                "END_TIME": response[0][4],
                "H_TOKENS": response[0][5],
                "POWER_LEVEL": response[0][8],
                "IMAGE": response[0][9],
                "DESCRIPTION": response[0][10],
                "TITLE": response[0][11],
                "TIME_TAKEN": response[0][12],
                "EST_H_TOKEN" : response[0][13]}]


"""
Gets completed expeditions and returns it.
"""
def get_completed_expeditions(userID):
    sql_statement = "SELECT * FROM myuserexpedition as ue INNER JOIN myexpedition as e on ue.expeditionId = e.expeditionId WHERE ue.userId = '" + str(
        userID) + "' AND ue.isOngoing = 'P';"
    response = mysql_helper.select_statement(sql_statement)
    if not response:
        return [1]
    return [0, {"USER_ID": response[0][0],
                "IS_ONGOING": response[0][1],
                "EXPEDITION_ID": response[0][2],
                "START_TIME": response[0][3],
                "END_TIME": response[0][4],
                "H_TOKENS": response[0][5],
                "POWER_LEVEL": response[0][8],
                "IMAGE": response[0][9],
                "DESCRIPTION": response[0][10],
                "TITLE": response[0][11],
                "TIME_TAKEN": response[0][12],
                "EST_H_TOKEN" : response[0][13]}]


"""
End User Expedition. Update isAvailable to 'P' (Pending) and set expedition isongoing to 'N' 
"""
def end_expedition(userID):
    sql_statement = "UPDATE myuser set isAvailable = %s WHERE id = %s"
    response = mysql_helper.sql_operation(sql_statement, ['P', str(userID)])
    if not response:
        print("First Statement has errors")
        return 1
    sql_statement = "UPDATE myuserexpedition set isOngoing = %s WHERE userId = %s and isOngoing = %s"
    print(sql_statement)
    response = mysql_helper.sql_operation(sql_statement, ['P', str(userID), 'Y'])
    if not response:
        print("Second statement has error")
        return 1
    return 0

"""
End User Expedition. Update isAvailable to 'P' (Pending) and set expedition isongoing to 'N' 
"""
def complete_expedition(userID):
    sql_statement = "UPDATE myuser set isAvailable = %s WHERE id = %s"
    response = mysql_helper.sql_operation(sql_statement, ['Y', str(userID)])
    if not response:
        print("First Statement has errors")
        return 1
    sql_statement = "UPDATE myuserexpedition set isOngoing = %s WHERE userId = %s and isOngoing = %s"
    print(sql_statement)
    response = mysql_helper.sql_operation(sql_statement, ['N', str(userID), 'P'])
    if not response:
        print("Second statement has error")
        return 1
    return 0



