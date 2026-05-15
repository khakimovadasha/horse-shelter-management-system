<template>
  <AppDashboardSection
    title="Мои лошади"
    subtitle="Лошади под вашим кураторством"
    action-label="Все"
    action-to="/app/horses"
  >
    <div v-if="items.length" :class="$style.content">
      <div :class="$style.filters">
        <q-select
          v-model="statusFilter"
          outlined
          dense
          emit-value
          map-options
          :options="statusOptions"
          :class="$style.filterSelect"
          dropdown-icon="expand_more"
        />
      </div>

      <div v-if="filteredItems.length" :class="$style.list">
        <ProfileHorseItem
          v-for="item in paginatedItems"
          :key="item.id"
          :to="item.to"
          :horse-name="item.horseName"
          :breed="item.breed"
          :secondary-text="item.secondaryText"
          :status-label="item.statusLabel"
          :status-tone="item.statusTone"
        />

        <AppPagination
          v-model="currentPage"
          :max="totalPages"
          :class="$style.pagination"
        />
      </div>

      <div v-else :class="$style.empty">
        По выбранному статусу лошадей нет
      </div>
    </div>

    <div v-else :class="$style.empty">
      Закреплённых лошадей пока нет
    </div>
  </AppDashboardSection>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

import ProfileHorseItem from 'src/components/blocks/ProfileHorseItem/ProfileHorseItem.vue'
import AppDashboardSection from 'src/components/ui/AppDashboardSection/AppDashboardSection.vue'
import AppPagination from 'src/components/ui/AppPagination/AppPagination.vue'

const PAGE_SIZE = 4

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
})

const statusFilter = ref('all')
const currentPage = ref(1)

const statusOptions = [
  { label: 'Все статусы', value: 'all' },
  { label: 'Здоров', value: 'healthy' },
  { label: 'Болен', value: 'sick' },
  { label: 'Реабилитация', value: 'rehabilitation' },
  { label: 'Выбыл', value: 'deceased' },
]

const filteredItems = computed(() => {
  const sorted = [...props.items].sort((a, b) => a.horseName.localeCompare(b.horseName, 'ru'))

  if (statusFilter.value === 'all') {
    return sorted
  }

  return sorted.filter((item) => item.statusTone === statusFilter.value)
})

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(filteredItems.value.length / PAGE_SIZE))
})

const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredItems.value.slice(start, start + PAGE_SIZE)
})

watch(statusFilter, () => {
  currentPage.value = 1
})

watch(
  () => filteredItems.value.length,
  () => {
    if (currentPage.value > totalPages.value) {
      currentPage.value = totalPages.value
    }
  }
)
</script>

<style module lang="scss" src="./ProfileHorsesSection.module.scss"></style>
