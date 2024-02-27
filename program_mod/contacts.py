import json
from registration_mod.validation import Validation

def add_contact():
    """Add a new contact"""
    try:
        with open("contacts.json", "r") as infile:
            contacts = json.load(infile)
    except FileNotFoundError:
        contacts = []

    data = {}
    data["name"] = input("  Enter Full Name: ")
    data["email"] = input("  Enter Email Address: ")
    while(not Validation.valid_email(data["email"])):
        data["email"] = input("  Enter Email Address: ")
    data["online"] = False      # default to offline

    # add data in contacts list
    for contact in contacts:
        if contact["email"] == data["email"]:
            contact["name"] = data["name"]
            contact["online"] = data["online"]
            break
    else:
        contacts.append(data)

    with open("contacts.json", "w") as outfile:
        json.dump(contacts, outfile, indent = 1)

    print("  Contact Added.")


def list_contacts():
    """List all online contacts"""
    try:
        with open("contacts.json", "r") as infile:
            contacts = json.load(infile)
    except FileNotFoundError:
        contacts = []
    print("  The following contacts are online:")

    for contact in contacts:
        # TODO: check if contact is added,
        #       if contact has sent message at least once,
        #       if contact is online (if online.py is running)
        if contact["online"] != False:
            print("  * {}".format(contact["name"]) + " <{}>".format(contact["email"]))
