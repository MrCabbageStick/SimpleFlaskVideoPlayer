from dataclasses import dataclass


@dataclass
class Movie:
    _id: str
    filename: str
    title: str
    series_id: str
    episode: int

@dataclass
class Series:
    _id: str
    title: str

@dataclass
class User:
    _id: str
    login: str
    name: str
    permission_level: int
    password: str