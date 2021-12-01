import requests
from Ticket import Ticket


class APIFetcher:
    email: str
    password: str
    subdomain: str

    def __init__(self, email: str, password: str, subdomain: str):
        self.email = email
        self.password = password
        self.subdomain = subdomain + ".zendesk.com"

    def getTickets(self):
        try:
            link = "https://" + self.subdomain + "/api/v2/tickets.json"
            print("loading...")
            response = requests.get(link, auth=(self.email, self.password))
            if response.status_code != 200:
                fail_message = 'Status:' + str(response.status_code) + "\n" + \
                               'Problem with the request. Exiting...'
                print(fail_message)
                print("You may have entered incorrect credentials, please run "
                      "and try again!")
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
        except requests.exceptions.ConnectionError:
            print("You may have entered incorrect credentials, please run and "
                  "try again!")
            print("Exiting program...")
            exit()
