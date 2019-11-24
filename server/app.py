import ratings_manager
import reward_manager
import user_manager
import milestone_manager
import expedition_manager
import bookmark_manager
import hero_manager
from flask import Flask, request, jsonify
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

@app.route('/checkSlowness/', methods=["POST"])
def checkSlowness():
    name = request.form.get("name")
    return jsonify({"NAME": name})



@app.route('/getHeroAvailability/', methods=["POST"])
def getHeroAvailability():
    userID = request.form.get('userID')
    response = user_manager.getHeroAvailability(userID)
    if response[0] is not 0:
        return jsonify ({"ERROR_CODE" : response[0]})
    else:
        return jsonify({"ERROR_CODE" : response[0],
                        "AVAILABILITY" : response[1]})


@app.route('/checkUsername/', methods=["POST"])
def checkUsername():
    username = request.form.get('username')
    print("attempting to check for: " + username)
    return jsonify({"ERROR_CODE" : user_manager.check_username_exist(username)})


"""
Author:     Felix
Purpose:    Get fetch username and password using username and password
Returns:    Success -> Returns [List of account credentials]
            Invalid ID -> Returns Invalid Account: Account credentials is incorrect
            Error   -> Returns Error message
"""
@app.route('/getUser/', methods=['POST'])
def getUser():
    userID = request.form.get('userID')
    print("attempt to search for: " + userID)
    user_obj = user_manager.getUserObj(userID)
    user_obj.print_details()
    return jsonify(user_obj.get_jsonified_data())


"""
Author:     Felix
Purpose:    Get fetch username and password using username and password
Returns:    Success -> Returns [List of account credentials]
            Invalid ID -> Returns Invalid Account: Account credentials is incorrect
            Error   -> Returns Error message
"""


@app.route('/get_user_mobile/', methods=['POST'])
def getUserMobile():
    mobile_number = request.form.get('mobile_number')
    print("attempt to search for: " + mobile_number)
    user_obj = user_manager.getUserObjMobile(mobile_number)
    user_obj.print_details()
    return jsonify(user_obj.get_jsonified_data())

"""
Author:     Felix
Purpose:    Generates an OTP.
Returns:    Response to alert users that SMS notification has been sent.
"""


@app.route('/getOTP/', methods=['POST'])
def get_OTP():
    mobile_number = request.form.get('mobile_number')
    print("Mobile Number is: " + str(mobile_number))
    return jsonify({
        "ERROR_CODE":  user_manager.generateOTP(mobile_number)
    })


"""
Author:     Felix
Purpose:    Checks for valid OTP.
Returns:    NONE -> Correct OTP
            INVALID OTP -> User keys in incorrect OTP.
"""

@app.route('/checkOTP/', methods=['POST'])
def check_OTP():
    mobile_number = request.form.get('mobile_number')
    OTP = request.form.get('OTP')
    return jsonify({
        "ERROR_CODE": user_manager.check_otp(mobile_number, OTP)
    })
@app.route('/addUser/', methods=["POST"])
def addUser():
    username = request.form.get('username')
    password = request.form.get('password')
    age = request.form.get('age')
    mobile_number = request.form.get('mobile_number')
    email = request.form.get('email')
    response = user_manager.add_user(password, username, email, age, mobile_number)
    if response[0] == 0:
        return jsonify({
            "ERROR_CODE": response[0],
            "USER_ID" : response[1]
        })
    else:
        return jsonify({
            "ERROR_CODE": response[0]
        })


@app.route('/updateHTokens/', methods=["POST"])
def updateHTokens():
    UserID = request.form.get('userID')
    HTokens = int(request.form.get('HTokens'))
    method = int(request.form.get("Method"))     # 1 = add, 0 = subtract
    return jsonify({
        "ERROR_CODE" : user_manager.updateHToken(HTokens, UserID, method)
    })


""" **************************************************************************************************************  
    _    _           _       _         _____            __ _ _      
   | |  | |         | |     | |       |  __ \          / _(_) |     
   | |  | |_ __   __| | __ _| |_ ___  | |__) | __ ___ | |_ _| | ___ 
   | |  | | '_ \ / _` |/ _` | __/ _ \ |  ___/ '__/ _ \|  _| | |/ _ \
   | |__| | |_) | (_| | (_| | ||  __/ | |   | | | (_) | | | | |  __/
    \____/| .__/ \__,_|\__,_|\__\___| |_|   |_|  \___/|_| |_|_|\___|
          | |                                                       
          |_|    
  ************************************************************************************************************ """

