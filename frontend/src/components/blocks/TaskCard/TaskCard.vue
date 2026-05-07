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
      v-if="showStartButton"
      label="Взять в работу"
      outline
      :class="$style.primaryAction"
      :disable="startLoading"
      @click="$emit('start', task)"
    />

    <AppButton
      v-else-if="showCompleteButton"
      :label="completeLoading ? 'Завершение...' : 'Завершить'"
      unelevated
      :class="[$style.primaryAction, $style.primaryActionFilled]"
      :disable="completeLoading"
      @click="$emit('complete', task)"
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
  currentUserId: {
    type: Number,
    default: null,
  },
  startLoading: {
    type: Boolean,
    default: false,
  },
  completeLoading: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['start', 'complete'])

const statusLabel = computed(() => {
  switch (props.task.status) {
    case 'waiting':
      return 'Ожидает'
    case 'in_progress':
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
    case 'in_progress':
      return 'in_progress'
    case 'completed':
      return 'completed'
    default:
      return 'default'
  }
})

const showStartButton = computed(() => props.task.status === 'waiting')

const showCompleteButton = computed(() => {
  return (
    props.task.status === 'in_progress' &&
    props.task.executorId === props.currentUserId
  )
})

const formattedDate = computed(() => {
  const sourceDate = props.task.status === 'completed'
    ? props.task.completedAt || props.task.dueDate
    : props.task.dueDate

  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
  }).format(new Date(sourceDate))
})

const dateLabel = computed(() => {
  return props.task.status === 'completed' ? 'Дата выполнения' : 'Плановая дата'
})

const isOverdue = computed(() => {
  return props.task.status !== 'completed' && props.task.isOverdue
})
</script>

<style module lang="scss" src="./TaskCard.module.scss"></style>
