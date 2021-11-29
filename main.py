from typing import List
import requests
import datetime


class APIFetcher:
    email: str
    password: str
    subdomain: str

    def __init__(self):
        self.email = "shehzaad767@gmail.com"
        self.password = "zendeskHOPETOPASS"
        self.subdomain = "zccshehzaad777.zendesk.com"

    def getTickets(self):
        link = "https://" + self.subdomain + "/api/v2/tickets.json"
        response = requests.get(link, auth=(self.email, self.password))
        if response.status_code != 200:
            fail_message = 'Status:' + str(response.status_code) + "\n" + \
                           'Problem with the request. Exiting...'
            print(fail_message)
            exit()

        data = response.json()
        tickets = []
        for ticket in data["tickets"]:
            t_id = ticket["id"]
            created_at = ticket["created_at"]
            description = ticket["description"]
            title = ticket["subject"]
            lastUpdate = ticket["updated_at"]
            t = Ticket(t_id, created_at,
                       description, title, lastUpdate)
            tickets.append(t)
        return tickets


def formatDate(iso: str):
    return str(datetime.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ"))


class Ticket:
    """This class provides a format for the ticket details to then be shown on
    screen in a Presenter class."""
    id: int
    created_at: str
    description: str
    subject: str
    lastUpdate: str

    def __init__(self, t_id: int, created_at: str,
                 desc: str, subject: str, lastUpdate: str):
        self.id = t_id
        self.created_at = created_at
        self.description = desc
        self.subject = subject
        self.lastUpdate = lastUpdate

    def formattedTicket(self):
        green = '\033[92m'
        END = '\033[0m'
        formattedTicket = "\n" + \
                          f"{green}Ticket ID: " + \
                          f"{str(self.id)} \n" + \
                          f"Subject: {self.subject}{END}" + \
                          "\n" + "Created at: " + \
                          formatDate(
                              self.created_at) + ", Last Updated: " + \
                          formatDate(self.lastUpdate) + \
                          "\n" + "Ticket Description: " + self.description + \
                          "\n"
        return formattedTicket


class Tickets:
    tickets: List[Ticket]

    def __init__(self, tickets: List[Ticket] = None):
        if tickets is None:
            self.tickets = []
        else:
            self.tickets = tickets

    def addTickets(self, tickets: List[Ticket]):
        self.tickets.extend(tickets)

    def getAllTickets(self):
        return self.tickets

    def getTicketByID(self, t_id: int):
        for ticket in self.tickets:
            if ticket.id == t_id:
                return ticket
        return "No ticket found by that ID."


class Controller:
    ticketManager: Tickets
    dbFetcher: APIFetcher

    def __init__(self):
        self.dbFetcher = APIFetcher()
        self.ticketManager = Tickets(self.dbFetcher.getTickets())

    def callCorrectMethod(self, selection: str):
        validSelections = ["1", "2", "update"]
        if selection not in validSelections:
            return "Please enter a valid selection."
        if selection == "1":
            return self.listAllTickets()
        elif selection == "2":
            return self.listByID()
        else:
            self.dbFetcher.getTickets()
            return "Tickets updated."

    def listAllTickets(self):
        tickets = self.ticketManager.getAllTickets()
        formattedTickets = []
        for ticket in tickets:
            formattedTickets.append(ticket.formattedTicket())
        return formattedTickets

    def listByID(self):
        userInput = input("Please enter the ID of the ticket you wish to see.")
        ticketRet = self.ticketManager.getTicketByID(int(userInput))
        if type(ticketRet) == str:
            return ticketRet
        return ticketRet.formattedTicket()


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
        self.programManager = Controller()

    def run(self):
        print("\n")
        print(self.initialMessage)
        while True:
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


if __name__ == "__main__":
    m = Main()
    m.run()
