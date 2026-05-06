<template>
  <AppDataPanel
    title="Список процедур"
    subtitle="Все медицинские процедуры"
  >
    <AppDataTable
      v-if="!isMobile"
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

      <template #cell-notes="{ value }">
        <div :class="$style.notesCell">{{ value }}</div>
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
            v-if="canComplete && row.status !== 'completed'"
            :label="isCompleting(row.id) ? 'Выполняется...' : 'Выполнить'"
            :loading="isCompleting(row.id)"
            :disable="isCompleting(row.id)"
            @click="emit('complete', row)"
          />
        </div>
      </template>
    </AppDataTable>

    <div v-else :class="$style.mobileList">
      <article
        v-for="row in rows"
        :key="row.id"
        :class="[
          $style.mobileCard,
          row.rowTone === 'danger' ? $style.mobileCardDanger : '',
        ]"
      >
        <div :class="$style.mobileCardHeader">
          <div>
            <div :class="$style.mobileCardTitle">{{ row.procedureType }}</div>
            <div :class="$style.mobileHorse">{{ row.horseName }}</div>
          </div>

          <AppStatusBadge
            :label="getStatusLabel(row.status)"
            :tone="getStatusTone(row.status)"
          />
        </div>

        <div :class="$style.mobileMeta">
          <div :class="[$style.mobileMetaItem, $style.mobileMetaItemStacked]">
            <span :class="$style.mobileMetaLabel">Описание</span>
            <span :class="[$style.mobileMetaValue, $style.mobileNotes]">{{ row.notes }}</span>
          </div>

          <div :class="$style.mobileMetaItem">
            <span :class="$style.mobileMetaLabel">Дата</span>
            <span :class="$style.mobileMetaValue">{{ formatDate(row.scheduledAt) }}</span>
          </div>

          <div :class="$style.mobileMetaItem">
            <span :class="$style.mobileMetaLabel">Время</span>
            <span :class="$style.mobileMetaValue">{{ formatTime(row.scheduledAt) }}</span>
          </div>

          <div :class="$style.mobileMetaItem">
            <span :class="$style.mobileMetaLabel">В медкарту</span>
            <span :class="$style.mobileFlagValue">
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
            </span>
          </div>
        </div>

        <div
          v-if="canComplete && row.status !== 'completed'"
          :class="$style.mobileActions"
        >
          <AppTableAction
            :label="isCompleting(row.id) ? 'Выполняется...' : 'Выполнить'"
            :loading="isCompleting(row.id)"
            :disable="isCompleting(row.id)"
            @click="emit('complete', row)"
          />
        </div>
      </article>
    </div>
  </AppDataPanel>
</template>

<script setup>
import { computed } from 'vue'
import { useQuasar } from 'quasar'
import AppDataPanel from 'src/components/blocks/AppDataPanel/AppDataPanel.vue'
import AppDataTable from 'src/components/blocks/AppDataTable/AppDataTable.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'
import AppTableAction from 'src/components/ui/AppTableAction/AppTableAction.vue'

const props = defineProps({
  rows: {
    type: Array,
    default: () => [],
  },
  canComplete: {
    type: Boolean,
    default: false,
  },
  completingIds: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['complete'])

const $q = useQuasar()
const isMobile = computed(() => $q.screen.lt.md)

const columns = [
  { key: 'horseName', label: 'Лошадь' },
  { key: 'procedureType', label: 'Тип процедуры' },
  { key: 'notes', label: 'Описание' },
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
const isCompleting = (id) => props.completingIds.includes(id)

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
