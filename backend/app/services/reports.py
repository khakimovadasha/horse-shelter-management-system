from collections import defaultdict
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.finance_operation import (
    FinanceCategory,
    FinanceOperation,
    FinanceOperationType,
)
from app.models.horse import Horse, HorseStatus
from app.models.medical_record import MedicalRecord
from app.models.procedure import Procedure, ProcedureStatus
from app.models.role import Role
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.finance_operation import validate_finance_category_matches_type
from app.schemas.finance_operation import EXPENSE_CATEGORIES
from app.schemas.report import (
    AllHorsesFiltersRead,
    AllHorsesItemRead,
    AllHorsesReportRead,
    AllHorsesSummaryRead,
    AllTasksFiltersRead,
    AllTasksReportItemRead,
    AllTasksReportRead,
    AllTasksSummaryRead,
    FinanceFiltersRead,
    FinanceReportItemRead,
    FinanceReportRead,
    FinanceReportSummaryRead,
    HorseDetailFiltersRead,
    HorseDetailItemRead,
    HorseDetailReportRead,
    HorseDetailSummaryRead,
    MedicalProcedureReportItemRead,
    MedicalProceduresFiltersRead,
    MedicalProceduresReportRead,
    MedicalProceduresSummaryRead,
    RelatedMedicalRecordRead,
    RelatedProcedureRead,
    RelatedTaskRead,
    ReportGeneratedByRead,
    ReportFilterHorseOptionRead,
    ReportFilterOptionsRead,
    ReportFilterUserOptionRead,
    ReportHorseBaseRead,
    ShelterSummaryFiltersRead,
    ShelterSummaryFinanceSectionRead,
    ShelterSummaryHorsesSectionRead,
    ShelterSummaryMedicineSectionRead,
    ShelterSummaryOverviewRead,
    ShelterSummaryReportRead,
    ShelterSummaryTasksSectionRead,
    ShelterSummaryUsersSectionItemRead,
    ShelterSummaryUsersSectionRead,
    UserTasksFiltersRead,
    UserTaskUserSummaryRead,
    UserTasksReportItemRead,
    UserTasksReportRead,
    UserTasksSummaryRead,
)

MEDICAL_PROCEDURE_REPORT_STATUSES = {"all", "planned", "completed", "overdue"}
ALL_TASKS_REPORT_STATUSES = {"all", "waiting", "in_progress", "completed", "overdue"}
USER_TASKS_REPORT_STATUSES = {"in_progress", "completed"}
MOSCOW_TZ = timezone(timedelta(hours=3))


def get_report_generated_at() -> datetime:
    return datetime.now(MOSCOW_TZ)


def validate_date_range(date_from: date, date_to: date) -> None:
    if date_from > date_to:
        raise HTTPException(
            status_code=422,
            detail="Дата начала не может быть больше даты окончания",
        )


def validate_date_filters(
    date_from: date | None,
    date_to: date | None,
    exact_date: date | None,
) -> None:
    if exact_date is not None and (date_from is not None or date_to is not None):
        raise HTTPException(
            status_code=422,
            detail="Нельзя одновременно передавать exact_date и диапазон дат",
        )

    if (date_from is None) ^ (date_to is None):
        raise HTTPException(
            status_code=422,
            detail="Для диапазона нужно передать и date_from, и date_to",
        )

    if date_from is not None and date_to is not None:
        validate_date_range(date_from, date_to)


def validate_status_filter(value: str, allowed_values: set[str], field_name: str) -> None:
    if value not in allowed_values:
        raise HTTPException(
            status_code=422,
            detail=f"Недопустимое значение фильтра {field_name}",
        )


def build_day_bounds(date_from: date, date_to: date) -> tuple[datetime, datetime]:
    return (
        datetime.combine(date_from, time.min),
        datetime.combine(date_to, time.max),
    )


