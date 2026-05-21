<template>
  <ReportMobileCard
    :title="amountLabel"
    :subtitle="formatDateTime(operation.date)"
  >
    <template #aside>
      <AppStatusBadge
        :label="operationTypeLabel"
        :tone="operation.operation_type === 'income' ? 'completed' : 'overdue'"
      />
    </template>

    <ReportMobileMetaRow
      label="Категория"
      :value="categoryLabel"
    />

    <ReportMobileMetaRow
      v-if="operation.horse_name"
      label="Лошадь"
      :value="operation.horse_name"
    />

    <ReportMobileMetaRow
      v-if="operation.description"
      label="Описание"
      stacked
    >
      {{ operation.description }}
    </ReportMobileMetaRow>
  </ReportMobileCard>
</template>

<script setup>
import { computed } from 'vue'
import ReportMobileCard from 'src/components/blocks/ReportMobileCard/ReportMobileCard.vue'
import ReportMobileMetaRow from 'src/components/blocks/ReportMobileMetaRow/ReportMobileMetaRow.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'

const props = defineProps({
  operation: {
    type: Object,
    required: true,
  },
  operationTypeLabel: {
    type: String,
    required: true,
  },
  categoryLabel: {
    type: String,
    required: true,
  },
  formatDateTime: {
    type: Function,
    required: true,
  },
  formatMoney: {
    type: Function,
    required: true,
  },
})

const amountLabel = computed(() => props.formatMoney(props.operation.amount))
</script>
