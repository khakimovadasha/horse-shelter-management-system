<template>
  <q-page :class="['page-container', $style.page]">
    <div :class="$style.header">
      <div>
        <h1 class="page-title">Задачи по уходу</h1>
        <p class="page-subtitle">Всего задач: {{ filteredTasks.length }}</p>
      </div>

      <AppButton
        v-if="canCreate"
        icon="add"
        label="Создать задачу"
        color="primary"
        unelevated
        :class="$style.addButton"
        @click="isCreateDialogOpen = true"
      />
    </div>

    <TasksFilters
      class="q-mt-lg"
      v-model:status="selectedStatus"
      v-model:horse-id="selectedHorseId"
      v-model:executor="selectedExecutorId"
      :horse-options="horseFilterOptions"
      :executor-options="executorOptions"
    />

    <div class="q-mt-xl">
      <div v-if="tasksLoading" :class="$style.state">
        Загрузка...
      </div>

      <div v-else-if="tasksError" :class="[$style.state, $style.stateError]">
        Ошибка загрузки: {{ tasksError }}
      </div>

      <div v-else-if="!filteredTasks.length" :class="$style.state">
        Задачи не найдены
      </div>

      <div v-else :class="$style.grid">
        <TaskCard
          v-for="task in filteredTasks"
          :key="task.id"
          :task="task"
          :current-user-id="currentUser?.id ?? null"
          :start-loading="startingIds.includes(task.id)"
          :complete-loading="completingIds.includes(task.id)"
          @start="handleStartTask"
          @complete="handleCompleteTask"
        />
      </div>
    </div>

    <TaskCreateDialog
      v-if="canCreate"
      v-model="isCreateDialogOpen"
      :horse-options="taskHorseOptions"
      :submitting="creatingTask"
      @submit="handleCreateTask"
    />
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { Notify } from 'quasar'
import { completeTask, createTask, startTask } from 'src/api/tasks'
import TaskCard from 'src/components/blocks/TaskCard/TaskCard.vue'
import TaskCreateDialog from 'src/components/blocks/TaskCreateDialog/TaskCreateDialog.vue'
import TasksFilters from 'src/components/blocks/TasksFilters/TasksFilters.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import { useCurrentUserStore } from 'src/stores/currentUser'
import { useHorsesStore } from 'src/stores/horses'
import { useTasksStore } from 'src/stores/tasks'
import { canCreateTask } from 'src/utils/permissions'
import { notifySuccess } from 'src/utils/notifySuccess'

const selectedStatus = ref('all')
const selectedHorseId = ref('all')
const selectedExecutorId = ref('all')
const startingIds = ref([])
const completingIds = ref([])
const isCreateDialogOpen = ref(false)
const creatingTask = ref(false)

const tasksStore = useTasksStore()
const horsesStore = useHorsesStore()
const currentUserStore = useCurrentUserStore()

const {
  items: tasks,
  loading: tasksLoading,
  error: tasksError,
} = storeToRefs(tasksStore)
const { items: horses } = storeToRefs(horsesStore)
const { user: currentUser } = storeToRefs(currentUserStore)

const canCreate = computed(() => canCreateTask(currentUser.value))

const now = () => Date.now()

const mapTask = (task) => ({
  id: task.id,
  title: task.title,
  description: task.description,
  horseId: task.horse_id,
  horseName: task.horse?.name || (task.horse_id ? `Лошадь #${task.horse_id}` : 'Общая задача'),
  dueDate: task.due_date,
  completedAt: task.completed_at,
  status: task.status,
  executorId: task.executor_id,
  executorName: task.executor
    ? [task.executor.first_name, task.executor.last_name].filter(Boolean).join(' ')
    : '',
  startedAt: task.started_at,
  isOverdue:
    task.status !== 'completed' &&
    new Date(task.due_date).getTime() < now(),
})

const sortedHorseOptions = computed(() => {
  return horses.value
    .map((horse) => ({
      label: horse.name,
      value: horse.id,
    }))
    .sort((a, b) => a.label.localeCompare(b.label, 'ru'))
})

const horseFilterOptions = computed(() => {
  return [{ label: 'Все лошади', value: 'all' }, ...sortedHorseOptions.value]
})

const taskHorseOptions = computed(() => {
  return [{ label: 'Без привязки к лошади', value: null }, ...sortedHorseOptions.value]
})

const executorOptions = computed(() => {
  const items = tasks.value
    .filter((task) => task.executor?.id)
    .map((task) => ({
      label: [task.executor.first_name, task.executor.last_name].filter(Boolean).join(' '),
      value: task.executor.id,
    }))
    .filter((option, index, array) =>
      array.findIndex((item) => item.value === option.value) === index
    )
    .sort((a, b) => a.label.localeCompare(b.label, 'ru'))

  return [{ label: 'Все исполнители', value: 'all' }, ...items]
})

const filteredTasks = computed(() => {
  return tasks.value
    .map(mapTask)
    .filter((task) => {
      if (selectedStatus.value !== 'all' && task.status !== selectedStatus.value) {
        return false
      }

      if (selectedHorseId.value !== 'all' && task.horseId !== selectedHorseId.value) {
        return false
      }

      if (selectedExecutorId.value !== 'all' && task.executorId !== selectedExecutorId.value) {
        return false
      }

      return true
    })
    .sort((a, b) => new Date(b.dueDate).getTime() - new Date(a.dueDate).getTime())
})

const loadTasksPage = async () => {
  try {
    await Promise.all([
      tasksStore.fetchTasks(),
      horsesStore.fetchHorses().catch(() => {}),
      currentUserStore.fetchCurrentUser().catch(() => {}),
    ])
  } catch {
    // Текст ошибки уже лежит в tasksStore.
  }
}

const handleCreateTask = async (payload) => {
  if (creatingTask.value) {
    return
  }

  creatingTask.value = true

  try {
    const createdTask = await createTask(payload)
    tasksStore.addTask(createdTask)
    isCreateDialogOpen.value = false
    notifySuccess('Задача успешно создана')
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось создать задачу',
    })
  } finally {
    creatingTask.value = false
  }
}

const handleStartTask = async (task) => {
  if (startingIds.value.includes(task.id)) {
    return
  }

  startingIds.value = [...startingIds.value, task.id]

  try {
    const updatedTask = await startTask(task.id)
    tasksStore.updateTask(updatedTask)
    notifySuccess('Задача успешно взята в работу')
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось взять задачу в работу',
    })
  } finally {
    startingIds.value = startingIds.value.filter((id) => id !== task.id)
  }
}

const handleCompleteTask = async (task) => {
  if (completingIds.value.includes(task.id)) {
    return
  }

  completingIds.value = [...completingIds.value, task.id]

  try {
    const updatedTask = await completeTask(task.id)
    tasksStore.updateTask(updatedTask)
    notifySuccess('Задача успешно завершена')
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось завершить задачу',
    })
  } finally {
    completingIds.value = completingIds.value.filter((id) => id !== task.id)
  }
}

onMounted(loadTasksPage)
</script>

<style module lang="scss" src="./TasksPage.module.scss"></style>
