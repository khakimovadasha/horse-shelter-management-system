<template>
  <AppDataPanel
    v-if="report"
    :title="report.report_title"
    :subtitle="previewSubtitle"
  >
    <div :class="$style.layout">
      <section :class="$style.metaSection">
        <div :class="$style.metaGrid">
          <ReportMetaCard
            title="Параметры отчёта"
            :entries="reportMetaEntries"
          />

          <ReportMetaCard
            title="Фильтры"
            :entries="formattedFilters"
          />

          <ReportMetaCard
            title="Краткая сводка"
            :entries="formattedSummary"
          />
        </div>
      </section>

      <section v-if="report.report_type === 'all_horses'" :class="$style.section">
        <div :class="$style.cards">
          <article
            v-for="item in report.items"
            :key="item.horse.id"
            :class="$style.horseCard"
          >
            <div :class="$style.cardHeader">
              <div>
                <h3 :class="$style.cardTitle">{{ item.horse.name }}</h3>
                <p :class="$style.cardSubtitle">
                  {{ item.horse.breed || 'Порода не указана' }}
                </p>
              </div>

              <AppStatusBadge
                :label="labelHorseStatus(item.horse.status)"
                :tone="item.horse.status"
              />
            </div>

            <div :class="$style.horseInfoGrid">
              <div :class="$style.infoItem">
                <span>Пол</span>
                <strong>{{ labelHorseGender(item.horse.gender) }}</strong>
              </div>
              <div :class="$style.infoItem">
                <span>Возраст</span>
                <strong>{{ item.horse.age ? `${item.horse.age} лет` : '—' }}</strong>
              </div>
              <div :class="$style.infoItem">
                <span>Куратор</span>
                <strong>{{ item.horse.curator_name || '—' }}</strong>
              </div>
              <div :class="$style.infoItem">
                <span>Дата поступления</span>
                <strong>{{ formatDate(item.horse.arrival_date) }}</strong>
              </div>
            </div>

            <div v-if="item.horse.description" :class="$style.textBlock">
              {{ item.horse.description }}
            </div>

            <div v-if="item.medical_records.length" :class="$style.nestedSection">
              <div :class="$style.nestedTitle">Медзаписи</div>
              <ul :class="$style.nestedList">
                <li v-for="record in item.medical_records" :key="record.id">
                  {{ formatDate(record.record_date) }} — {{ record.title }}
                </li>
              </ul>
            </div>

            <div v-if="item.procedures.length" :class="$style.nestedSection">
              <div :class="$style.nestedTitle">Процедуры</div>
              <ul :class="$style.nestedList">
                <li v-for="procedure in item.procedures" :key="procedure.id">
                  {{ formatDate(procedure.planned_date) }} — {{ procedure.procedure_name }}
                </li>
              </ul>
            </div>

            <div v-if="item.tasks.length" :class="$style.nestedSection">
              <div :class="$style.nestedTitle">Задачи</div>
              <ul :class="$style.nestedList">
                <li v-for="task in item.tasks" :key="task.id">
                  {{ task.title }} — {{ labelTaskStatus(task.status) }}
                </li>
              </ul>
            </div>
          </article>
        </div>
      </section>

      <section v-else-if="report.report_type === 'horse_detail'" :class="$style.section">
        <div :class="$style.detailCard">
          <div :class="$style.cardHeader">
            <div>
              <h3 :class="$style.cardTitle">{{ report.item.horse.name }}</h3>
              <p :class="$style.cardSubtitle">
                {{ report.item.horse.breed || 'Порода не указана' }}
              </p>
            </div>

            <AppStatusBadge
              :label="labelHorseStatus(report.item.horse.status)"
              :tone="report.item.horse.status"
            />
          </div>

          <div :class="$style.horseInfoGrid">
            <div :class="$style.infoItem">
              <span>Пол</span>
              <strong>{{ labelHorseGender(report.item.horse.gender) }}</strong>
            </div>
            <div :class="$style.infoItem">
              <span>Возраст</span>
              <strong>{{ report.item.horse.age ? `${report.item.horse.age} лет` : '—' }}</strong>
            </div>
            <div :class="$style.infoItem">
              <span>Куратор</span>
              <strong>{{ report.item.horse.curator_name || '—' }}</strong>
            </div>
            <div :class="$style.infoItem">
              <span>Дата поступления</span>
              <strong>{{ formatDate(report.item.horse.arrival_date) }}</strong>
            </div>
          </div>

          <div v-if="report.item.horse.description" :class="$style.textBlock">
            {{ report.item.horse.description }}
          </div>

          <div :class="$style.detailSections">
            <div :class="$style.nestedSection">
              <div :class="$style.nestedTitle">История медицинской карты</div>

              <AppDataTable
                v-if="!isMobile"
                :columns="medicalRecordColumns"
                :rows="report.item.medical_records"
                row-key="id"
              >
                <template #cell-record_date="{ row }">
                  {{ formatDateTime(row.record_date) }}
                </template>
                <template #cell-record_type="{ row }">
                  {{ labelMedicalRecordType(row.record_type) }}
                </template>
              </AppDataTable>

              <div v-else :class="$style.mobileList">
                <ReportMedicalRecordMobileItem
                  v-for="record in report.item.medical_records"
                  :key="record.id"
                  :record="record"
                  :type-label="labelMedicalRecordType(record.record_type)"
                  :format-date-time="formatDateTime"
                />
              </div>
            </div>

            <div v-if="report.item.procedures.length" :class="$style.nestedSection">
              <div :class="$style.nestedTitle">Процедуры</div>

              <AppDataTable
                v-if="!isMobile"
                :columns="relatedProcedureColumns"
                :rows="report.item.procedures"
                row-key="id"
              >
                <template #cell-status="{ row }">
                  <AppStatusBadge
                    :label="labelProcedureStatus(row.status)"
                    :tone="row.status"
                  />
                </template>
                <template #cell-planned_date="{ row }">
                  {{ formatDateTime(row.planned_date) }}
                </template>
              </AppDataTable>

              <div v-else :class="$style.mobileList">
                <ReportProcedureMobileItem
                  v-for="procedure in report.item.procedures"
                  :key="procedure.id"
                  :procedure="procedure"
                  :status-label="labelProcedureStatus(procedure.status)"
                  :format-date-time="formatDateTime"
                />
              </div>
            </div>

            <div v-if="report.item.tasks.length" :class="$style.nestedSection">
              <div :class="$style.nestedTitle">Задачи</div>

              <AppDataTable
                v-if="!isMobile"
                :columns="relatedTaskColumns"
                :rows="report.item.tasks"
                row-key="id"
              >
                <template #cell-status="{ row }">
                  <AppStatusBadge
                    :label="labelTaskStatus(row.status)"
                    :tone="normalizeTaskTone(row.status)"
                  />
                </template>
                <template #cell-due_date="{ row }">
                  {{ formatDateTime(row.due_date) }}
                </template>
              </AppDataTable>

              <div v-else :class="$style.mobileList">
                <ReportTaskMobileItem
                  v-for="task in report.item.tasks"
                  :key="task.id"
                  :task="task"
                  :status-label="labelTaskStatus(task.status)"
                  :tone="normalizeTaskTone(task.status)"
                  :format-date-time="formatDateTime"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      <section
        v-else-if="report.report_type === 'medical_procedures'"
        :class="$style.section"
      >
        <AppDataTable
          v-if="!isMobile"
          :columns="medicalProceduresColumns"
          :rows="report.items"
          row-key="id"
        >
          <template #cell-procedure_date="{ row }">
            {{ formatDateTime(row.procedure_date) }}
          </template>
          <template #cell-status="{ row }">
            <AppStatusBadge
              :label="labelProcedureStatus(row.status)"
              :tone="row.status"
            />
          </template>
        </AppDataTable>

        <div v-else :class="$style.mobileList">
          <ReportProcedureMobileItem
            v-for="procedure in report.items"
            :key="procedure.id"
            :procedure="procedure"
            :status-label="labelProcedureStatus(procedure.status)"
            :format-date-time="formatDateTime"
          />
        </div>
      </section>

      <section v-else-if="report.report_type === 'all_tasks'" :class="$style.section">
        <AppDataTable
          v-if="!isMobile"
          :columns="allTasksColumns"
          :rows="report.items"
          row-key="id"
        >
          <template #cell-due_date="{ row }">
            {{ formatDateTime(row.due_date) }}
          </template>
          <template #cell-status="{ row }">
            <AppStatusBadge
              :label="labelTaskStatus(row.status)"
              :tone="normalizeTaskTone(row.status)"
            />
          </template>
        </AppDataTable>

        <div v-else :class="$style.mobileList">
          <ReportTaskMobileItem
            v-for="task in report.items"
            :key="task.id"
            :task="task"
            :status-label="labelTaskStatus(task.status)"
            :tone="normalizeTaskTone(task.status)"
            :format-date-time="formatDateTime"
          />
        </div>
      </section>

      <section v-else-if="report.report_type === 'user_tasks'" :class="$style.section">
        <div v-if="report.summary.users.length" :class="$style.summaryTable">
          <AppDataTable
            v-if="!isMobile"
            :columns="userTasksSummaryColumns"
            :rows="report.summary.users"
            row-key="user_id"
          />

          <div v-else :class="$style.mobileList">
            <ReportUserSummaryMobileItem
              v-for="user in report.summary.users"
              :key="user.user_id"
              :user="user"
              :role-label="labelUserRole(user.role)"
            />
          </div>
        </div>

        <AppDataTable
          v-if="!isMobile"
          :columns="userTasksColumns"
          :rows="report.items"
          row-key="id"
        >
          <template #cell-status="{ row }">
            <AppStatusBadge
              :label="labelTaskStatus(row.status)"
              :tone="normalizeTaskTone(row.status)"
            />
          </template>
          <template #cell-due_date="{ row }">
            {{ formatDateTime(row.due_date) }}
          </template>
        </AppDataTable>

        <div v-else :class="$style.mobileList">
          <ReportTaskMobileItem
            v-for="task in report.items"
            :key="task.id"
            :task="task"
            :status-label="labelTaskStatus(task.status)"
            :tone="normalizeTaskTone(task.status)"
            :format-date-time="formatDateTime"
          />
        </div>
      </section>

      <section v-else-if="report.report_type === 'finance'" :class="$style.section">
        <AppDataTable
          v-if="!isMobile"
          :columns="financeColumns"
          :rows="report.items"
          row-key="id"
        >
          <template #cell-date="{ row }">
            {{ formatDateTime(row.date) }}
          </template>
          <template #cell-operation_type="{ row }">
            <AppStatusBadge
              :label="labelOperationType(row.operation_type)"
              :tone="row.operation_type === 'income' ? 'completed' : 'overdue'"
            />
          </template>
          <template #cell-category="{ row }">
            {{ labelFinanceCategory(row.category) }}
          </template>
          <template #cell-amount="{ row }">
            {{ formatMoney(row.amount) }}
          </template>
        </AppDataTable>

        <div v-else :class="$style.mobileList">
          <ReportFinanceMobileItem
            v-for="operation in report.items"
            :key="operation.id"
            :operation="operation"
            :operation-type-label="labelOperationType(operation.operation_type)"
            :category-label="labelFinanceCategory(operation.category)"
            :format-date-time="formatDateTime"
            :format-money="formatMoney"
          />
        </div>
      </section>

      <section v-else-if="report.report_type === 'shelter_summary'" :class="$style.section">
        <div :class="$style.summarySections">
          <div v-if="report.horses_section" :class="$style.nestedSection">
            <div :class="$style.nestedTitle">Лошади</div>

            <AppDataTable
              v-if="!isMobile"
              :columns="summaryHorsesColumns"
              :rows="report.horses_section.items"
              row-key="id"
            >
              <template #cell-status="{ row }">
                <AppStatusBadge
                  :label="labelHorseStatus(row.status)"
                  :tone="row.status"
                />
              </template>
              <template #cell-arrival_date="{ row }">
                {{ formatDate(row.arrival_date) }}
              </template>
            </AppDataTable>

            <div v-else :class="$style.mobileList">
              <ReportHorseSummaryMobileItem
                v-for="horse in report.horses_section.items"
                :key="horse.id"
                :horse="horse"
                :status-label="labelHorseStatus(horse.status)"
                :format-date="formatDate"
              />
            </div>
          </div>

          <div v-if="report.medicine_section" :class="$style.nestedSection">
            <div :class="$style.nestedTitle">Медицина</div>

            <AppDataTable
              v-if="!isMobile"
              :columns="medicalProceduresColumns"
              :rows="report.medicine_section.items"
              row-key="id"
            >
              <template #cell-procedure_date="{ row }">
                {{ formatDateTime(row.procedure_date) }}
              </template>
              <template #cell-status="{ row }">
                <AppStatusBadge
                  :label="labelProcedureStatus(row.status)"
                  :tone="row.status"
                />
              </template>
            </AppDataTable>

            <div v-else :class="$style.mobileList">
              <ReportProcedureMobileItem
                v-for="procedure in report.medicine_section.items"
                :key="procedure.id"
                :procedure="procedure"
                :status-label="labelProcedureStatus(procedure.status)"
                :format-date-time="formatDateTime"
              />
            </div>
          </div>

          <div v-if="report.tasks_section" :class="$style.nestedSection">
            <div :class="$style.nestedTitle">Задачи</div>

            <AppDataTable
              v-if="!isMobile"
              :columns="allTasksColumns"
              :rows="report.tasks_section.items"
              row-key="id"
            >
              <template #cell-due_date="{ row }">
                {{ formatDateTime(row.due_date) }}
              </template>
              <template #cell-status="{ row }">
                <AppStatusBadge
                  :label="labelTaskStatus(row.status)"
                  :tone="normalizeTaskTone(row.status)"
                />
              </template>
            </AppDataTable>

            <div v-else :class="$style.mobileList">
              <ReportTaskMobileItem
                v-for="task in report.tasks_section.items"
                :key="task.id"
                :task="task"
                :status-label="labelTaskStatus(task.status)"
                :tone="normalizeTaskTone(task.status)"
                :format-date-time="formatDateTime"
              />
            </div>
          </div>

          <div v-if="report.finance_section" :class="$style.nestedSection">
            <div :class="$style.nestedTitle">Финансы</div>

            <AppDataTable
              v-if="!isMobile"
              :columns="financeColumns"
              :rows="report.finance_section.items"
              row-key="id"
            >
              <template #cell-date="{ row }">
                {{ formatDateTime(row.date) }}
              </template>
              <template #cell-operation_type="{ row }">
                <AppStatusBadge
                  :label="labelOperationType(row.operation_type)"
                  :tone="row.operation_type === 'income' ? 'completed' : 'overdue'"
                />
              </template>
              <template #cell-category="{ row }">
                {{ labelFinanceCategory(row.category) }}
              </template>
              <template #cell-amount="{ row }">
                {{ formatMoney(row.amount) }}
              </template>
            </AppDataTable>

            <div v-else :class="$style.mobileList">
              <ReportFinanceMobileItem
                v-for="operation in report.finance_section.items"
                :key="operation.id"
                :operation="operation"
                :operation-type-label="labelOperationType(operation.operation_type)"
                :category-label="labelFinanceCategory(operation.category)"
                :format-date-time="formatDateTime"
                :format-money="formatMoney"
              />
            </div>
          </div>

          <div v-if="report.users_section" :class="$style.nestedSection">
            <div :class="$style.nestedTitle">Пользователи</div>

            <AppDataTable
              v-if="!isMobile"
              :columns="summaryUsersColumns"
              :rows="report.users_section.items"
              row-key="user_id"
            >
              <template #cell-role="{ row }">
                {{ labelUserRole(row.role) }}
              </template>
              <template #cell-is_active="{ row }">
                <AppStatusBadge
                  :label="row.is_active ? 'Активен' : 'Заблокирован'"
                  :tone="row.is_active ? 'active' : 'blocked'"
                />
              </template>
            </AppDataTable>

            <div v-else :class="$style.mobileList">
              <ReportUserSummaryMobileItem
                v-for="user in report.users_section.items"
                :key="user.user_id"
                :user="user"
                :role-label="labelUserRole(user.role)"
              />
            </div>
          </div>
        </div>
      </section>
    </div>
  </AppDataPanel>
