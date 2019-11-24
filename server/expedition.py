class expeditionClass:
    def __init__(self, expedition_id, requiredPowerLevel, image, description, title, timeTaken, hTokens, eligible):
        self.ExpeditionID = str(expedition_id)
        self.ReqPowerLevel = requiredPowerLevel
        self.Image = image
        self.Description = description
        self.Title = title
        self.TimeTaken = timeTaken
        self.HToken = hTokens
        self.IsEligible = eligible

    def print_details(self):
        print("%s, %s, %s, %s, %s, %s, %s, %s" % (self.ExpeditionID, self.ReqPowerLevel, self.Image,
                                                  self.Description, self.Title, self.TimeTaken, self.HToken,
                                                  self.IsEligible))


    def return_jsonify(self):
        return {"EID" : self.ExpeditionID,
                "POWER_LEVEL" : self.ReqPowerLevel,
                "IMAGE": self.Image,
                "DESCRIPTION" : self.Description,
                "TITLE": self.Title,
                "TIME_TAKEN": self.TimeTaken,
                "HTOKEN": self.HToken,
                "IS_ELIGIBLE": self.IsEligible}

