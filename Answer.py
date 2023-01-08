# Dependencies
from typing import Tuple
from Database import Database

#
class Answer:
    # Vars
    questionNumber: int
    userID: int
    correct: int # should be 1 or 0

    # Constructor
    def __init__(self, questionNumber: int, userID: int, correct: int):
        # Set
        self.questionNumber = questionNumber
        self.userID = userID
        self.correct = correct

    # Gets all answers by a certain attribute
    def Get(Attribute: str, Value, database: Database):
        # Execute
        database.cursor.execute(f"SELECT * FROM answer WHERE {Attribute} = ?", [Value])

        # Return
        return database.cursor.fetchall()

    # A helper method for figuring out what where clause
    def Where(questionUserId: tuple):
        # Ensure the length is 2
        assert(len(questionUserId) == 2, "invalid questionUserId")
        assert(not (questionUserId[0] == None and questionUserId[1] == None), "invalid questionUserId")

        # Vars
        where = ""
        params = []

        # Could probably be optimised
        if (questionUserId[0] != None and questionUserId[1] != None):
            where = "questionNumber = ? AND userID = ?"
            params = [questionUserId[0], questionUserId[1]]
        else:
            if (questionUserId[0] == None):
                where = "userID = ?"
                params = [questionUserId[0], questionUserId[1]]
            else:
                where = "questionNumber = ?"
                params = [questionUserId[0], questionUserId[0]]

        # Return
        return where, params
    # Gets a question by question number (and possibly a user)
    def GetById(questionUserId: tuple, database: Database):
        # Perform the query
        where, params = Answer.Where(questionUserId)
        database.cursor.execute(f"SELECT * FROM answer WHERE {where}", params)

        # Make sure length is > 0
        questions = database.cursor.fetchall()
        if (len(questions) == 0):
            return

        # Return first user
        return questions[0], where, params

    # Adds an answer to the database
    def Add(self, database: Database):
        # Make sure cursor exists
        database.IsConnected()
            
        # Make sure user id is not already within database
        if (Answer.GetById((self.questionNumber, self.userID), database)):
            raise RuntimeError("Answer already within database")

        # Add to the database
        database.cursor.execute('''
        INSERT INTO answer
        VALUES(?, ?, ?)
        ''', [self.questionNumber, self.userID, self.correct])
        database.connection.commit()

    # Remove a question from the database
    def Remove(self, database: Database):
        # Make sure cursor exists
        database.IsConnected()

        # Make sure question is not already within database
        question, where, params = Answer.GetById((self.questionNumber, self.userID), database)
        if (not question):
            raise RuntimeError("Question not within database")

        # Add to the database
        database.cursor.execute(f'''
        DELETE FROM question
        WHERE {where}
        ''', params)

    # Updates the question with all current information
    def Update(self, database: Database):
        # Make sure cursor exists
        database.IsConnected()
            
        # Make sure user id is not already within database
        assert(self.questionUserId[0] != None and self.questionUserId[1] != None, "invalid questionUserId")
        question = Answer.GetById((self.questionNumber, self.userID), database)
        if (not question):
            raise RuntimeError("Question not within database")

        # Update
        database.cursor.execute('''
        UPDATE question
        SET correct = ?
        WHERE questionNumber = ? AND userID = ?
        ''', [self.correct, self.questionNumber, self.userID])