import os
import sys
sys.path.append("Main")
from expense_tracker import main

def register():
    db = open("database.txt", "r")
    Username = input("Create Username: ")
    Password = input("Create Password: ")
    Password1 = input("Confirm Password: ")
    d = []
    f = []
    for i in db:
        a, b = i.split(", ")
        b = b.strip()
        d.append(a)
        f.append(b)
    data = dict(zip(d,f))

    if Password != Password1:
        print("Passwords don't match, try again!")    
        register()
    else:
        if len(Password) <= 7:
            print("Password too short, Try Again!")
            register()
        elif Username in db:
            print("Username has been used")
            register()
        else:
            db = open("database.txt", "a")
            db.write(Username + ", " + Password + "\n")
            print("Success! User registered.")

def access():
    db = open("database.txt", "r")
    Username = input("Enter Username: ")
    Password = input("Enter Password: ")

    if not len (Username or Password) < 1:
        d = []
        f = []
        for i in db:
            a,b = i.split(", ")
            b = b.strip()
            d.append(a)
            f.append(b)
        data = dict(zip(d,f))

        try:
            if data[Username]:
                try:
                    if Password == data[Username]:
                        os.system('cls')
                        print("Login Success")
                        print("Hi", Username)
                        main()
                    else:
                        print("Username/Password incorrect")
                        access ()
                except:
                    print("Incorrect Username/Password")
                    access()
            else:
                print("Username doesn't exist")
                access()
        except:
            print("Login Error!!!")
            access()

def home(option = None ):
    option = input("1. Login | 2. SignUp(2)\n" + ("Please enter option : ")) 
    if option == "1":
        access()
    elif option == "2":
        register()
    else:
        print("Please enter option")
home()