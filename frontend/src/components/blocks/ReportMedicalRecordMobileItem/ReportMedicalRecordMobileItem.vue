<template>
  <ReportMobileCard
    :title="record.title"
    :subtitle="typeLabel"
  >
    <ReportMobileMetaRow
      label="Дата"
      :value="formatDateTime(record.record_date)"
    />

    <ReportMobileMetaRow
      v-if="record.description"
      label="Описание"
      stacked
    >
      {{ record.description }}
    </ReportMobileMetaRow>
  </ReportMobileCard>
</template>

<script setup>
import ReportMobileCard from 'src/components/blocks/ReportMobileCard/ReportMobileCard.vue'
import ReportMobileMetaRow from 'src/components/blocks/ReportMobileMetaRow/ReportMobileMetaRow.vue'

defineProps({
  record: {
    type: Object,
    required: true,
  },
  typeLabel: {
    type: String,
    required: true,
  },
  formatDateTime: {
    type: Function,
    required: true,
  },
})
</script>
