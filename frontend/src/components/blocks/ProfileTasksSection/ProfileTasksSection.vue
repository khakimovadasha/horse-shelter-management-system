<template>
  <AppDashboardSection
    title="Мои задачи"
    subtitle="Список всех ваших задач"
    action-label="Все"
    action-to="/app/tasks"
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
        <UpcomingTaskItem
          v-for="item in paginatedItems"
          :key="item.id"
          :task-title="item.taskTitle"
          :description="item.description"
          :due-at="item.dueAt"
          :status-label="item.statusLabel"
          :status-tone="item.statusTone"
          :action-label="item.actionLabel"
          :action-filled="item.actionFilled"
          :action-disabled="item.actionDisabled"
          @action-click="$emit('complete-task', item.id)"
        />

        <AppPagination
          v-model="currentPage"
          :max="totalPages"
          :class="$style.pagination"
        />
      </div>

      <div v-else :class="$style.empty">
        По выбранному статусу задач нет
      </div>
    </div>

    <div v-else :class="$style.empty">
      Задач пока нет
    </div>
  </AppDashboardSection>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

import UpcomingTaskItem from 'src/components/blocks/UpcomingTaskItem/UpcomingTaskItem.vue'
import AppDashboardSection from 'src/components/ui/AppDashboardSection/AppDashboardSection.vue'
import AppPagination from 'src/components/ui/AppPagination/AppPagination.vue'

const PAGE_SIZE = 4

defineEmits(['complete-task'])

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
  { label: 'В работе', value: 'in_progress' },
  { label: 'Выполненные', value: 'completed' },
]

const filteredItems = computed(() => {
  if (statusFilter.value === 'all') {
    return props.items
  }

  return props.items.filter((item) => {
    if (statusFilter.value === 'completed') {
      return item.statusTone === 'completed'
    }

    return item.statusTone === 'in_progress' || item.statusTone === 'overdue'
  })
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

<style module lang="scss" src="./ProfileTasksSection.module.scss"></style>
