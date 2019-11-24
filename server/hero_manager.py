import user_manager
import mysql_helper
import random
from equipment import equipmentClass


def randomize_equipment_id():
    # print("Randomized equipment ran!")
    randomized_number = random.randint(0, 101)

    """
    *   Common:     1 - 50
    *   Rare:       50 - 80
    *   Epic:       80 - 95
    *   Legendary:  95 - 100 
    """
    if randomized_number < 50:
        return "Common"
    elif 49 < randomized_number < 80:
        return "Rare"
    elif 79 < randomized_number < 95:
        return "Epic"
    else:
        return "Legendary"


"""
Author:     Felix Wang
Purpose:    Returns a randomized Equipment
Returns:    If method is successful:    Equipment_Obj
            If method is unsuccessful:  False
Parameters: rarity : string (E.g 'Common')
"""
def randomize_equipment_by_rarity(rarity):
    sql_statement = "SELECT * FROM myequipment WHERE equipmentRarity = '" + rarity + "'"
    equipment_list = mysql_helper.select_statement(sql_statement)
    equipment_obj_list = []

    for eq in equipment_list:
        print(eq)
        equipment_obj = equipmentClass(eq[0], eq[1], eq[2], eq[3], eq[4], eq[5], eq[6], 'N')
        equipment_obj_list.append(equipment_obj)

    if len(equipment_obj_list) == 0:
        print ("ERROR: Equipment with '%s' rarity does not exist " % rarity)
        return False
    else:
        randomized_number = random.randint(0, len(equipment_obj_list) - 1)
        print ("SUCCESS: Returned equipment object with %s rarity." % rarity)
        return equipment_obj_list[randomized_number]


def get_existing_equipment(User_id):
    sql_statement = "SELECT * FROM myheroinventory hi INNER JOIN myequipment eq " \
                    "ON hi.equipmentId = eq.equipmentId WHERE hi.userId = '" + User_id + "'"
    response = mysql_helper.select_statement(sql_statement)
    if not response:
        return [1]
    equipment_list = response
    print("%s results returned " % (str(len(equipment_list))))

    equipment_obj_list = []
    try:
        for eq in equipment_list:
            equipment_obj = equipmentClass(eq[3], eq[4], eq[5], eq[6], eq[7], eq[8], eq[9], eq[2])
            equipment_obj_list.append(equipment_obj)
    except IndexError:
        return []
    return [0, equipment_obj_list]


def equip_equipment(userID, equipmentID):
    sql_statement = "UPDATE myheroinventory SET isEquipped = 'Y' WHERE userId = %s AND equipmentId = %s"
    print(userID, equipmentID)
    print(sql_statement)
    if not mysql_helper.sql_operation(sql_statement, [str(userID), str(equipmentID)]):
        return 1
    else:
        return 0


def unequip_equipment(userID, equipmentID):
    sql_statement = "UPDATE myheroinventory SET isEquipped = 'N' WHERE userId = %s AND equipmentId = %s"
    if not mysql_helper.sql_operation(sql_statement, [str(userID), str(equipmentID)]):
        return 1
    else:
        return 0


"""
Author:     Felix Wang
Purpose:    Adds equipment to the selected user
Returns:    Message
Parameters: User id : int
"""


def obtain_equipment(User_id, Equipment_id):
    sql_statement = "SELECT * FROM myheroinventory WHERE userId = '" + str(User_id) + "' AND equipmentId = '" + str(Equipment_id) + "';"

    # If equipment already exist. Exit the method
    if mysql_helper.check_if_record_exist(sql_statement):
        print("Item already exist")
        return "Success"

    # Save the equipment into the database
    sql_statement = "INSERT INTO myheroinventory (userId, equipmentId, isEquipped) VALUES (%s, %s, %s)"
    data_value = [User_id, Equipment_id, 'N']
    response = mysql_helper.sql_operation(sql_statement, data_value)
    if not response:
        print(response)
        return response
    print("Equipment Obtained Sucesssfully")
    return "Success"


def update_total_power(userID):
    sql_statement = "SELECT SUM(e.equipmentPowerLevel) FROM myheroinventory hi INNER JOIN myequipment e " \
                    "ON hi.equipmentID = e.equipmentID WHERE userId = '" + str(userID) + "' AND isEquipped = 'Y'"

    response = mysql_helper.select_statement(sql_statement)
    if not response:
        return [1]
    print(response[0][0])
    if response[0][0] is None:
        return [0, 0]
    else:
        return [0, response[0][0]]


if __name__ == '__main__':
    # user_obj = user_manager.getUserObj(1)
    # user_obj.print_details()
    # obtain_equipment(user_obj.Id, '1')
    # equipment_obj_list = get_existing_equipment(user_obj.Id)
    # for eq in equipment_obj_list:
    #     eq.print_details()
    equipment_obj = randomize_equipment_by_rarity('commoner')
    equipment_obj.print_details()
