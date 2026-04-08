<template>
  <q-card class="app-card horses-filters">
    <div class="horses-filters__grid horses-filters__grid--three">
      <AppTextField
        clearable
        placeholder="Поиск по кличке..."
        class="horses-filters__field"
        :model-value="search"
        @update:model-value="$emit('update:search', $event)"
      >
        <template #prepend>
          <q-icon name="search" />
        </template>
      </AppTextField>

      <AppSelectField
        class="horses-filters__field"
        :model-value="status"
        :options="statusOptions"
        @update:model-value="$emit('update:status', $event)"
      />

      <AppSelectField
        class="horses-filters__field"
        :model-value="sort"
        :options="sortOptions"
        @update:model-value="$emit('update:sort', $event)"
      />
    </div>
  </q-card>
</template>

<script setup>
import AppSelectField from 'src/components/ui/AppSelectField.vue'
import AppTextField from 'src/components/ui/AppTextField.vue'

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
