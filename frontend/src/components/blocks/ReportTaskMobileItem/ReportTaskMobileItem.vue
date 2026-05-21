<template>
  <ReportMobileCard
    :title="task.title"
    :subtitle="task.horse_name || ''"
  >
    <template #aside>
      <AppStatusBadge
        :label="statusLabel"
        :tone="tone"
      />
    </template>

    <ReportMobileMetaRow
      v-if="task.description"
      label="Описание"
      stacked
    >
      {{ task.description }}
    </ReportMobileMetaRow>

    <ReportMobileMetaRow
      v-if="task.executor_name"
      label="Ответственный"
      :value="task.executor_name"
    />

    <ReportMobileMetaRow
      label="Срок"
      :value="formatDateTime(task.due_date)"
    />
  </ReportMobileCard>
</template>

<script setup>
import ReportMobileCard from 'src/components/blocks/ReportMobileCard/ReportMobileCard.vue'
import ReportMobileMetaRow from 'src/components/blocks/ReportMobileMetaRow/ReportMobileMetaRow.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'

defineProps({
  task: {
    type: Object,
    required: true,
  },
  statusLabel: {
    type: String,
    required: true,
  },
  tone: {
    type: String,
    required: true,
  },
  formatDateTime: {
    type: Function,
    required: true,
  },
})
</script>
