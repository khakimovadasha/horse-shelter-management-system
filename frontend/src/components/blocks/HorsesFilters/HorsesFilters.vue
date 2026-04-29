<template>
  <AppFiltersPanel>
    <AppFiltersGrid desktop-columns="1.3fr 1fr 1fr">
      <AppFilterField>
        <AppTextField
          clearable
          placeholder="Поиск по кличке..."
          :model-value="search"
          @update:model-value="$emit('update:search', $event)"
        >
          <template #prepend>
            <q-icon name="search" />
          </template>
        </AppTextField>
      </AppFilterField>

      <AppFilterField>
        <AppSelectField
          :model-value="status"
          :options="statusOptions"
          @update:model-value="$emit('update:status', $event)"
        />
      </AppFilterField>

      <AppFilterField>
        <AppSelectField
          :model-value="sort"
          :options="sortOptions"
          @update:model-value="$emit('update:sort', $event)"
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
  sort: {
    type: String,
    default: 'name_asc',
  },
})

defineEmits(['update:search', 'update:status', 'update:sort'])

const statusOptions = [
  { label: 'Все статусы', value: 'all' },
  { label: 'Здоров', value: 'healthy' },
  { label: 'Болен', value: 'sick' },
  { label: 'Реабилитация', value: 'rehabilitation' },
]

const sortOptions = [
  { label: 'По имени', value: 'name_asc' },
  { label: 'По дате поступления', value: 'arrival_date_desc' },
  { label: 'По статусу', value: 'status' },
]
</script>
