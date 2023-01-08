# Dependencies
import sqlite3

#
class Database:
    # Vars
    name = "Quiz"
    cursor = None
    connection = None

    # Constructor
    def __init__(self, name: str):
        self.name = name

    # Connect to the database
    def connect(self):
        with sqlite3.connect(f"{self.name}.db") as db:
            # Connect
            self.connection = db
            db.row_factory = sqlite3.Row # SELECT returns as dict, instead of tuple
            self.cursor = db.cursor()
            print(f"Connected to database ({self.name})")

            # Initialise
            self.InitialiseDB()
            print(f"Initialised database ({self.name})")

    # Checks if database has connected, raises an error if not
    def IsConnected(self):
        # Make sure we have connected
        if (not self.cursor):
            raise RuntimeError("Not connected to Database")

        # Return
        return True

    # Initialise data, creating tables, etc.
    def InitialiseDB(self):
        # Make sure we have connected
        self.IsConnected()

        # Create tables
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(20) NOT NULL,
            firstName VARCHAR(20) NOT NULL,
            surname VARCHAR(20) NOT NULL,
            password VARCHAR(20) NOT NULL
        );
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS question (
            questionNumber INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            answer TEXT NOT NULL
        );
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS answer (
            questionNumber INTEGER NOT NULL,
            userID INTEGER NOT NULL,
            correct INTEGER,
            FOREIGN KEY (questionNumber) REFERENCES question(questionNumber),
            FOREIGN KEY (userID) REFERENCES user(userID),
            PRIMARY KEY (questionNumber, userID)
        );
        ''')