class Singleton():
    
    _instances = {}
    
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self):
        pass

class MyClass(Singleton):
    
    def __init__(self, p1):
        self.p1 = p1

c1 = MyClass(1)
c2 = MyClass(2)

print(c1.p1)
print(c2.p1)

# Output:
# Creating instance (inside __new__)
# Initializing instance (inside __init__)
