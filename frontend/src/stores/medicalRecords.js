import { defineStore } from 'pinia'
import { getHorseMedicalRecords } from 'src/api/horses'

export const useMedicalRecordsStore = defineStore('medicalRecords', {
  state: () => ({
    itemsByHorseId: {},
    loadingByHorseId: {},
    errorByHorseId: {},
  }),

  actions: {
    async fetchHorseMedicalRecords(horseId, force = false) {
      const id = String(horseId)

      if (this.loadingByHorseId[id]) {
        return
      }

      if (this.itemsByHorseId[id] && !force) {
        return
      }

      this.loadingByHorseId[id] = true
      this.errorByHorseId[id] = ''

      try {
        this.itemsByHorseId[id] = await getHorseMedicalRecords(horseId)
      } catch (err) {
        this.errorByHorseId[id] =
          err.response?.data?.detail || err.message || 'Не удалось загрузить медицинские записи'
        throw err
      } finally {
        this.loadingByHorseId[id] = false
      }
    },

    prependMedicalRecord(horseId, record) {
      const id = String(horseId)
      const existingRecords = this.itemsByHorseId[id] || []
      this.itemsByHorseId[id] = [
        record,
        ...existingRecords.filter((item) => item.id !== record.id),
      ]
      this.errorByHorseId[id] = ''
    },
  },
})
