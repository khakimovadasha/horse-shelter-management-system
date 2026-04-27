import { defineStore } from 'pinia'
import { getMe } from 'src/api/auth'

export const useCurrentUserStore = defineStore('currentUser', {
  state: () => ({
    user: null,
    loading: false,
    error: '',
    loaded: false,
  }),

  actions: {
    clearCurrentUser() {
      this.user = null
      this.loading = false
      this.error = ''
      this.loaded = false
    },

    async fetchCurrentUser(force = false) {
      if (this.loading) {
        return
      }

      if (this.loaded && !force) {
        return
      }

      this.loading = true
      this.error = ''

      try {
        this.user = await getMe()
        this.loaded = true
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Не удалось загрузить текущего пользователя'
        throw err
      } finally {
        this.loading = false
      }
    },
  },
})
