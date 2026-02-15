import pytest
import csv
import os
from project import User
import datetime
from encryption import encrypt_vigenere as encrypt
from encryption import decrypt_vigenere as decrypt




@pytest.fixture
def user1():
    return User(name= "hedi", password= "12345678", file= "test_users.csv")

@pytest.fixture
def user2():
    return User(name= "Lili BenJ", password= "abcdefgh", file= "test_users.csv")


def test_encryption():
    assert 'abcdefg1234??. this Was cs50' == decrypt('this is cs50', encrypt('this is cs50', 'abcdefg1234??. this Was cs50')) 

def test_new_user_fist_one():
    """
    test to create the first user
    """
    with open("test_users.csv",'w') as table_w:
        writer = csv.DictWriter(table_w, fieldnames= ['id', 'user_name', 'hashed_password'])
        writer.writeheader()
    user = User.new_user(name="hedi", password="12345678", file= "test_users.csv") # new_user will flush the data to csv
    assert user.name == "hedi"
    assert user.password == "12345678"
    assert user.hashed_password == "ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f"
    assert user.id == '1'
    with open("test_users.csv", 'r') as table:
        ishere = False #will check if the id is even here, if it stays False then that mean the id isn't here
        reader = csv.DictReader(table)
        for row in reader:
            if int(row["id"]) == 1:
                ishere = True
                assert row["user_name"] == user.name
                assert row["hashed_password"] == user.hashed_password
                break
        assert ishere == True


def test_new_user_next_one():
    """
    Here we test if the program succesfulully creates a new(second) user
    """
    user = User.new_user("Lili BenJ", "abcdefgh", file= "test_users.csv") # new_user will flush the data to csv
    assert user.name == "Lili BenJ"
    assert user.password == "abcdefgh"
    assert user.hashed_password == "9c56cc51b374c3ba189210d5b6d4bf57790d351c96c47c02190ecf1e430635ab"
    assert user.id == '2'
    with open("test_users.csv", 'r') as table:
        ishere = False 
        reader = csv.DictReader(table)
        for row in reader:
            if int(row["id"]) == 2:
                ishere = True
                assert row["user_name"] == user.name
                assert row["hashed_password"] == user.hashed_password
                break
        assert ishere == True





def test_init1(user1):
    """
    the first user is created
    we now create an istance based on an already existing user
    """
    assert user1.name == "hedi"
    assert user1.password == "12345678"
    assert user1.hashed_password == "ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f"
    assert user1.id == '1'



def test_new_table_this(user2): #here i have to do mocks about user input, actually no need for that
    """
    will check if the file is referenced in test_tables.csv /done
    will open a file in the 'test_data' directry / done
    the file name is f'{id}_{month}_{year}.csv' / done
    will then create a file and use as fildnames the user input /done
    the fildnames will be crypted, the key is the user.password / done
    will test if the fildnames are correct / done
    will delete the csvv so that other tests can be run / not sure if if should
    """
    with open('test_tables.csv', 'w') as tables:
        writer = csv.DictWriter(tables, fieldnames= ['id','table_file_name'])
        writer.writeheader()

    today = datetime.date.today()
    file_name = f"{user2.id}_{today.month}_{today.year}.csv"
    try:
        os.remove(f"test_data/{file_name}")
    except FileNotFoundError:
        pass

    user2.new_table("30min gym", "sleep before 11PM", "practice guitar for 30min", month= "this", dir= "test_data", repertory="test_tables.csv")
    with open(f"test_tables.csv", 'r') as tables:
        reader = csv.DictReader(tables)
        for row in reader:
            pass
        assert row["id"] == user2.id
        assert row["table_file_name"] == file_name
    try:
        with open(f"test_data/{file_name}", "r") as table:
            assert True
    except FileNotFoundError:
        # no need to clean the csv since the clean up is done at the start of the program
        #tables_csv_w.truncate() #but i do it bc i am not sure depending on other tests
        pytest.fail(f"The file '{file_name}' is not found in the directory 'test_data'")
    
    # mock input maybe no need to mock, i can maybe use an iterator or something, actually i put the habits as *args
    with open(f"test_data/{file_name}", "r") as table:
        reader = csv.DictReader(table)
        assert reader.fieldnames[0] == 'day'
        assert reader.fieldnames[1] == 'learning'
        assert reader.fieldnames[2] == 'trQNTfObO'
        assert reader.fieldnames[3] == 'UOIJVfJNHRVJewx9/'
        assert reader.fieldnames[4] == 'RUEHZPKNaJYNZHZhHRVdxvURP'

def test_new_table_next(user2):
    today = datetime.date.today()
    new_month = today.month + 1
    new_year = today.year
    if new_month > 12:
        new_month = 1
        new_year = today.year + 1
    file_name = f"{user2.id}_{new_month}_{new_year}.csv"

    try:
        os.remove(f"test_data/{file_name}")
    except FileNotFoundError:
        pass

    user2.new_table("30min gym", "sleep before 11PM", "practice guitar for 30min", month= "next", dir= "test_data", repertory="test_tables.csv")
    with open(f"test_tables.csv", 'r') as tables:
        reader = csv.DictReader(tables)
        for row in reader:
            pass
        assert row["id"] == user2.id
        assert row["table_file_name"] == file_name
    try:
        with open(f"test_data/{file_name}", "r") as table:
            assert True
    except FileNotFoundError:
        # no need to clean the csv since the clean up is done at the start of the program
        pytest.fail(f"The file '{file_name}' is not found in the directory 'test_data'")
    

def test_today(user2):
    today = datetime.date.today()
    kw = {'learning': 'python iter() and yied',
          '30min gym': 'yes',
          'sleep before 11PM': 'no',
          'practice guitar for 30min': 'yes'}

    user2.today(dir= "test_data", repertory="test_tables.csv",**kw)
    today = datetime.date.today()
    file_name = f"{user2.id}_{today.month}_{today.year}.csv"
    with open(f"test_data/{file_name}", 'r') as table:
        reader = csv.DictReader(table)
        for row in reader:
            pass
        assert row['day'] == str(today.day)
        assert row['learning'] == r'R\XMUUgRVHVlnfIWFb]NKK'
        assert row[encrypt('abcdefgh', '30min gym')] == 'yes'
        assert row[encrypt('abcdefgh', 'sleep before 11PM')] == 'no'
        assert row[encrypt('abcdefgh','practice guitar for 30min')] == 'yes'

    today = datetime.date.today()
    new_month = today.month + 1
    new_year = today.year
    if new_month > 12:
        new_month = 1
        new_year = today.year + 1
    file_name = f"{user2.id}_{new_month}_{new_year}.csv"
    try:
        os.remove(f"test_data/{file_name}")
    except FileNotFoundError:
       pass
    file_name = f"{user2.id}_{today.month}_{today.year}.csv"
    try:
        os.remove(f"test_data/{file_name}")
    except FileNotFoundError:
       pass
    
