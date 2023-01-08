# Dependencies
from math import floor
from Database import Database
from User import User
from Answer import Answer
from Menu import Menu
import os

# Initialise database
database = Database("Quiz")
database.connect()

# Clears the console
def clear():
    # Windows
    if (os.name == "nt"):
        os.system("cls")
    else: # others
        os.system("clear")

# Grabs input from user
def GrabInput(prompt: str, Rtype: any = str, maxLength: int = 2147483647):
    response = None
    while True:
        # Grab user response
        response = input(prompt)

        # Ensure type matches
        try:
            response = Rtype(response)
        except:
            print("Invalid input, please try again.")
            continue

        # Check length
        if (type(response) == str and len(response) > maxLength) or (type(response) == int and response > maxLength):
            print("Invalid input, please try again")
            continue

        # Done
        break

    # Return
    return response
        
# Prompt login
loginMenu = Menu("Select one", None, [
    "Login",
    "Register"
])
loginmenuresponse, _ = loginMenu.Start(None, True)
user = None

if (loginmenuresponse == "Login"):
    user = User.PromptLogin(database)
    print(f"Logged in as {user.username}")
elif (loginmenuresponse == "Register"):
    # Make sure username is not taken
    username = GrabInput("Please enter your username:\n> ", str, 20)
    if (len(User.Get("username", username, database)) != 0):
        print("Invalid username.")
        os.abort()

    # Grab rest of inputs
    firstName = GrabInput("Please enter your first name:\n> ", str, 20)
    surname = GrabInput("Please enter your surname:\n> ", str, 20)
    password = GrabInput("Please enter your password:\n> ", str, 20)

    # Create user
    user = User(None, username, firstName, surname, password)
    user.Add(database)

# Grab every question
database.cursor.execute("SELECT * FROM question")
questionsList = [dict(row) for row in database.cursor.fetchall()]
questions = iter(questionsList)

# Menu
while True:
    clear()

    # User input
    menu = Menu("Select one", None, [
        "Answer the next question",
        "View question statistics"
    ])

    # Getting repsonse
    menuresponse, _ = menu.Start(None, True)

    # Doing it
    if (menuresponse == "Answer the next question"):
        # Grab the next question
        question = questions.__next__()

        # Prompt the question and see if they got it correct
        answer = input(question["prompt"] + "\n> ")
        correct = int(answer == question['answer'])

        # Add answer to database
        try:
            Answer(
                question['questionNumber'],
                user.userID,
                correct
            ).Add(database)
        except:
            print("You have already answered this question, your answer will not be registered.")

        # Grab all answers for this question
        database.cursor.execute("SELECT * FROM answer WHERE questionNumber = ?", [question['questionNumber']])
        answers = [dict(row) for row in database.cursor.fetchall()]
        correctAnswers = list(filter(lambda answer: bool(answer['correct']), answers))
        correctPercentage = floor((len(correctAnswers) / len(answers)) * 100)

        # Tell the user some data
        print(f"You got the question {correct and 'correct' or 'incorrect'}. {correctPercentage}% (out of {len(answers)}) of users got this question right.\nPress enter to continue...")
        input()
    elif (menuresponse == "View question statistics"):
        # Ask for a question number
        questionNumber = GrabInput("Please enter the question number you would like to see:\n> ", int, len(questionsList))
        
        # Grab all answers for this question
        database.cursor.execute("SELECT * FROM answer WHERE questionNumber = ?", [questionNumber])
        answers = [dict(row) for row in database.cursor.fetchall()]

        # Division by 0
        answerCount = len(answers)
        if (answerCount == 0):
            print("No one has answered this question yet.\nPress enter to continue...")
        else:
            # Maths
            correctAnswers = list(filter(lambda answer: bool(answer['correct']), answers))
            correctPercentage = floor((len(correctAnswers) / answerCount) * 100) 

            # Output
            print(f"Out of {answerCount} answers, {correctPercentage}% were correct!\nPress enter to continue...")

        #
        input()