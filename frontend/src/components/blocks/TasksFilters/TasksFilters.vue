<template>
  <AppFiltersPanel>
    <AppFiltersGrid desktop-columns="1fr 1fr 1fr">
      <AppFilterField>
        <AppSelectField
          :model-value="status"
          :options="statusOptions"
          @update:model-value="$emit('update:status', $event)"
        />
      </AppFilterField>

      <AppFilterField>
        <AppSelectField
          :model-value="horseId"
          :options="horseOptions"
          @update:model-value="$emit('update:horseId', $event)"
        />
      </AppFilterField>

      <AppFilterField>
        <AppSelectField
          :model-value="executor"
          :options="executorOptions"
          @update:model-value="$emit('update:executor', $event)"
        />
      </AppFilterField>
    </AppFiltersGrid>
  </AppFiltersPanel>
</template>

<script setup>
import AppFiltersGrid from 'src/components/blocks/AppFiltersGrid/AppFiltersGrid.vue'
import AppFiltersPanel from 'src/components/blocks/AppFiltersPanel/AppFiltersPanel.vue'
import AppFilterField from 'src/components/ui/AppFilterField/AppFilterField.vue'
import AppSelectField from 'src/components/ui/AppSelectField/AppSelectField.vue'

defineProps({
  status: {
    type: String,
    default: 'all',
  },
  horseId: {
    type: [String, Number],
    default: 'all',
  },
  executor: {
    type: String,
    default: 'all',
  },
  horseOptions: {
    type: Array,
    default: () => [],
  },
  executorOptions: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['update:status', 'update:horseId', 'update:executor'])

const statusOptions = [
  { label: 'Все статусы', value: 'all' },
  { label: 'Ожидает', value: 'waiting' },
  { label: 'В работе', value: 'inProgress' },
  { label: 'Выполнено', value: 'completed' },
]
</script>
