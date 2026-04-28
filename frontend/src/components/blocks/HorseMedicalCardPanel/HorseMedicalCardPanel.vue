<template>
  <q-card :class="[$style.root, 'app-card']">
    <div :class="$style.header">
      <div>
        <div :class="$style.title">Медицинская карта</div>
        <div :class="$style.subtitle">История медицинских записей</div>
      </div>

      <AppButton
        v-if="canCreateRecord"
        color="primary"
        unelevated
        no-caps
        icon="add"
        label="Добавить запись"
        :class="$style.addButton"
        @click="isCreateDialogOpen = true"
      />
    </div>

    <div :class="$style.timeline">
      <div :class="$style.line"></div>

      <div v-if="loading" :class="$style.state">
        Загрузка медицинских записей...
      </div>

      <div v-else-if="error" :class="[$style.state, $style.stateError]">
        Ошибка загрузки: {{ error }}
      </div>

      <div v-else-if="records.length === 0" :class="$style.state">
        Медицинских записей пока нет.
      </div>

      <div
        v-for="record in records"
        v-else
        :key="record.id"
        :class="$style.timelineItem"
      >
        <div :class="$style.dot"></div>

        <div :class="$style.timelineContent">
          <div :class="$style.meta">
            <span :class="$style.type">{{ getRecordTypeLabel(record.record_type) }}</span>
            <span :class="$style.date">{{ formatDate(record.record_date) }}</span>
          </div>

          <div :class="$style.timelineTitle">{{ record.title }}</div>

          <div :class="$style.text">{{ record.description }}</div>

          <div v-if="record.next_procedure_date" :class="$style.text">
            Следующая процедура: {{ formatDate(record.next_procedure_date) }}
          </div>
        </div>
      </div>
    </div>
  </q-card>

  <MedicalRecordCreateDialog
    v-model="isCreateDialogOpen"
    :submitting="isCreatingRecord"
    @submit="handleCreateRecord"
  />
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useQuasar } from 'quasar'
import { createHorseMedicalRecord } from 'src/api/horses'
import MedicalRecordCreateDialog from 'src/components/blocks/MedicalRecordCreateDialog/MedicalRecordCreateDialog.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import { useCurrentUserStore } from 'src/stores/currentUser'
import { useMedicalRecordsStore } from 'src/stores/medicalRecords'
import { canCreateMedicalRecord } from 'src/utils/permissions'

const props = defineProps({
  horseId: {
    type: Number,
    required: true,
  },
})

const $q = useQuasar()
const medicalRecordsStore = useMedicalRecordsStore()
const currentUserStore = useCurrentUserStore()

const { user: currentUser } = storeToRefs(currentUserStore)

const horseId = computed(() => String(props.horseId))
const records = computed(() => {
  const items = medicalRecordsStore.itemsByHorseId[horseId.value] || []

  return [...items].sort((a, b) => {
    const firstDate = new Date(a.record_date).getTime()
    const secondDate = new Date(b.record_date).getTime()

    if (firstDate !== secondDate) {
      return firstDate - secondDate
    }

    return a.id - b.id
  })
})
const loading = computed(() => Boolean(medicalRecordsStore.loadingByHorseId[horseId.value]))
const error = computed(() => medicalRecordsStore.errorByHorseId[horseId.value] || '')
const canCreateRecord = computed(() => canCreateMedicalRecord(currentUser.value))
const isCreateDialogOpen = ref(false)
const isCreatingRecord = ref(false)

const recordTypeLabels = {
  inspection: 'Осмотр',
  diagnosis: 'Диагноз',
  treatment: 'Лечение',
  analysis: 'Анализ',
  procedure: 'Процедура',
  note: 'Заметка',
}

const loadMedicalRecords = async () => {
  await medicalRecordsStore.fetchHorseMedicalRecords(horseId.value).catch(() => {})
}

const formatDate = (value) => {
  return new Date(value).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}

const getRecordTypeLabel = (recordType) => {
  return recordTypeLabels[recordType] || recordType
}

const handleCreateRecord = async (payload) => {
  isCreatingRecord.value = true

  try {
    const createdRecord = await createHorseMedicalRecord(props.horseId, payload)
    medicalRecordsStore.prependMedicalRecord(props.horseId, createdRecord)
    isCreateDialogOpen.value = false

    $q.notify({
      type: 'positive',
      message: 'Медицинская запись добавлена',
    })
  } catch (err) {
    $q.notify({
      type: 'negative',
      message:
        err.response?.data?.detail || err.message || 'Не удалось добавить медицинскую запись',
    })
  } finally {
    isCreatingRecord.value = false
  }
}

onMounted(loadMedicalRecords)

onMounted(() => {
  currentUserStore.fetchCurrentUser().catch(() => {})
})

watch(
  () => props.horseId,
  () => {
    loadMedicalRecords()
    isCreateDialogOpen.value = false
  }
)
</script>

<style module lang="scss" src="./HorseMedicalCardPanel.module.scss"></style>