def get_role_code(user: User, db: Session) -> str:
    role = db.execute(select(Role).where(Role.id == user.role_id)).scalar_one_or_none()
    return role.code if role is not None else "user"


def build_full_name(user: User | None) -> str | None:
    if user is None:
        return None
    return f"{user.first_name} {user.last_name}".strip()


def build_generated_by(user: User, db: Session) -> ReportGeneratedByRead:
    return ReportGeneratedByRead(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        role=get_role_code(user, db),
    )


def get_report_filter_options(db: Session) -> ReportFilterOptionsRead:
    horses = db.execute(
        select(Horse).order_by(Horse.name.asc(), Horse.id.asc())
    ).scalars().all()
    users = db.execute(
        select(User).order_by(User.last_name.asc(), User.first_name.asc(), User.id.asc())
    ).scalars().all()

    return ReportFilterOptionsRead(
        horses=[
            ReportFilterHorseOptionRead(
                id=horse.id,
                name=horse.name,
            )
            for horse in horses
        ],
        users=[
            ReportFilterUserOptionRead(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=build_full_name(user) or user.email,
                role=get_role_code(user, db),
                is_active=user.is_active,
            )
            for user in users
        ],
    )


def ensure_horse_exists(horse_id: int, db: Session) -> Horse:
    horse = db.execute(select(Horse).where(Horse.id == horse_id)).scalar_one_or_none()
    if horse is None:
        raise HTTPException(status_code=404, detail="Лошадь не найдена")
    return horse


def ensure_user_exists(user_id: int, db: Session) -> User:
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


def resolve_user_map(db: Session) -> dict[int, User]:
    users = db.execute(select(User)).scalars().all()
    return {user.id: user for user in users}


def resolve_horse_map(db: Session) -> dict[int, Horse]:
    horses = db.execute(select(Horse)).scalars().all()
    return {horse.id: horse for horse in horses}


def serialize_horse_base(horse: Horse, user_map: dict[int, User]) -> ReportHorseBaseRead:
    curator = user_map.get(horse.curator_id) if horse.curator_id is not None else None
    return ReportHorseBaseRead(
        id=horse.id,
        name=horse.name,
        gender=horse.gender,
        age=horse.age,
        breed=horse.breed,
        color=horse.color,
        status=horse.status,
        curator_id=horse.curator_id,
        curator_name=build_full_name(curator),
        arrival_date=horse.arrival_date,
        description=horse.description,
        history=horse.history,
    )


def get_procedure_report_status(procedure: Procedure) -> str:
    if procedure.status == ProcedureStatus.completed:
        return "completed"
    if procedure.planned_date < datetime.utcnow():
        return "overdue"
    return "planned"


def get_task_base_status(task: Task) -> str:
    if task.status == TaskStatus.completed:
        return "completed"
    if task.status == TaskStatus.in_progress:
        return "in_progress"
    return "waiting"


def is_task_overdue(task: Task) -> bool:
    return task.status != TaskStatus.completed and task.due_date < datetime.utcnow()


def matches_task_report_status(task: Task, status: str) -> bool:
    if status == "all":
        return True
    if status == "overdue":
        return is_task_overdue(task)
    return get_task_base_status(task) == status


def serialize_related_medical_record(record: MedicalRecord) -> RelatedMedicalRecordRead:
    return RelatedMedicalRecordRead(
        id=record.id,
        record_date=record.record_date,
        record_type=record.record_type.value,
        title=record.title,
        description=record.description,
    )


def serialize_related_procedure(procedure: Procedure) -> RelatedProcedureRead:
    return RelatedProcedureRead(
        id=procedure.id,
        procedure_name=procedure.procedure_name,
        status=get_procedure_report_status(procedure),
        planned_date=procedure.planned_date,
        completed_date=procedure.completed_date,
        notes=procedure.notes,
        add_to_medical_record=procedure.add_to_medical_record,
    )


