from typing import Annotated
from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.models import Game, Provider
from dto.search_schems import SearchResult
from backend.database import get_db
from services.cache import CacheService


app = FastAPI(title="Search Game or Provider")

# cache = CacheService()

@app.get("/search/", tags=["Search"])
async def search(
        query: Annotated[str | None, Query(min_length=2, max_length=100)] = None,
        db: AsyncSession = Depends(get_db)
) -> SearchResult:

    # if cache.get(query):
    #     return SearchResult(
    #         games=cache.hget('query', 'games'),
    #         providers=cache.hget('query', 'providers')
    #     )

    result = SearchResult()

    if query:
        # Поиск игр
        games_stmt = select(Game.id).where(Game.title.ilike(f"%{query}%"))
        games_result = await db.execute(games_stmt)
        result.games = [row[0] for row in games_result]

        # Поиск провайдеров
        providers_stmt = select(Provider.id).where(Provider.name.ilike(f"%{query}%"))
        providers_result = await db.execute(providers_stmt)
        result.providers = [row[0] for row in providers_result]

    # await cache.set(query, result)

    return result





