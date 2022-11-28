from fastapi import APIRouter

from fastapi_solution.src.persons.api.router import router as persons_router
from fastapi_solution.src.genres.api.router import router as genres_router

router = APIRouter()

router.include_router(persons_router, prefix='/persons', tags=['persons'])
router.include_router(genres_router, prefix='/genres', tags=['genres'])
