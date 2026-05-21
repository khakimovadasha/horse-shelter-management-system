export const REPORT_TYPES = {
  all_horses: 'all_horses',
  horse_detail: 'horse_detail',
  medical_procedures: 'medical_procedures',
  all_tasks: 'all_tasks',
  user_tasks: 'user_tasks',
  finance: 'finance',
  shelter_summary: 'shelter_summary',
}

export const HORSE_STATUS_OPTIONS = [
  { label: 'Все статусы', value: null },
  { label: 'Здоров', value: 'healthy' },
  { label: 'Болен', value: 'sick' },
  { label: 'Реабилитация', value: 'rehabilitation' },
  { label: 'Выбыл', value: 'deceased' },
]

export const PROCEDURE_STATUS_OPTIONS = [
  { label: 'Все статусы', value: 'all' },
  { label: 'Запланировано', value: 'planned' },
  { label: 'Выполнено', value: 'completed' },
  { label: 'Просрочено', value: 'overdue' },
]

export const TASK_STATUS_OPTIONS = [
  { label: 'Все статусы', value: 'all' },
  { label: 'Ожидает', value: 'waiting' },
  { label: 'В работе', value: 'in_progress' },
  { label: 'Выполнено', value: 'completed' },
  { label: 'Просрочено', value: 'overdue' },
]

export const USER_TASK_STATUS_OPTIONS = [
  { label: 'В работе', value: 'in_progress' },
  { label: 'Выполнено', value: 'completed' },
]

export const FINANCE_OPERATION_TYPE_OPTIONS = [
  { label: 'Все типы', value: null },
  { label: 'Доход', value: 'income' },
  { label: 'Расход', value: 'expense' },
]

export const FINANCE_CATEGORY_OPTIONS = [
  { label: 'Все категории', value: null },
  { label: 'Пожертвования', value: 'donations' },
  { label: 'Спонсорство', value: 'sponsorship' },
  { label: 'Гранты', value: 'grants' },
  { label: 'Продажи', value: 'sales' },
  { label: 'Прочие доходы', value: 'other_income' },
  { label: 'Медикаменты', value: 'medications' },
  { label: 'Корма', value: 'feed' },
  { label: 'Уход', value: 'care' },
  { label: 'Снаряжение', value: 'equipment' },
  { label: 'Транспорт', value: 'transport' },
  { label: 'Ремонт', value: 'repair' },
  { label: 'Коммунальные услуги', value: 'utilities' },
  { label: 'Прочие расходы', value: 'other_expense' },
]

export const REPORT_TYPE_DEFINITIONS = [
  {
    value: REPORT_TYPES.all_horses,
    label: 'Отчёт по всем лошадям',
    requiresAdmin: false,
    fields: ['status', 'curator_id', 'include_medical_records', 'include_procedures', 'include_tasks'],
    initialFilters: {
      status: null,
      curator_id: null,
      include_medical_records: false,
      include_procedures: false,
      include_tasks: false,
    },
  },
  {
    value: REPORT_TYPES.horse_detail,
    label: 'Отчёт по конкретной лошади',
    requiresAdmin: false,
    fields: ['horse_id', 'include_procedures', 'include_tasks'],
    initialFilters: {
      horse_id: null,
      include_procedures: true,
      include_tasks: true,
    },
  },
  {
    value: REPORT_TYPES.medical_procedures,
    label: 'Отчёт по медицинским процедурам',
    requiresAdmin: false,
    fields: ['procedure_status', 'horse_id_optional', 'date_from', 'date_to'],
    initialFilters: {
      status: 'all',
      horse_id: null,
      date_from: '',
      date_to: '',
    },
  },
  {
    value: REPORT_TYPES.all_tasks,
    label: 'Отчёт по всем задачам',
    requiresAdmin: false,
    fields: ['task_status', 'horse_id_optional', 'date_from', 'date_to'],
    initialFilters: {
      status: 'all',
      horse_id: null,
      date_from: '',
      date_to: '',
    },
  },
  {
    value: REPORT_TYPES.user_tasks,
    label: 'Отчёт по задачам пользователей',
    requiresAdmin: false,
    fields: ['user_id', 'user_task_status'],
    initialFilters: {
      user_id: null,
      status: 'in_progress',
    },
  },
  {
    value: REPORT_TYPES.finance,
    label: 'Финансовый отчёт',
    requiresAdmin: true,
    fields: ['operation_type', 'category', 'date_from', 'date_to', 'horse_id_optional'],
    initialFilters: {
      operation_type: null,
      category: null,
      date_from: '',
      date_to: '',
      horse_id: null,
    },
  },
  {
    value: REPORT_TYPES.shelter_summary,
    label: 'Сводный отчёт по приюту',
    requiresAdmin: false,
    fields: [
      'date_from',
      'date_to',
      'include_horses',
      'include_medicine',
      'include_tasks',
      'include_finance',
      'include_users',
    ],
    initialFilters: {
      date_from: '',
      date_to: '',
      include_horses: true,
      include_medicine: true,
      include_tasks: true,
      include_finance: false,
      include_users: true,
    },
  },
]

export const REPORT_TYPE_MAP = Object.fromEntries(
  REPORT_TYPE_DEFINITIONS.map((definition) => [definition.value, definition]),
)

export const createInitialFiltersByType = () => {
  return Object.fromEntries(
    REPORT_TYPE_DEFINITIONS.map((definition) => [
      definition.value,
      { ...definition.initialFilters },
    ]),
  )
}

export const getAvailableReportTypes = (isAdmin) => {
  return REPORT_TYPE_DEFINITIONS.filter((definition) => {
    return isAdmin || !definition.requiresAdmin
  }).map(({ value, label }) => ({ value, label }))
}

