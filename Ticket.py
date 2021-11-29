import datetime


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


def formatDate(iso: str):
    return str(datetime.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ"))
