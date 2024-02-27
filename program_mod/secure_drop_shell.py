import subprocess
import threading
import multiprocessing
import sys
import json
from multiprocessing import Pool
import time
from program_mod.contacts import add_contact, list_contacts
from program_mod.send import send_file



class SecureDropShell: 
    def __init__(self):
        self.stop_event = threading.Event()
    def run (self):
        while True:
            while self.stop_event.is_set():
                time.sleep(5)
       
            
            
            user_input = input("secure_drop> ")
            if user_input == "exit":
                exit_shell()
            
            elif user_input == "help":
                display_help()
            
            elif user_input.startswith("send "):
                _, peer_ip, file_path = user_input.split()
                # Call the send_file function
                send_file(file_path, peer_ip)
            
            elif user_input in command_functions:
                command_functions[user_input]()
            
            else:
               execute_command(user_input)
    
    def pause(self):
        print("PAUSED\n")
        self.stop_event.set()
    
    def resume(self):
        self.stop_event.clear()


def shell_run():
    while True:
        user_input = input("secure_drop> ")

        if user_input == "exit":
            exit_shell()
        elif user_input == "help":
            display_help()
        elif user_input.startswith("send "):
            _, peer_ip, file_path = user_input.split()

            # Call the send_file function
            send_file(file_path, peer_ip)
        elif user_input in command_functions:
            command_functions[user_input]()
        else:
            execute_command(user_input)

def execute_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def exit_shell():
    """Exit SecureDrop"""
    with open("data.json", "r") as infile:
        user_data = json.load(infile)
    user_data["online"] = False
    with open("data.json", "w") as infile:
        json.dump(user_data, infile)
    
    print("Exiting SecureDrop")
    sys.exit()

def display_help():
    for command, description in command_functions.items():
        print(f"  \"{command}\" -> {description.__doc__}")

command_functions = {
    "add": add_contact,
    "list": list_contacts,
    "send": send_file,
    "exit": exit_shell,
}

Global_SecureDropShell = SecureDropShell()
