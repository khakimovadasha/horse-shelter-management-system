import { defineStore } from 'pinia'
import { getMyHorses, getMyProfileSummary, getMyTasks } from 'src/api/auth'

const createEmptySummary = () => ({
  curated_horses_count: 0,
  my_tasks_count: 0,
})

export const useProfileStore = defineStore('profile', {
  state: () => ({
    summary: createEmptySummary(),
    horses: [],
    tasks: [],
    userId: null,
    loading: false,
    error: '',
    loaded: false,
  }),

  actions: {
    clearProfile() {
      this.summary = createEmptySummary()
      this.horses = []
      this.tasks = []
      this.userId = null
      this.loading = false
      this.error = ''
      this.loaded = false
    },

    recalculateSummary() {
      this.summary = {
        curated_horses_count: this.horses.length,
        my_tasks_count: this.tasks.length,
      }
    },

    async fetchProfileData(userId, force = false) {
      if (!userId) {
        this.clearProfile()
        return
      }

      if (this.loading) {
        return
      }

      if (this.loaded && this.userId === userId && !force) {
        return
      }

      this.loading = true
      this.error = ''

      try {
        const [summary, horses, tasks] = await Promise.all([
          getMyProfileSummary(),
          getMyHorses(),
          getMyTasks(),
        ])

        this.summary = summary
        this.horses = horses
        this.tasks = tasks
        this.userId = userId
        this.loaded = true
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Не удалось загрузить профиль'
        throw err
      } finally {
        this.loading = false
      }
    },

    syncHorse(horse) {
      if (!this.userId) {
        return
      }

      const isMine = horse.curator_id === this.userId
      const exists = this.horses.some((item) => item.id === horse.id)

      if (isMine) {
        this.horses = exists
          ? this.horses.map((item) => (item.id === horse.id ? horse : item))
          : [horse, ...this.horses]
      } else if (exists) {
        this.horses = this.horses.filter((item) => item.id !== horse.id)
      }

      if (this.loaded) {
        this.recalculateSummary()
      }
    },

    syncTask(task) {
      if (!this.userId) {
        return
      }

      const isMine = task.executor_id === this.userId
      const exists = this.tasks.some((item) => item.id === task.id)

      if (isMine) {
        this.tasks = exists
          ? this.tasks.map((item) => (item.id === task.id ? task : item))
          : [task, ...this.tasks]
      } else if (exists) {
        this.tasks = this.tasks.filter((item) => item.id !== task.id)
      }

      if (this.loaded) {
        this.recalculateSummary()
      }
    },
  },
})