</template>

<script setup>
import { computed } from 'vue'
import { useQuasar } from 'quasar'
import AppDataPanel from 'src/components/blocks/AppDataPanel/AppDataPanel.vue'
import AppDataTable from 'src/components/blocks/AppDataTable/AppDataTable.vue'
import ReportFinanceMobileItem from 'src/components/blocks/ReportFinanceMobileItem/ReportFinanceMobileItem.vue'
import ReportHorseSummaryMobileItem from 'src/components/blocks/ReportHorseSummaryMobileItem/ReportHorseSummaryMobileItem.vue'
import ReportMedicalRecordMobileItem from 'src/components/blocks/ReportMedicalRecordMobileItem/ReportMedicalRecordMobileItem.vue'
import ReportMetaCard from 'src/components/blocks/ReportMetaCard/ReportMetaCard.vue'
import ReportProcedureMobileItem from 'src/components/blocks/ReportProcedureMobileItem/ReportProcedureMobileItem.vue'
import ReportTaskMobileItem from 'src/components/blocks/ReportTaskMobileItem/ReportTaskMobileItem.vue'
import ReportUserSummaryMobileItem from 'src/components/blocks/ReportUserSummaryMobileItem/ReportUserSummaryMobileItem.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'
import { FINANCE_CATEGORY_OPTIONS } from 'src/constants/reports'

