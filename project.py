import hashlib
import csv
import sys
import datetime
from tabulate import tabulate
from encryption import encrypt_vigenere as encrypt
from encryption import decrypt_vigenere as decrypt

today = datetime.date.today()

class User:
    def __init__(self, name, password, file= "users.csv"):
        """
        Create an object of a user
        The password will be hashed with SHA256 to fit the database
        if the user don't exist --> sys.exit()
        """
        self.name = name
        self.password = password
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()
        exist = False
        with open(file, 'r') as table:
            reader = csv.DictReader(table)
            for row in reader:
                if row['user_name'] == name and row['hashed_password'] == hashlib.sha256(password.encode()).hexdigest():
                    self.id = row['id']
                    exist = True
        if exist == False:
            sys.exit(f"The user don't exists in the file: {file}")

                

    @classmethod
    def new_user(cls, name, password, file= "users.csv"):
        """
        This methode is an alternative to __init__ and is used if the user doesn't exist in the data base yet
        Add a user to users.csv
        give it a new id
        create a new user object
        don't forget to flush() to the csv file
        """
        #add to csv, generate a new ID
        with open(file, 'r') as table_r , open(file, 'a', newline='') as table_a:
            reader = csv.DictReader(table_r)
            writer = csv.DictWriter(table_a,fieldnames=['id', 'user_name', 'hashed_password'])
            for row in reader:
                pass
            try:
                last_id = int(row['id'])
            except NameError:
                last_id = None
            if last_id == None:
                id_ = 1
            else:
                id_ = last_id + 1
            writer.writerow({'id': id_, 'user_name': name, 'hashed_password': hashlib.sha256(password.encode()).hexdigest()})

        instance = cls(name, password, file= file)
        return instance


    def new_table(self, *habits, month= "this", dir= "data", repertory= "tables.csv"): #month can eather be this or next
        """
        Creates a new table for this month or the next, acording to users input
        The user can create up to 1-5 habits and there will automaticaly be a 'Learning' value in the table
        take as args the way a new table will be created
        dont forget to flush the data
        writes in tables.csv the id and the the filename
        if wants to create an already existing table --> sys.exit()
        """

        if month == "this":
            with open(repertory, 'r') as tables:
                reader = csv.DictReader(tables)
                for row in reader:
                    if row['id'] == self.id and row["table_file_name"] == f"{self.id}_{today.month}_{today.year}.csv":
                        sys.exit('this habit tracker already exists')
            with open(f"{dir}/{self.id}_{today.month}_{today.year}.csv", "w") as table:
                encrypted_habits = ["day", "learning"]
                for hab in habits:
                    encrypted_habits.append(encrypt(self.password, hab))
                writer = csv.DictWriter(table, fieldnames= encrypted_habits)
                writer.writeheader()
            with open(repertory, 'a') as tables:
                writer =  csv.DictWriter(tables, fieldnames= ["id", "table_file_name"])
                writer.writerow({'id': self.id, 'table_file_name': f"{self.id}_{today.month}_{today.year}.csv"})
        else:
            new_month = today.month + 1
            new_year = today.year
            if new_month > 12:
                new_month = 1
                new_year = today.year + 1
            with open(repertory, 'r') as tables:
                reader = csv.DictReader(tables)
                for row in reader:
                    if row['id'] == self.id and row["table_file_name"] == f"{self.id}_{new_month}_{new_year}.csv":
                        sys.exit('this habit tracker already exists')
            with open(f"{dir}/{self.id}_{new_month}_{new_year}.csv", "w") as table:
                encrypted_habits = ["day", "learning"]
                for hab in habits:
                    encrypted_habits.append(encrypt(self.password, hab))
                writer = csv.DictWriter(table, fieldnames= encrypted_habits)
                writer.writeheader()
            with open(repertory, 'a') as tables:
                writer =  csv.DictWriter(tables, fieldnames= ["id", "table_file_name"])
                writer.writerow({'id': self.id, 'table_file_name': f"{self.id}_{new_month}_{new_year}.csv"})
        


    def today(self, dir= "data", repertory= "tables.csv", **kwargs):
        """
        Promps the user to track today's habits 'today' is based on system time
        If no table for this month the program exits
        dont forget to flush the data
        Don't allow the user to do 2 «today entries» the same Day
        """
        with open(repertory, 'r') as tables:
            reader = csv.DictReader(tables)
            exist = False
            for row in reader:
                if row['id'] == self.id and row['table_file_name'] == f"{self.id}_{today.month}_{today.year}.csv":
                    exist = True
            if not exist:
                sys.exit("You don't have a habit tracker for this month, you can create one using the 'n' mode")
        try:
            with open(f"{dir}/{self.id}_{today.month}_{today.year}.csv", 'r') as table:
                reader = csv.DictReader(table)
                last_row = None
                for row in reader:
                    last_row = row
                if last_row and last_row['day'] == str(today.day):
                    sys.exit('You already completed your entry today')
        except FileNotFoundError:
            sys.exit(f"Habit tracker not found but is on {repertory}")

        with open(f"{dir}/{self.id}_{today.month}_{today.year}.csv", 'a') as table:
            fieldn = ['day']
            for field in kwargs.keys():
                if field == 'learning':
                    fieldn.append(field)
                else:
                    fieldn.append(encrypt(self.password, field))
            writer = csv.DictWriter(table, fieldnames= fieldn)
            dicttowrite = {}
            for field in fieldn:
                if field == 'day':
                    dicttowrite[field] = today.day
                elif field == 'learning':
                    dicttowrite[field] = encrypt(self.password, kwargs['learning'])
                else:
                    dicttowrite[field] = kwargs[decrypt(self.password, field)]
            writer.writerow(dicttowrite)


    def show(self, table, dir= "data"):
        """
        Print on the command line the specified table using tabulate module
        """
        with open(f"{dir}/{table}", 'r') as table:
            reader = csv.reader(table)
            reader = csv.DictReader(table)
            head = reader.fieldnames
            for i in range(len(head)):
                if head[i] == 'day':
                    pass
                elif head[i] == 'learning':
                    pass
                else:
                    head[i] = decrypt(self.password, head[i])

            table = []
            for i in reader:
                tmp= []
                for j in i:
                    if j == 'day':
                        tmp.append(i[j])
                    elif j == 'learning':
                        tmp.append(decrypt(self.password, i[j]))
                    else:
                        tmp.append(i[j])        
                table.append(tmp)

            print(tabulate(table,headers=head, tablefmt="grid"))
            

    


