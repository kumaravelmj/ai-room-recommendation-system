# routers/router.py
from fastapi import APIRouter, Query, Body, Depends, Path, Request, Response
from fastapi.responses import JSONResponse
from uuid import UUID
from dtos.api_response_dto import APIResponse
from dtos.room_dto import RoomQueryDTO, KnowledgeBaseDTO
from controllers.room_controller import RoomController
from dtos.custom_app_exception import CustomAppException
from errors.error_codes import ErrorCode, ErrorCodeStatus
from constants.http_status import HttpStatusCode

router = APIRouter(prefix="/training/api")


def get_controller():
    return RoomController()




@router.post("/create-knowledgebase")
async def create_knowledgebase(
    request: KnowledgeBaseDTO = Body(...)
):
    try:
        controller = get_controller()

        result = await controller.create_knowledgebase_controller(
            content=request.content
        )

        return JSONResponse(
            content=result.to_dict(),
            status_code=result.code
        )

    except CustomAppException:
        raise

    except Exception as e:
        raise CustomAppException(
            message=f"Router error in create_knowledgebase: {str(e)}",
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
            error_code_id=ErrorCodeStatus[ErrorCode.INTERNAL_SERVER_ERROR]
        )
    


@router.post("/search-room")
async def search_room(
    request: RoomQueryDTO = Body(...)
):
    try:
        controller = get_controller()

        result= await controller.search_room_controller(
            query=request.query
        )

        return JSONResponse(
            content=result.to_dict(),
            status_code=result.code
        )

    except CustomAppException:
        raise

    except Exception as e:
        raise CustomAppException(
            message=f"Router error in search_room: {str(e)}",
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            status_code=HttpStatusCode.INTERNAL_SERVER_ERROR,
            error_code_id=ErrorCodeStatus[ErrorCode.INTERNAL_SERVER_ERROR]
        )
