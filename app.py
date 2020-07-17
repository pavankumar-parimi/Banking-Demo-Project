import re
from Models.UserModel import UserModel
from Models.TransactionModel import TransactionModel


def user_register():
    email = input("Enter Email Id : ")
    password = input("Enter Password : ")
    mobile_no = input("Enter Mobile No : ")
    role = input("Enter Role 'A' or 'U' : ")
    email_regex = '^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$'
    password_regex = '((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@*#$%]).{6,20})'

    amount = input("You need to deposit a base amount of 1000Rs to open account:")

    if role == 'a' or role == 'A':
        role = "A"
    elif role == 'u' or role == 'U':
        role = "U"
    else:
        role = "U"

    if int(amount) >= 1000:
        if re.match(email_regex, email) and re.match(password_regex, password):
            user_model_obj = UserModel()
            return user_model_obj.user_registration(email, password, mobile_no, role, int(amount))
        else:
            return "Either Email_Id or Password doesn't meet our reg_ex requirements."
    else:
        return "Sorry, we can't open you the account without base amount in the account while registering."


def user_login():
    email = input("Enter Email Id : ")
    password = input("Enter Password : ")
    user_model_obj = UserModel()
    return user_model_obj.user_authentication(email, password)


def after_successful_login(role, email):
    if role == "U":
        print("Enter 1 to Credit")
        print("Enter 2 to Debit")
        choice = input("Enter your choice :")
        transaction_model_obj = TransactionModel()
        if choice == '1':
            transaction_model_obj.user_credit_trans(email)
        elif choice == '2':
            transaction_model_obj.user_debit_trans(email)
        else:
            transaction_model_obj.user_all_trans(email)
    else:
        email = input("Enter the user id:")
        transaction_model_obj = TransactionModel()
        transaction_model_obj.admin_all_trans(email)


while True:
    print("/t/t Welcome to ABC Bank /t/t")

    print("Enter 1 to Register")
    print("Enter 2 to Login")
    print("Enter 3 to Exit")

    choice = input("Enter Your Choice : ")

    data = choice[0]

    if data == '1':
        """ Register the user """
        result = user_register()
        print(result)
    elif data == '2':
        """ Login the user """
        result = user_login()
        if result:
            after_successful_login(result[0], result[1])
        else:
            print("The credentials that you have entered are wrong!!, Please try again")
    else:
        """ Exiting the application """
        break