def serialize_related_task(task: Task, user_map: dict[int, User]) -> RelatedTaskRead:
    task_status = get_task_base_status(task)
    executor_name = None
    if task.status in {TaskStatus.in_progress, TaskStatus.completed} and task.executor_id is not None:
        executor_name = build_full_name(user_map.get(task.executor_id))

    return RelatedTaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task_status,
        due_date=task.due_date,
        completed_at=task.completed_at,
        executor_name=executor_name,
    )


def serialize_medical_procedure_item(
    procedure: Procedure,
    horse_map: dict[int, Horse],
) -> MedicalProcedureReportItemRead:
    horse = horse_map[procedure.horse_id]
    procedure_date = (
        procedure.completed_date
        if procedure.status == ProcedureStatus.completed and procedure.completed_date is not None
        else procedure.planned_date
    )
    return MedicalProcedureReportItemRead(
        id=procedure.id,
        horse_id=procedure.horse_id,
        horse_name=horse.name,
        procedure_name=procedure.procedure_name,
        procedure_date=procedure_date,
        completed_date=procedure.completed_date,
        status=get_procedure_report_status(procedure),
        notes=procedure.notes,
        add_to_medical_record=procedure.add_to_medical_record,
    )


def serialize_all_tasks_item(task: Task, horse_map: dict[int, Horse], user_map: dict[int, User]) -> AllTasksReportItemRead:
    horse_name = horse_map[task.horse_id].name if task.horse_id is not None and task.horse_id in horse_map else None
    executor_name = None
    if task.status in {TaskStatus.in_progress, TaskStatus.completed} and task.executor_id is not None:
        executor_name = build_full_name(user_map.get(task.executor_id))

    return AllTasksReportItemRead(
        id=task.id,
        title=task.title,
        description=task.description,
        horse_id=task.horse_id,
        horse_name=horse_name,
        executor_id=task.executor_id,
        executor_name=executor_name,
        due_date=task.due_date,
        completed_at=task.completed_at,
        status=get_task_base_status(task),
    )


def serialize_user_tasks_item(task: Task, horse_map: dict[int, Horse], user_map: dict[int, User]) -> UserTasksReportItemRead:
    horse_name = horse_map[task.horse_id].name if task.horse_id is not None and task.horse_id in horse_map else None
    user_name = build_full_name(user_map.get(task.executor_id)) if task.executor_id is not None else None
    return UserTasksReportItemRead(
        id=task.id,
        user_id=task.executor_id,
        user_name=user_name,
        title=task.title,
        horse_id=task.horse_id,
        horse_name=horse_name,
        status=get_task_base_status(task),
        due_date=task.due_date,
        completed_at=task.completed_at,
    )


def serialize_finance_item(operation: FinanceOperation, horse_map: dict[int, Horse]) -> FinanceReportItemRead:
    horse_name = horse_map[operation.horse_id].name if operation.horse_id is not None and operation.horse_id in horse_map else None
    return FinanceReportItemRead(
        id=operation.id,
        date=operation.date,
        operation_type=operation.operation_type,
        category=operation.category,
        amount=operation.amount,
        horse_id=operation.horse_id,
        horse_name=horse_name,
        description=operation.description,
    )


def matches_datetime_filters(
    value: datetime | None,
    date_from: date | None,
    date_to: date | None,
    exact_date: date | None,
) -> bool:
    if value is None:
        return False

    if exact_date is not None:
        return value.date() == exact_date

    if date_from is not None and date_to is not None:
        start_datetime, end_datetime = build_day_bounds(date_from, date_to)
        return start_datetime <= value <= end_datetime

    return True


