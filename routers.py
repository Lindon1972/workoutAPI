from fastapi import APIRouter
from workout_api.atleta.controller import router as atleta
from workout_api.categoria.controller import router as categoria
from workout_api.centro_treinamento.controller import router as centro_treinamento

api_router = APIRouter()
api_router.include_router(atleta, prefix='/atletas', tags=['Atletas'])
api_router.include_router(categoria, prefix='/categorias', tags=['Categorias'])
api_router.include_router(centro_treinamento, prefix='/CTs', tags=['Centros de Treinamento - CTs'])
