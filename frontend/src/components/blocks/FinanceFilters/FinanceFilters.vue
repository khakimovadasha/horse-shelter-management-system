<template>
  <AppFiltersPanel>
    <AppFiltersGrid desktop-columns="1fr 1fr">
      <AppFilterField>
        <AppSelectField
          :model-value="operationType"
          :options="typeOptions"
          @update:model-value="$emit('update:operationType', $event)"
        />
      </AppFilterField>

      <AppFilterField>
        <AppSelectField
          :model-value="category"
          :options="categoryOptions"
          @update:model-value="$emit('update:category', $event)"
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
  operationType: {
    type: String,
    default: 'all',
  },
  category: {
    type: String,
    default: 'all',
  },
})

defineEmits(['update:operationType', 'update:category'])

const typeOptions = [
  { label: 'Все типы', value: 'all' },
  { label: 'Доход', value: 'income' },
  { label: 'Расход', value: 'expense' },
]

const categoryOptions = [
  { label: 'Все категории', value: 'all' },
  { label: 'Пожертвования', value: 'donations' },
  { label: 'Спонсорство', value: 'sponsorship' },
  { label: 'Гранты', value: 'grants' },
  { label: 'Продажи', value: 'sales' },
  { label: 'Прочие поступления', value: 'other_income' },
  { label: 'Медикаменты', value: 'medications' },
  { label: 'Корма', value: 'feed' },
  { label: 'Уход и содержание', value: 'care' },
  { label: 'Инвентарь и оборудование', value: 'equipment' },
  { label: 'Транспорт', value: 'transport' },
  { label: 'Ремонт', value: 'repair' },
  { label: 'Коммунальные расходы', value: 'utilities' },
  { label: 'Прочие расходы', value: 'other_expense' },
]
</script>