def get_all_horses_report(
    db: Session,
    current_user: User,
    status: HorseStatus | None,
    curator_id: int | None,
    include_medical_records: bool,
    include_procedures: bool,
    include_tasks: bool,
) -> AllHorsesReportRead:
    if curator_id is not None:
        ensure_user_exists(curator_id, db)

    query = select(Horse)
    if status is not None:
        query = query.where(Horse.status == status)
    if curator_id is not None:
        query = query.where(Horse.curator_id == curator_id)

    horses = db.execute(query.order_by(Horse.name.asc(), Horse.id.asc())).scalars().all()
    user_map = resolve_user_map(db)

    items: list[AllHorsesItemRead] = []
    for horse in horses:
        medical_records: list[RelatedMedicalRecordRead] = []
        procedures: list[RelatedProcedureRead] = []
        tasks: list[RelatedTaskRead] = []

        if include_medical_records:
            raw_records = db.execute(
                select(MedicalRecord)
                .where(MedicalRecord.horse_id == horse.id)
                .order_by(MedicalRecord.record_date.desc(), MedicalRecord.id.desc())
            ).scalars().all()
            medical_records = [serialize_related_medical_record(record) for record in raw_records]

        if include_procedures:
            raw_procedures = db.execute(
                select(Procedure)
                .where(Procedure.horse_id == horse.id)
                .order_by(Procedure.planned_date.desc(), Procedure.id.desc())
            ).scalars().all()
            procedures = [serialize_related_procedure(procedure) for procedure in raw_procedures]

        if include_tasks:
            raw_tasks = db.execute(
                select(Task)
                .where(Task.horse_id == horse.id)
                .order_by(Task.due_date.desc(), Task.id.desc())
            ).scalars().all()
            tasks = [serialize_related_task(task, user_map) for task in raw_tasks]

        items.append(
            AllHorsesItemRead(
                horse=serialize_horse_base(horse, user_map),
                medical_records=medical_records,
                procedures=procedures,
                tasks=tasks,
            )
        )

    summary = AllHorsesSummaryRead(
        total_horses=len(horses),
        healthy_count=sum(1 for horse in horses if horse.status == HorseStatus.healthy),
        sick_count=sum(1 for horse in horses if horse.status == HorseStatus.sick),
        rehabilitation_count=sum(1 for horse in horses if horse.status == HorseStatus.rehabilitation),
        deceased_count=sum(1 for horse in horses if horse.status == HorseStatus.deceased),
    )

    return AllHorsesReportRead(
        report_type="all_horses",
        report_title="Отчёт по всем лошадям",
        generated_at=get_report_generated_at(),
        generated_by=build_generated_by(current_user, db),
        filters=AllHorsesFiltersRead(
            status=status,
            curator_id=curator_id,
            include_medical_records=include_medical_records,
            include_procedures=include_procedures,
            include_tasks=include_tasks,
        ),
        summary=summary,
        items=items,
    )


def get_horse_detail_report(
    db: Session,
    current_user: User,
    horse_id: int,
    include_procedures: bool,
    include_tasks: bool,
) -> HorseDetailReportRead:
    horse = ensure_horse_exists(horse_id, db)
    user_map = resolve_user_map(db)

    medical_records = db.execute(
        select(MedicalRecord)
        .where(MedicalRecord.horse_id == horse.id)
        .order_by(MedicalRecord.record_date.desc(), MedicalRecord.id.desc())
    ).scalars().all()

    raw_procedures = []
    raw_tasks = []
    if include_procedures:
        raw_procedures = db.execute(
            select(Procedure)
            .where(Procedure.horse_id == horse.id)
            .order_by(Procedure.planned_date.desc(), Procedure.id.desc())
        ).scalars().all()

    if include_tasks:
        raw_tasks = db.execute(
            select(Task)
            .where(Task.horse_id == horse.id)
            .order_by(Task.due_date.desc(), Task.id.desc())
        ).scalars().all()

    item = HorseDetailItemRead(
        horse=serialize_horse_base(horse, user_map),
        medical_records=[serialize_related_medical_record(record) for record in medical_records],
        procedures=[serialize_related_procedure(procedure) for procedure in raw_procedures],
        tasks=[serialize_related_task(task, user_map) for task in raw_tasks],
    )

    return HorseDetailReportRead(
        report_type="horse_detail",
        report_title=f"Отчёт по лошади: {horse.name}",
        generated_at=get_report_generated_at(),
        generated_by=build_generated_by(current_user, db),
        filters=HorseDetailFiltersRead(
            horse_id=horse_id,
            include_procedures=include_procedures,
            include_tasks=include_tasks,
        ),
        summary=HorseDetailSummaryRead(
            medical_records_count=len(medical_records),
            procedures_count=len(raw_procedures),
            tasks_count=len(raw_tasks),
        ),
        item=item,
    )


