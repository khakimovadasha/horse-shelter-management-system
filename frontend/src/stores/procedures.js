import { defineStore } from 'pinia'
import { getHorseProcedures, getProcedures } from 'src/api/procedures'

export const useProceduresStore = defineStore('procedures', {
  state: () => ({
    items: [],
    loading: false,
    error: '',
    loaded: false,
    itemsByHorseId: {},
    loadingByHorseId: {},
    errorByHorseId: {},
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

    async fetchHorseProcedures(horseId, force = false) {
      const id = String(horseId)

      if (this.loadingByHorseId[id]) {
        return
      }

      if (this.itemsByHorseId[id] && !force) {
        return
      }

      this.loadingByHorseId = {
        ...this.loadingByHorseId,
        [id]: true,
      }
      this.errorByHorseId = {
        ...this.errorByHorseId,
        [id]: '',
      }

      try {
        this.itemsByHorseId = {
          ...this.itemsByHorseId,
          [id]: await getHorseProcedures(horseId),
        }
      } catch (err) {
        this.errorByHorseId = {
          ...this.errorByHorseId,
          [id]: err.response?.data?.detail || err.message || 'Не удалось загрузить процедуры',
        }
        throw err
      } finally {
        this.loadingByHorseId = {
          ...this.loadingByHorseId,
          [id]: false,
        }
      }
    },

    updateProcedure(procedure) {
      this.items = this.items.map((item) => (item.id === procedure.id ? procedure : item))

      const horseId = String(procedure.horse_id)
      const horseItems = this.itemsByHorseId[horseId]

      if (horseItems) {
        this.itemsByHorseId = {
          ...this.itemsByHorseId,
          [horseId]: horseItems.map((item) => (item.id === procedure.id ? procedure : item)),
        }
      }

      this.loaded = true
      this.error = ''
    },

    addProcedure(procedure) {
      this.items = [procedure, ...this.items]

      const horseId = String(procedure.horse_id)
      const horseItems = this.itemsByHorseId[horseId]

      if (horseItems) {
        this.itemsByHorseId = {
          ...this.itemsByHorseId,
          [horseId]: [procedure, ...horseItems],
        }
      }

      this.loaded = true
      this.error = ''
    },
  },
})
