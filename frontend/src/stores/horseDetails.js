import { defineStore } from 'pinia'
import { getHorseById } from 'src/api/horses'

export const useHorseDetailsStore = defineStore('horseDetails', {
  state: () => ({
    items: {},
    loadingById: {},
    errorById: {},
  }),

  actions: {
    async fetchHorse(horseId, force = false) {
      const id = String(horseId)

      if (this.loadingById[id]) {
        return
      }

      if (this.items[id] && !force) {
        return
      }

      this.loadingById[id] = true
      this.errorById[id] = ''

      try {
        this.items[id] = await getHorseById(horseId)
      } catch (err) {
        this.errorById[id] =
          err.response?.data?.detail || err.message || 'Не удалось загрузить данные лошади'
        throw err
      } finally {
        this.loadingById[id] = false
      }
    },

    updateHorse(horse) {
      const id = String(horse.id)
      this.items[id] = horse
      this.errorById[id] = ''
    },
  },
})
