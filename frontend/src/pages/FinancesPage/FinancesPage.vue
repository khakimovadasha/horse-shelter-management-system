<template>
  <q-page class="page-container">
    <div :class="$style.header">
      <div>
        <h1 class="page-title">Финансовый учет</h1>
        <p class="page-subtitle">Доходы и расходы приюта</p>
      </div>

      <AppButton
        color="primary"
        unelevated
        no-caps
        icon="add"
        label="Добавить операцию"
        :class="$style.addButton"
      />
    </div>

    <section :class="$style.statsGrid">
      <AppStatCard
        title="Общий доход"
        :value="formatCurrency(summary.total_income)"
        icon="trending_up"
        tone="success"
        value-tone="success"
      />

      <AppStatCard
        title="Общий расход"
        :value="formatCurrency(summary.total_expense)"
        icon="trending_down"
        tone="danger"
        value-tone="danger"
      />

      <AppStatCard
        title="Баланс"
        :value="formatCurrency(summary.balance)"
        icon="attach_money"
        tone="success"
        value-tone="success"
      />
    </section>

    <div :class="$style.filtersSection">
      <FinanceFilters
        v-model:operation-type="operationType"
        v-model:category="category"
      />
    </div>

    <div :class="$style.tableSection">
      <FinanceOperationsTable
        :rows="tableRows"
        :loading="loading"
        :error="error"
      />
    </div>
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import FinanceFilters from 'src/components/blocks/FinanceFilters/FinanceFilters.vue'
import FinanceOperationsTable from 'src/components/blocks/FinanceOperationsTable/FinanceOperationsTable.vue'
import AppStatCard from 'src/components/ui/AppStatCard/AppStatCard.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import { useFinanceOperationsStore } from 'src/stores/financeOperations'

const financeOperationsStore = useFinanceOperationsStore()
const { items, loading, error, summary } = storeToRefs(financeOperationsStore)

const operationType = ref('all')
const category = ref('all')

const categoryLabels = {
  donations: 'Пожертвования',
  sponsorship: 'Спонсорство',
  grants: 'Гранты',
  sales: 'Продажи',
  other_income: 'Прочие поступления',
  medications: 'Медикаменты',
  feed: 'Корма',
  care: 'Содержание',
  equipment: 'Инвентарь',
  transport: 'Транспорт',
  repair: 'Ремонт',
  utilities: 'Коммунальные расходы',
  other_expense: 'Прочие расходы',
}

const filteredOperations = computed(() => {
  return items.value.filter((operation) => {
    const matchesType = operationType.value === 'all' || operation.operation_type === operationType.value
    const matchesCategory = category.value === 'all' || operation.category === category.value

    return matchesType && matchesCategory
  })
})

const tableRows = computed(() => {
  return filteredOperations.value.map((operation) => ({
    id: operation.id,
    operationType: operation.operation_type,
    operationTypeLabel: operation.operation_type === 'income' ? 'Доход' : 'Расход',
    category: operation.category,
    categoryLabel: categoryLabels[operation.category] || operation.category,
    description: operation.description,
    date: formatDate(operation.date),
    amount: formatSignedAmount(operation.amount, operation.operation_type),
  }))
})

const formatDate = (value) => {
  return new Date(value).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}

const formatCurrency = (value) => {
  const number = Number(value || 0)

  return `${number.toLocaleString('ru-RU')} ₽`
}

const formatSignedAmount = (value, operationType) => {
  const number = Number(value || 0)
  const sign = operationType === 'income' ? '+' : '-'

  return `${sign}${number.toLocaleString('ru-RU')} ₽`
}

onMounted(() => {
  financeOperationsStore.fetchFinanceOperations().catch(() => {})
  financeOperationsStore.fetchFinanceSummary().catch(() => {})
})
</script>

<style module lang="scss" src="./FinancesPage.module.scss"></style>
