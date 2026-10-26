from typing import Dict, List
from utilities.llm_utility import LLMUtility
from repositories.room_repository import KnowledgeBaseRepository
from dtos.api_response_dto import APIResponse
from constants.http_status import HttpStatusCode
from dtos.custom_app_exception import CustomAppException
from errors.error_codes import ErrorCode, ErrorCodeStatus
from constants.http_status import HttpStatusCode
import os
from utilities.bedrock import Boto3BedrockEmbedding
from config.config_manager import config
import json
class RoomService:

    def __init__(self):
        self.llm_utility = LLMUtility()
        self.kb_repository = KnowledgeBaseRepository()

    async def create_knowledgebase_service(self, content: str) -> Dict[str]:
        
        try:
            embed_model = Boto3BedrockEmbedding()
            
            chunks = await self.llm_utility.SemanticChunk(content,embed_model)

            
            embeddings = self.llm_utility.generate_embeddings(chunks, embed_model)

            
            await self.kb_repository.create_knowledgebase_repository(
                chunks=chunks,
                embeddings=embeddings
            )

            return {
                "message": "Knowledge base created successfully",
    
            }
        except CustomAppException:
            raise
        except Exception as e:
            raise CustomAppException(
                message=f"Service error in creating knowledge base details: {str(e)}",
                code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                error_code_id=ErrorCodeStatus[ErrorCode.INTERNAL_SERVER_ERROR]
            )

    

    async def generate_ai_response(
        self,
        query: str,
        context_chunks
    ) -> APIResponse:
        prompt =await self.llm_utility.build_prompt(
            query,
            context_chunks
        )
        llm_output = await self.llm_utility.invoke_llm(prompt)
        llm_result=json.loads(llm_output)
        
        return APIResponse(
            data={
                "query": query,
                "answer": llm_result,
                "context_used": context_chunks
            },
            errors=None,
            code=HttpStatusCode.OK
        )

    async def search_room_service(self, query: str) -> Dict[str,any]:
        try:
            embed_model=Boto3BedrockEmbedding()

            query_embedding =  self.llm_utility.generate_embeddings(query,embed_model)
            

            similar_chunks = await self.kb_repository.vector_search(
                query_embedding=query_embedding,
                top_k=config.top_k,
                similarity_threshold=0.0,
            )
            if not similar_chunks:
                return APIResponse(
                    data={"query": query, "answer": {"Answer": "I don't know."}, "context_used": []},
                    errors=None,
                    code=HttpStatusCode.OK,
                )
            context = [row[0] for row in similar_chunks if row and row[0]]
            result = await self.generate_ai_response(query=query, context_chunks=context)
            return result
            
        except CustomAppException:
            raise
        except Exception as e:
            raise CustomAppException(
                message=f"Search room Service error: {str(e)}",
                code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                error_code_id=ErrorCodeStatus[ErrorCode.INTERNAL_SERVER_ERROR]
            )