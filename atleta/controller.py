from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi_pagination import Page, paginate
from pydantic import UUID4
from sqlalchemy import select
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaOutAll, AtletaUpdate
from workout_api.categoria.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post('/', summary='Criar atleta', status_code=status.HTTP_201_CREATED, response_model=AtletaOut)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)) -> AtletaOut:
    
    cpf = atleta_in.cpf

    nome_categoria = atleta_in.categoria.nome
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=nome_categoria))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Categoria {nome_categoria} não encontrada!')
    
    nome_centro_treinamento = atleta_in.centro_treinamento.nome
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=nome_centro_treinamento))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Centro de Treinamento {nome_centro_treinamento} não encontrado!')
    
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail=f'Já existe um Atleta com este CPF: {cpf}')

    return atleta_out


@router.get('/', summary='Consultar todos os atletas', status_code=status.HTTP_200_OK, response_model=list[AtletaOutAll])
async def get_all(db_session: DatabaseDependency) -> list[AtletaOutAll]:
    atletas: list[AtletaOutAll] = (await db_session.execute(select(AtletaModel))).scalars().all()
    return ([AtletaOutAll.model_validate(atleta) for atleta in atletas])


@router.get('/{id}', summary='Consultar atleta pelo ID', status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def query_by_id(id, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID não encontrado!')
    
    return atleta


@router.patch('/{id}', summary='Editar atleta pelo ID', status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def set(id:UUID4, db_session: DatabaseDependency, atleta_up:AtletaUpdate = Body(...)) -> AtletaOut:
    
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID não encontrado!')
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete('/{id}', summary='Excluir atleta pelo ID', status_code=status.HTTP_204_NO_CONTENT)
async def set(id:UUID4, db_session: DatabaseDependency) -> None:
    
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID não encontrado!')
    
    await db_session.delete(atleta)
    await db_session.commit()
    

@router.get('/cpf/{cpf}', summary='Consultar atleta pelo CPF', status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def query_by_cpf(cpf, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(cpf=cpf))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='CPF não encontrado!')
    
    return atleta


@router.get('/nome/{nome}', summary='Consultar atleta pelo NOME', status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def query_by_cpf(nome, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter(AtletaModel.nome.ilike(f'%{nome}%')))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nome não encontrado!')
    
    return atleta


