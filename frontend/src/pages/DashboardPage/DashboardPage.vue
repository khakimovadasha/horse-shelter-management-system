<template>
  <q-page class="page-container">
    <section :class="$style.hero">
      <h1 :class="$style.title">Добро пожаловать</h1>
      <p :class="$style.subtitle">Сегодня {{ todayLabel }}</p>
    </section>

    <section :class="$style.statsGrid">
      <AppStatCard
        title="Всего лошадей"
        :value="String(totalHorses)"
        subtitle="в приюте"
        icon="favorite_border"
        tone="neutral"
        value-tone="default"
        to="/app/horses"
      />

      <AppStatCard
        title="Запланировано задач"
        :value="String(plannedTasksCount)"
        subtitle="ожидают выполнения"
        icon="task_alt"
        tone="info"
        value-tone="default"
        to="/app/tasks"
      />

      <AppStatCard
        title="Запланировано процедур"
        :value="String(plannedProceduresCount)"
        subtitle="ожидают выполнения"
        icon="monitor_heart"
        tone="success"
        value-tone="default"
        to="/app/procedures"
      />

      <AppStatCard
        title="Больные лошади"
        :value="String(sickHorsesCount)"
        subtitle="требуют наблюдения"
        icon="error_outline"
        tone="danger"
        value-tone="default"
        to="/app/horses?status=sick"
      />
    </section>

    <section :class="$style.sectionsGrid">
      <DashboardUpcomingProceduresSection :items="upcomingProcedures" />
      <DashboardUpcomingTasksSection :items="upcomingTasks" />
    </section>
  </q-page>
</template>

<script setup>
import { computed, onMounted } from 'vue'

import DashboardUpcomingProceduresSection from 'src/components/blocks/DashboardUpcomingProceduresSection/DashboardUpcomingProceduresSection.vue'
import DashboardUpcomingTasksSection from 'src/components/blocks/DashboardUpcomingTasksSection/DashboardUpcomingTasksSection.vue'
import AppStatCard from 'src/components/ui/AppStatCard/AppStatCard.vue'
import { useHorsesStore } from 'src/stores/horses'
import { useProceduresStore } from 'src/stores/procedures'
import { useTasksStore } from 'src/stores/tasks'

const horsesStore = useHorsesStore()
const proceduresStore = useProceduresStore()
const tasksStore = useTasksStore()

const todayLabel = computed(() =>
  new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(new Date())
)

const totalHorses = computed(() => horsesStore.items.length)

const plannedTasksCount = computed(
  () => tasksStore.items.filter((task) => task.status !== 'completed').length
)

const plannedProceduresCount = computed(
  () =>
    proceduresStore.items.filter((procedure) => procedure.status !== 'completed')
      .length
)

const sickHorsesCount = computed(
  () => horsesStore.items.filter((horse) => horse.status === 'sick').length
)

const formatShortDateTime = (value) => {
  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return ''
  }

  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
    hour: '2-digit',
    minute: '2-digit',
  })
    .format(date)
    .replace(',', ' в')
}

const getProcedureStatusMeta = (procedure) => {
  const plannedDate = new Date(procedure.planned_date)
  const isOverdue = procedure.status !== 'completed' && plannedDate < new Date()

  if (isOverdue) {
    return {
      label: 'Просрочено',
      tone: 'overdue',
    }
  }

  return {
    label: 'Запланировано',
    tone: 'planned',
  }
}

const getTaskStatusMeta = (task) => {
  const dueDate = new Date(task.due_date)
  const isOverdue = task.status !== 'completed' && dueDate < new Date()

  if (isOverdue) {
    return {
      label: 'Просрочено',
      tone: 'overdue',
    }
  }

  if (task.status === 'in_progress') {
    return {
      label: 'В работе',
      tone: 'inProgress',
    }
  }

  return {
    label: 'Ожидает',
    tone: 'waiting',
  }
}

const upcomingProcedures = computed(() =>
  [...proceduresStore.items]
    .filter((procedure) => procedure.status !== 'completed')
    .sort((a, b) => new Date(a.planned_date) - new Date(b.planned_date))
    .slice(0, 4)
    .map((procedure) => {
      const status = getProcedureStatusMeta(procedure)

      return {
        id: procedure.id,
        horseName: procedure.horse?.name || `Лошадь #${procedure.horse_id}`,
        procedureName: procedure.procedure_name,
        scheduledAt: formatShortDateTime(procedure.planned_date),
        statusLabel: status.label,
        statusTone: status.tone,
      }
    })
)

const upcomingTasks = computed(() =>
  [...tasksStore.items]
    .filter((task) => task.status !== 'completed')
    .sort((a, b) => new Date(a.due_date) - new Date(b.due_date))
    .slice(0, 4)
    .map((task) => {
      const status = getTaskStatusMeta(task)

      return {
        id: task.id,
        taskTitle: task.title,
        description: task.description,
        dueAt: formatShortDateTime(task.due_date),
        statusLabel: status.label,
        statusTone: status.tone,
      }
    })
)

onMounted(async () => {
  await Promise.allSettled([
    horsesStore.fetchHorses(),
    proceduresStore.fetchProcedures(),
    tasksStore.fetchTasks(),
  ])
})
</script>

<style module lang="scss" src="./DashboardPage.module.scss"></style>
