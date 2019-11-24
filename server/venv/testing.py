import unittest
import user_manager
import milestone_manager
import reward_manager
import mysql_helper
import hero_manager
import equipment
import expedition_manager

from rewards import rewardsClass
from user import userClass

# 1 Felix Use Case
# Need to perform 4 basic flows.
# class testExpedition(unittest.TestCase):
#
#     # Basic Path Set 1 (Success Condition)
#     # [(65 - 66), (67), (70 - 72), (73), (76 - 94), (95)]
#     def test_start_expedition(self):
#         self.user = userClass(1, 'felixwrh', 'Felix Wang', '92233511', 'felixwrh96@gmail.com', '12',
#                               'nil,nil,nil,nil,nil,nil', '800', 0, 0)
#         self.assertTrue(expedition_manager.startExpedition(self.user, '1'))
#
#     # Basic Path Set 2 (Invalid Expedition ID)
#     # [(65 - 66), (67), (68 - 69), (95)]
#     def test_start_expedition2(self):
#         self.user = userClass(1, 'felixwrh', 'Felix Wang', '92233511', 'felixwrh96@gmail.com', '12',
#                               'nil,nil,nil,nil,nil,nil', '800', 0, 0)
#         self.assertFalse(expedition_manager.startExpedition(self.user, '555'))
#
#     # Basic Path Set 3 (Invalid User ID)
#     # [(64 - 67), (67), (70 - 72), (73), (74 - 75), (95)]
#     def test_start_expedition3(self):
#         self.user = userClass(10, 'felixwrh', 'Felix Wang', '92233511', 'felixwrh96@gmail.com', '12',
#                               'nil,nil,nil,nil,nil,nil', '800', 0, 0)
#         self.assertFalse(expedition_manager.startExpedition(self.user, '1'))


# Testing Obtain Equipment Method

# 2
# class testEquipment(unittest.TestCase):
#
#     def test_obtain_equipment(self):
#         self.assertEqual(equipment_manager.obtain_equipment('1', '1'), 'Success')


"""
UNIT TESTING FOR ObtainRewards()
"""
# 3
# class testRewards(unittest.TestCase):
#     def setUp(self):
#         self.user = userClass(1, 'felixwrh', 'Felix Wang', '92233511', 'felixwrh96@gmail.com', '12',
#                                  'nil,nil,nil,nil,nil,nil', 800, 900, 0)
#         self.reward = rewardsClass(1, 'Starbucks Voucher', 'This is a sample description', 600, 'image.jpg', 30)
#
#     def test_redeem_rewards(self):
#         # Testing with a valid User ID and a valid reward ID
#         self.assertTrue(reward_manager.redeem_reward(self.user, self.reward))

        # Testing with an invalid reward ID
        # self.assertFalse(reward_manager.redeem_reward(self.user, 8))

        # Testing with an invalid user ID
        # self.assertFalse(reward_manager.redeem_reward(8, self.reward))

"""
UNIT TESTING FOR milestone_reached()
"""

# # 4
# class testMilestone(unittest.TestCase):
#     def setUp(self):
#         self.user = userClass(1, 'felixwrh', 'Felix Wang', '92233511', 'felixwrh96@gmail.com', '12',
#                               'nil,nil,nil,nil,nil,nil', '800', 0, 0)
#
#     def test_milestone_reached(self):
#         # Testing with a valid User ID.
#         self.assertIsInstance(milestone_manager.reached_milestone(self.user.Id), equipment.equipmentClass)
#
#         # Testing with an invalid User ID.
#         self.assertFalse(milestone_manager.reached_milestone(8))

"""
UNIT TESTING FOR updateProfile
"""
# 5 Felix Use Case
# Need to perform 4 basic flows.
# class testUser(unittest.TestCase):
    # Basic Path Set 1 (Success Condition # 1)
    #
    # def test_update_profile_1(self):
    #     user_dict = {"emailAddress": "felixwrh13@gmail.com", "age": "22", "contactNumber": None,
    #                  "password": '_Pass1234'}
    #     self.assertTrue(user_manager.updateProfile(user_dict, 1))
    #
    #
    # def test_update_profile_2(self):
    #     user_dict = {"emailAddress": None, "age": None, "contactNumber": None,
    #                  "password": None}
    #     self.assertFalse(user_manager.updateProfile(user_dict, 1))
    #
    # def test_update_profile_3(self):
    #     user_dict = {"emailAddress": "felixwrh13@gmail.com", "age": "22", "contactNumber": "92233511",
    #                  "password": '_Pass1234'}
    #     self.assertTrue(user_manager.updateProfile(user_dict, 1))


# 5 Felix Use Case
# Need to perform 3 basic flows.
class testEquipment(unittest.TestCase):
    # Basic Path Set 1 (Success Condition # 1)

    # def test_randomize_equipment_by_rarity_1(self):
    #     self.assertIsInstance(hero_manager.randomize_equipment_by_rarity('common'), equipment.equipmentClass)

    def test_randomize_equipment_by_rarity_2(self):
        self.assertFalse(hero_manager.randomize_equipment_by_rarity('Super Rare'))


if __name__ == '__main__':
    unittest.main()


