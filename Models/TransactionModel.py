from Database.ConnectionModel import ConnectionModel
from bson import ObjectId
from datetime import datetime


def all_trans_details(ref, user_id):
    response = ref.find_one({"user_id": ObjectId(user_id)},
                            {"_id": 0, "user_id": 1, "debit_trans": 1, "credit_trans": 1})
    return response


class TransactionModel(ConnectionModel):
    
    user_collection_name = "user"
    user_trans_collection_name = 'trans_details'

    def __init__(self):
        self.user_trans_collection = ConnectionModel.connection(TransactionModel.user_trans_collection_name)
        self.user_collection = ConnectionModel.connection(TransactionModel.user_collection_name)

    def user_debit_trans(self, user_id):
        amount = self.user_collection.find_one({"_id": ObjectId(user_id)}, {"amount": 1})["amount"]
        amount_value = int(input("Enter withdrawal amount: "))
        if amount_value > 100:
            if amount - amount_value > 500:
                response_1 = self.user_collection.update_one({"_id": ObjectId(user_id)},
                                                             {"$inc": {"amount": -amount_value}})
                response_2 = self.user_trans_collection.update_one({"user_id": ObjectId(user_id)}, {
                    "$push": {
                        "debit_trans": {
                            "debit_amount": amount_value,
                            "debit_time": datetime.utcnow()
                        }
                    }
                })
                if response_1.acknowledged and response_2.acknowledged:
                    return "Debited Successfully!!"
                else:
                    return "Something went wrong try again!!"
            else:
                return "Sorry, we can't allow you for this transaction, your account has only minimum balance."
        else:
            return "Debited amount atleast 100Rs"

    def user_credit_trans(self, user_id):
        amount_value = int(input("Enter the crediting amount: "))
        if amount_value > 0:
            response_1 = self.user_collection.update_one({"_id": ObjectId(user_id)}, {"$inc": {"amount": amount_value}})
            response_2 = self.user_trans_collection.update_one({"user_id": ObjectId(user_id)}, {
                "$push": {
                    "credit_trans": {
                        "cred_amount": amount_value,
                        "time": datetime.utcnow()
                    }
                }
            })

            if response_1.acknowledged and response_2.acknowledged:
                return "Credited Successfully"
            else:
                return "Something Went wrong try again!!"

        else:
            return "Amount can't be in negative!!"

    def user_all_trans(self, user_id):
        return all_trans_details(self.user_trans_collection, user_id)

    def admin_all_trans(self, user_id):
        return all_trans_details(self.user_trans_collection, user_id)