def get_medical_procedures_report(
    db: Session,
    current_user: User,
    status: str,
    horse_id: int | None,
    date_from: date | None,
    date_to: date | None,
    exact_date: date | None,
) -> MedicalProceduresReportRead:
    validate_date_filters(date_from, date_to, exact_date)
    validate_status_filter(status, MEDICAL_PROCEDURE_REPORT_STATUSES, "status")
    if horse_id is not None:
        ensure_horse_exists(horse_id, db)

    procedures = db.execute(select(Procedure).order_by(Procedure.planned_date.desc(), Procedure.id.desc())).scalars().all()
    horse_map = resolve_horse_map(db)

    filtered: list[Procedure] = []
    for procedure in procedures:
        if horse_id is not None and procedure.horse_id != horse_id:
            continue

        report_status = get_procedure_report_status(procedure)
        if status != "all" and report_status != status:
            continue

        procedure_date = (
            procedure.completed_date
            if procedure.status == ProcedureStatus.completed and procedure.completed_date is not None
            else procedure.planned_date
        )
        if not matches_datetime_filters(procedure_date, date_from, date_to, exact_date):
            continue

        filtered.append(procedure)

    items = [serialize_medical_procedure_item(procedure, horse_map) for procedure in filtered]

    return MedicalProceduresReportRead(
        report_type="medical_procedures",
        report_title="Отчёт по медицинским процедурам",
        generated_at=get_report_generated_at(),
        generated_by=build_generated_by(current_user, db),
        filters=MedicalProceduresFiltersRead(
            status=status,
            horse_id=horse_id,
            date_from=date_from,
            date_to=date_to,
            exact_date=exact_date,
        ),
        summary=MedicalProceduresSummaryRead(
            total_items=len(filtered),
            planned_count=sum(1 for procedure in filtered if get_procedure_report_status(procedure) == "planned"),
            completed_count=sum(1 for procedure in filtered if get_procedure_report_status(procedure) == "completed"),
            overdue_count=sum(1 for procedure in filtered if get_procedure_report_status(procedure) == "overdue"),
        ),
        items=items,
    )


def get_all_tasks_report(
    db: Session,
    current_user: User,
    status: str,
    horse_id: int | None,
    date_from: date | None,
    date_to: date | None,
    exact_date: date | None,
) -> AllTasksReportRead:
    validate_date_filters(date_from, date_to, exact_date)
    validate_status_filter(status, ALL_TASKS_REPORT_STATUSES, "status")
    if horse_id is not None:
        ensure_horse_exists(horse_id, db)

    tasks = db.execute(select(Task).order_by(Task.due_date.desc(), Task.id.desc())).scalars().all()
    horse_map = resolve_horse_map(db)
    user_map = resolve_user_map(db)

    filtered: list[Task] = []
    for task in tasks:
        if horse_id is not None and task.horse_id != horse_id:
            continue

        if not matches_task_report_status(task, status):
            continue

        if not matches_datetime_filters(task.due_date, date_from, date_to, exact_date):
            continue

        filtered.append(task)

    items = [serialize_all_tasks_item(task, horse_map, user_map) for task in filtered]

    return AllTasksReportRead(
        report_type="all_tasks",
        report_title="Отчёт по всем задачам",
        generated_at=get_report_generated_at(),
        generated_by=build_generated_by(current_user, db),
        filters=AllTasksFiltersRead(
            status=status,
            horse_id=horse_id,
            date_from=date_from,
            date_to=date_to,
            exact_date=exact_date,
        ),
        summary=AllTasksSummaryRead(
            total_items=len(filtered),
            waiting_count=sum(1 for task in filtered if get_task_base_status(task) == "waiting"),
            in_progress_count=sum(1 for task in filtered if get_task_base_status(task) == "in_progress"),
            completed_count=sum(1 for task in filtered if get_task_base_status(task) == "completed"),
            overdue_count=sum(1 for task in filtered if is_task_overdue(task)),
        ),
        items=items,
    )


