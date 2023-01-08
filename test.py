# Dependencies
from Database import Database
from User import User
from Question import Question
from Answer import Answer

# Initialise database
database = Database("Quiz")
database.connect()

# User Checks
if True:
    # Get all users
    database.cursor.execute("SELECT * FROM user")
    allUsers = [dict(row) for row in database.cursor.fetchall()]
    print(f"Grabbed user table:\n{allUsers}")

    # Create a user
    testUser = User(
        1,
        "test_User",
        "Bob",
        "Smith",
        "MrBob"
    )

    # Add user to database
    try:
        testUser.Add(database)
        print("Added test user to database")
    except:
        print("User already in database")

    # Grab user
    testUserDB = User.GetById(1, database)
    if (testUserDB == None):
        print("Unable to get test user")
    else:
        print(f"Grabbed test user - {testUserDB['username']}")

# Question Checks
if True:
    # Get all questions
    database.cursor.execute("SELECT * FROM question")
    allQuestions = [dict(row) for row in database.cursor.fetchall()]
    print(f"Grabbed question table:\n{allQuestions}")

    # Create a question
    question = Question(
        None,
        "69 + 420 = ?",
        "489"
    )

    # Add question to database
    try:
        question.Add(database)
        print("Added question to database")
    except:
        print("Unable to add question to database")

    # Grab question
    questionDB = Question.GetById(1, database)
    if (questionDB == None):
        print("Unable to get question")
    else:
        print(f"Grabbed question - {questionDB['prompt']} > {questionDB['answer']}")

# Answer Checks
if False:
    # Get all answers
    database.cursor.execute("SELECT * FROM answer")
    allAnswers = [dict(row) for row in database.cursor.fetchall()]
    print(f"Grabbed answer table:\n{allAnswers}")

    # Create an answer
    answer = Answer(
        1,
        1,
        1
    )

    # Add answer to database
    try:
        answer.Add(database)
        print("Added answer to database")
    except:
        print("Unable to add answer to database")

    # Grab answer
    answerDB, _, _ = Answer.GetById((1, 1), database)
    if (answerDB == None):
        print("Unable to get answer")
    else:
        print(f"Was {answerDB['correct'] == 1 and 'correct' or 'incorrect'}")