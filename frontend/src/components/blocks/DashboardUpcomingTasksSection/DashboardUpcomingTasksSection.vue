<template>
  <AppDashboardSection
    title="Список ближайших задач"
    subtitle="Запланированные задачи по уходу"
    action-label="Все"
    :action-to="actionTo"
  >
    <div :class="$style.list">
      <UpcomingTaskItem
        v-for="item in items"
        :key="item.id"
        :task-title="item.taskTitle"
        :description="item.description"
        :due-at="item.dueAt"
        :status-label="item.statusLabel"
        :status-tone="item.statusTone"
      />
    </div>
  </AppDashboardSection>
</template>

<script setup>
import UpcomingTaskItem from 'src/components/blocks/UpcomingTaskItem/UpcomingTaskItem.vue'
import AppDashboardSection from 'src/components/ui/AppDashboardSection/AppDashboardSection.vue'

defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  actionTo: {
    type: String,
    default: '/app/tasks',
  },
})
</script>

<style module lang="scss" src="./DashboardUpcomingTasksSection.module.scss"></style>
