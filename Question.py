# Dependencies
from Database import Database

#
class Question:
    # Vars
    questionNumber: int
    prompt: str
    answer: str

    # Constructor
    def __init__(self, questionNumber: int, prompt: str, answer: str):
        # Set
        self.questionNumber = questionNumber
        self.prompt = prompt
        self.answer = answer

    # Gets all questions by a certain attribute
    def Get(Attribute: str, Value, database: Database):
        # Execute
        database.cursor.execute(f"SELECT * FROM question WHERE {Attribute} = ?", [Value])

        # Return
        return database.cursor.fetchall()

    # Gets a question by number
    def GetById(questionNumber: int, database: Database):
        # Get all the users
        questions = Question.Get("questionNumber", questionNumber, database)

        # Make sure length is > 0
        if (len(questions) == 0):
            return

        # Return first user
        return questions[0]

    # Adds a question to the database
    def Add(self, database: Database):
        # Make sure cursor exists
        database.IsConnected()
            
        # Make sure user id is not already within database
        if (Question.GetById(self.questionNumber, database)):
            raise RuntimeError("Question already within database")

        # Add to the database
        database.cursor.execute('''
        INSERT INTO question
        VALUES(?, ?, ?)
        ''', [self.questionNumber, self.prompt, self.answer])
        database.connection.commit()

    # Remove a question from the database
    def Remove(self, database: Database):
        # Make sure cursor exists
        database.IsConnected()
            
        # Make sure question is not already within database
        if (not Question.GetById(self.questionNumber, database)):
            raise RuntimeError("Question not within database")

        # Add to the database
        database.cursor.execute('''
        DELETE FROM question
        WHERE questionNumber = ?
        ''', [self.questionNumber])

    # Updates the question with all current information
    def Update(self, database: Database):
        # Make sure cursor exists
        database.IsConnected()
            
        # Make sure user id is not already within database
        if (not Question.GetById(self.userID, database)):
            raise RuntimeError("Question not within database")

        # Update
        database.cursor.execute('''
        UPDATE question
        SET prompt = ?,
            answer = ?
        WHERE questionNumber = ?
        ''', [self.prompt, self.answer, self.questionNumber])