def main():
    global today
    """
    this function is used to have all the logic of the behavior of the program, regcognise the command line arguments, error handling, interact with functions
    """
    if len(sys.argv) != 2:
        sys.exit("Wrong use of commad line args, run 'python project.py help'")
    if sys.argv[1].lower() == "h" or sys.argv[1].lower() == "help":
        print_help()
        sys.exit()
    elif sys.argv[1].lower() not in ["t", "l", "n", "p", "s"]:
        sys.exit("Wrong use of commad line args, run 'python project.py help'")
    
    while True:
        status = input("Do you have an account ? (yes/no): ").lower()
        if status == "yes" or status == "no":
            break
        else:
            print("Answer by 'yes' or 'no'.")

    if status == "yes":
        user_name, password = login()
        user = User(user_name, password)
    else:
        user_name, password = sign_up()
        user = User.new_user(user_name, password)

    if sys.argv[1] == "n":
        while True:
            month = input("You want to create a new table for this or next month ? (this/next): ")
            if month == "this" or month == "next":
                break
        while True:
            try:
                n = int(input("How many habits do you want to track ? (advice: 1 to 3): "))
            except ValueError:
                pass
            else:
                break
        habits = []
        for i in range(n):
            habits.append(input(f"What is habit number {i + 1}? "))
            
        user.new_table(*habits, month= month)

    elif sys.argv[1] == "t":
        with open("tables.csv", 'r') as tables:
            reader = csv.DictReader(tables)
            exist = False
            for row in reader:
                if row['id'] == user.id and row['table_file_name'] == f"{user.id}_{today.month}_{today.year}.csv":
                    exist = True
            if not exist:
                sys.exit("You don't have a habit tracker for this month, you can create one using the 'n' mode")
        kwarg = {}
        with open(f"data/{user.id}_{today.month}_{today.year}.csv", "r") as table:
            reader = csv.DictReader(table)
            for field in reader.fieldnames:
                if field == "learning":
                    kwarg[field] = input("What did you learn today? ")
                elif field == "day":
                    pass
                else:
                    while True:
                        kwarg[field] = input(f"Did you {decrypt(user.password, field)} today? (yes/no) ")
                        if kwarg[field].lower() == 'yes' or kwarg[field].lower() == 'no':
                            break
        user.today(**kwarg)

    elif sys.argv[1] == "p":
        with open('tables.csv', 'r') as tables:
            list_of_trackers = []
            reader = csv.DictReader(tables)
            for row in reader:
                if row['id'] == user.id:
                    list_of_trackers.append(row['table_file_name'])
        try:
            if list_of_trackers[0]:
                print('Here are all you habit trackers tables:')
        except IndexError:
            print(f"User: {user.name} don't have any habit trackers table")
            sys.exit("you dont have any habit tracker")
        for x in sorted(list_of_trackers):
            print(x)
        while True:
            x = input("Which table do you want to print ? \n(write the name of the table as displayed): ")
            if x in list_of_trackers:
                break
        user.show(x)
        





    


def login():
    name = input("User name: ")
    while len(name) < 4:
        name = input("User name: ")
    password = input("Password: ")
    while len(password) < 8:
        print("At least 8 characters")
        password = input("Password: ")
    return name, password

def sign_up():
    name = input("User name: ")
    while len(name) < 4:
        name = input("User name: ")
    while True:
        password = input("Password: ")
        if len(password) < 8:
            print("At least 8 characters")
        else:
            confirm = input("Confirm your password: ")
            if password == confirm:
                break
    return name, password

def print_help():
    print(
        "t: Complete today's line\n" +
        "n: Create a new montly table\n" +
        "p: Print on the terminal the specified table using tabulate module")






if __name__ == "__main__":
    main()