from APIFetcher import APIFetcher
from Tickets import Tickets


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