const props = defineProps({
  report: {
    type: Object,
    default: null,
  },
  horsesOptions: {
    type: Array,
    default: () => [],
  },
  usersOptions: {
    type: Array,
    default: () => [],
  },
  isAdmin: {
    type: Boolean,
    default: false,
  },
})

const $q = useQuasar()
const isMobile = computed(() => $q.screen.lt.md)

const previewSubtitle = computed(() => {
  return props.report ? 'Предпросмотр сформированного отчёта' : ''
})

const generatedByLabel = computed(() => {
  if (!props.report?.generated_by) {
    return '—'
  }

  const user = props.report.generated_by
  return `${user.first_name} ${user.last_name}`.trim()
})

const reportMetaEntries = computed(() => {
  return [
    {
      label: 'Дата формирования',
      value: formatGeneratedAt(props.report?.generated_at),
    },
    {
      label: 'Сформировал',
      value: generatedByLabel.value,
    },
  ]
})

const formattedFilters = computed(() => {
  const filters = props.report?.filters || {}
  const entries = []

  Object.entries(filters).forEach(([key, value]) => {
    if (value === null || value === '' || value === false) {
      return
    }

    entries.push({
      label: labelFilterKey(key),
      value: formatFilterValue(key, value),
    })
  })

  return entries.length ? entries : [{ label: 'Фильтры', value: 'Не заданы' }]
})

