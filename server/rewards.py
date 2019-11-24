class rewardsClass():

    def __init__(self, rewardId, rewardName, rewardDescription, rewardHToken, rewardImage, rewardDuration, rewardCategory):
        self.RewardId = rewardId
        self.RewardName = rewardName
        self.RewardDescription = rewardDescription
        self.RewardHToken = rewardHToken
        self.RewardImage = rewardImage
        self.RewardDuration = rewardDuration
        self.RewardCategory = rewardCategory


    def print_details(self):
        print("%s, %s, %s, %s, %s, %s, %s " % (self.RewardId, self.RewardName, self.RewardDescription, self.RewardHToken,
                                           self.RewardImage, self.RewardDuration, self.RewardCategory))


    def return_jsonify(self):
        return{
            "REWARD_ID" : self.RewardId,
            "REWARD_NAME" : self.RewardName,
            "REWARD_DESCRIPTION" : self.RewardDescription,
            "REWARD_H_TOKEN" : self.RewardHToken,
            "REWARD_IMAGE" : self.RewardImage,
            "REWARD_DURATION" : self.RewardDuration,
            "REWARD_CATEGORY" : self.RewardCategory
        }
