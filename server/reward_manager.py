from rewards import rewardsClass
import datetime
# from datetime import *
import mysql_helper


"""
Author:     Pravinraj
Purpose:    Retrieves a reward_object
Parameters: reward_id : int
Returns:    If method work as expected:  Reward Object 
            If method fails to function: False
"""
def get_reward_by_id(reward_id):
    sql_statement = "SELECT * FROM myrewards WHERE rewardId = '" + str(reward_id) + "';"

    try:
        record = mysql_helper.select_statement(sql_statement)[0]
    except IndexError:
        print("ERROR: Reward ID does not exist")
        return False
    reward = rewardsClass(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
    return reward

def get_all_rewards():
    sql_statement = "SELECT * FROM myrewards;"

    response = mysql_helper.select_statement(sql_statement)
    if not response:
        return [1]
    rewards_list = []
    for record in response:
        reward = rewardsClass(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
        rewards_list.append(reward)
    return [0, rewards_list]


"""
Author:     Pravinraj
Purpose:    User redeems a reward from the marketplace
Parameters: user_id : int, reward_id : int
Returns:    If method work as expected: True  
            If method fails to function:False
"""


def redeem_reward(user_obj, reward_obj):
    # CHECK IF THERE IS SUFFICIENT H-TOKEN
    if int(user_obj.HTokens) < int(reward_obj.RewardHToken):
        print("ERROR: Insufficient H-Tokens")
        return 10

    # IF REWARD DOES NOT EXIST
    reward = get_reward_by_id(reward_obj.RewardId)

    # ADDING REWARD INTO USER'S INVENTORY
    sql_statement = "INSERT INTO myrewardinventory (userId, rewardId, rewardExpiry, isRedeemed) " \
                    "VALUES (%s, %s, %s, %s)"
    expiry_date = get_expiry_date(int(reward.RewardDuration))
    data_values = [user_obj.Id, reward_obj.RewardId, expiry_date, 'N']
    sql_response = mysql_helper.sql_operation(sql_statement, data_values)
    if not sql_response:
        print(sql_response)
        return False

    # UPDATE THE USER HTOKEN BALANCE
    remaining_HTokens = user_obj.HTokens - int(reward_obj.RewardHToken)
    sql_statement = "UPDATE myuser SET hTokens = %s WHERE id = %s"
    data_values = [remaining_HTokens, user_obj.Id]
    sql_response = mysql_helper.sql_operation(sql_statement, data_values)
    if not sql_response:
        print(sql_response)
        return 1

    print ("SUCCESS: Obtained rewards successfully.")
    return 0


"""
Author:     Pravinraj
Purpose:    To get the expiry date of the reward
Parameters: days_taken: int
returns:    expiry date : string (e.g 2019-12-01 15:05:29.565763)
"""
def get_expiry_date(days_taken):
    end_timestamp = datetime.datetime.now() + datetime.timedelta(days=days_taken)
    return str(end_timestamp)


def get_endtime(userID, voucherID):
    sql_statement = "SELECT endTime FROM myrewardinventory WHERE userId = " + userID + " AND voucherId = " + voucherID + ";"
    print(sql_statement)
    response = mysql_helper.select_statement(sql_statement)
    print("firstLAYER", response[0][0])

    time = datetime.datetime.strptime(response[0][0], "%Y-%m-%d %H:%M:%S")
    time = time.strftime("%I:%M %p")
    print(time)
    if not time:
        return 1
    else:
        return time

def get_reward_user(userID):
    sql_statement = "SELECT * FROM myrewardinventory ri INNER JOIN myrewards r ON ri.rewardId = r.rewardId where " \
                    "ri.userID = '" + userID + "';"

    response = mysql_helper.select_statement(sql_statement)
    if response == False:
        return [1]
    response_list = []
    for record in response:
        if record[5] != None:
            time = datetime.datetime.strptime(record[5], "%Y-%m-%d %H:%M:%S")
            time = time.strftime("%I:%M %p")
            print(time)
        else:
            time = record[5]
        response_list.append({"VOUCHER_ID" : record[0],
                              "REWARD_ID" : record[2],
                              "REWARD_EXPIRY" : record[3],
                              "END_TIME" : time,
                              "REWARD_NAME" : record[7],
                              "REWARD_DESCRIPTION" : record[8],
                              "REWARD_IMG" : record[10],
                              "REWARD_CATEGORY" : record[12]})
    return [0, response_list]

def update_endtime(userID, voucherID):
    sql_statement = "UPDATE myrewardinventory SET endTime = ADDTIME(current_timestamp, \"00:05:00\") WHERE userID = %s AND voucherID = %s;"
    print(userID, voucherID)
    print(sql_statement)
    if not mysql_helper.sql_operation(sql_statement, [str(userID), str(voucherID)]):
        return 1
    else:
        return 0

#deletes rewards which has an expired endtime
def update_rewards(userID):
    sql_statement = "DELETE FROM myrewardinventory WHERE userId=%s and endTime < current_timestamp;"
    if not mysql_helper.sql_operation(sql_statement, [str(userID)]):
        return 1
    else:
        return 0

# if __name__ == '__main__':
#     print(obtain_reward(1, 1))
#     # print(get_expiry_date(30))
#     pass
