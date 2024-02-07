# User class
class Customer:
    # initializer method

    def __init__(self, customer_id, Username, gender, Email, PhoneNo, date_joined, address, Password,
                 hashed_password=None):
        self.__customer_id = customer_id
        self.__Username = Username
        self.__gender = gender
        self.__Email = Email
        self.__PhoneNo = PhoneNo
        self.__date_joined = date_joined
        self.__address = address
        self.__Password = Password
        self.__hashed_password = hashed_password

    def get_customer_id(self):
        return self.__customer_id

    def get_Username(self):
        return self.__Username

    def get_gender(self):
        return self.__gender

    def get_Email(self):
        return self.__Email

    def get_PhoneNo(self):
        return self.__PhoneNo

    def get_date_joined(self):
        return self.__date_joined

    def get_address(self):
        return self.__address

    def get_hashed_password(self):
        return self.__hashed_password

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_Username(self, Username):
        self.__Username = Username

    def set_gender(self, gender):
        self.__gender = gender

    def set_Email(self, Email):
        self.__Email = Email

    def set_PhoneNo(self, PhoneNo):
        self.__PhoneNo = PhoneNo

    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined

    def set_address(self, address):
        self.__address = address

    def set_hashed_password(self, hashed_password):
        self.__hashed_password = hashed_password