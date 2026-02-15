# Self-mastery habit tracker
### Video Demo:  https://www.youtube.com/watch?v=QZJYQkulDWk&ab_channel=HediBenJemaa
### Description:

---

#### Disclaimer:
I wrote all the text myself — ChatGPT just helped format it nicely in Markdown.

---

Three months ago, I started using a habit tracker in my analog journal. It helps me understand what I’m actually doing each day, seen on a monthly scale. The tracker is simple: I write down, in one sentence, what I learned that day (it can be a new computer science concept, a philosophical idea, or even a new Brazilian Jiu-Jitsu move), since I value continuous learning. Then I go through the three or four habits I’ve set for the month and check a box if I did them—or leave it blank if I didn’t. It’s binary: either yes or no. I go through this process every night before bed. (I've included a picture of it.)

This analog system is easy to use, but it has some disadvantages:  
1. I have to carry my journal everywhere I plan to sleep.  
2. I have to manually draw a new table every month.  
3. Anyone can simply open my journal and read about my personal struggles. For example, a secretly alcoholic person might track a habit like “don’t drink.” He wouldn’t want his wife to open the journal and discover he's struggling with alcohol.

So I decided to build this habit tracker digitally, as my final CS50P project, using Python. The project was challenging, and I learned a lot across different areas:  
- I learned security concepts like hashing and encryption.  
- I improved my file handling skills in Python (context managers—David Malan and Carter Zenke told you!).  
- I learned test-driven development.  
- And much more...

---

#### Required project folder structure:

- `project.py`  
- `test_project.py`  
- `encryption.py`  
- `env/` — virtual environment *(not strictly required if `project.py` and `test_project.py` are run within the correct environment)*  
- `data/` — folder for user data  
- `test_data/` — folder for test data 
- `tables.csv`      (first line: "id,table_file_name\n")
- `test_tables.csv` (first line: "id,table_file_name\n")
- `users.csv`       (first line: "id,user_name,hashed_password\n")
- `test_users.csv`  (first line: "id,user_name,hashed_password\n")

---

#### User class:

##### Instance variables:
- `id` : User ID as stored in `users.csv`  
- `name` : Username as stored in `users.csv`  
- `password` : The plain password input by the user. It is never stored on the hard drive—only exists in RAM while `project.py` is running (and in the user’s brain 😄).  
- `hashed_password` : The SHA-256 hashed version of the password, as stored in `users.csv`.

##### Instance methods:
- `__init__` : Initializes a `User` object only if user authentication is successful (i.e., the hashed password provided by the user matches the hashed password in the file, e.g., `users.csv`).  
- `new_user` : If the user does not yet have an account (i.e., is not in the auth database such as `users.csv`), this class method will create a new user entry in the database and return a `User` object via `__init__`.  
- `new_table` : Creates a new CSV habit tracker table in a folder (e.g., `data/`). This new table is also recorded in another CSV file (e.g., `tables.csv`). The habit tracker can include a variable number of habits. These habits are encrypted in the CSV to preserve user privacy (since someone could otherwise open the CSV and read the tracked habits).  
- `today` : Takes `**kwargs` containing the user's entries for the day. The method encrypts sensitive data (such as the "learning" entry) and updates the habit tracker accordingly.  
- `show` : Displays the habit tracker in the terminal using ASCII-art table formatting.



#### Functions — `project.py`

- `main` : I wrote `main` thinking of it as a switch, due to its tree-like structure of decisions (if-then style). It handles all user interaction.  
- `login` : This function handles user interaction by prompting for login inputs. As such, it’s not really unit-testable.  
- `sign_up` : This function handles user interaction by prompting for account creation inputs. Like `login`, it is not easily unit-testable.
- `print_help` : If `sys.argv[1]` is `'h'` or `'help'`, `main` will call this function to display the program’s available modes.

---

#### Functions — `encryption.py`

- `encrypt_vigenere` : Takes a key and a message, and encrypts the message using the Vigenère cipher.  
- `decrypt_vigenere` : Takes a key and an encrypted message, and decrypts it using the Vigenère cipher.



# About Me


### First Name: Hedi  
### Last Name: Ben Jemaa  
### From: Tunis, Tunisia `and` Paris, France 
### edX: Hedi_BJ
### GitHub: Hedi-BJ
### Contact:  
- **Instagram**: [@hedi_benjemaa](https://instagram.com/hedi_benjemaa)  
- **Email**: [hedibenjemaa.pro@gmail.com](mailto:hedibenjemaa.pro@gmail.com)
