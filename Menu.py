# Dependencies
from __future__ import annotations
from typing import List, Tuple

# A console menu selection system
class Menu:
    name = "Menu 1"
    parent = None # a menu
    children = [] # list of str or menu

    # Constructor
    def __init__(self, name: str = "Menu 1", parent = None, children: List[Tuple(str, Menu)] = []):
        self.name = name
        self.parent = parent
        self.children = children

        if (parent):
            parent.children.append(self)

    # Add an child to the menu
    def Add(self, name: Tuple(str, Menu)):
        self.children.append(name)

    # Returns what to prompt the user
    def GetPrompt(self):
        prompt = ""

        for i, child in enumerate(self.children):
            name = child.name if isinstance(child, Menu) else child
            prompt += f"{i}. {name}\n"

        if (self.parent):
            prompt += f"{len(self.children)}. Exit\n"

        return prompt + "> "

    # Prompts the actual user for a response
    def Prompt(self):
        prompt = self.GetPrompt()
        response = input(prompt)
        childrenCount = len(self.children)
        max = childrenCount if (self.parent) else childrenCount - 1

        # Checking for invalid responses
        while (response.isnumeric() == False or (0 > int(response) or int(response) > max)):
            print("Invalid.")
            response = input(prompt)

        #
        return int(response)

    # Recursive prompt
    def Start(self, menu = None, printTitle = True):
        # Default
        menu = menu or self

        # Prompt the user and resolve it
        if (printTitle):
            print(self.name)
        response = menu.Prompt()
        result = "exit" if response == len(menu.children) else menu.children[response]

        # Exiting
        if (result == "exit"):
            # Make sure there is a parent
            if (menu.parent == None):
                print("No parent.")

            # Restart with parent menu
            parent = menu.parent
            print(parent.name)
            return self.Start(parent)
        # If it's a string, we found the bottom most node and cannot go further
        if (isinstance(result, str)):
            return result, menu
        else:
            # Another menu
            return self.Start(result)