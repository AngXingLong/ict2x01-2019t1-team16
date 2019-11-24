import mysql_helper
import hero_manager
import user_manager

"""
Author:     Yuma Lee
Purpose:    Updates the milestone progress, Adds equipment into Hero's inventory
Parameters: user_id : int
Returns:    If method work as expected:   equipment_object  
            If method fails to function:  False
"""

def reached_milestone(userId):
    # Get the user's current milestone
    milestone_number = get_milestone_number(userId)
    if milestone_number > 3:
        print("WARNING: User has already reached 3 milestones for the day.")
        return [6]

    # Increment and add the user milestone
    sql_statement = "UPDATE myUser SET milestone = %s WHERE id = '" + str(userId) + "';"
    data_values = [str(milestone_number + 1)]
    mysql_helper.sql_operation(sql_statement, data_values)

    # Generate a random equipment.
    rarity = hero_manager.randomize_equipment_id()
    equipment_obj = hero_manager.randomize_equipment_by_rarity(rarity)
    if not equipment_obj:
        print("ERROR: No Equipment Returned")
        return [7]

    # Add the equipment into the user inventory
    hero_manager.obtain_equipment(userId, equipment_obj.Id)
    equipment_obj.print_details()
    return [0, equipment_obj]


def get_milestone_number(userId):
    # Select milestone number from database
    sql_statement = "SELECT milestone FROM myUser WHERE id = '" + str(userId) + "';"
    record = mysql_helper.select_statement(sql_statement)
    if len(record) is 0:
        return "Invalid userId"
    return record[0][0]


# if __name__ == '__main__':
#     equipment_obj = reached_milestone(12)
#     equipment_obj.print_details()
