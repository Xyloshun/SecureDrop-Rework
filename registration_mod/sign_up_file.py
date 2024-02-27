import json
import pwinput
from registration_mod.hash_password import hash_passwd
from email_validator import validate_email, EmailNotValidError
from registration_mod.validation import Validation

def sign_up():
    data = {} 
    print("No users are registered with this client.")
    accept = input("Do you want to register a new user (y/n) ")
    
    if accept == 'y':
        data["name"] = input("Enter Full Name: ")
        data["email"] = input("Enter Email Address: ")  
        while(not Validation.valid_email(data["email"])):
            data["email"] = input("Enter Email Address: ")

        data["password"] = pwinput.pwinput(prompt="Enter Password: ",mask='*')
        confirm_password = pwinput.pwinput(prompt="Re-enter Password: ",mask='*')
        if(Validation.password_confirmation(data["password"], confirm_password)):
            print("\nPasswords match.")
            data["password"] = hash_passwd(data["password"])
            data["online"] = False      # default to offline
            print("User Registered.")
            print("Exiting SecureDrop.")
            json_object = json.dumps(data)
            with open("data.json","w") as outfile:
                outfile.write(json_object)
        