@app.route('/updateUserDetails/', methods=['POST'])
def update_user_details():
    details = request.form.get('details')
    userID = request.form.get('userID')
    data = json.loads(details)
    data = {k:None if v is '' else v for (k, v) in data.items()}
    print(data)
    # data = {x for x in }
    user_manager.updateProfile(data, userID)
    return jsonify({
        "ERROR_CODE": 0
    })


""" **************************************************************************************************************  
     _____            _                            _   
    |  ___|          (_)                          | |  
    | |__  __ _ _   _ _ _ __  _ __ ___   ___ _ __ | |_ 
    |  __|/ _` | | | | | '_ \| '_ ` _ \ / _ \ '_ \| __|
    | |__| (_| | |_| | | |_) | | | | | |  __/ | | | |_ 
    \____/\__, |\__,_|_| .__/|_| |_| |_|\___|_| |_|\__|
             | |       | |                             
             |_|       |_|                                
  ************************************************************************************************************ """
@app.route('/getEquipment/', methods=['POST'])
def getEquipment():
    userID = request.form.get('userID')
    response = hero_manager.get_existing_equipment(userID)

    if response[0] is 0:
        response2 = hero_manager.update_total_power(userID)
        equipment_list = []
        for equipment in response[1]:
            equipment_list.append(equipment.get_jsonified_data())
        return jsonify({"ERROR_CODE": response[0],
                        "DETAILS": equipment_list,
                        "POWER_LEVEL": response2[1]})
    else:
        return jsonify({"ERROR_CODE" : response[0]})

""" **************************************************************************************************************  
     __  __ _ _           _                   
    |  \/  (_) |         | |                  
    | \  / |_| | ___  ___| |_ ___  _ __   ___ 
    | |\/| | | |/ _ \/ __| __/ _ \| '_ \ / _ \
    | |  | | | |  __/\__ \ || (_) | | | |  __/
    |_|  |_|_|_|\___||___/\__\___/|_| |_|\___|                                    
  ************************************************************************************************************ """

@app.route('/reachedMilestone/', methods=['POST'])
def reach_milestone():
    userID = request.form.get('userID')
    response= milestone_manager.reached_milestone(userID)
    if response[0] == 0:
        return jsonify({
            "ERROR_CODE" : response[0],
            "EQUIPMENT_OBJ" : response[1].get_jsonified_data()
        })
    else:
        return jsonify({
            "ERROR_CODE": response[0],
        })


@app.route('/getExpeditions/', methods=['POST'])
def get_expeditions():
    userID = request.form.get('userID')
    print (userID)
    user_obj = user_manager.getUserObj(userID)
    expedition_obj_list = expedition_manager.getExpeditions(user_obj)
    expedition_list = []
    for x in expedition_obj_list:
        expedition_list.append(x.return_jsonify())

    return jsonify({"ERROR_CODE" : 0,
                    "EXPEDITION_LIST" : expedition_list})


@app.route('/startExpedition/', methods=["POST"])
def start_expedition():
    userID = request.form.get('userID')
    expeditionID = request.form.get("expeditionID")
    print(userID, expeditionID)
    return jsonify({"ERROR_CODE": expedition_manager.startExpedition(userID, expeditionID)})


@app.route('/get_ongoing_expeditions/', methods=["POST"])
def get_ongoing_expedition():
    userID = request.form.get('userID')
    print(userID)
    response = expedition_manager.get_ongoing_expeditions(userID)
    if response[0] == 0:
        return jsonify({"ERROR_CODE": response[0],
                        "DETAILS": response[1]})
    else:
        return jsonify({"ERROR_CODE" : response[0]})


@app.route('/get_completed_expeditions/', methods=["POST"])
def get_completed_expedition():
    userID = request.form.get('userID')
    print(userID)
    response = expedition_manager.get_completed_expeditions(userID)
    if response[0] == 0:
        return jsonify({"ERROR_CODE": response[0],
                        "DETAILS": response[1]})
    else:
        return jsonify({"ERROR_CODE" : response[0]})

@app.route('/get_expedition_id/', methods=["POST"])
def get_expedition_id():
    expedition_id = request.form.get('expeditionID')
    response = expedition_manager.getExpeditionByID(expedition_id)
    if response[0] == 0:
        return jsonify({"ERROR_CODE": response[0],
                        "DETAILS": response[1].return_jsonify()})
    else:
        return jsonify({"ERROR_CODE": response[0]})