const formattedSummary = computed(() => {
  if (!props.report?.summary) {
    return []
  }

  return Object.entries(props.report.summary)
    .filter(([key, value]) => {
      if (key === 'users') {
        return false
      }

      if (
        props.report?.report_type === 'shelter_summary' &&
        !props.isAdmin &&
        ['income_total', 'expense_total', 'active_users_count'].includes(key)
      ) {
        return false
      }

      return !Array.isArray(value) && (value === null || typeof value !== 'object')
    })
    .map(([key, value]) => ({
      label: labelSummaryKey(key),
      value: formatSummaryValue(value),
    }))
})

const medicalRecordColumns = [
  { key: 'record_date', label: 'Дата' },
  { key: 'record_type', label: 'Тип записи' },
  { key: 'title', label: 'Заголовок' },
  { key: 'description', label: 'Описание' },
]

const relatedProcedureColumns = [
  { key: 'procedure_name', label: 'Процедура' },
  { key: 'planned_date', label: 'Дата' },
  { key: 'status', label: 'Статус' },
  { key: 'notes', label: 'Примечание' },
]

const relatedTaskColumns = [
  { key: 'title', label: 'Задача' },
  { key: 'status', label: 'Статус' },
  { key: 'due_date', label: 'Срок выполнения' },
  { key: 'executor_name', label: 'Ответственный' },
]

