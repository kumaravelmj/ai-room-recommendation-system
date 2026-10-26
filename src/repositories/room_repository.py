from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pgvector.sqlalchemy import Vector
from datetime import datetime
from dtos.custom_app_exception import CustomAppException
from database.database import Database
from models.room_model import RoomServiceDB
from errors.error_codes import ErrorCode, ErrorCodeStatus
from constants.http_status import HttpStatusCode
from llama_index.core.node_parser import *
from sqlalchemy import text
class KnowledgeBaseRepository:

    def __init__(self):
        self.db_instance = Database()

   
    
    async def create_knowledgebase_repository(
        self,
        chunks: List[str],
        embeddings: List[List[float]],
    ) -> None:

        db: Session = self.db_instance.SessionLocal()

        try:
            kb_objects = []

            for index, (content, embedding) in enumerate(zip(chunks, embeddings)):
                if hasattr(content,"get_content"):
                    content_text=content.get_content()
                else:
                    content_text=content
                kb_objects.append(
                    RoomServiceDB(
                        content=content_text,
                        embedding_vector=embedding,
                        created_at=datetime.utcnow()
                    )
                )

            db.add_all(kb_objects)
            db.commit()

        except SQLAlchemyError as e:
            db.rollback()
            raise e
        except Exception as e:
            raise CustomAppException(
                message=f"Database error in knowledge base repository: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                error_code_id=ErrorCodeStatus[ErrorCode.DATABASE_ERROR]
            )

        finally:
            db.close()

   
  
    async def vector_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        similarity_threshold: float = 0.7,
    ) -> List[str]:

        db_session = self.db_instance.SessionLocal()

        try:
            if not query_embedding:
                return []

            sql = text("""
                SELECT content,
                       1 - (embedding_vector <=> CAST(:embedding AS vector)) AS cosine_similarity
                FROM room_service_db_3454
                WHERE is_active = TRUE
                  AND 1 - (embedding_vector <=> CAST(:embedding AS vector)) >= :threshold
                ORDER BY embedding_vector <=> CAST(:embedding AS vector) ASC
                LIMIT :top_k
            """)
            results = db_session.execute(
                sql,
                {
                    "embedding": str(query_embedding),
                    "threshold": similarity_threshold,
                    "top_k": max(1, min(int(top_k), 20)),
                },
            ).fetchall()
            return results

        except SQLAlchemyError as e:
            raise e

        finally:
            db_session.close()