import secrets
import string

def generate_key(length):
    charaters = string.ascii_letters + string.digits + string.punctuation
    key = ''.join(secrets.choice(charaters) for i in range(length))
    return key

import hashlib
import hashlib
import secrets

def generate_random_hash(length=10):
    """
    Genera un hash SHA-256 basado en una clave aleatoria.

    :param length: Longitud deseada del hash (por defecto 10).
    :return: Hash truncado con la longitud especificada.
    """
    random_key = secrets.token_hex(16)  # Genera una clave aleatoria segura
    hash_object = hashlib.sha256(random_key.encode())  # Crea el hash
    hash_hex = hash_object.hexdigest()  # Convierte a hexadecimal
    return hash_hex[:length]  # Trunca a la longitud deseada



class Key():
    def __init__(self) -> None:
        self.key = generate_random_hash(30)
    
    def equal(self,key):
        return self.key == key.clave
    


class KeyName(Key):

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
