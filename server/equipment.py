class equipmentClass():

    def __init__(self, id, name, description, power_level, equipment_type, rarity, img, equipped):
        self.Id = id
        self.Name = name
        self.Description = description
        self.PowerLevel = power_level
        self.EquipmentType = equipment_type
        self.Rarity = rarity
        self.IsEquipped = equipped
        self.Image = img

    def print_details(self):
        print("%s, %s, %s, %s, %s, %s, %s, %s" % (self.Id, self.Name, self.Description, self.PowerLevel,
                                          self.EquipmentType, self.Rarity, self.Image, self.IsEquipped))


    def get_jsonified_data(self):
        return {"EQUIPMENT_ID" : self.Id,
                "NAME" : self.Name,
                "DESCRIPTION" : self.Description,
                "POWER_LEVEL" : self.PowerLevel,
                "EQUIPMENT_TYPE" : self.EquipmentType,
                "RARITY" : self.Rarity,
                "IMG" : self.Image,
                "IS_EQUIPPED" : self.IsEquipped}