@app.route('/end_expedition/', methods=["POST"])
def end_expedition():
    userID = request.form.get("userID")
    print(userID)
    return jsonify({"ERROR_CODE": expedition_manager.end_expedition(userID)})

@app.route('/complete_expedition/', methods=["POST"])
def complete_expedition():
    userID = request.form.get("userID")
    print(userID)
    return jsonify({"ERROR_CODE": expedition_manager.complete_expedition(userID)})

"""
     ____              _                         _        
    | __ )  ___   ___ | | ___ __ ___   __ _ _ __| | _____  
    |  _ \ / _ \ / _ \| |/ / '_ ` _ \ / _` | '__| |/ / __| 
    | |_) | (_) | (_) |   <| | | | | | (_| | |  |   <\__ \ 
    |____/ \___/ \___/|_|\_\_| |_| |_|\__,_|_|  |_|\_\___/ 
                                                        
"""
@app.route('/add_bookmark/', methods=["POST"])
def add_bookmark():
    # userID, starting_address, ending_address, bookmark_name)
    userID = request.form.get("userID")
    starting_addr = request.form.get("starting_address")
    ending_addr = request.form.get("ending_address")
    bookmark_name = request.form.get("bookmark_name")

    print(userID, starting_addr, ending_addr, bookmark_name)

    return jsonify({
        "ERROR_CODE" : bookmark_manager.add_bookmarks(userID, starting_addr, ending_addr, bookmark_name)
    })


@app.route('/get_bookmarks/', methods=["POST"])
def get_bookmarks():
    userID = request.form.get("userID")
    response = bookmark_manager.get_bookmarks(userID)
    if response[0] == 0:
        return jsonify({
            "ERROR_CODE" : response[0],
            "DETAILS" : response[1]
        })
    else:
        return jsonify({
            "ERROR_CODE" : response[0]
        })


@app.route('/get_total_power/', methods=["POST"])
def update_total_power():
    userID = request.form.get("userID")
    response = hero_manager.update_total_power(userID)
    if response[0] is 0:
        return jsonify({"ERROR_CODE" : response[0],
                        "DETAILS" : response[1]})
    else:
        return jsonify({"ERROR_CODE" : response[0]})


@app.route('/equip/', methods=["POST"])
def equip_item():
    userID = request.form.get("userID")
    equipmentID = request.form.get("equipmentID")
    hero_manager.equip_equipment(userID, equipmentID)
    response = hero_manager.update_total_power(userID)
    if response[0] is 0:
        user_manager.updateHeroPower(userID, int(response[1]))
        return jsonify({"ERROR_CODE": response[0],
                        "DETAILS": response[1]})
    else:
        return jsonify({"ERROR_CODE": response[0]})


@app.route('/unequip/', methods=["POST"])
def unequip_item():
    userID = request.form.get("userID")
    equipmentID = request.form.get("equipmentID")
    hero_manager.unequip_equipment(userID, equipmentID)
    response = hero_manager.update_total_power(userID)
    if response[0] is 0:
        user_manager.updateHeroPower(userID, int(response[1]))
        return jsonify({"ERROR_CODE": response[0],
                        "DETAILS": response[1]})
    else:
        return jsonify({"ERROR_CODE": response[0]})

@app.route('/equip_switch/', methods=["POST"])
def equip_switch_item():
    userID = request.form.get("userID")
    equipmentID = request.form.get("equipmentID")
    replaced_equipmentID = request.form.get("replaced_equipmentID")
    hero_manager.equip_equipment(userID, equipmentID)
    hero_manager.unequip_equipment(userID, replaced_equipmentID)


    response = hero_manager.update_total_power(userID)
    if response[0] is 0:
        user_manager.updateHeroPower(userID, int(response[1]))
        return jsonify({"ERROR_CODE": response[0],
                        "DETAILS": response[1]})
    else:
        return jsonify({"ERROR_CODE": response[0]})

"""
  ____                            _     
 |  _ \ _____      ____ _ _ __ __| |___ 
 | |_) / _ \ \ /\ / / _` | '__/ _` / __|
 |  _ <  __/\ V  V / (_| | | | (_| \__ \
 |_| \_\___| \_/\_/ \__,_|_|  \__,_|___/
                                        
"""

