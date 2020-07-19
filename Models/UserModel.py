from Database.ConnectionModel import ConnectionModel
from datetime import datetime


class UserModel(ConnectionModel):
    user_collection_name = "user"
    user_trans_collection_name = "trans_details"

    def __init__(self):
        self.user_collection = ConnectionModel.connection(UserModel.user_collection_name)
        self.user_trans_collection = ConnectionModel.connection(UserModel.user_trans_collection_name)

    def user_registration(self, email, password, mobile_no, role, amount):
        cross_ref = self.user_collection.find({"email": email}).count()
        if cross_ref:
            return "There is already an user with that id"
        data = {
            "email": email,
            "password": password,
            "mobile_no": mobile_no,
            "role": role,
            "amount": amount
        }
        response = self.user_collection.insert_one(data)
        trans_data = {"user_id": self.user_collection.find_one({"email": email})["_id"], "debit_trans": [],
                      "credit_trans": [{"cred_amount": amount, "time": datetime.utcnow()}]}
        response_2 = self.user_trans_collection.insert_one(trans_data)
        if response.inserted_id and response_2.inserted_id:
            return "Registered Successfully!!"
        else:
            return "Registration Failed!!"

    def user_authentication(self, email, password):
        query = {
            "email": email,
            "password": password
        }
        response = self.user_collection.find_one(query, {"role": 1})
        if response:
            return response["role"], response["_id"]
        else:
            return 0
