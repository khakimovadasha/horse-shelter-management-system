<template>
  <q-page class="page-container">
    <section :class="$style.hero">
      <h1 :class="$style.title">Добро пожаловать</h1>
      <p :class="$style.subtitle">Сегодня {{ todayLabel }}</p>
    </section>

    <section :class="$style.statsGrid">
      <AppStatCard
        title="Всего лошадей"
        value="5"
        subtitle="в приюте"
        icon="favorite_border"
        tone="neutral"
        value-tone="default"
      />

      <AppStatCard
        title="Активные задачи"
        value="2"
        subtitle="требуют внимания"
        icon="task_alt"
        tone="info"
        value-tone="default"
      />

      <AppStatCard
        title="Запланировано процедур"
        value="3"
        subtitle="на ближайшее время"
        icon="monitor_heart"
        tone="success"
        value-tone="default"
      />

      <AppStatCard
        title="Требуют внимания"
        value="3"
        subtitle="просроченные элементы"
        icon="error_outline"
        tone="danger"
        value-tone="default"
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
import { useProceduresStore } from 'src/stores/procedures'
import { useTasksStore } from 'src/stores/tasks'

const proceduresStore = useProceduresStore()
const tasksStore = useTasksStore()

const todayLabel = computed(() =>
  new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(new Date())
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
    proceduresStore.fetchProcedures(),
    tasksStore.fetchTasks(),
  ])
})
</script>

<style module lang="scss" src="./DashboardPage.module.scss"></style>
