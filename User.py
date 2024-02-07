# User class
class Staff:
    # initializer method

    def __init__(self, Staff_id, Username, Email, PhoneNo, Password, hashed_password=None):
        self.__Staff_id = Staff_id
        self.__Username = Username
        self.__Email = Email
        self.__PhoneNo = PhoneNo
        self.__Password = Password
        self.__hashed_password = hashed_password

    # accessor methods
    def get_Staff_id(self):
        return self.__Staff_id

    def get_Username(self):
        return self.__Username

    def get_Email(self):
        return self.__Email

    def get_PhoneNo(self):
        return self.__PhoneNo

    def get_Password(self):
        return self.__Password

    def get_hashed_password(self):
        return self.__hashed_password

    # mutator methods
    def set_Staff_id(self, Staff_id):
        self.__Staff_id = Staff_id

    def set_Email(self, Email):
        self.__Email = Email

    def set_PhoneNo(self, PhoneNo):
        self.__PhoneNo = PhoneNo

    def set_Password(self, Password):
        self.__Password= Password

    def set_hashed_password(self, hashed_password):
        self.__hashed_password = hashed_password

    def set_Username(self, Username):
        self.__Username = Username


class Product:
        # initializer method
        def __init__(self, Product_id, Name, Description, Price, Amt_sold):
            self.__Product_id = Product_id
            self.__Name = Name
            self.__Description = Description
            self.__Price = Price
            self.__Amt_sold = Amt_sold

        # accessor methods
        def get_Product_id(self):
            return self.__Product_id

        def get_Name(self):
            return self.__Name

        def get_Description(self):
            return self.__Description

        def get_Price(self):
            return self.__Price

        def get_Amt_sold(self):
            return self.__Amt_sold

        # mutator methods
        def set_Product_id(self, Product_id):
            self.__Product_id = Product_id

        def set_Description(self, Description):
            self.__Description = Description

        def set_Price(self, Price):
            self.__Price = Price

        def set_Name(self, Name):
            self.__Name = Name

        def set_Amt_sold(self, Amt_sold):
            self.__Amt_sold = Amt_sold