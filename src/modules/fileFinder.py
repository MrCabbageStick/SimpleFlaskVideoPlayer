import os

def findFilesByExtension(path: str, *extensions: str) -> list[str]:

    return [file for file in os.listdir(path) if file.split('.')[-1] in extensions]