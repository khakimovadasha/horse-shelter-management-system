<template>
  <article :class="[$style.card, isOverdue && $style.cardOverdue]">
    <div :class="$style.header">
      <div>
        <h3 :class="$style.title">{{ task.title }}</h3>
        <div :class="$style.horseName">{{ task.horseName }}</div>
      </div>

      <AppStatusBadge
        :label="statusLabel"
        :tone="statusTone"
      />
    </div>

    <div :class="$style.descriptionBlock">
      <div :class="$style.descriptionLabel">Описание:</div>
      <p :class="$style.description">
        {{ task.description }}
      </p>
    </div>

    <div :class="$style.meta">
      <div
        v-if="task.executorName"
        :class="$style.metaRow"
      >
        <span :class="$style.metaLabel">Исполнитель:</span>
        <span :class="$style.metaValue">{{ task.executorName }}</span>
      </div>

      <div :class="$style.metaRow">
        <span :class="$style.metaLabel">{{ dateLabel }}:</span>
        <span :class="[$style.metaValue, isOverdue && $style.metaValueDanger]">
          {{ formattedDate }}
        </span>
      </div>
    </div>

    <div
      v-if="isOverdue"
      :class="$style.overdueBanner"
    >
      Задача просрочена
    </div>

    <AppButton
      v-if="primaryActionLabel"
      :label="primaryActionLabel"
      :outline="task.status === 'waiting'"
      :unelevated="task.status === 'inProgress'"
      :class="[$style.primaryAction, task.status === 'inProgress' && $style.primaryActionFilled]"
    />
  </article>
</template>

<script setup>
import { computed } from 'vue'
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'

const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
})

const statusLabel = computed(() => {
  switch (props.task.status) {
    case 'waiting':
      return 'Ожидает'
    case 'inProgress':
      return 'В работе'
    case 'completed':
      return 'Выполнено'
    default:
      return 'Ожидает'
  }
})

const statusTone = computed(() => {
  switch (props.task.status) {
    case 'waiting':
      return 'waiting'
    case 'inProgress':
      return 'inProgress'
    case 'completed':
      return 'completed'
    default:
      return 'default'
  }
})

const primaryActionLabel = computed(() => {
  if (props.task.status === 'waiting') {
    return 'Взять в работу'
  }

  if (props.task.status === 'inProgress') {
    return 'Выполнено'
  }

  return ''
})

const formattedDueDate = computed(() => {
  const sourceDate = props.task.status === 'completed'
    ? props.task.completedDate || props.task.dueDate
    : props.task.dueDate

  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
  }).format(new Date(sourceDate))
})

const formattedDate = computed(() => formattedDueDate.value)

const dateLabel = computed(() => {
  return props.task.status === 'completed' ? 'Дата выполнения' : 'Плановая дата'
})

const isOverdue = computed(() => {
  return props.task.status !== 'completed' && props.task.isOverdue
})
</script>

<style module lang="scss" src="./TaskCard.module.scss"></style>
