from sqlalchemy import Column, Integer, Text, DateTime, String,Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
import uuid


Base = declarative_base()


class RoomServiceDB(Base):
    __tablename__ = "room_service_db_3454"

    room_service_db_id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    uuid = Column(UUID(as_uuid=True),default=uuid.uuid4,unique=True,nullable=False,index=True)
    content = Column(Text,nullable=False)
    embedding_vector = Column(Vector(1024),nullable=False)
    is_active = Column(Boolean,nullable=False,default=True)
    created_by = Column(String(50),nullable=False,default="Admin")
    created_at = Column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at = Column(DateTime(timezone=True),nullable=True,onupdate=func.now())
    updated_by = Column(String(50),nullable=True)