def get_user_tasks_report(
    db: Session,
    current_user: User,
    user_id: int | None,
    status: str,
) -> UserTasksReportRead:
    validate_status_filter(status, USER_TASKS_REPORT_STATUSES, "status")
    if user_id is not None:
        ensure_user_exists(user_id, db)

    tasks = db.execute(
        select(Task)
        .where(Task.executor_id.is_not(None))
        .order_by(Task.due_date.desc(), Task.id.desc())
    ).scalars().all()

    user_map = resolve_user_map(db)
    horse_map = resolve_horse_map(db)

    summary_source: list[Task] = []
    filtered: list[Task] = []
    for task in tasks:
        if user_id is not None and task.executor_id != user_id:
            continue
        if get_task_base_status(task) not in USER_TASKS_REPORT_STATUSES:
            continue

        summary_source.append(task)
        if get_task_base_status(task) == status:
            filtered.append(task)

    grouped_summary: dict[int, list[Task]] = defaultdict(list)
    for task in summary_source:
        if task.executor_id is not None:
            grouped_summary[task.executor_id].append(task)

    summary_items = [
        UserTaskUserSummaryRead(
            user_id=current_executor_id,
            full_name=build_full_name(user_map[current_executor_id]) or "",
            total_tasks=len(current_tasks),
            in_progress_count=sum(1 for task in current_tasks if get_task_base_status(task) == "in_progress"),
            completed_count=sum(1 for task in current_tasks if get_task_base_status(task) == "completed"),
        )
        for current_executor_id, current_tasks in sorted(
            grouped_summary.items(),
            key=lambda item: build_full_name(user_map[item[0]]) or "",
        )
    ]

    items = [serialize_user_tasks_item(task, horse_map, user_map) for task in filtered]

    return UserTasksReportRead(
        report_type="user_tasks",
        report_title="Отчёт по задачам пользователей",
        generated_at=get_report_generated_at(),
        generated_by=build_generated_by(current_user, db),
        filters=UserTasksFiltersRead(user_id=user_id, status=status),
        summary=UserTasksSummaryRead(
            total_items=len(filtered),
            users=summary_items,
        ),
        items=items,
    )


