<template>
  <q-page :class="['page-container', $style.page]">
    <div :class="$style.header">
      <div>
        <h1 class="page-title">Медицинские процедуры</h1>
        <p class="page-subtitle">Всего процедур: {{ filteredProcedures.length }}</p>
      </div>

      <AppButton
        icon="add"
        label="Добавить процедуру"
        color="primary"
        unelevated
        :class="$style.addButton"
      />
    </div>

    <ProceduresFilters
      class="q-mt-lg"
      v-model:status="selectedStatus"
      v-model:horse-id="selectedHorseId"
      v-model:search="searchQuery"
      :horse-options="horseOptions"
    />

    <div class="q-mt-xl">
      <ProceduresTable :rows="filteredProcedures" />
    </div>
  </q-page>
</template>

<script setup>
import { computed, ref } from 'vue'
import ProceduresFilters from 'src/components/blocks/ProceduresFilters/ProceduresFilters.vue'
import ProceduresTable from 'src/components/blocks/ProceduresTable/ProceduresTable.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'

const searchQuery = ref('')
const selectedStatus = ref('all')
const selectedHorseId = ref('all')

const procedures = [
  {
    id: 1,
    horseId: 2,
    horseName: 'Звездочка',
    procedureType: 'Прием антибиотиков',
    scheduledAt: '2026-02-26T10:00:00',
    status: 'planned',
    rowTone: '',
  },
  {
    id: 2,
    horseId: 3,
    horseName: 'Гром',
    procedureType: 'Физиотерапия',
    scheduledAt: '2026-02-26T14:00:00',
    status: 'planned',
    rowTone: '',
  },
  {
    id: 3,
    horseId: 1,
    horseName: 'Буран',
    procedureType: 'Вакцинация',
    scheduledAt: '2026-02-23T11:00:00',
    status: 'overdue',
    rowTone: 'danger',
  },
  {
    id: 4,
    horseId: 4,
    horseName: 'Луна',
    procedureType: 'Плановый осмотр',
    scheduledAt: '2026-02-25T15:30:00',
    status: 'completed',
    rowTone: '',
  },
  {
    id: 5,
    horseId: 2,
    horseName: 'Звездочка',
    procedureType: 'Повторный осмотр',
    scheduledAt: '2026-02-28T11:00:00',
    status: 'planned',
    rowTone: '',
  },
]

const horseOptions = computed(() => {
  const items = procedures
    .map((procedure) => ({
      label: procedure.horseName,
      value: procedure.horseId,
    }))
    .filter((option, index, array) => {
      return array.findIndex((item) => item.value === option.value) === index
    })
    .sort((a, b) => a.label.localeCompare(b.label, 'ru'))

  return [{ label: 'Все лошади', value: 'all' }, ...items]
})

const filteredProcedures = computed(() => {
  let result = [...procedures]
  const search = searchQuery.value.trim().toLowerCase()

  if (selectedStatus.value !== 'all') {
    result = result.filter((procedure) => procedure.status === selectedStatus.value)
  }

  if (selectedHorseId.value !== 'all') {
    result = result.filter((procedure) => procedure.horseId === selectedHorseId.value)
  }

  if (search) {
    result = result.filter((procedure) =>
      procedure.procedureType.toLowerCase().includes(search)
    )
  }

  return result
})
</script>

<style module lang="scss" src="./ProceduresPage.module.scss"></style>
