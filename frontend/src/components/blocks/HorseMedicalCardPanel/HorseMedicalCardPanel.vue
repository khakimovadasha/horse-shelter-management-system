<template>
  <q-card :class="[$style.root, 'app-card']">
    <div :class="$style.header">
      <div>
        <div :class="$style.title">Медицинская карта</div>
        <div :class="$style.subtitle">История медицинских записей</div>
      </div>

      <AppButton
        color="primary"
        unelevated
        no-caps
        icon="add"
        label="Добавить запись"
        :class="$style.addButton"
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
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { getHorseMedicalRecords } from 'src/api/horses'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'

const props = defineProps({
  horseId: {
    type: Number,
    required: true,
  },
})

const records = ref([])
const loading = ref(false)
const error = ref('')
const recordTypeLabels = {
  inspection: 'Осмотр',
  diagnosis: 'Диагноз',
  treatment: 'Лечение',
  analysis: 'Анализ',
  procedure: 'Процедура',
  note: 'Заметка',
}

const loadMedicalRecords = async () => {
  loading.value = true
  error.value = ''

  try {
    records.value = await getHorseMedicalRecords(props.horseId)
  } catch (err) {
    error.value =
      err.response?.data?.detail || err.message || 'Не удалось загрузить медицинские записи'
  } finally {
    loading.value = false
  }
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

onMounted(loadMedicalRecords)

watch(
  () => props.horseId,
  () => {
    loadMedicalRecords()
  }
)
</script>

<style module lang="scss" src="./HorseMedicalCardPanel.module.scss"></style>
