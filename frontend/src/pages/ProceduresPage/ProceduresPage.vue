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
      <div v-if="loading" :class="$style.state">
        Загрузка...
      </div>

      <div v-else-if="error" :class="[$style.state, $style.stateError]">
        Ошибка загрузки: {{ error }}
      </div>

      <ProceduresTable
        v-else
        :rows="filteredProcedures"
      />
    </div>
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { getProcedures } from 'src/api/procedures'
import ProceduresFilters from 'src/components/blocks/ProceduresFilters/ProceduresFilters.vue'
import ProceduresTable from 'src/components/blocks/ProceduresTable/ProceduresTable.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import { useHorsesStore } from 'src/stores/horses'

const searchQuery = ref('')
const selectedStatus = ref('all')
const selectedHorseId = ref('all')
const procedures = ref([])
const loading = ref(false)
const error = ref('')

const horsesStore = useHorsesStore()
const { items: horses } = storeToRefs(horsesStore)

const now = () => Date.now()

const getHorseName = (horseId) => {
  return horses.value.find((horse) => horse.id === horseId)?.name || `Лошадь #${horseId}`
}

const getProcedureDisplayStatus = (procedure) => {
  if (
    procedure.status === 'planned' &&
    procedure.planned_date &&
    new Date(procedure.planned_date).getTime() < now()
  ) {
    return 'overdue'
  }

  return procedure.status
}

const mapProcedure = (procedure) => {
  const displayStatus = getProcedureDisplayStatus(procedure)

  return {
    id: procedure.id,
    horseId: procedure.horse_id,
    horseName: getHorseName(procedure.horse_id),
    procedureType: procedure.procedure_name,
    scheduledAt: procedure.completed_date || procedure.planned_date,
    status: displayStatus,
    addToMedicalRecord: procedure.add_to_medical_record,
    rowTone: displayStatus === 'overdue' ? 'danger' : '',
  }
}

const horseOptions = computed(() => {
  const items = horses.value
    .map((procedure) => ({
      label: procedure.name,
      value: procedure.id,
    }))
    .sort((a, b) => a.label.localeCompare(b.label, 'ru'))

  return [{ label: 'Все лошади', value: 'all' }, ...items]
})

const filteredProcedures = computed(() => {
  let result = procedures.value.map(mapProcedure)
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

  return result.sort((a, b) => {
    return new Date(b.scheduledAt).getTime() - new Date(a.scheduledAt).getTime()
  })
})

const loadProceduresPage = async () => {
  loading.value = true
  error.value = ''

  try {
    const [proceduresData] = await Promise.all([
      getProcedures(),
      horsesStore.fetchHorses().catch(() => {}),
    ])

    procedures.value = proceduresData
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Не удалось загрузить процедуры'
  } finally {
    loading.value = false
  }
}

onMounted(loadProceduresPage)
</script>

<style module lang="scss" src="./ProceduresPage.module.scss"></style>
