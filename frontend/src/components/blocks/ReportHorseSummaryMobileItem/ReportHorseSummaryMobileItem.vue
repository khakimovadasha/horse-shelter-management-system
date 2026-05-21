<template>
  <ReportMobileCard
    :title="horse.name"
    :subtitle="horse.breed || 'Порода не указана'"
  >
    <template #aside>
      <AppStatusBadge
        :label="statusLabel"
        :tone="horse.status"
      />
    </template>

    <ReportMobileMetaRow
      v-if="horse.curator_name"
      label="Куратор"
      :value="horse.curator_name"
    />

    <ReportMobileMetaRow
      label="Дата поступления"
      :value="formatDate(horse.arrival_date)"
    />
  </ReportMobileCard>
</template>

<script setup>
import ReportMobileCard from 'src/components/blocks/ReportMobileCard/ReportMobileCard.vue'
import ReportMobileMetaRow from 'src/components/blocks/ReportMobileMetaRow/ReportMobileMetaRow.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'

defineProps({
  horse: {
    type: Object,
    required: true,
  },
  statusLabel: {
    type: String,
    required: true,
  },
  formatDate: {
    type: Function,
    required: true,
  },
})
</script>
