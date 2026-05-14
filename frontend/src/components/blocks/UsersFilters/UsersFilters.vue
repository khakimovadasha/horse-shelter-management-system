<template>
  <AppFiltersPanel>
    <AppFiltersGrid :columns="2">
      <AppFilterField>
        <AppSelectField
          :model-value="role"
          :options="roleOptions"
          placeholder="Все роли"
          hide-bottom-space
          @update:model-value="$emit('update:role', $event)"
        />
      </AppFilterField>

      <AppFilterField>
        <AppSelectField
          :model-value="status"
          :options="statusOptions"
          placeholder="Все статусы"
          hide-bottom-space
          @update:model-value="$emit('update:status', $event)"
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
  role: {
    type: String,
    default: 'all',
  },
  status: {
    type: String,
    default: 'all',
  },
})

defineEmits(['update:role', 'update:status'])

const roleOptions = [
  { label: 'Все роли', value: 'all' },
  { label: 'Администратор', value: 'admin' },
  { label: 'Ветеринар', value: 'veterinarian' },
  { label: 'Волонтёр', value: 'user' },
]

const statusOptions = [
  { label: 'Все статусы', value: 'all' },
  { label: 'Активные', value: 'active' },
  { label: 'Заблокированные', value: 'blocked' },
]
</script>
