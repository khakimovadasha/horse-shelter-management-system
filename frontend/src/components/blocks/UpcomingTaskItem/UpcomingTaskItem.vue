<template>
  <article :class="$style.root">
    <div :class="$style.header">
      <div :class="$style.taskTitle">{{ taskTitle }}</div>
      <AppStatusBadge :label="statusLabel" :tone="statusTone" />
    </div>

    <div :class="$style.description">{{ description }}</div>
    <div :class="$style.dueAt">{{ dueAt }}</div>

    <AppButton
      v-if="actionLabel"
      :label="actionLabel"
      :disable="actionDisabled"
      :unelevated="actionFilled"
      :outline="!actionFilled"
      :class="[$style.primaryAction, actionFilled && $style.primaryActionFilled]"
      @click="$emit('action-click')"
    />
  </article>
</template>

<script setup>
import AppButton from 'src/components/ui/AppButton/AppButton.vue'
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'

defineEmits(['action-click'])

defineProps({
  taskTitle: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  dueAt: {
    type: String,
    required: true,
  },
  statusLabel: {
    type: String,
    required: true,
  },
  statusTone: {
    type: String,
    required: true,
  },
  actionLabel: {
    type: String,
    default: '',
  },
  actionFilled: {
    type: Boolean,
    default: false,
  },
  actionDisabled: {
    type: Boolean,
    default: false,
  },
})
</script>

<style module lang="scss" src="./UpcomingTaskItem.module.scss"></style>
