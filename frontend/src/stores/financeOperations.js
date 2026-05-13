import { defineStore } from 'pinia'
import { getFinanceOperations, getFinanceSummary } from 'src/api/financeOperations'

const getOperationAmount = (operation) => Number(operation?.amount || 0)

const calculateSummary = (items) => {
  const totalIncome = items
    .filter((operation) => operation.operation_type === 'income')
    .reduce((sum, operation) => sum + getOperationAmount(operation), 0)

  const totalExpense = items
    .filter((operation) => operation.operation_type === 'expense')
    .reduce((sum, operation) => sum + getOperationAmount(operation), 0)

  return {
    total_income: totalIncome,
    total_expense: totalExpense,
    balance: totalIncome - totalExpense,
  }
}

export const useFinanceOperationsStore = defineStore('financeOperations', {
  state: () => ({
    items: [],
    loading: false,
    error: '',
    loaded: false,
    summary: {
      total_income: 0,
      total_expense: 0,
      balance: 0,
    },
    summaryLoading: false,
    summaryError: '',
    summaryLoaded: false,
  }),

  actions: {
    async fetchFinanceOperations(force = false) {
      if (this.loading) {
        return
      }

      if (this.loaded && !force) {
        return
      }

      this.loading = true
      this.error = ''

      try {
        this.items = await getFinanceOperations()
        this.loaded = true
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Не удалось загрузить финансовые операции'
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchFinanceSummary(force = false) {
      if (this.summaryLoading) {
        return
      }

      if (this.summaryLoaded && !force) {
        return
      }

      this.summaryLoading = true
      this.summaryError = ''

      try {
        this.summary = await getFinanceSummary()
        this.summaryLoaded = true
      } catch (err) {
        this.summaryError = err.response?.data?.detail || err.message || 'Не удалось загрузить сводку по финансам'
        throw err
      } finally {
        this.summaryLoading = false
      }
    },

    refreshSummaryFromItems() {
      this.summary = calculateSummary(this.items)
      this.summaryLoaded = true
      this.summaryError = ''
    },

    addFinanceOperation(operation) {
      this.items = [operation, ...this.items]
      this.loaded = true
      this.error = ''
      this.refreshSummaryFromItems()
    },

    updateFinanceOperation(operation) {
      const index = this.items.findIndex((item) => item.id === operation.id)

      if (index === -1) {
        this.items = [operation, ...this.items]
      } else {
        this.items = this.items.map((item) => (item.id === operation.id ? operation : item))
      }

      this.loaded = true
      this.error = ''
      this.refreshSummaryFromItems()
    },

    removeFinanceOperation(operationId) {
      this.items = this.items.filter((item) => item.id !== operationId)
      this.loaded = true
      this.error = ''
      this.refreshSummaryFromItems()
    },
  },
})
