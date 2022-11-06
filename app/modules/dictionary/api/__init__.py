from fastapi import APIRouter

from .v1.dictionary import router as dictionary_router


router = APIRouter()

router.include_router(dictionary_router, prefix="/dictionary")