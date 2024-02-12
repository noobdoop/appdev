# User class
class Customer:
    # initializer method

    def __init__(self, customer_id, Username, gender, Email, PhoneNo, address, Password,
                 hashed_password=None):
        self.__customer_id = customer_id
        self.__Username = Username
        self.__gender = gender
        self.__Email = Email
        self.__PhoneNo = PhoneNo
        self.__address = address
        self.__Password = Password
        self.__hashed_password = hashed_password

    def get_customer_id(self):
        return self.__customer_id

    def get_Count_id(self):
        return self.__Count_id

    def get_Username(self):
        return self.__Username

    def get_gender(self):
        return self.__gender

    def get_Email(self):
        return self.__Email

    def get_PhoneNo(self):
        return self.__PhoneNo

    def get_address(self):
        return self.__address

    def get_hashed_password(self):
        return self.__hashed_password

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_Count_id(self, Count_id):
        self.__Count_id = Count_id

    def set_Username(self, Username):
        self.__Username = Username

    def set_gender(self, gender):
        self.__gender = gender

    def set_Email(self, Email):
        self.__Email = Email

    def set_PhoneNo(self, PhoneNo):
        self.__PhoneNo = PhoneNo

    def set_address(self, address):
        self.__address = address

    def set_hashed_password(self, hashed_password):
        self.__hashed_password = hashed_password

class Feedback:
    def __init__(self, Name, Email, PhoneNo, Feedback_type, Feedback):
        self.__Name = Name
        self.__Email = Email
        self.__PhoneNo = PhoneNo
        self.__Feedback_type = Feedback_type
        self.__Feedback = Feedback

    def get_Name(self):
        return self.__Name
    def get_Email(self):
        return self.__Email
    def get_PhoneNo(self):
        return self.__PhoneNo
    def get_Feedback_type(self):
        return self.__Feedback_type
    def get_Feedback(self):
        return self.__Feedback

    def set_Name(self, Name):
        self.__Name = Name
    def set_Email(self, Email):
        self.__Email = Email
    def set_PhoneNo(self, PhoneNo):
        self.__PhoneNo = PhoneNo

    def set_Feedback_type(self, Feedback_type):
        self.__Feedback_type = Feedback_type

    def set_Feedback(self, Feedback):
        self.__Feedback = Feedback