def get_finance_report(
    db: Session,
    current_user: User,
    operation_type: FinanceOperationType | None,
    category: FinanceCategory | None,
    date_from: date | None,
    date_to: date | None,
    horse_id: int | None,
) -> FinanceReportRead:
    validate_date_filters(date_from, date_to, None)
    if horse_id is not None:
        ensure_horse_exists(horse_id, db)
    if operation_type is not None and category is not None:
        try:
            validate_finance_category_matches_type(operation_type, category)
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    query = select(FinanceOperation)
    if date_from is not None and date_to is not None:
        start_datetime, end_datetime = build_day_bounds(date_from, date_to)
        query = query.where(
            FinanceOperation.date >= start_datetime,
            FinanceOperation.date <= end_datetime,
        )
    if operation_type is not None:
        query = query.where(FinanceOperation.operation_type == operation_type)
    if category is not None:
        query = query.where(FinanceOperation.category == category)
    if horse_id is not None:
        query = query.where(FinanceOperation.horse_id == horse_id)

    operations = db.execute(
        query.order_by(FinanceOperation.date.desc(), FinanceOperation.id.desc())
    ).scalars().all()
    horse_map = resolve_horse_map(db)

    total_income = sum(
        (operation.amount for operation in operations if operation.operation_type == FinanceOperationType.income),
        start=Decimal("0.00"),
    )
    total_expense = sum(
        (operation.amount for operation in operations if operation.operation_type == FinanceOperationType.expense),
        start=Decimal("0.00"),
    )

    return FinanceReportRead(
        report_type="finance",
        report_title="Финансовый отчёт",
        generated_at=get_report_generated_at(),
        generated_by=build_generated_by(current_user, db),
        filters=FinanceFiltersRead(
            operation_type=operation_type,
            category=category,
            date_from=date_from,
            date_to=date_to,
            horse_id=horse_id,
        ),
        summary=FinanceReportSummaryRead(
            total_income=total_income,
            total_expense=total_expense,
            balance=total_income - total_expense,
            operations_count=len(operations),
        ),
        items=[serialize_finance_item(operation, horse_map) for operation in operations],
    )