const medicalProceduresColumns = [
  { key: 'horse_name', label: 'Лошадь' },
  { key: 'procedure_name', label: 'Процедура' },
  { key: 'procedure_date', label: 'Дата' },
  { key: 'status', label: 'Статус' },
  { key: 'notes', label: 'Примечание' },
]

const allTasksColumns = [
  { key: 'title', label: 'Задача' },
  { key: 'horse_name', label: 'Лошадь' },
  { key: 'executor_name', label: 'Ответственный' },
  { key: 'due_date', label: 'Срок выполнения' },
  { key: 'status', label: 'Статус' },
]

const userTasksSummaryColumns = [
  { key: 'full_name', label: 'Пользователь' },
  { key: 'total_tasks', label: 'Всего задач', align: 'right' },
  { key: 'in_progress_count', label: 'В работе', align: 'right' },
  { key: 'completed_count', label: 'Выполнено', align: 'right' },
]

const userTasksColumns = [
  { key: 'user_name', label: 'Пользователь' },
  { key: 'title', label: 'Задача' },
  { key: 'horse_name', label: 'Лошадь' },
  { key: 'status', label: 'Статус' },
  { key: 'due_date', label: 'Срок выполнения' },
]

const financeColumns = [
  { key: 'date', label: 'Дата' },
  { key: 'operation_type', label: 'Тип операции' },
  { key: 'category', label: 'Категория' },
  { key: 'amount', label: 'Сумма', align: 'right' },
  { key: 'horse_name', label: 'Лошадь' },
  { key: 'description', label: 'Описание' },
]

