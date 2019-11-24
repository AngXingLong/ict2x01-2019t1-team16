import  mysql_helper


sql_statement = "UPDATE myotp SET OTP = %s WHERE phone_number = %s"
data = ('999999',  '92233511')
mysql_helper.insert(sql_statement, data)