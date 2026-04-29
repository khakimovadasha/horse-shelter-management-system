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
      <div v-if="proceduresLoading" :class="$style.state">
        Загрузка...
      </div>

      <div v-else-if="proceduresError" :class="[$style.state, $style.stateError]">
        Ошибка загрузки: {{ proceduresError }}
      </div>

      <ProceduresTable
        v-else
        :rows="filteredProcedures"
        :can-complete="canComplete"
        :completing-ids="completingIds"
        @complete="handleCompleteProcedure"
      />
    </div>
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useQuasar } from 'quasar'
import { completeProcedure } from 'src/api/procedures'
import ProceduresFilters from 'src/components/blocks/ProceduresFilters/ProceduresFilters.vue'
import ProceduresTable from 'src/components/blocks/ProceduresTable/ProceduresTable.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import { useCurrentUserStore } from 'src/stores/currentUser'
import { useHorsesStore } from 'src/stores/horses'
import { useProceduresStore } from 'src/stores/procedures'
import { canCompleteProcedure } from 'src/utils/permissions'

const $q = useQuasar()

const searchQuery = ref('')
const selectedStatus = ref('all')
const selectedHorseId = ref('all')
const completingIds = ref([])

const horsesStore = useHorsesStore()
const currentUserStore = useCurrentUserStore()
const proceduresStore = useProceduresStore()

const { items: horses } = storeToRefs(horsesStore)
const { user: currentUser } = storeToRefs(currentUserStore)
const {
  items: procedures,
  loading: proceduresLoading,
  error: proceduresError,
} = storeToRefs(proceduresStore)

const canComplete = computed(() => canCompleteProcedure(currentUser.value))
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
    .map((horse) => ({
      label: horse.name,
      value: horse.id,
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
  try {
    await Promise.all([
      proceduresStore.fetchProcedures(),
      horsesStore.fetchHorses().catch(() => {}),
      currentUserStore.fetchCurrentUser().catch(() => {}),
    ])
  } catch {
    // Процедуры и так положат текст ошибки в store.
  }
}

const handleCompleteProcedure = async (row) => {
  if (!canComplete.value || completingIds.value.includes(row.id)) {
    return
  }

  completingIds.value = [...completingIds.value, row.id]

  try {
    const updatedProcedure = await completeProcedure(row.horseId, row.id)

    proceduresStore.updateProcedure(updatedProcedure)

    $q.notify({
      type: 'positive',
      message: 'Процедура отмечена как выполненная',
    })
  } catch (err) {
    $q.notify({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось отметить процедуру как выполненную',
    })
  } finally {
    completingIds.value = completingIds.value.filter((id) => id !== row.id)
  }
}

onMounted(loadProceduresPage)
</script>

<style module lang="scss" src="./ProceduresPage.module.scss"></style>
