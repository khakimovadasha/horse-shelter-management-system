<template>
  <q-page :class="['page-container', $style.page]">
    <div :class="$style.header">
      <div>
        <h1 class="page-title">Задачи по уходу</h1>
        <p class="page-subtitle">Всего задач: {{ filteredTasks.length }}</p>
      </div>

      <AppButton
        icon="add"
        label="Создать задачу"
        color="primary"
        unelevated
        :class="$style.addButton"
      />
    </div>

    <TasksFilters
      class="q-mt-lg"
      v-model:status="selectedStatus"
      v-model:horse-id="selectedHorseId"
      v-model:executor="selectedExecutor"
      :horse-options="horseOptions"
      :executor-options="executorOptions"
    />

    <div :class="$style.grid">
      <TaskCard
        v-for="task in filteredTasks"
        :key="task.id"
        :task="task"
      />
    </div>
  </q-page>
</template>

<script setup>
import { computed, ref } from 'vue'
import TaskCard from 'src/components/blocks/TaskCard/TaskCard.vue'
import TasksFilters from 'src/components/blocks/TasksFilters/TasksFilters.vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'

const selectedStatus = ref('all')
const selectedHorseId = ref('all')
const selectedExecutor = ref('all')

const tasks = [
  {
    id: 1,
    title: 'Смена подстилки',
    horseId: 1,
    horseName: 'Буран',
    description: 'Полная замена соломы в стойле',
    executorName: '',
    dueDate: '2026-02-26',
    status: 'waiting',
  },
  {
    id: 2,
    title: 'Дополнительное кормление',
    horseId: 2,
    horseName: 'Звездочка',
    description: 'Усиленное питание по назначению ветеринара',
    executorName: 'Елена Морозова',
    dueDate: '2026-02-25',
    status: 'inProgress',
  },
  {
    id: 3,
    title: 'Чистка копыт',
    horseId: 3,
    horseName: 'Гром',
    description: 'Регулярная процедура ухода',
    executorName: 'Иван Кузнецов',
    dueDate: '2026-02-24',
    completedDate: '2026-02-24',
    status: 'completed',
  },
  {
    id: 4,
    title: 'Утренняя прогулка',
    horseId: 4,
    horseName: 'Луна',
    description: 'Спокойный выгул на плацу в течение 30 минут',
    executorName: 'Мария Соколова',
    dueDate: '2026-02-27',
    status: 'inProgress',
  },
]

const today = new Date('2026-02-26T12:00:00')

const horseOptions = computed(() => {
  const items = tasks
    .map((task) => ({
      label: task.horseName,
      value: task.horseId,
    }))
    .filter((option, index, array) =>
      array.findIndex((item) => item.value === option.value) === index
    )
    .sort((a, b) => a.label.localeCompare(b.label, 'ru'))

  return [{ label: 'Все лошади', value: 'all' }, ...items]
})

const executorOptions = computed(() => {
  const items = tasks
    .map((task) => task.executorName)
    .filter(Boolean)
    .filter((value, index, array) => array.indexOf(value) === index)
    .sort((a, b) => a.localeCompare(b, 'ru'))
    .map((name) => ({
      label: name,
      value: name,
    }))

  return [{ label: 'Все исполнители', value: 'all' }, ...items]
})

const filteredTasks = computed(() => {
  return tasks
    .map((task) => ({
      ...task,
      isOverdue:
        task.status !== 'completed' &&
        new Date(`${task.dueDate}T23:59:59`).getTime() < today.getTime(),
    }))
    .filter((task) => {
      if (selectedStatus.value !== 'all' && task.status !== selectedStatus.value) {
        return false
      }

      if (selectedHorseId.value !== 'all' && task.horseId !== selectedHorseId.value) {
        return false
      }

      if (selectedExecutor.value !== 'all' && task.executorName !== selectedExecutor.value) {
        return false
      }

      return true
    })
})
</script>

<style module lang="scss" src="./TasksPage.module.scss"></style>
