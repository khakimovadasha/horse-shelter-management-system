<template>
  <q-page class="page-container horse-page">
    <div v-if="loading" class="horses-page__state">
      Загрузка...
    </div>

    <div v-else-if="error" class="horses-page__state horses-page__state--error">
      Ошибка загрузки: {{ error }}
    </div>

    <template v-else-if="horse">
      <router-link to="/horses" class="horse-detail-back">
        <q-icon name="arrow_back" size="20px" />
        <span>Назад</span>
      </router-link>

      <HorseProfileHeader :horse="horse" class="q-mt-lg" />

      <HorseDetailTabs class="q-mt-lg" />

      <HorseMedicalCardPanel class="q-mt-lg" />
    </template>
  </q-page>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getHorseById } from 'src/api/horses'

import HorseProfileHeader from 'src/components/blocks/HorseProfileHeader.vue'
import HorseDetailTabs from 'src/components/blocks/HorseDetailTabs.vue'
import HorseMedicalCardPanel from 'src/components/blocks/HorseMedicalCardPanel.vue'

const route = useRoute()

const horse = ref(null)
const loading = ref(true)
const error = ref('')

const loadHorse = async () => {
  loading.value = true
  error.value = ''

  try {
    horse.value = await getHorseById(route.params.id)
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Не удалось загрузить данные лошади'
  } finally {
    loading.value = false
  }
}

onMounted(loadHorse)

watch(
  () => route.params.id,
  () => {
    loadHorse()
  }
)
</script>
