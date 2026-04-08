<template>
  <q-page class="page-container">
    <div class="horses-page__header">
      <div>
        <h1 class="page-title">Лошади</h1>
        <p class="page-subtitle">
          Всего лошадей в приюте: {{ filteredHorses.length }}
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

    <HorsesFilters
      class="q-mt-lg"
      v-model:search="searchQuery"
      v-model:status="selectedStatus"
      v-model:sort="selectedSort"
    />

    <div class="q-mt-xl">
      <div v-if="loading" class="horses-page__state">
        Загрузка...
      </div>

      <div v-else-if="error" class="horses-page__state horses-page__state--error">
        Ошибка загрузки: {{ error }}
      </div>

      <div v-else-if="filteredHorses.length === 0" class="horses-page__state">
        По выбранным параметрам лошади не найдены.
      </div>

      <div v-else class="horses-grid">
        <HorseCard
          v-for="horse in filteredHorses"
          :key="horse.id"
          :horse="horse"
        />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { getHorses } from 'src/api/horses'
import HorseCard from 'src/components/HorseCard.vue'
import HorsesFilters from 'src/components/HorsesFilters.vue'

const horses = ref([])
const loading = ref(true)
const error = ref('')

const searchQuery = ref('')
const selectedStatus = ref('all')
const selectedSort = ref('name_asc')

const statusOrder = {
  sick: 1,
  rehabilitation: 2,
  healthy: 3,
  deceased: 4,
}

const filteredHorses = computed(() => {
  let result = [...horses.value]

  const search = searchQuery.value.trim().toLowerCase()

  if (search) {
    result = result.filter((horse) =>
      horse.name?.toLowerCase().includes(search)
    )
  }

  if (selectedStatus.value !== 'all') {
    result = result.filter((horse) => horse.status === selectedStatus.value)
  }

  if (selectedSort.value === 'name_asc') {
    result.sort((a, b) => a.name.localeCompare(b.name, 'ru'))
  }

  if (selectedSort.value === 'arrival_date_desc') {
    result.sort(
      (a, b) => new Date(b.arrival_date) - new Date(a.arrival_date)
    )
  }

  if (selectedSort.value === 'status') {
    result.sort((a, b) => {
      const aOrder = statusOrder[a.status] ?? 999
      const bOrder = statusOrder[b.status] ?? 999
      return aOrder - bOrder
    })
  }

  return result
})

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