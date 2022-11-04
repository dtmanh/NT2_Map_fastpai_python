import json
from fastapi import Body, Depends, APIRouter, Path, Request
from pydantic import PositiveInt
from app.schemas.filter_schema import FilterSchema
from app.services.auth.auth_bearer import JWTBearer
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
from databases.db import Session, get_db
from app.services.system_log import system_log_service
router = APIRouter()
TAG = 'System Log'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

@router.get("/system-log/list", dependencies=[LOGIN], tags=[TAG])
async def get_system_log(request: Request, session: Session = DB, body: FilterSchema = Depends()):
    body.filter = json.loads(body.filter)
    system_logs = system_log_service.get_filter(session, body)

    if len(body.filter) != 0:
        description = "Tìm kiếm nhật kí sử dụng"
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.SEARCH,
            type=LOG_TYPE.LOG_MANAGER,
            description=description,
        ))
    return system_logs


@router.get("/system-log/{log_id}", dependencies=[LOGIN], tags=[TAG])
async def get_system_log(request: Request, session: Session = DB, log_id: PositiveInt = Path(title="The ID of system log to get")):
    system_log = system_log_service.get_detail(session, log_id)
    return system_log


@router.post("/system-log/export", dependencies=[LOGIN], tags=[TAG])
async def get_system_log(request: Request, session: Session = DB, body: FilterSchema = Body(...)):
    body.filter = json.loads(body.filter)
    description = "Xuất dữ liệu nhật kí hệ thống"

    system_log_service.system_log_create(session, request, OverideSystemLogSchema(
        action=LOG_ACTION.EXPORT,
        type=LOG_TYPE.LOG_MANAGER,
        description=description,
    ))
    return True


@router.get("/system-log/test-elasticsearch", dependencies=[LOGIN], tags=[TAG])
def test_elasticsearch():
    return system_log_service.test_elasticsearch()
