from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated


class KnowledgeBaseDTO(BaseModel):
    content: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200_000)]


class RoomQueryDTO(BaseModel):
    query: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=4_000)]
