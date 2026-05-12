<template>
  <AppDataPanel
    title="Журнал операций"
    subtitle="История финансовых транзакций"
  >
    <div v-if="loading" :class="$style.state">
      Загрузка операций...
    </div>

    <div v-else-if="error" :class="[$style.state, $style.stateError]">
      Ошибка загрузки: {{ error }}
    </div>

    <AppDataTable
      v-else
      :columns="columns"
      :rows="rows"
      row-key="id"
    >
      <template #empty>
        Нет финансовых операций.
      </template>

      <template #cell-date="{ row }">
        {{ row.date }}
      </template>

      <template #cell-operationType="{ row }">
        <div :class="[$style.typeBadge, row.operationType === 'income' ? $style.typeBadgeIncome : $style.typeBadgeExpense]">
          <q-icon
            :name="row.operationType === 'income' ? 'trending_up' : 'trending_down'"
            size="16px"
          />
          <span>{{ row.operationTypeLabel }}</span>
        </div>
      </template>

      <template #cell-category="{ row }">
        <div :class="$style.categoryBadge">
          {{ row.categoryLabel }}
        </div>
      </template>

      <template #cell-description="{ row }">
        {{ row.description }}
      </template>

      <template #cell-amount="{ row }">
        <span :class="[row.operationType === 'income' ? $style.amountIncome : $style.amountExpense]">
          {{ row.amount }}
        </span>
      </template>
    </AppDataTable>
  </AppDataPanel>
</template>

<script setup>
import { computed } from 'vue'
import AppDataPanel from 'src/components/blocks/AppDataPanel/AppDataPanel.vue'
import AppDataTable from 'src/components/blocks/AppDataTable/AppDataTable.vue'

defineProps({
  rows: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
})

const columns = computed(() => [
  { key: 'date', label: 'Дата' },
  { key: 'operationType', label: 'Тип' },
  { key: 'category', label: 'Категория' },
  { key: 'description', label: 'Описание' },
  { key: 'amount', label: 'Сумма', align: 'right' },
])
</script>

<style module lang="scss" src="./FinanceOperationsTable.module.scss"></style>
