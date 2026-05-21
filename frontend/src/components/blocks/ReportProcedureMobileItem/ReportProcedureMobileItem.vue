<template>
  <ReportMobileCard
    :title="procedure.procedure_name"
    :subtitle="procedure.horse_name || ''"
  >
    <template #aside>
      <AppStatusBadge
        :label="statusLabel"
        :tone="procedure.status"
      />
    </template>

    <ReportMobileMetaRow
      v-if="procedure.notes"
      label="Примечание"
      stacked
    >
      {{ procedure.notes }}
    </ReportMobileMetaRow>

    <ReportMobileMetaRow
      :label="dateLabel"
      :value="dateValue"
    />

    <ReportMobileMetaRow
      v-if="showMedicalFlag"
      label="В медкарту"
      :value="procedure.add_to_medical_record ? 'Да' : 'Нет'"
    />
  </ReportMobileCard>
</template>

<script setup>
import { computed } from 'vue'
import ReportMobileCard from 'src/components/blocks/ReportMobileCard/ReportMobileCard.vue'
import ReportMobileMetaRow from 'src/components/blocks/ReportMobileMetaRow/ReportMobileMetaRow.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'

const props = defineProps({
  procedure: {
    type: Object,
    required: true,
  },
  statusLabel: {
    type: String,
    required: true,
  },
  formatDateTime: {
    type: Function,
    required: true,
  },
})

const showMedicalFlag = computed(() => Object.hasOwn(props.procedure, 'add_to_medical_record'))

const dateLabel = computed(() => {
  if (props.procedure.procedure_date) {
    return 'Дата'
  }

  return 'Плановая дата'
})

const dateValue = computed(() => {
  return props.formatDateTime(
    props.procedure.procedure_date || props.procedure.planned_date,
  )
})
</script>