const summaryHorsesColumns = [
  { key: 'name', label: 'Кличка' },
  { key: 'breed', label: 'Порода' },
  { key: 'status', label: 'Статус' },
  { key: 'curator_name', label: 'Куратор' },
  { key: 'arrival_date', label: 'Дата поступления' },
]

const summaryUsersColumns = [
  { key: 'full_name', label: 'Пользователь' },
  { key: 'role', label: 'Роль' },
  { key: 'is_active', label: 'Статус' },
  { key: 'curated_horses_count', label: 'Лошадей', align: 'right' },
  { key: 'in_progress_tasks_count', label: 'В работе', align: 'right' },
  { key: 'completed_tasks_count', label: 'Выполнено', align: 'right' },
]

const formatDate = (value) => {
  if (!value) {
    return '—'
  }

  return new Intl.DateTimeFormat('ru-RU').format(new Date(value))
}

const formatDateTime = (value) => {
  if (!value) {
    return '—'
  }

  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

const formatGeneratedAt = (value) => {
  if (!value) {
    return '—'
  }

  if (typeof value === 'string') {
    const match = value.match(/^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})/)

    if (match) {
      const [, year, month, day, hour, minute] = match
      return `${day}.${month}.${year}, ${hour}:${minute}`
    }
  }

  return formatDateTime(value)
}

const formatMoney = (value) => {
  if (value === null || value === undefined) {
    return '—'
  }

  return `${new Intl.NumberFormat('ru-RU').format(Number(value))} ₽`
}

const labelHorseStatus = (status) => {
  return {
    healthy: 'Здоров',
    sick: 'Болен',
    rehabilitation: 'Реабилитация',
    deceased: 'Выбыл',
  }[status] || status
}

const labelProcedureStatus = (status) => {
  return {
    planned: 'Запланировано',
    completed: 'Выполнено',
    overdue: 'Просрочено',
  }[status] || status
}

const labelTaskStatus = (status) => {
  return {
    waiting: 'Ожидает',
    in_progress: 'В работе',
    completed: 'Выполнено',
    overdue: 'Просрочено',
  }[status] || status
}

const normalizeTaskTone = (status) => {
  return status === 'in_progress' ? 'in_progress' : status
}

