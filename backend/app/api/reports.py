from datetime import date

from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.auth import get_current_user, require_admin
from app.db.session import get_db
from app.models.finance_operation import FinanceCategory, FinanceOperationType
from app.models.horse import HorseStatus
from app.models.user import User
from app.schemas.report import (
    AllHorsesReportRead,
    AllTasksReportRead,
    FinanceReportRead,
    HorseDetailReportRead,
    MedicalProceduresReportRead,
    ReportFilterOptionsRead,
    ShelterSummaryReportRead,
    UserTasksReportRead,
)
from app.services.reports import (
    get_all_horses_report,
    get_all_tasks_report,
    get_finance_report,
    get_horse_detail_report,
    get_medical_procedures_report,
    get_report_filter_options,
    get_role_code,
    get_shelter_summary_report,
    get_user_tasks_report,
)
from app.services.report_exports import export_report

router = APIRouter(prefix="/reports", tags=["Reports"])

EXPORT_FORMATS = {"pdf", "xlsx"}


def build_export_response(report, export_format: str) -> StreamingResponse:
    if export_format not in EXPORT_FORMATS:
        raise HTTPException(status_code=422, detail="Неподдерживаемый формат экспорта")

    file_content, media_type, filename = export_report(report, export_format)
    return StreamingResponse(
        BytesIO(file_content),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/options", response_model=ReportFilterOptionsRead)
def report_filter_options(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_report_filter_options(db)


@router.get("/all-horses", response_model=AllHorsesReportRead)
def all_horses_report(
    status: HorseStatus | None = Query(default=None),
    curator_id: int | None = Query(default=None),
    include_medical_records: bool = Query(default=False),
    include_procedures: bool = Query(default=False),
    include_tasks: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_horses_report(
        db=db,
        current_user=current_user,
        status=status,
        curator_id=curator_id,
        include_medical_records=include_medical_records,
        include_procedures=include_procedures,
        include_tasks=include_tasks,
    )


@router.get("/all-horses/export")
def export_all_horses_report(
    export_format: str = Query(..., alias="format"),
    status: HorseStatus | None = Query(default=None),
    curator_id: int | None = Query(default=None),
    include_medical_records: bool = Query(default=False),
    include_procedures: bool = Query(default=False),
    include_tasks: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = get_all_horses_report(
        db=db,
        current_user=current_user,
        status=status,
        curator_id=curator_id,
        include_medical_records=include_medical_records,
        include_procedures=include_procedures,
        include_tasks=include_tasks,
    )
    return build_export_response(report, export_format)


@router.get("/horse-detail", response_model=HorseDetailReportRead)
def horse_detail_report(
    horse_id: int = Query(...),
    include_procedures: bool = Query(default=False),
    include_tasks: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_horse_detail_report(
        db=db,
        current_user=current_user,
        horse_id=horse_id,
        include_procedures=include_procedures,
        include_tasks=include_tasks,
    )


@router.get("/horse-detail/export")
def export_horse_detail_report(
    export_format: str = Query(..., alias="format"),
    horse_id: int = Query(...),
    include_procedures: bool = Query(default=False),
    include_tasks: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = get_horse_detail_report(
        db=db,
        current_user=current_user,
        horse_id=horse_id,
        include_procedures=include_procedures,
        include_tasks=include_tasks,
    )
    return build_export_response(report, export_format)


@router.get("/medical-procedures", response_model=MedicalProceduresReportRead)
def medical_procedures_report(
    status: str = Query(default="all"),
    horse_id: int | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    exact_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_medical_procedures_report(
        db=db,
        current_user=current_user,
        status=status,
        horse_id=horse_id,
        date_from=date_from,
        date_to=date_to,
        exact_date=exact_date,
    )


@router.get("/medical-procedures/export")
def export_medical_procedures_report(
    export_format: str = Query(..., alias="format"),
    status: str = Query(default="all"),
    horse_id: int | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    exact_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = get_medical_procedures_report(
        db=db,
        current_user=current_user,
        status=status,
        horse_id=horse_id,
        date_from=date_from,
        date_to=date_to,
        exact_date=exact_date,
    )
    return build_export_response(report, export_format)


@router.get("/all-tasks", response_model=AllTasksReportRead)
def all_tasks_report(
    status: str = Query(default="all"),
    horse_id: int | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    exact_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_tasks_report(
        db=db,
        current_user=current_user,
        status=status,
        horse_id=horse_id,
        date_from=date_from,
        date_to=date_to,
        exact_date=exact_date,
    )


@router.get("/all-tasks/export")
def export_all_tasks_report(
    export_format: str = Query(..., alias="format"),
    status: str = Query(default="all"),
    horse_id: int | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    exact_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = get_all_tasks_report(
        db=db,
        current_user=current_user,
        status=status,
        horse_id=horse_id,
        date_from=date_from,
        date_to=date_to,
        exact_date=exact_date,
    )
    return build_export_response(report, export_format)


@router.get("/user-tasks", response_model=UserTasksReportRead)
def user_tasks_report(
    user_id: int | None = Query(default=None),
    status: str = Query(default="in_progress"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_tasks_report(
        db=db,
        current_user=current_user,
        user_id=user_id,
        status=status,
    )


@router.get("/user-tasks/export")
def export_user_tasks_report(
    export_format: str = Query(..., alias="format"),
    user_id: int | None = Query(default=None),
    status: str = Query(default="in_progress"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = get_user_tasks_report(
        db=db,
        current_user=current_user,
        user_id=user_id,
        status=status,
    )
    return build_export_response(report, export_format)


@router.get("/finance", response_model=FinanceReportRead)
def finance_report(
    operation_type: FinanceOperationType | None = Query(default=None),
    category: FinanceCategory | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    horse_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_finance_report(
        db=db,
        current_user=current_user,
        operation_type=operation_type,
        category=category,
        date_from=date_from,
        date_to=date_to,
        horse_id=horse_id,
    )


@router.get("/finance/export")
def export_finance_report(
    export_format: str = Query(..., alias="format"),
    operation_type: FinanceOperationType | None = Query(default=None),
    category: FinanceCategory | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    horse_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    report = get_finance_report(
        db=db,
        current_user=current_user,
        operation_type=operation_type,
        category=category,
        date_from=date_from,
        date_to=date_to,
        horse_id=horse_id,
    )
    return build_export_response(report, export_format)


@router.get("/shelter-summary", response_model=ShelterSummaryReportRead)
def shelter_summary_report(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    include_horses: bool = Query(default=True),
    include_medicine: bool = Query(default=True),
    include_tasks: bool = Query(default=True),
    include_finance: bool = Query(default=False),
    include_users: bool = Query(default=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_shelter_summary_report(
        db=db,
        current_user=current_user,
        date_from=date_from,
        date_to=date_to,
        include_horses=include_horses,
        include_medicine=include_medicine,
        include_tasks=include_tasks,
        include_finance=include_finance,
        include_users=include_users,
    )


@router.get("/shelter-summary/export")
def export_shelter_summary_report(
    export_format: str = Query(..., alias="format"),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    include_horses: bool = Query(default=True),
    include_medicine: bool = Query(default=True),
    include_tasks: bool = Query(default=True),
    include_finance: bool = Query(default=False),
    include_users: bool = Query(default=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = get_shelter_summary_report(
        db=db,
        current_user=current_user,
        date_from=date_from,
        date_to=date_to,
        include_horses=include_horses,
        include_medicine=include_medicine,
        include_tasks=include_tasks,
        include_finance=include_finance,
        include_users=include_users,
    )
    return build_export_response(report, export_format)
