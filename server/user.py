class userClass():

    def __init__(self, id, username, fullName, contactNumber, email, age, equipment, powerLevel, hTokens, steps):
        self.Id = str(id)
        self.Username = username
        self.Name = fullName
        self.ContactNumber = contactNumber
        self.Email = email
        self.Age = age
        self.Equipment = equipment
        self.PowerLevel = powerLevel
        self.HTokens = hTokens
        self.Steps = steps


    def print_details(self):
        print("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" %(self.Id, self.Username, self.Name, self.ContactNumber,
                                                          self.Email, self.Age, self.Equipment,
                                                          self.PowerLevel, self.HTokens, self.Steps))



    def get_jsonified_data(self):
        return {"USER_ID" : self.Id, "USERNAME" : self.Username, "NAME" : self.Name, "MOBILE_NUMBER" : self.ContactNumber,
                "EMAIL" : self.Email, "AGE" : self.Age, "H_TOKENS" : self.HTokens}