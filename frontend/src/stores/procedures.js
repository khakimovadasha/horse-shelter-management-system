import { defineStore } from 'pinia'
import { getProcedures } from 'src/api/procedures'

export const useProceduresStore = defineStore('procedures', {
  state: () => ({
    items: [],
    loading: false,
    error: '',
    loaded: false,
  }),

  actions: {
    async fetchProcedures(force = false) {
      if (this.loading) {
        return
      }

      if (this.loaded && !force) {
        return
      }

      this.loading = true
      this.error = ''

      try {
        this.items = await getProcedures()
        this.loaded = true
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Не удалось загрузить процедуры'
        throw err
      } finally {
        this.loading = false
      }
    },

    updateProcedure(procedure) {
      this.items = this.items.map((item) => (item.id === procedure.id ? procedure : item))
      this.loaded = true
      this.error = ''
    },
  },
})
