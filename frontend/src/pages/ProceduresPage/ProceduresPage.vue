<template>
  <q-page :class="['page-container', $style.page]">
    <div :class="$style.header">
      <div>
        <h1 class="page-title">Медицинские процедуры</h1>
        <p class="page-subtitle">Всего процедур: {{ filteredProcedures.length }}</p>
      </div>

      <AppButton
        v-if="canCreate"
        icon="add"
        label="Добавить процедуру"
        color="primary"
        unelevated
        :class="$style.addButton"
        @click="isCreateDialogOpen = true"
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

      <template v-else>
        <ProceduresTable
          :rows="paginatedProcedures"
          :can-complete="canComplete"
          :completing-ids="completingIds"
          @complete="handleCompleteProcedure"
        />

        <div v-if="totalPages > 1" :class="$style.pagination">
          <AppPagination
            v-model="currentPage"
            :max="totalPages"
          />
        </div>
      </template>
    </div>

    <ProcedureCreateDialog
      v-model="isCreateDialogOpen"
      :horse-options="procedureHorseOptions"
      :submitting="isCreatingProcedure"
      @submit="handleCreateProcedure"
    />
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { Notify } from 'quasar'
import { completeProcedure, createProcedure } from 'src/api/procedures'
import ProcedureCreateDialog from 'src/components/blocks/ProcedureCreateDialog/ProcedureCreateDialog.vue'
import ProceduresFilters from 'src/components/blocks/ProceduresFilters/ProceduresFilters.vue'
import ProceduresTable from 'src/components/blocks/ProceduresTable/ProceduresTable.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppPagination from 'src/components/ui/AppPagination/AppPagination.vue'
import { useCurrentUserStore } from 'src/stores/currentUser'
import { useHorsesStore } from 'src/stores/horses'
import { useMedicalRecordsStore } from 'src/stores/medicalRecords'
import { useProceduresStore } from 'src/stores/procedures'
import { canCompleteProcedure, canCreateProcedure } from 'src/utils/permissions'

const PAGE_SIZE = 8

const searchQuery = ref('')
const selectedStatus = ref('all')
const selectedHorseId = ref('all')
const currentPage = ref(1)
const completingIds = ref([])
const isCreateDialogOpen = ref(false)
const isCreatingProcedure = ref(false)

const horsesStore = useHorsesStore()
const currentUserStore = useCurrentUserStore()
const medicalRecordsStore = useMedicalRecordsStore()
const proceduresStore = useProceduresStore()

const { items: horses } = storeToRefs(horsesStore)
const { user: currentUser } = storeToRefs(currentUserStore)
const {
  items: procedures,
  loading: proceduresLoading,
  error: proceduresError,
} = storeToRefs(proceduresStore)

const canCreate = computed(() => canCreateProcedure(currentUser.value))
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

const procedureHorseOptions = computed(() => {
  return horses.value
    .map((horse) => ({
      label: horse.name,
      value: horse.id,
    }))
    .sort((a, b) => a.label.localeCompare(b.label, 'ru'))
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

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(filteredProcedures.value.length / PAGE_SIZE))
})

const paginatedProcedures = computed(() => {
  const startIndex = (currentPage.value - 1) * PAGE_SIZE
  const endIndex = startIndex + PAGE_SIZE
  return filteredProcedures.value.slice(startIndex, endIndex)
})

const loadProceduresPage = async () => {
  try {
    await Promise.all([
      proceduresStore.fetchProcedures(),
      horsesStore.fetchHorses().catch(() => {}),
      currentUserStore.fetchCurrentUser().catch(() => {}),
    ])
  } catch {
    // Текст ошибки уже лежит в store процедур.
  }
}

const handleCreateProcedure = async (payload) => {
  if (!canCreate.value || isCreatingProcedure.value) {
    return
  }

  isCreatingProcedure.value = true

  try {
    const createdProcedure = await createProcedure(payload.horse_id, {
      procedure_name: payload.procedure_name,
      notes: payload.notes,
      planned_date: payload.planned_date,
      add_to_medical_record: payload.add_to_medical_record,
    })

    proceduresStore.addProcedure(createdProcedure)
    isCreateDialogOpen.value = false
    currentPage.value = 1

    Notify.create({
      type: 'positive',
      message: 'Процедура добавлена',
    })
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось добавить процедуру',
    })
  } finally {
    isCreatingProcedure.value = false
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

    const medicalRecordsCacheKey = String(updatedProcedure.horse_id)
    const hasCachedMedicalRecords = Boolean(
      medicalRecordsStore.itemsByHorseId[medicalRecordsCacheKey]
    )

    if (updatedProcedure.add_to_medical_record && hasCachedMedicalRecords) {
      await medicalRecordsStore.fetchHorseMedicalRecords(updatedProcedure.horse_id, true)
    }

    Notify.create({
      type: 'positive',
      message: 'Процедура отмечена как выполненная',
    })
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось отметить процедуру как выполненную',
    })
  } finally {
    completingIds.value = completingIds.value.filter((id) => id !== row.id)
  }
}

watch([searchQuery, selectedStatus, selectedHorseId], () => {
  currentPage.value = 1
})

watch(totalPages, (pages) => {
  if (currentPage.value > pages) {
    currentPage.value = pages
  }
})

onMounted(loadProceduresPage)
</script>

<style module lang="scss" src="./ProceduresPage.module.scss"></style>
