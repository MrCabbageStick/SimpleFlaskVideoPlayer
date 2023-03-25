from dataclasses import dataclass

@dataclass
class Lol:
    xD: str
    xDD: str
    xDDD: str

    def hejka():
        print("hejka")


lol = Lol("Lol", "LooooL", "Looooool")

print(lol.__dict__)