from modules.fileFinder import findFilesByExtension

class ThumbnailsManager:

    dir_path: str
    extensions: list[str] = []
    thumbnails: dict[str, str] = {}

    def __init__(self, thumbnail_dir_path: str, extensions: list[str], placeholder_thumbnail_filename: str) -> None:
        
        self.dir_path = thumbnail_dir_path
        self.extensions = extensions
        self.placeholder = placeholder_thumbnail_filename

    
    def loadThumbnails(self):

        for file in findFilesByExtension(self.dir_path, *self.extensions):

            self.thumbnails[".".join(file.split(".")[:-1])] = file

    
    def getThumbnail(self, _id: str):

        return self.thumbnails.get(_id) or self.placeholder

