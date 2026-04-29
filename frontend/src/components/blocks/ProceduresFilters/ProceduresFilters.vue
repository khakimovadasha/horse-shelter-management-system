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
        <AppTextField
          clearable
          placeholder="Поиск по типу процедуры..."
          :model-value="search"
          @update:model-value="$emit('update:search', $event)"
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
import AppTextField from 'src/components/ui/AppTextField/AppTextField.vue'

defineProps({
  search: {
    type: String,
    default: '',
  },
  status: {
    type: String,
    default: 'all',
  },
  horseId: {
    type: [String, Number],
    default: 'all',
  },
  horseOptions: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['update:search', 'update:status', 'update:horseId'])

const statusOptions = [
  { label: 'Все статусы', value: 'all' },
  { label: 'Запланировано', value: 'planned' },
  { label: 'Выполнено', value: 'completed' },
  { label: 'Просрочено', value: 'overdue' },
]
</script>