@app.route('/get_rewards/', methods=["POST"])
def get_rewards():
    response = reward_manager.get_all_rewards()
    if response[0] is 0:
        rewards_json_list = []
        for x in response[1]:
            rewards_json_list.append(x.return_jsonify())
        return jsonify({"ERROR_CODE" : response[0],
                        "DETAILS" : rewards_json_list})
    else:
        return jsonify({"ERROR_CODE" : response[0]})

@app.route('/get_rewards_by_id/', methods=["POST"])
def get_rewards_id():
    reward_id = request.form.get("RewardID")
    response = reward_manager.get_reward_by_id(reward_id)
    return jsonify({"ERROR_CODE" : 0, "DETAILS" : response.return_jsonify()})

@app.route('/redeem_rewards/', methods=["POST"])
def redeem_rewards():
    user_id = request.form.get("UserID")
    reward_id = request.form.get("RewardID")
    print("Redeem Rewards: UserID = %s, RewardID = %s" %(user_id, reward_id))
    user_obj = user_manager.getUserObj(user_id)
    reward_obj = reward_manager.get_reward_by_id(reward_id)
    print(user_id, reward_id)
    return jsonify({"ERROR_CODE" : reward_manager.redeem_reward(user_obj, reward_obj)})


@app.route('/get_endtime/', methods=["POST"])
def get_endtime():
    user_id = request.form.get("UserID")
    voucher_id = request.form.get("VoucherID")
    print (user_id)
    print(voucher_id)
    response = reward_manager.get_endtime(user_id,voucher_id)
    if response != 1:
        print("the reponse i want to see: %s", response)
        print(response)
        return jsonify({"ERROR_CODE": response,
                        "DETAILS": response})
    else:
        print("the response i dont want to see: %s", response)
        return jsonify({"ERROR_CODE": response})

@app.route('/get_reward_user/', methods=["POST"])
def get_reward_user():
    user_id = request.form.get("UserID")
    response = reward_manager.get_reward_user(user_id)
    if response[0] == 0:
        return jsonify({"ERROR_CODE" : response[0],
                        "DETAILS" : response[1]})
    else:
        return jsonify({"ERROR_CODE" : response[0]})

@app.route('/update_endtime/', methods=["POST"])
def update_endtime():
    user_id = request.form.get("UserID")
    voucher_id = request.form.get("VoucherID") #ADD THIS VAR INTO HTML
    print(user_id, voucher_id)
    response = reward_manager.update_endtime(user_id, voucher_id)
    print(response)
    print("Onclick Test", voucher_id)
    if response == 0:
        return jsonify({"ERROR_CODE" : response,
                        "DETAILS" : response})
    else:
        return jsonify({"ERROR_CODE" : response})

@app.route('/update_rewards/', methods=["POST"])
def update_rewards():
    user_id = request.form.get("UserID")
    print(user_id)
    response = reward_manager.update_rewards(user_id)
    print(response)
    if response == 0:
        return jsonify({"ERROR_CODE" : response,
                        "DETAILS" : response})
    else:
        return jsonify({"ERROR_CODE" : response})

"""
  _____       _   _                 
 |  __ \     | | (_)                
 | |__) |__ _| |_ _ _ __   __ _ ___ 
 |  _  // _` | __| | '_ \ / _` / __|
 | | \ \ (_| | |_| | | | | (_| \__ \
 |_|  \_\__,_|\__|_|_| |_|\__, |___/
                           __/ |    
                          |___/     
"""
@app.route('/getRatings/', methods=["POST"])
def getRatings():
    starting_address = request.form.get("starting_address")
    ending_address = request.form.get("ending_address")
    response = ratings_manager.get_ratings(starting_address, ending_address)
    if response[0] == 0:
        return jsonify({"ERROR_CODE" : response[0],
                        "DETAILS" : response[1]})

    return jsonify({"ERROR_CODE" : response[0]})



@app.route('/addRating/', methods=["POST"])
def addRating():
    starting_address = request.form.get("starting_address")
    ending_address = request.form.get("ending_address")
    rating = request.form.get("rating")
    print(starting_address, ending_address, rating)
    return jsonify({"ERROR_CODE" : ratings_manager.add_ratings(starting_address, ending_address, rating)})

@app.route('/deleteBookmark/', methods=["POST"])
def deleteBookmark():
    bookmark_name = request.form.get("bookmark_name")
    userID = request.form.get("userID")
    print(bookmark_name, userID)
    return jsonify({"ERROR_CODE": bookmark_manager.delete_bookmarks(userID, bookmark_name)})


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.debug = True
    app.run(threaded=True, port=5000)
