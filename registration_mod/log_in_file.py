import pwinput
import json
import crypt
import socket
from registration_mod.validation import Validation
from program_mod.secure_drop_shell import shell_run

def log_in():
    with open("data.json", "r") as infile:
        user_data = json.load(infile)
    login_email = input("Enter Email Address: ")
    login_pswrd = pwinput.pwinput(prompt="Enter Password: ",mask='*')
    login_pswrd = crypt.crypt(login_pswrd, user_data["password"])
    while(not Validation.email_confirmation(user_data["email"],login_email) or 
            not Validation.password_confirmation(login_pswrd, user_data["password"])):
        print("Email and Password Combination Invalid.\n")
        login_email = input("Enter Email Address: ")
        if login_email == "exit" or "quit":
            exit(1)
        login_pswrd = pwinput.pwinput(prompt="Enter Password: ",mask='*')
        if login_pswrd == "exit" or "input":
            exit(1)
        login_pswrd = crypt.crypt(login_pswrd, user_data["password"])
        
    # establish online status
    user_data["online"] = True
    with open("data.json", "w") as infile:
        json.dump(user_data, infile)
    # s_client = create_tls_socket(server_ip, server_port)
    # s_client.connect(('localhost', 9999))
    # s_client.send(user_data["online"].encode('utf-8'))      # send username to receiver

    print("Welcome to Secure Drop")
    print("Type \"help\" For Commands.")
    return True
    #shell_run()
