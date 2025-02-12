class GlobalState:
    _instance = None  # Atributo de clase para almacenar la instancia única

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_state"):
            self._state = dict()  # Aseguramos que solo se inicialice una vez 

    def register_state(self, state):
        self._state[state.get_key()] = state

    def get_state_by_key(self, key: str):
        return self._state.get(key)


global_state = GlobalState()

class State:
  def __init__(self, key: str, value=None):
    self._global_state = global_state
    self._key = key
    self._value = value
    self.register_with_global()
  
  def register_with_global(self):
    self._global_state.register_state(self)

  def get_key(self):
    return self._key

  def get_state(self):
    return self._value


# en global state lo que se puede hacer es 