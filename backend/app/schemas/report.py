from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

from app.models.finance_operation import FinanceCategory, FinanceOperationType
from app.models.horse import HorseGender, HorseStatus


class ReportGeneratedByRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    role: str


class ReportFilterHorseOptionRead(BaseModel):
    id: int
    name: str


class ReportFilterUserOptionRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    full_name: str
    role: str
    is_active: bool


class ReportFilterOptionsRead(BaseModel):
    horses: list[ReportFilterHorseOptionRead]
    users: list[ReportFilterUserOptionRead]


class RelatedMedicalRecordRead(BaseModel):
    id: int
    record_date: datetime
    record_type: str
    title: str
    description: str


class RelatedProcedureRead(BaseModel):
    id: int
    procedure_name: str
    status: str
    planned_date: datetime
    completed_date: datetime | None
    notes: str | None
    add_to_medical_record: bool


class RelatedTaskRead(BaseModel):
    id: int
    title: str
    description: str
    status: str
    due_date: datetime
    completed_at: datetime | None
    executor_name: str | None


class ReportHorseBaseRead(BaseModel):
    id: int
    name: str
    gender: HorseGender
    age: int | None
    breed: str | None
    color: str | None
    status: HorseStatus
    curator_id: int | None
    curator_name: str | None
    arrival_date: date
    description: str | None
    history: str | None


class AllHorsesFiltersRead(BaseModel):
    status: HorseStatus | None
    curator_id: int | None
    include_medical_records: bool
    include_procedures: bool
    include_tasks: bool


class AllHorsesSummaryRead(BaseModel):
    total_horses: int
    healthy_count: int
    sick_count: int
    rehabilitation_count: int
    deceased_count: int


class AllHorsesItemRead(BaseModel):
    horse: ReportHorseBaseRead
    medical_records: list[RelatedMedicalRecordRead]
    procedures: list[RelatedProcedureRead]
    tasks: list[RelatedTaskRead]


class AllHorsesReportRead(BaseModel):
    report_type: str
    report_title: str
    generated_at: datetime
    generated_by: ReportGeneratedByRead
    filters: AllHorsesFiltersRead
    summary: AllHorsesSummaryRead
    items: list[AllHorsesItemRead]


class HorseDetailFiltersRead(BaseModel):
    horse_id: int
    include_procedures: bool
    include_tasks: bool


class HorseDetailSummaryRead(BaseModel):
    medical_records_count: int
    procedures_count: int
    tasks_count: int


class HorseDetailItemRead(BaseModel):
    horse: ReportHorseBaseRead
    medical_records: list[RelatedMedicalRecordRead]
    procedures: list[RelatedProcedureRead]
    tasks: list[RelatedTaskRead]


class HorseDetailReportRead(BaseModel):
    report_type: str
    report_title: str
    generated_at: datetime
    generated_by: ReportGeneratedByRead
    filters: HorseDetailFiltersRead
    summary: HorseDetailSummaryRead
    item: HorseDetailItemRead


class MedicalProceduresFiltersRead(BaseModel):
    status: str
    horse_id: int | None
    date_from: date | None
    date_to: date | None
    exact_date: date | None


class MedicalProceduresSummaryRead(BaseModel):
    total_items: int
    planned_count: int
    completed_count: int
    overdue_count: int


class MedicalProcedureReportItemRead(BaseModel):
    id: int
    horse_id: int
    horse_name: str
    procedure_name: str
    procedure_date: datetime
    completed_date: datetime | None
    status: str
    notes: str | None
    add_to_medical_record: bool


class MedicalProceduresReportRead(BaseModel):
    report_type: str
    report_title: str
    generated_at: datetime
    generated_by: ReportGeneratedByRead
    filters: MedicalProceduresFiltersRead
    summary: MedicalProceduresSummaryRead
    items: list[MedicalProcedureReportItemRead]


class AllTasksFiltersRead(BaseModel):
    status: str
    horse_id: int | None
    date_from: date | None
    date_to: date | None
    exact_date: date | None


class AllTasksSummaryRead(BaseModel):
    total_items: int
    waiting_count: int
    in_progress_count: int
    completed_count: int
    overdue_count: int


