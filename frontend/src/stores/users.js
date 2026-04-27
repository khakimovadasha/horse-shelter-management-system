import { defineStore } from 'pinia'
import { getUsers } from 'src/api/users'

export const useUsersStore = defineStore('users', {
  state: () => ({
    items: [],
    loading: false,
    error: '',
    loaded: false,
  }),

  actions: {
    async fetchUsers(force = false) {
      if (this.loading) {
        return
      }

      if (this.loaded && !force) {
        return
      }

      this.loading = true
      this.error = ''

      try {
        this.items = await getUsers()
        this.loaded = true
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Не удалось загрузить пользователей'
        throw err
      } finally {
        this.loading = false
      }
    },
  },
})
