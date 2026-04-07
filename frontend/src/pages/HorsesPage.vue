<template>
  <q-page class="page-container">
    <div class="horses-page__header">
      <div>
        <h1 class="page-title">Лошади</h1>
        <p class="page-subtitle">
          Всего лошадей в приюте: {{ horses.length }}
        </p>
      </div>

      <q-btn
        color="primary"
        unelevated
        no-caps
        icon="add"
        label="Добавить лошадь"
        class="horses-page__add-btn"
      />
    </div>

    <HorsesFilters class="q-mt-lg" />

    <div class="q-mt-xl">
      <div v-if="loading" class="horses-page__state">
        Загрузка...
      </div>

      <div v-else-if="error" class="horses-page__state horses-page__state--error">
        Ошибка загрузки: {{ error }}
      </div>

      <div v-else class="horses-grid">
        <HorseCard
          v-for="horse in horses"
          :key="horse.id"
          :horse="horse"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getHorses } from 'src/api/horses'
import HorseCard from 'src/components/HorseCard.vue'
import HorsesFilters from 'src/components/HorsesFilters.vue'

const horses = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    horses.value = await getHorses()
  } catch (err) {
    error.value = err.message || 'Не удалось загрузить список лошадей'
  } finally {
    loading.value = false
  }
})
</script>