from Database.ConnectionModel import ConnectionModel


class UserModel(ConnectionModel):
    collection_name = "user"

    def __init__(self):
        self.user_collection = ConnectionModel.connection(UserModel.collection_name)

    def user_registration(self, email, password, mobile_no, role, amount):
        data = {
            "email": email,
            "password": password,
            "mobile_no": mobile_no,
            "role": role,
            "amount": amount
        }
        response = self.user_collection.insert_one(data)
        if response.inserted_id:
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
            return response["role"], response["email"]
        else:
            return 0
