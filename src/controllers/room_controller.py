# controllers/booking_controller.py
from typing import Optional
from uuid import UUID
from datetime import datetime,time,date
from pydantic import ValidationError
from services.room_service import RoomService
from errors.error_codes import ErrorCode, ErrorCodeStatus
from constants.http_status import HttpStatusCode
from dtos.api_response_dto import APIResponse
from dtos.room_dto import KnowledgeBaseDTO ,RoomQueryDTO
from dtos.custom_app_exception import CustomAppException

class RoomController:

    def __init__(self):
        self.room_service = RoomService()

    
    #  Knowledge Base Controller

    async def create_knowledgebase_controller(self, content: str) -> APIResponse:
        

        try:

            # Step 1: Call service
            room_data=await self.room_service.create_knowledgebase_service(
                content=content
            )

            # Step 2: Return success response
            return APIResponse(
                data=room_data,
                code=HttpStatusCode.CREATED
            )

        except CustomAppException:
            raise
        except Exception as e:
            raise CustomAppException(
                message=f"Controller error in creating knowledge base details: {str(e)}",
                code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                error_code_id=ErrorCodeStatus[ErrorCode.INTERNAL_SERVER_ERROR]
            )



    async def search_room_controller(self, query) -> APIResponse:
        

        try:

            return await self.room_service.search_room_service(
                query=query
            )

        except CustomAppException:
            raise
        except Exception as e:
            raise CustomAppException(
                message=f"Search room controller error: {str(e)}",
                code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
                error_code_id=ErrorCodeStatus[ErrorCode.INTERNAL_SERVER_ERROR]
            )