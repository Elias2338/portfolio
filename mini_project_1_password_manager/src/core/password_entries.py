
'''Class to Save a Password for a Service and a User'''
class Passwords():
    def __init__(self, service, username, password):
        self.service = service
        self.username = username
        self.password = password

    def toDict(self):
        return {"service": self.service, "username": self.username, "password": self.password}
    
    