def get_shelter_summary_report(
    db: Session,
    current_user: User,
    date_from: date | None,
    date_to: date | None,
    include_horses: bool,
    include_medicine: bool,
    include_tasks: bool,
    include_finance: bool,
    include_users: bool,
) -> ShelterSummaryReportRead:
    validate_date_filters(date_from, date_to, None)
    is_admin_user = get_role_code(current_user, db) == "admin"
    if not is_admin_user:
        include_finance = False
        include_users = False

    has_period = date_from is not None and date_to is not None
    start_datetime = end_datetime = None
    if has_period:
        start_datetime, end_datetime = build_day_bounds(date_from, date_to)

    horses = db.execute(select(Horse).order_by(Horse.name.asc(), Horse.id.asc())).scalars().all()
    procedures_query = select(Procedure).order_by(Procedure.planned_date.desc(), Procedure.id.desc())
    tasks_query = select(Task).order_by(Task.due_date.desc(), Task.id.desc())
    finance_query = select(FinanceOperation).order_by(FinanceOperation.date.desc(), FinanceOperation.id.desc())

    if has_period:
        procedures_query = procedures_query.where(
            Procedure.planned_date >= start_datetime,
            Procedure.planned_date <= end_datetime,
        )
        tasks_query = tasks_query.where(
            Task.due_date >= start_datetime,
            Task.due_date <= end_datetime,
        )
        finance_query = finance_query.where(
            FinanceOperation.date >= start_datetime,
            FinanceOperation.date <= end_datetime,
        )

    procedures = db.execute(procedures_query).scalars().all()
    tasks = db.execute(tasks_query).scalars().all()
    finance_operations = db.execute(finance_query).scalars().all()
    users = db.execute(select(User).order_by(User.last_name.asc(), User.first_name.asc())).scalars().all()

    user_map = {user.id: user for user in users}
    horse_map = {horse.id: horse for horse in horses}

    total_income = sum(
        (operation.amount for operation in finance_operations if operation.operation_type == FinanceOperationType.income),
        start=Decimal("0.00"),
    )
    total_expense = sum(
        (operation.amount for operation in finance_operations if operation.operation_type == FinanceOperationType.expense),
        start=Decimal("0.00"),
    )

    horses_section = None
    if include_horses:
        horses_section = ShelterSummaryHorsesSectionRead(
            total_items=len(horses),
            healthy_count=sum(1 for horse in horses if horse.status == HorseStatus.healthy),
            sick_count=sum(1 for horse in horses if horse.status == HorseStatus.sick),
            rehabilitation_count=sum(1 for horse in horses if horse.status == HorseStatus.rehabilitation),
            deceased_count=sum(1 for horse in horses if horse.status == HorseStatus.deceased),
            items=[serialize_horse_base(horse, user_map) for horse in horses],
        )

    medicine_section = None
    if include_medicine:
        medicine_section = ShelterSummaryMedicineSectionRead(
            total_items=len(procedures),
            planned_count=sum(1 for procedure in procedures if get_procedure_report_status(procedure) == "planned"),
            completed_count=sum(1 for procedure in procedures if get_procedure_report_status(procedure) == "completed"),
            overdue_count=sum(1 for procedure in procedures if get_procedure_report_status(procedure) == "overdue"),
            items=[serialize_medical_procedure_item(procedure, horse_map) for procedure in procedures],
        )

    tasks_section = None
    if include_tasks:
        tasks_section = ShelterSummaryTasksSectionRead(
            total_items=len(tasks),
            waiting_count=sum(1 for task in tasks if get_task_base_status(task) == "waiting"),
            in_progress_count=sum(1 for task in tasks if get_task_base_status(task) == "in_progress"),
            completed_count=sum(1 for task in tasks if get_task_base_status(task) == "completed"),
            overdue_count=sum(1 for task in tasks if is_task_overdue(task)),
            items=[serialize_all_tasks_item(task, horse_map, user_map) for task in tasks],
        )

    finance_section = None
    if include_finance:
        finance_section = ShelterSummaryFinanceSectionRead(
            total_income=total_income,
            total_expense=total_expense,
            balance=total_income - total_expense,
            operations_count=len(finance_operations),
            items=[serialize_finance_item(operation, horse_map) for operation in finance_operations],
        )

    users_section = None
    if include_users:
        curated_counts = defaultdict(int)
        for horse in horses:
            if horse.curator_id is not None:
                curated_counts[horse.curator_id] += 1

        in_progress_counts = defaultdict(int)
        completed_counts = defaultdict(int)
        for task in tasks:
            if task.executor_id is None:
                continue
            task_status = get_task_base_status(task)
            if task_status == "in_progress":
                in_progress_counts[task.executor_id] += 1
            if task_status == "completed":
                completed_counts[task.executor_id] += 1

        users_section = ShelterSummaryUsersSectionRead(
            total_items=len(users),
            active_users_count=sum(1 for user in users if user.is_active),
            items=[
                ShelterSummaryUsersSectionItemRead(
                    user_id=user.id,
                    full_name=build_full_name(user) or "",
                    role=get_role_code(user, db),
                    is_active=user.is_active,
                    curated_horses_count=curated_counts[user.id],
                    in_progress_tasks_count=in_progress_counts[user.id],
                    completed_tasks_count=completed_counts[user.id],
                )
                for user in users
            ],
        )

    return ShelterSummaryReportRead(
        report_type="shelter_summary",
        report_title="Сводный отчёт по приюту",
        generated_at=get_report_generated_at(),
        generated_by=build_generated_by(current_user, db),
        filters=ShelterSummaryFiltersRead(
            date_from=date_from,
            date_to=date_to,
            include_horses=include_horses,
            include_medicine=include_medicine,
            include_tasks=include_tasks,
            include_finance=include_finance if is_admin_user else None,
            include_users=include_users if is_admin_user else None,
        ),
        summary=ShelterSummaryOverviewRead(
            total_horses=len(horses),
            sick_horses=sum(1 for horse in horses if horse.status == HorseStatus.sick),
            procedures_count=len(procedures),
            active_tasks_count=sum(1 for task in tasks if get_task_base_status(task) in {"waiting", "in_progress"}),
            overdue_tasks_count=sum(1 for task in tasks if is_task_overdue(task)),
            income_total=total_income if is_admin_user else None,
            expense_total=total_expense if is_admin_user else None,
            active_users_count=sum(1 for user in users if user.is_active) if is_admin_user else None,
        ),
        horses_section=horses_section,
        medicine_section=medicine_section,
        tasks_section=tasks_section,
        finance_section=finance_section,
        users_section=users_section,
    )
