<template>
  <AppDataPanel
    title="Задачи по уходу"
    subtitle="Задачи, связанные с этой лошадью"
  >
    <template v-if="canCreate" #actions>
      <AppButton
        color="primary"
        unelevated
        no-caps
        icon="add"
        label="Создать задачу"
        :class="$style.addButton"
        @click="isCreateDialogOpen = true"
      />
    </template>

    <div v-if="loading" :class="$style.state">
      Загрузка задач...
    </div>

    <div v-else-if="error" :class="[$style.state, $style.stateError]">
      Ошибка загрузки: {{ error }}
    </div>

    <div v-else-if="!rows.length" :class="$style.state">
      Задач пока нет.
    </div>

    <div v-else :class="$style.list">
      <article
        v-for="row in rows"
        :key="row.id"
        :class="[$style.item, row.isOverdue && $style.itemDanger]"
      >
        <div :class="$style.itemHeader">
          <div>
            <h3 :class="$style.title">{{ row.title }}</h3>
            <p :class="$style.description">{{ row.description }}</p>
          </div>

          <AppStatusBadge
            :label="getStatusLabel(row.status)"
            :tone="getStatusTone(row.status)"
          />
        </div>

        <div :class="$style.meta">
          <div v-if="row.executorName" :class="$style.metaRow">
            <span :class="$style.metaLabel">Исполнитель:</span>
            <span :class="$style.metaValue">{{ row.executorName }}</span>
          </div>

          <div :class="$style.metaRow">
            <span :class="$style.metaLabel">{{ row.dateLabel }}:</span>
            <span :class="[$style.metaValue, row.isOverdue && $style.metaValueDanger]">
              {{ row.dateValue }}
            </span>
          </div>
        </div>

        <div
          v-if="row.isOverdue"
          :class="$style.overdueBanner"
        >
          Задача просрочена
        </div>

        <AppButton
          v-if="row.showStartButton"
          label="Взять в работу"
          outline
          :class="$style.primaryAction"
          :disable="startingIds.includes(row.id)"
          @click="handleStartTask(row)"
        />

        <AppButton
          v-else-if="row.showCompleteButton"
          :label="completingIds.includes(row.id) ? 'Завершение...' : 'Завершить'"
          unelevated
          :class="[$style.primaryAction, $style.primaryActionFilled]"
          :disable="completingIds.includes(row.id)"
          @click="handleCompleteTask(row)"
        />
      </article>
    </div>
  </AppDataPanel>

  <TaskCreateDialog
    v-if="canCreate"
    v-model="isCreateDialogOpen"
    :horse-options="horseOptions"
    :initial-horse-id="horseId"
    :disable-horse-selection="true"
    :submitting="isCreatingTask"
    @submit="handleCreateTask"
  />
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { Notify } from 'quasar'
import { completeTask, createTask, startTask } from 'src/api/tasks'
import AppDataPanel from 'src/components/blocks/AppDataPanel/AppDataPanel.vue'
import TaskCreateDialog from 'src/components/blocks/TaskCreateDialog/TaskCreateDialog.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'
import { useCurrentUserStore } from 'src/stores/currentUser'
import { useTasksStore } from 'src/stores/tasks'
import { notifySuccess } from 'src/utils/notifySuccess'
import { canCreateTask } from 'src/utils/permissions'

const props = defineProps({
  horseId: {
    type: Number,
    required: true,
  },
  horseName: {
    type: String,
    default: '',
  },
})

const tasksStore = useTasksStore()
const currentUserStore = useCurrentUserStore()
const { user: currentUser } = storeToRefs(currentUserStore)

const horseIdKey = computed(() => String(props.horseId))
const items = computed(() => tasksStore.itemsByHorseId[horseIdKey.value] || [])
const loading = computed(() => Boolean(tasksStore.loadingByHorseId[horseIdKey.value]))
const error = computed(() => tasksStore.errorByHorseId[horseIdKey.value] || '')
const canCreate = computed(() => canCreateTask(currentUser.value))
const isCreateDialogOpen = ref(false)
const isCreatingTask = ref(false)
const startingIds = ref([])
const completingIds = ref([])

