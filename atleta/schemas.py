from typing import Annotated, Optional
from pydantic import UUID4, Field, PositiveFloat
from workout_api.categoria.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta, CentroTreinamentoIn
from workout_api.contrib.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='Jonas', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=28)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=68.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.66)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do Atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de Treinamento do Atleta')]


class AtletaIn(Atleta):
    pass


class AtletaOut(AtletaIn, OutMixin):
    id: Annotated[UUID4, Field(description='Identificador do Atleta')]


class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta')]


class AtletaOutAll(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='Jonas', max_length=50)]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de Treinamento do Atleta')]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do Atleta')]