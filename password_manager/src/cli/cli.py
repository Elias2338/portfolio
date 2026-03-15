'''Command Line Interface for the Password Manager'''
from core.password_entries import Passwords
from core.save_data import save_data

def main_menu(password_list, keySafe):

    print("\n--- LOGIN SUCCESSFUL! WELCOME ---")

    while True:
        print("1. Show all passwords")
        print("2. Save password")
        print("3. Delete password (by service and user)")
        print("4. Finish")

        auswahl = input("\nWhat do you want to do? ")
        if auswahl not in "123":
            auswahl = "4"
        
        print(f"\nYou picked: {auswahl}\n")

        #Show all passwords
        if auswahl == "1":
            print("--- LIST OF ALL PASSWORDS ---\n")

            for i in range(len(password_list)):
                print(f"{i+1}.\n"
                    f"  Service: {password_list[i].service}\n"
                    f"  User: {password_list[i].username}\n"
                    f"  Password: {password_list[i].password}\n")
                
            print("--- END LIST OF ALL PASSWORDS ---\n3")

        #Save password
        if auswahl == "2":
            service = input("Service: ")
            username = input("Username: ")
            password = input("Password: ")

            #Add password to database
            password_list.append(Passwords(service, username, password))
            print(f"\nAdded Service: {service} with User: {username}\n")

        #Delete password
        if auswahl == "3":
            service = input("Service: ")
            username = input("Username: ")

            #Find correct Object to remove from database
            for potential_entry in password_list:
                if potential_entry.service == service and potential_entry.username == username:
                    password_list.remove(potential_entry)
                    print(f"\nDeleted Service: {service} with User: {username}\n")
                    break
            #If Object not in the database
            print(f"\nCould not find Service: {service} with User: {username}\n")

        #Finish program
        if auswahl == "4":
            save_data(password_list, keySafe)
            print("Terminating the program...\n")
            break

#Ask user for master password
def startpage():
    print("\n--- PASSWORT MANAGER ---\n")
    return input("Please enter the Password: ")


