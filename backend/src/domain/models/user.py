class User:

    def __init__(self, uid, email, name, role="student"):
        self.uid = uid
        self.email = email
        self.name = name
        self.role = role

    def to_dict(self):
        return {
            "uid": self.uid,
            "email": self.email,
            "name": self.name,
            "role": self.role
        }
