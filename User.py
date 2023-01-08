# Dependencies
from Database import Database
from typing import Union

#
class User:
    # Vars
    userID: Union[int, None]
    username: str
    firstName: str
    surname: str
    password: str

    # Constructor
    def __init__(self, userID: Union[int, None], username: str, firstName: str, surname: str, password: str):
        # Make sure not more than 20 characters long
        if (len(username) >= 20 or len(firstName) >= 20 or len(surname) >= 20 or len(password) >= 20):
            raise ValueError("One of your string values is longer then 20 characters")

        # Set
        self.userID = userID
        self.username = username
        self.firstName = firstName
        self.surname = surname
        self.password = password

    # Gets all users by a certain attribute
    def Get(Attribute: str, Value, database: Database):
        # Execute
        database.cursor.execute(f"SELECT * FROM user WHERE {Attribute} = ?", [Value])

        # Return
        return database.cursor.fetchall()

    # Gets a user by user id
    def GetById(userID: int, database: Database):
        # Get all the users
        users = User.Get("userID", userID, database)

        # Make sure length is > 0
        if (len(users) == 0):
            return

        # Return first user
        return users[0]

    # Adds the user to the database
    def Add(self, database: Database):
        # Make sure cursor exists
        database.IsConnected()
            
        # Make sure user id is not already within database
        if (User.GetById(self.userID, database)):
            raise RuntimeError("User already within database")

        # Add to the database
        database.cursor.execute('''
        INSERT INTO user
        VALUES(?, ?, ?, ?, ?)
        ''', [self.userID, self.username, self.firstName, self.surname, self.password])
        database.connection.commit()

    # Remove a user from the database
    def Remove(self, database: Database):
        # Make sure cursor exists
        database.IsConnected()
            
        # Make sure user id is not already within database
        if (not User.GetById(self.userID, database)):
            raise RuntimeError("User not within database")

        # Add to the database
        database.cursor.execute('''
        DELETE FROM user
        WHERE userID = ?
        ''', [self.userID])

    # Updates the user with all current information
    def Update(self, database: Database):
        # Make sure cursor exists
        database.IsConnected()
            
        # Make sure user id is not already within database
        if (not User.GetById(self.userID, database)):
            raise RuntimeError("User not within database")

        # Update
        database.cursor.execute('''
        UPDATE user
        SET username = ?,
            firstName = ?,
            surname = ?,
            password = ?
        WHERE userID = ?
        ''', [self.username, self.firstName, self.surname, self.password, self.userID])

    # Prompt user to login
    def PromptLogin(database: Database):
        # Vars
        user = None
        username = None
        password = None

        # Loop
        while True:
            # Ask for the username
            username = input("Please enter your username:\n> ")

            # Validate input
            lenPassword = len(username)
            if (lenPassword == 0 or lenPassword > 20):
                print("Invalid username, too long/short")
                continue

            # Ask for the password
            password = input("Please enter your password:\n> ")

            # Validate input
            lenPassword = len(password)
            if (lenPassword == 0 or lenPassword > 20):
                print("Invalid password, too long/short")
                continue

            # Find user in database with match
            database.cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", [username, password])

            # Check we got something
            user = database.cursor.fetchone()
            if (user == None):
                print("Invalid login, please try again")
                continue

            # Done
            user = dict(user)
            break

        # Deconstruct user to tuple, create User object and return
        return User(user["userID"], user["username"], user["firstName"], user["surname"], user["password"])