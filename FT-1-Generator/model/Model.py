class Model:
    def __init__(self):
        self.username = ""
        self.password = ""

    def verify_password(self):
        return self.username == "USER" and self.password == "PASS"