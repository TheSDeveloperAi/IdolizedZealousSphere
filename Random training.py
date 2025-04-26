class Customer:
    def __init__(self, name: str, code: int, block: bool):
        self.name = name
        self.code = code
        self.block = block
    def __str__(self):
        return f"Customer(name = "{self.name}", code = {self.code}, block = {self.code})"
