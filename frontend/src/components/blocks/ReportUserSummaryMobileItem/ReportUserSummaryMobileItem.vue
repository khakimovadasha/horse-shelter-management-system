<template>
  <ReportMobileCard
    :title="user.full_name"
    :subtitle="roleLabel"
  >
    <template #aside>
      <AppStatusBadge
        :label="user.is_active ? 'Активен' : 'Заблокирован'"
        :tone="user.is_active ? 'active' : 'blocked'"
      />
    </template>

    <ReportMobileMetaRow
      v-if="showTasksTotal"
      label="Всего задач"
      :value="String(user.total_tasks)"
    />

    <ReportMobileMetaRow
      v-if="showCuratedHorses"
      label="Лошадей"
      :value="String(user.curated_horses_count)"
    />

    <ReportMobileMetaRow
      label="В работе"
      :value="String(user.in_progress_count ?? user.in_progress_tasks_count ?? 0)"
    />

    <ReportMobileMetaRow
      label="Выполнено"
      :value="String(user.completed_count ?? user.completed_tasks_count ?? 0)"
    />
  </ReportMobileCard>
</template>

<script setup>
import { computed } from 'vue'
import ReportMobileCard from 'src/components/blocks/ReportMobileCard/ReportMobileCard.vue'
import ReportMobileMetaRow from 'src/components/blocks/ReportMobileMetaRow/ReportMobileMetaRow.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'

const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
  roleLabel: {
    type: String,
    required: true,
  },
})

const showTasksTotal = computed(() => Object.hasOwn(props.user, 'total_tasks'))
const showCuratedHorses = computed(() => Object.hasOwn(props.user, 'curated_horses_count'))
</script>
