import { defineStore } from 'pinia'
import { getHorseTasks, getTasks } from 'src/api/tasks'
import { useProfileStore } from 'src/stores/profile'

export const useTasksStore = defineStore('tasks', {
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

    async fetchHorseTasks(horseId, force = false) {
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
          [id]: await getHorseTasks(horseId),
        }
      } catch (err) {
        this.errorByHorseId = {
          ...this.errorByHorseId,
          [id]: err.response?.data?.detail || err.message || 'Не удалось загрузить задачи',
        }
        throw err
      } finally {
        this.loadingByHorseId = {
          ...this.loadingByHorseId,
          [id]: false,
        }
      }
    },

    updateTask(task) {
      const profileStore = useProfileStore()
      this.items = this.items.map((item) => (item.id === task.id ? task : item))

      if (task.horse_id !== null) {
        const horseId = String(task.horse_id)
        const horseItems = this.itemsByHorseId[horseId]

        if (horseItems) {
          this.itemsByHorseId = {
            ...this.itemsByHorseId,
            [horseId]: horseItems.map((item) => (item.id === task.id ? task : item)),
          }
        }
      }

      profileStore.syncTask(task)
      this.loaded = true
      this.error = ''
    },

    addTask(task) {
      const profileStore = useProfileStore()
      this.items = [task, ...this.items]

      if (task.horse_id !== null) {
        const horseId = String(task.horse_id)
        const horseItems = this.itemsByHorseId[horseId]

        if (horseItems) {
          this.itemsByHorseId = {
            ...this.itemsByHorseId,
            [horseId]: [task, ...horseItems],
          }
        }
      }

      profileStore.syncTask(task)
      this.loaded = true
      this.error = ''
    },
  },
})
