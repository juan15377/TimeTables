import secrets
import string

def generate_key(length):
    charaters = string.ascii_letters + string.digits + string.punctuation
    key = ''.join(secrets.choice(charaters) for i in range(length))
    return key


class Key():
    def __init__(self) -> None:
        self.key = generate_key(30)
    
    def equal(self,key):
        return self.key == key.clave
    


class KeyName(Key):

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