const horseOptions = computed(() => [
  {
    label: props.horseName || `Лошадь #${props.horseId}`,
    value: props.horseId,
  },
])

const rows = computed(() => {
  return [...items.value]
    .map((task) => {
      const isOverdue = (
        task.status !== 'completed' &&
        new Date(task.due_date).getTime() < Date.now()
      )

      return {
        id: task.id,
        title: task.title,
        description: task.description,
        status: task.status,
        executorId: task.executor_id,
        isOverdue,
        executorName: task.executor
          ? [task.executor.first_name, task.executor.last_name].filter(Boolean).join(' ')
          : '',
        dateLabel: task.status === 'completed' ? 'Дата выполнения' : 'Плановая дата',
        dateValue: formatDate(
          task.status === 'completed' ? task.completed_at || task.due_date : task.due_date
        ),
        sortDate: task.status === 'completed' ? task.completed_at || task.due_date : task.due_date,
        showStartButton: task.status === 'waiting',
        showCompleteButton: (
          task.status === 'in_progress' &&
          task.executor_id === currentUser.value?.id
        ),
      }
    })
    .sort((a, b) => new Date(b.sortDate).getTime() - new Date(a.sortDate).getTime())
})

const loadTasks = async () => {
  await tasksStore.fetchHorseTasks(props.horseId).catch(() => {})
}

const handleCreateTask = async (payload) => {
  if (isCreatingTask.value) {
    return
  }

  isCreatingTask.value = true

  try {
    const createdTask = await createTask({
      ...payload,
      horse_id: props.horseId,
    })

    tasksStore.addTask(createdTask)
    isCreateDialogOpen.value = false
    notifySuccess('Задача успешно создана')
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось создать задачу',
    })
  } finally {
    isCreatingTask.value = false
  }
}

const handleStartTask = async (row) => {
  if (startingIds.value.includes(row.id)) {
    return
  }

  startingIds.value = [...startingIds.value, row.id]

  try {
    const updatedTask = await startTask(row.id)
    tasksStore.updateTask(updatedTask)
    notifySuccess('Задача успешно взята в работу')
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось взять задачу в работу',
    })
  } finally {
    startingIds.value = startingIds.value.filter((id) => id !== row.id)
  }
}

const handleCompleteTask = async (row) => {
  if (completingIds.value.includes(row.id)) {
    return
  }

  completingIds.value = [...completingIds.value, row.id]

  try {
    const updatedTask = await completeTask(row.id)
    tasksStore.updateTask(updatedTask)
    notifySuccess('Задача успешно завершена')
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось завершить задачу',
    })
  } finally {
    completingIds.value = completingIds.value.filter((id) => id !== row.id)
  }
}

const getStatusLabel = (status) => {
  switch (status) {
    case 'waiting':
      return 'Ожидает'
    case 'in_progress':
      return 'В работе'
    case 'completed':
      return 'Выполнено'
    default:
      return status
  }
}

const getStatusTone = (status) => {
  switch (status) {
    case 'waiting':
      return 'waiting'
    case 'in_progress':
      return 'in_progress'
    case 'completed':
      return 'completed'
    default:
      return 'default'
  }
}

const formatDate = (value) => {
  return new Date(value).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
  })
}

onMounted(loadTasks)

onMounted(() => {
  currentUserStore.fetchCurrentUser().catch(() => {})
})

watch(
  () => props.horseId,
  () => {
    loadTasks()
    isCreateDialogOpen.value = false
    startingIds.value = []
    completingIds.value = []
  }
)
</script>

<style module lang="scss" src="./HorseTasksPanel.module.scss"></style>
