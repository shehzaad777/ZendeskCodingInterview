from typing import List
from Ticket import Ticket


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
