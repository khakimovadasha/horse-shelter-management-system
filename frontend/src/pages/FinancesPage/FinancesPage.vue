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
        @click="openCreateDialog"
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
        @edit="openEditDialog"
        @delete="handleDeleteOperation"
      />

      <div v-if="totalPages > 1" :class="$style.pagination">
        <AppPagination
          v-model="currentPage"
          :max="totalPages"
        />
      </div>
    </div>

    <FinanceOperationCreateDialog
      v-model="isOperationDialogOpen"
      :submitting="isSavingOperation"
      :initial-data="editingOperation"
      @submit="handleSubmitOperation"
    />
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { Notify } from 'quasar'
import {
  createFinanceOperation,
  deleteFinanceOperation,
  updateFinanceOperation,
} from 'src/api/financeOperations'
import FinanceFilters from 'src/components/blocks/FinanceFilters/FinanceFilters.vue'
import FinanceOperationCreateDialog from 'src/components/blocks/FinanceOperationCreateDialog/FinanceOperationCreateDialog.vue'
import FinanceOperationsTable from 'src/components/blocks/FinanceOperationsTable/FinanceOperationsTable.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppPagination from 'src/components/ui/AppPagination/AppPagination.vue'
import AppStatCard from 'src/components/ui/AppStatCard/AppStatCard.vue'
import { useFinanceOperationsStore } from 'src/stores/financeOperations'
import { notifySuccess } from 'src/utils/notifySuccess'

const PAGE_SIZE = 8

const financeOperationsStore = useFinanceOperationsStore()
const { items, loading, error, summary } = storeToRefs(financeOperationsStore)

const operationType = ref('all')
const category = ref('all')
const currentPage = ref(1)
const isOperationDialogOpen = ref(false)
const isSavingOperation = ref(false)
const editingOperation = ref(null)

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

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(filteredOperations.value.length / PAGE_SIZE))
})

const paginatedOperations = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredOperations.value.slice(start, start + PAGE_SIZE)
})

const tableRows = computed(() => {
  return paginatedOperations.value.map((operation) => ({
    id: operation.id,
    source: operation,
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

const openCreateDialog = () => {
  editingOperation.value = null
  isOperationDialogOpen.value = true
}

const openEditDialog = (row) => {
  editingOperation.value = row.source
  isOperationDialogOpen.value = true
}

onMounted(() => {
  financeOperationsStore.fetchFinanceOperations().catch(() => {})
  financeOperationsStore.fetchFinanceSummary().catch(() => {})
})

const handleSubmitOperation = async (payload) => {
  if (isSavingOperation.value) {
    return
  }

  isSavingOperation.value = true

  try {
    if (editingOperation.value?.id) {
      const updatedOperation = await updateFinanceOperation(editingOperation.value.id, payload)
      financeOperationsStore.updateFinanceOperation(updatedOperation)
      notifySuccess('Финансовая операция успешно обновлена')
    } else {
      const createdOperation = await createFinanceOperation(payload)
      financeOperationsStore.addFinanceOperation(createdOperation)
      notifySuccess('Финансовая операция успешно добавлена')
    }

    isOperationDialogOpen.value = false
    editingOperation.value = null
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось сохранить финансовую операцию',
    })
  } finally {
    isSavingOperation.value = false
  }
}

const handleDeleteOperation = async (row) => {
  const operation = row.source

  if (!operation?.id) {
    return
  }

  const confirmed = window.confirm('Удалить эту финансовую операцию?')
  if (!confirmed) {
    return
  }

  try {
    await deleteFinanceOperation(operation.id)
    financeOperationsStore.removeFinanceOperation(operation.id)
    notifySuccess('Финансовая операция успешно удалена')
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось удалить финансовую операцию',
    })
  }
}

watch([operationType, category], () => {
  currentPage.value = 1
})

watch(totalPages, (nextTotalPages) => {
  if (currentPage.value > nextTotalPages) {
    currentPage.value = nextTotalPages
  }
})

watch(isOperationDialogOpen, (isOpen) => {
  if (!isOpen) {
    editingOperation.value = null
  }
})
</script>

<style module lang="scss" src="./FinancesPage.module.scss"></style>
