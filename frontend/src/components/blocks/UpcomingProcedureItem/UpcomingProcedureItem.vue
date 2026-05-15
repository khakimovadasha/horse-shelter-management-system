<template>
  <article :class="$style.root">
    <div :class="$style.header">
      <div :class="$style.horseName">{{ horseName }}</div>
      <AppStatusBadge :label="statusLabel" :tone="statusTone" />
    </div>

    <div :class="$style.procedureName">{{ procedureName }}</div>
    <div :class="$style.scheduledAt">{{ scheduledAt }}</div>
  </article>
</template>

<script setup>
import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'

defineProps({
  horseName: {
    type: String,
    required: true,
  },
  procedureName: {
    type: String,
    required: true,
  },
  scheduledAt: {
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

<style module lang="scss" src="./UpcomingProcedureItem.module.scss"></style>