class AllTasksReportItemRead(BaseModel):
    id: int
    title: str
    description: str
    horse_id: int | None
    horse_name: str | None
    executor_id: int | None
    executor_name: str | None
    due_date: datetime
    completed_at: datetime | None
    status: str


class AllTasksReportRead(BaseModel):
    report_type: str
    report_title: str
    generated_at: datetime
    generated_by: ReportGeneratedByRead
    filters: AllTasksFiltersRead
    summary: AllTasksSummaryRead
    items: list[AllTasksReportItemRead]


class UserTasksFiltersRead(BaseModel):
    user_id: int | None
    status: str


class UserTaskUserSummaryRead(BaseModel):
    user_id: int
    full_name: str
    total_tasks: int
    in_progress_count: int
    completed_count: int


class UserTasksSummaryRead(BaseModel):
    total_items: int
    users: list[UserTaskUserSummaryRead]


class UserTasksReportItemRead(BaseModel):
    id: int
    user_id: int | None
    user_name: str | None
    title: str
    horse_id: int | None
    horse_name: str | None
    status: str
    due_date: datetime
    completed_at: datetime | None


class UserTasksReportRead(BaseModel):
    report_type: str
    report_title: str
    generated_at: datetime
    generated_by: ReportGeneratedByRead
    filters: UserTasksFiltersRead
    summary: UserTasksSummaryRead
    items: list[UserTasksReportItemRead]


class FinanceFiltersRead(BaseModel):
    operation_type: FinanceOperationType | None
    category: FinanceCategory | None
    date_from: date | None
    date_to: date | None
    horse_id: int | None


class FinanceReportSummaryRead(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
    operations_count: int


class FinanceReportItemRead(BaseModel):
    id: int
    date: datetime
    operation_type: FinanceOperationType
    category: FinanceCategory
    amount: Decimal
    horse_id: int | None
    horse_name: str | None
    description: str


class FinanceReportRead(BaseModel):
    report_type: str
    report_title: str
    generated_at: datetime
    generated_by: ReportGeneratedByRead
    filters: FinanceFiltersRead
    summary: FinanceReportSummaryRead
    items: list[FinanceReportItemRead]


class ShelterSummaryFiltersRead(BaseModel):
    date_from: date | None
    date_to: date | None
    include_horses: bool
    include_medicine: bool
    include_tasks: bool
    include_finance: bool | None
    include_users: bool | None


class ShelterSummaryOverviewRead(BaseModel):
    total_horses: int
    sick_horses: int
    procedures_count: int
    active_tasks_count: int
    overdue_tasks_count: int
    income_total: Decimal | None
    expense_total: Decimal | None
    active_users_count: int | None


class ShelterSummaryHorsesSectionRead(BaseModel):
    total_items: int
    healthy_count: int
    sick_count: int
    rehabilitation_count: int
    deceased_count: int
    items: list[ReportHorseBaseRead]


class ShelterSummaryMedicineSectionRead(BaseModel):
    total_items: int
    planned_count: int
    completed_count: int
    overdue_count: int
    items: list[MedicalProcedureReportItemRead]


class ShelterSummaryTasksSectionRead(BaseModel):
    total_items: int
    waiting_count: int
    in_progress_count: int
    completed_count: int
    overdue_count: int
    items: list[AllTasksReportItemRead]


class ShelterSummaryFinanceSectionRead(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
    operations_count: int
    items: list[FinanceReportItemRead]


class ShelterSummaryUsersSectionItemRead(BaseModel):
    user_id: int
    full_name: str
    role: str
    is_active: bool
    curated_horses_count: int
    in_progress_tasks_count: int
    completed_tasks_count: int


class ShelterSummaryUsersSectionRead(BaseModel):
    total_items: int
    active_users_count: int
    items: list[ShelterSummaryUsersSectionItemRead]


class ShelterSummaryReportRead(BaseModel):
    report_type: str
    report_title: str
    generated_at: datetime
    generated_by: ReportGeneratedByRead
    filters: ShelterSummaryFiltersRead
    summary: ShelterSummaryOverviewRead
    horses_section: ShelterSummaryHorsesSectionRead | None
    medicine_section: ShelterSummaryMedicineSectionRead | None
    tasks_section: ShelterSummaryTasksSectionRead | None
    finance_section: ShelterSummaryFinanceSectionRead | None
    users_section: ShelterSummaryUsersSectionRead | None
