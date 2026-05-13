import { defineStore } from 'pinia'
import { getFinanceOperations, getFinanceSummary } from 'src/api/financeOperations'

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

    addFinanceOperation(operation) {
      this.items = [operation, ...this.items]
      this.loaded = true
      this.error = ''

      const amount = Number(operation.amount || 0)

      if (operation.operation_type === 'income') {
        this.summary = {
          ...this.summary,
          total_income: Number(this.summary.total_income || 0) + amount,
          balance: Number(this.summary.balance || 0) + amount,
        }
      } else {
        this.summary = {
          ...this.summary,
          total_expense: Number(this.summary.total_expense || 0) + amount,
          balance: Number(this.summary.balance || 0) - amount,
        }
      }

      this.summaryLoaded = true
      this.summaryError = ''
    },
  },
})
