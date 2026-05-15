<template>
  <article :class="$style.root">
    <div :class="$style.header">
      <div :class="$style.taskTitle">{{ taskTitle }}</div>
      <AppStatusBadge :label="statusLabel" :tone="statusTone" />
    </div>

    <div :class="$style.description">{{ description }}</div>
    <div :class="$style.dueAt">{{ dueAt }}</div>
  </article>
</template>

<script setup>
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'

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
})
</script>

<style module lang="scss" src="./UpcomingTaskItem.module.scss"></style>
