<template>
  <q-page :class="['page-container', $style.page]">
    <div v-if="pageLoading" :class="$style.state">
      Загрузка профиля...
    </div>

    <div v-else-if="pageError" :class="[$style.state, $style.stateError]">
      Ошибка загрузки: {{ pageError }}
    </div>

    <template v-else-if="currentUser">
      <section :class="$style.layout">
        <UserProfileCard
          :class="$style.profileCard"
          :user="currentUser"
        />

        <div :class="$style.statsGrid">
          <AppStatCard
            title="Закреплённых лошадей"
            :value="String(profileSummary.curated_horses_count)"
            subtitle="под кураторством"
            icon="favorite_border"
            tone="neutral"
            value-tone="default"
          />

          <AppStatCard
            title="Моих задач"
            :value="String(profileSummary.my_tasks_count)"
            subtitle="всего"
            icon="task_alt"
            tone="info"
            value-tone="default"
          />
        </div>
      </section>

      <section :class="$style.sectionsGrid">
        <ProfileHorsesSection :items="myHorseItems" />
        <ProfileTasksSection
          :items="myTaskItems"
          @complete-task="handleCompleteTask"
        />
      </section>
    </template>
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { Notify } from 'quasar'

import { completeTask } from 'src/api/tasks'
import ProfileHorsesSection from 'src/components/blocks/ProfileHorsesSection/ProfileHorsesSection.vue'
import ProfileTasksSection from 'src/components/blocks/ProfileTasksSection/ProfileTasksSection.vue'
import UserProfileCard from 'src/components/blocks/UserProfileCard/UserProfileCard.vue'
import AppStatCard from 'src/components/ui/AppStatCard/AppStatCard.vue'
import { useCurrentUserStore } from 'src/stores/currentUser'
import { useProfileStore } from 'src/stores/profile'
import { useTasksStore } from 'src/stores/tasks'
import { notifySuccess } from 'src/utils/notifySuccess'

const currentUserStore = useCurrentUserStore()
const profileStore = useProfileStore()
const tasksStore = useTasksStore()

const { user: currentUser, loading, error } = storeToRefs(currentUserStore)
const {
  summary: profileSummary,
  horses: myHorses,
  tasks: myTasks,
  loading: profileLoading,
  error: profileError,
} = storeToRefs(profileStore)

const completingIds = ref([])

const pageLoading = computed(() => loading.value || profileLoading.value)
const pageError = computed(() => error.value || profileError.value)

const formatDateTime = (value) => {
  if (!value) {
    return 'Дата не указана'
  }

  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

const mapTaskStatus = (task) => {
  if (task.status === 'completed') {
    return { label: 'Выполнено', tone: 'completed' }
  }

  if (new Date(task.due_date).getTime() < Date.now()) {
    return { label: 'Просрочено', tone: 'overdue' }
  }

  return { label: 'В работе', tone: 'in_progress' }
}

const mapHorseStatus = (status) => {
  switch (status) {
    case 'sick':
      return { label: 'Болен', tone: 'sick' }
    case 'rehabilitation':
      return { label: 'Реабилитация', tone: 'rehabilitation' }
    case 'deceased':
      return { label: 'Выбыл', tone: 'deceased' }
    default:
      return { label: 'Здоров', tone: 'healthy' }
  }
}

const myTaskItems = computed(() => {
  return [...myTasks.value]
    .filter((task) => task.status === 'in_progress' || task.status === 'completed')
    .sort((a, b) => new Date(a.due_date).getTime() - new Date(b.due_date).getTime())
    .map((task) => {
      const status = mapTaskStatus(task)

      return {
        id: task.id,
        taskTitle: task.title,
        description: task.description,
        dueAt: formatDateTime(task.due_date),
        statusLabel: status.label,
        statusTone: status.tone,
        actionLabel: task.status === 'in_progress'
          ? (completingIds.value.includes(task.id) ? 'Завершение...' : 'Завершить')
          : '',
        actionFilled: task.status === 'in_progress',
        actionDisabled: completingIds.value.includes(task.id),
      }
    })
})

const myHorseItems = computed(() => {
  return [...myHorses.value].map((horse) => {
    const status = mapHorseStatus(horse.status)

    return {
      id: horse.id,
      to: `/app/horses/${horse.id}`,
      horseName: horse.name,
      breed: horse.breed || 'Порода не указана',
      secondaryText: horse.age != null ? `Возраст: ${horse.age} лет` : 'Возраст не указан',
      statusLabel: status.label,
      statusTone: status.tone,
    }
  })
})

const handleCompleteTask = async (taskId) => {
  if (completingIds.value.includes(taskId)) {
    return
  }

  completingIds.value = [...completingIds.value, taskId]

  try {
    const updatedTask = await completeTask(taskId)
    tasksStore.updateTask(updatedTask)
    notifySuccess('Задача успешно завершена')
  } catch (err) {
    Notify.create({
      type: 'negative',
      message: err.response?.data?.detail || 'Не удалось завершить задачу',
    })
  } finally {
    completingIds.value = completingIds.value.filter((id) => id !== taskId)
  }
}

onMounted(async () => {
  await currentUserStore.fetchCurrentUser().catch(() => {})

  if (!currentUser.value) {
    return
  }

  await profileStore.fetchProfileData(currentUser.value.id).catch(() => {})
})
</script>

<style module lang="scss" src="./UserProfilePage.module.scss"></style>
