import { defineStore } from 'pinia'
import { getTasks } from 'src/api/tasks'

export const useTasksStore = defineStore('tasks', {
  state: () => ({
    items: [],
    loading: false,
    error: '',
    loaded: false,
  }),

  actions: {
    async fetchTasks(force = false) {
      if (this.loading) {
        return
      }

      if (this.loaded && !force) {
        return
      }

      this.loading = true
      this.error = ''

      try {
        this.items = await getTasks()
        this.loaded = true
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Не удалось загрузить задачи'
        throw err
      } finally {
        this.loading = false
      }
    },

    updateTask(task) {
      this.items = this.items.map((item) => (item.id === task.id ? task : item))
      this.loaded = true
      this.error = ''
    },

    addTask(task) {
      this.items = [task, ...this.items]
      this.loaded = true
      this.error = ''
    },
  },
})
