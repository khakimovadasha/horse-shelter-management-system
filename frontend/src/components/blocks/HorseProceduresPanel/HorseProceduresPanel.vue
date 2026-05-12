<template>
  <AppDataPanel
    title="Процедуры"
    subtitle="Запланированные и выполненные процедуры"
  >
    <template v-if="canCreate" #actions>
      <AppButton
        color="primary"
        unelevated
        no-caps
        icon="add"
        label="Добавить процедуру"
        :class="$style.addButton"
        @click="isCreateDialogOpen = true"
      />
    </template>

    <div v-if="loading" :class="$style.state">
      Загрузка процедур...
    </div>

    <div v-else-if="error" :class="[$style.state, $style.stateError]">
      Ошибка загрузки: {{ error }}
    </div>

    <div v-else-if="!rows.length" :class="$style.state">
      Процедур пока нет.
    </div>

    <div v-else :class="$style.list">
      <article
        v-for="row in rows"
        :key="row.id"
        :class="[$style.item, row.status === 'overdue' && $style.itemDanger]"
      >
        <div :class="$style.itemHeader">
          <div>
            <h3 :class="$style.title">{{ row.procedureName }}</h3>
            <div :class="$style.date">{{ row.dateLabel }}</div>
          </div>

          <AppStatusBadge
            :label="getStatusLabel(row.status)"
            :tone="getStatusTone(row.status)"
          />
        </div>

        <p :class="$style.notes">{{ row.notes }}</p>

        <div
          v-if="canComplete && row.status !== 'completed'"
          :class="$style.actions"
        >
          <AppTableAction
            :label="completingIds.includes(row.id) ? 'Выполняется...' : 'Выполнить'"
            :disable="completingIds.includes(row.id)"
            @click="handleCompleteProcedure(row)"
          />
        </div>
      </article>
    </div>
  </AppDataPanel>

  <ProcedureCreateDialog
    v-if="canCreate"
    v-model="isCreateDialogOpen"
    :horse-options="horseOptions"
    :initial-horse-id="horseId"
    :disable-horse-selection="true"
    :submitting="isCreatingProcedure"
    @submit="handleCreateProcedure"
  />
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { Notify } from 'quasar'
import { completeProcedure, createProcedure } from 'src/api/procedures'
import AppDataPanel from 'src/components/blocks/AppDataPanel/AppDataPanel.vue'
import ProcedureCreateDialog from 'src/components/blocks/ProcedureCreateDialog/ProcedureCreateDialog.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'
import AppTableAction from 'src/components/ui/AppTableAction/AppTableAction.vue'
import { useCurrentUserStore } from 'src/stores/currentUser'
import { useMedicalRecordsStore } from 'src/stores/medicalRecords'
import { useProceduresStore } from 'src/stores/procedures'
import { notifySuccess } from 'src/utils/notifySuccess'
import { canCompleteProcedure, canCreateProcedure } from 'src/utils/permissions'

const props = defineProps({
  horseId: {
    type: Number,
    required: true,
  },
  horseName: {
    type: String,
    default: '',
  },
})

const proceduresStore = useProceduresStore()
const currentUserStore = useCurrentUserStore()
const medicalRecordsStore = useMedicalRecordsStore()
const { user: currentUser } = storeToRefs(currentUserStore)

const horseIdKey = computed(() => String(props.horseId))
const items = computed(() => proceduresStore.itemsByHorseId[horseIdKey.value] || [])
const loading = computed(() => Boolean(proceduresStore.loadingByHorseId[horseIdKey.value]))
const error = computed(() => proceduresStore.errorByHorseId[horseIdKey.value] || '')
const canCreate = computed(() => canCreateProcedure(currentUser.value))
const canComplete = computed(() => canCompleteProcedure(currentUser.value))
const isCreateDialogOpen = ref(false)
const isCreatingProcedure = ref(false)
const completingIds = ref([])

const horseOptions = computed(() => [
  {
    label: props.horseName || `Лошадь #${props.horseId}`,
    value: props.horseId,
  },
])

const now = () => Date.now()

const rows = computed(() => {
  return [...items.value]
    .map((procedure) => {
      const scheduledAt = procedure.completed_date || procedure.planned_date
      const isOverdue = (
        procedure.status === 'planned' &&
        procedure.planned_date &&
        new Date(procedure.planned_date).getTime() < now()
      )

      return {
        id: procedure.id,
        procedureName: procedure.procedure_name,
        notes: procedure.notes?.trim() || 'Без описания',
        status: isOverdue ? 'overdue' : procedure.status,
        scheduledAt,
        dateLabel: formatDateTime(scheduledAt),
      }
    })
    .sort((a, b) => new Date(b.scheduledAt).getTime() - new Date(a.scheduledAt).getTime())
})

const loadProcedures = async () => {
  await proceduresStore.fetchHorseProcedures(props.horseId).catch(() => {})
}

const handleCreateProcedure = async (payload) => {
  if (isCreatingProcedure.value) {
    return
  }

  isCreatingProcedure.value = true

  try {
    const createdProcedure = await createProcedure(props.horseId, {
      procedure_name: payload.procedure_name,
      notes: payload.notes,
      planned_date: payload.planned_date,
      add_to_medical_record: payload.add_to_medical_record,
    })

    proceduresStore.addProcedure(createdProcedure)
    isCreateDialogOpen.value = false
    notifySuccess('Медицинская процедура успешно добавлена')
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
    const updatedProcedure = await completeProcedure(props.horseId, row.id)

    proceduresStore.updateProcedure(updatedProcedure)

    if (updatedProcedure.add_to_medical_record) {
      await medicalRecordsStore.fetchHorseMedicalRecords(props.horseId, true).catch(() => {})
    }

    notifySuccess('Медицинская процедура успешно выполнена')
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось отметить процедуру как выполненную',
    })
  } finally {
    completingIds.value = completingIds.value.filter((id) => id !== row.id)
  }
}

const getStatusLabel = (status) => {
  switch (status) {
    case 'planned':
      return 'Запланировано'
    case 'completed':
      return 'Выполнено'
    case 'overdue':
      return 'Просрочено'
    default:
      return status
  }
}

const getStatusTone = (status) => {
  switch (status) {
    case 'planned':
      return 'planned'
    case 'completed':
      return 'completed'
    case 'overdue':
      return 'overdue'
    default:
      return 'default'
  }
}

const formatDateTime = (value) => {
  return new Date(value).toLocaleString('ru-RU', {
    day: 'numeric',
    month: 'long',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(loadProcedures)

onMounted(() => {
  currentUserStore.fetchCurrentUser().catch(() => {})
})

watch(
  () => props.horseId,
  () => {
    loadProcedures()
    isCreateDialogOpen.value = false
    completingIds.value = []
  }
)
</script>

<style module lang="scss" src="./HorseProceduresPanel.module.scss"></style>
