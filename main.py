from typing import List
from Controller import Controller


class Main:
    initialMessage: str
    toUseMessage: str
    programManager: Controller

    def __init__(self):
        self.initialMessage = \
            "Hey Zendesker, welcome to the ticket viewer. Enjoy!"
        self.toUseMessage = "Here are your options: \n" + \
                            "Enter '1' to view all current tickets \n" + \
                            "Enter '2' to view a specific ticket by its ID," + \
                            " we will ask for the ID shortly \n" + \
                            "Enter 'update' to update the current tickets " + \
                            "available, this will fetch all tickets again. " + \
                            "\nEnter 'quit' to quit the program"

    def run(self):
        print("\n")
        print(self.initialMessage)
        self.programManager = Controller()
        while True:
            print("\n")
            print(self.toUseMessage)
            userInput = input("Please enter your selected option:")
            if userInput == "quit":
                print("Thank you for using, have a nice day!")
                exit()
            response = self.programManager.callCorrectMethod(userInput)
            if type(response) == list:
                if len(response) > 25:
                    pageView(response)
                for r in response:
                    print(r)
            else:
                print(response)


def calcPrevNewLimits(curr: List[int]):
    limits = [curr[0] - 25]
    if curr[1] % 25 == 0:
        limits.append(curr[1] - 25)
    else:
        closestBound = curr[1] // 25
        limits.append(closestBound)
    return limits


def calcNextNewLimits(curr: List[int], maximum: int):
    limits = [curr[1]]
    if curr[1] + 25 < maximum:
        limits.append(curr[1] + 25)
    else:
        limits.append(maximum - 1)
    return limits


def pageView(response: List[str]):
    page = 1
    if len(response) % 25 == 0:
        allPages = len(response) / 25
    else:
        allPages = len(response) // 25 + 1
    allPages = int(allPages)
    lowTicket = 0
    highTicket = 25
    while True:
        for r in response[lowTicket:highTicket]:
            print(r)
        print("Displaying page " + str(page) + " of " + str(allPages))
        usrInp = input("Enter 'next' to see the next page, " +
                       "'previous' to see previous page and 'back' to "
                       "return to main program")
        if usrInp == 'next':
            if page < allPages:
                page += 1
                limits = calcNextNewLimits([lowTicket, highTicket],
                                           len(response) + 1)
                lowTicket = limits[0]
                highTicket = limits[1]
            else:
                print("No next page")
        elif usrInp == 'previous':
            if page == 1:
                print("No previous page")
            else:
                limits = calcPrevNewLimits([lowTicket, highTicket])
                lowTicket = limits[0]
                highTicket = limits[1]
                page -= 1
        elif usrInp == 'back':
            return
        else:
            print("Not a valid input")


if __name__ == "__main__":
    m = Main()
    m.run()
