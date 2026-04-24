import { defineStore } from 'pinia'
import { getHorses } from 'src/api/horses'

export const useHorsesStore = defineStore('horses', {
  state: () => ({
    items: [],
    loading: false,
    error: '',
    loaded: false,
  }),

  actions: {
    async fetchHorses(force = false) {
      if (this.loading) {
        return
      }

      if (this.loaded && !force) {
        return
      }

      this.loading = true
      this.error = ''

      try {
        this.items = await getHorses()
        this.loaded = true
      } catch (err) {
        this.error = err.message || 'Не удалось загрузить список лошадей'
        throw err
      } finally {
        this.loading = false
      }
    },
  },
})
