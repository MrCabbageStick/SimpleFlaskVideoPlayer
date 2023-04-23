from random import choices
import string

characters = [*string.ascii_lowercase, *string.ascii_uppercase, *string.digits]

def generateRandomId(k = 10):

    return "".join(choices(characters, k = k))


if __name__ == "__main__":
    print(generateRandomId())