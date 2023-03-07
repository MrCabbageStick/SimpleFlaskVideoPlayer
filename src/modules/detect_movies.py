from os import listdir

SUPPORTED_EXTENSIONS = [
    "mp4"
]

def scanForMovies(path: str):

    try:
        files = listdir(path)
    except:
        return []

    return [file for file in files if file.split(".")[-1] in SUPPORTED_EXTENSIONS]


if __name__ == "__main__":
    
    from sys import argv

    print(scanForMovies(argv[1]))