import mysql_helper



def add_ratings(starting_address, ending_address, rating):
    sql_statement = "INSERT INTO MYRATINGS (starting_address, ending_address, rating) VALUES(%s, %s, %s)"
    response = mysql_helper.sql_operation(sql_statement,[starting_address, ending_address, str(rating)])
    if not response:
        return 1
    return 0


def get_ratings(starting_address, ending_address):
    sql_statement = "SELECT starting_address, ending_address, AVG(rating) FROM myratings " \
                    "WHERE starting_address = '" + starting_address + "' " \
                    "AND ending_address = '" + ending_address + "'GROUP BY starting_address"


    response = mysql_helper.select_statement(sql_statement)
    print (response)
    if response == False:
        return [1]
    elif len(response) == 0:
        return [0, {"STARTING_ADDRESS" : starting_address,
                "ENDING_ADDRESS" : ending_address,
                "AVG_RATING" : "0"}]
    else:
        return [0, {"STARTING_ADDRESS" : response[0][0],
                    "ENDING_ADDRESS" : response[0][1],
                    "AVG_RATING" : str(response[0][2])}]


def delete_bookmarks(userID, bookmark_name):
    sql_statement = "DELETE FROM mybookmark WHERE userID = %s AND bookmark_name = %s"
    response = mysql_helper.sql_operation(sql_statement, [userID, bookmark_name])
    if not response:
        return 1
    else:
        return 0