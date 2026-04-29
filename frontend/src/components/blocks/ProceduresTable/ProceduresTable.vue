<template>
  <AppDataPanel
    title="Список процедур"
    subtitle="Все медицинские процедуры"
  >
    <AppDataTable
      :columns="columns"
      :rows="rows"
      row-key="id"
      row-tone-key="rowTone"
    >
      <template #cell-horseName="{ value }">
        <span :class="$style.horseName">{{ value }}</span>
      </template>

      <template #cell-procedureType="{ value }">
        <span :class="$style.procedureType">{{ value }}</span>
      </template>

      <template #cell-scheduledAt="{ row }">
        <div :class="$style.dateTime">
          <div :class="$style.date">{{ formatDate(row.scheduledAt) }}</div>
          <div :class="$style.time">{{ formatTime(row.scheduledAt) }}</div>
        </div>
      </template>

      <template #cell-status="{ row }">
        <AppStatusBadge
          :label="getStatusLabel(row.status)"
          :tone="getStatusTone(row.status)"
        />
      </template>

      <template #cell-addToMedicalRecord="{ row }">
        <div :class="$style.medicalRecordFlag">
          <q-icon
            v-if="row.addToMedicalRecord"
            name="done"
            :class="[$style.flagIcon, $style.flagIconPositive]"
          />
          <q-icon
            v-else
            name="close"
            :class="[$style.flagIcon, $style.flagIconNegative]"
          />
        </div>
      </template>

      <template #cell-actions="{ row }">
        <div :class="$style.actions">
          <AppTableAction
            v-if="row.status !== 'completed'"
            label="Выполнить"
          />
        </div>
      </template>
    </AppDataTable>
  </AppDataPanel>
</template>

<script setup>
import AppDataPanel from 'src/components/blocks/AppDataPanel/AppDataPanel.vue'
import AppDataTable from 'src/components/blocks/AppDataTable/AppDataTable.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'
import AppTableAction from 'src/components/ui/AppTableAction/AppTableAction.vue'

defineProps({
  rows: {
    type: Array,
    default: () => [],
  },
})

const columns = [
  { key: 'horseName', label: 'Лошадь' },
  { key: 'procedureType', label: 'Тип процедуры' },
  { key: 'scheduledAt', label: 'Дата и время' },
  { key: 'status', label: 'Статус' },
  { key: 'addToMedicalRecord', label: 'В медкарту', align: 'center' },
  { key: 'actions', label: 'Действия', align: 'right' },
]

const statusMap = {
  planned: { label: 'Запланировано', tone: 'planned' },
  completed: { label: 'Выполнено', tone: 'completed' },
  overdue: { label: 'Просрочено', tone: 'overdue' },
}

const getStatusLabel = (status) => statusMap[status]?.label || status
const getStatusTone = (status) => statusMap[status]?.tone || 'default'

const formatDate = (value) => {
  return new Date(value).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}

const formatTime = (value) => {
  return new Date(value).toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<style module lang="scss" src="./ProceduresTable.module.scss"></style>
