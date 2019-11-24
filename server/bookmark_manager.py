import mysql_helper


def get_bookmarks(userID):
    sql_statement = "SELECT * FROM mybookmark WHERE userID = '" + userID  + "';"
    response = mysql_helper.select_statement(sql_statement)
    if not response:
        return [1]
    else:
        bookmarks_list = []
        for x in response:
            bookmarks_list.append({"BOOKMARK_ID" : x[0],
                                   "USER_ID" : x[1],
                                   "BOOKMARK_NAME": x[2],
                                   "STARTING_ADDR" : x[3],
                                   "ENDING_ADDR": x[4]})

        return [0, bookmarks_list]


def add_bookmarks(userID, starting_address, ending_address, bookmark_name):
    sql_statement = "INSERT INTO mybookmark(userID, bookmark_name, starting_address, ending_address) " \
                    "VALUES(%s, %s, %s, %s)"

    response = mysql_helper.sql_operation(sql_statement, [userID, bookmark_name, starting_address, ending_address])
    if not response:
        return 1
    else:
        return 0


def delete_bookmarks(userID, bookmark_name):
    sql_statement = "DELETE FROM mybookmark WHERE userID = %s AND bookmark_name = %s"
    response = mysql_helper.sql_operation(sql_statement, [userID, bookmark_name])
    if not response:
        return 1
    else:
        return 0