const labelHorseGender = (gender) => {
  return {
    male: 'Жеребец',
    female: 'Кобыла',
    stallion: 'Жеребец',
    mare: 'Кобыла',
    gelding: 'Мерин',
  }[gender] || gender || '—'
}

const labelOperationType = (value) => {
  return value === 'income' ? 'Доход' : 'Расход'
}

const labelFinanceCategory = (value) => {
  return FINANCE_CATEGORY_OPTIONS.find((option) => option.value === value)?.label || value
}

const labelMedicalRecordType = (value) => {
  return {
    inspection: 'Осмотр',
    diagnosis: 'Диагноз',
    treatment: 'Лечение',
    analysis: 'Анализ',
    procedure: 'Процедура',
    note: 'Заметка',
  }[value] || value
}

const labelUserRole = (role) => {
  return {
    admin: 'Администратор',
    veterinarian: 'Ветеринар',
    user: 'Волонтёр',
  }[role] || role
}

const labelFilterKey = (key) => {
  return {
    status: 'Статус',
    curator_id: 'Куратор',
    horse_id: 'Лошадь',
    user_id: 'Пользователь',
    include_medical_records: 'Медзаписи',
    include_procedures: 'Процедуры',
    include_tasks: 'Задачи',
    include_horses: 'Лошади',
    include_medicine: 'Медицина',
    include_finance: 'Финансы',
    include_users: 'Пользователи',
    operation_type: 'Тип операции',
    category: 'Категория',
    date_from: 'Дата начала',
    date_to: 'Дата окончания',
  }[key] || key
}

const labelSummaryKey = (key) => {
  return {
    total_horses: 'Всего лошадей',
    healthy_count: 'Здоровых',
    sick_count: 'Больных',
    rehabilitation_count: 'На реабилитации',
    deceased_count: 'Выбывших',
    medical_records_count: 'Медзаписей',
    procedures_count: 'Процедур',
    tasks_count: 'Задач',
    total_items: 'Всего записей',
    planned_count: 'Запланировано',
    completed_count: 'Выполнено',
    overdue_count: 'Просрочено',
    waiting_count: 'Ожидает',
    in_progress_count: 'В работе',
    total_income: 'Общая сумма доходов',
    total_expense: 'Общая сумма расходов',
    balance: 'Баланс',
    operations_count: 'Количество операций',
    sick_horses: 'Лошадей на лечении',
    active_tasks_count: 'Активных задач',
    overdue_tasks_count: 'Просроченных задач',
    income_total: 'Доходы',
    expense_total: 'Расходы',
    active_users_count: 'Активных пользователей',
  }[key] || key
}

const formatFilterValue = (key, value) => {
  if (key === 'status') {
    if (value === 'all') {
      return 'Все'
    }

    return {
      healthy: 'Здоров',
      sick: 'Болен',
      rehabilitation: 'Реабилитация',
      deceased: 'Выбыл',
      planned: 'Запланировано',
      waiting: 'Ожидает',
      in_progress: 'В работе',
      completed: 'Выполнено',
      overdue: 'Просрочено',
    }[value] || value
  }

  if (key === 'operation_type') {
    return labelOperationType(value)
  }

  if (key === 'category') {
    return labelFinanceCategory(value)
  }

  if (key.startsWith('include_')) {
    return value ? 'Да' : 'Нет'
  }

  if (key.endsWith('_id')) {
    if (key === 'horse_id') {
      return props.horsesOptions.find((option) => option.value === value)?.label || String(value)
    }

    if (key === 'user_id' || key === 'curator_id') {
      return props.usersOptions.find((option) => option.value === value)?.label || String(value)
    }

    return String(value)
  }

  if (key === 'date_from' || key === 'date_to') {
    return formatDate(value)
  }

  return String(value)
}

const formatSummaryValue = (value) => {
  if (typeof value === 'number') {
    return new Intl.NumberFormat('ru-RU').format(value)
  }

  if (typeof value === 'string') {
    return value
  }

  return '—'
}
</script>

<style module lang="scss" src="./ReportPreviewPanel.module.scss"></style>
