from pydantic import BaseModel


class SearchResult(BaseModel):
    games: list[int] = []
    providers: list[int] = []