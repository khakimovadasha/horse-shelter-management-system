<template>
  <RouterLink :to="to" :class="$style.link">
    <article :class="$style.root">
      <div :class="$style.header">
        <div :class="$style.name">{{ horseName }}</div>
        <AppStatusBadge :label="statusLabel" :tone="statusTone" />
      </div>

      <div :class="$style.meta">{{ breed }}</div>
      <div :class="$style.secondary">{{ secondaryText }}</div>
    </article>
  </RouterLink>
</template>

<script setup>
import { RouterLink } from 'vue-router'

import AppStatusBadge from 'src/components/ui/AppStatusBadge/AppStatusBadge.vue'

defineProps({
  to: {
    type: String,
    required: true,
  },
  horseName: {
    type: String,
    required: true,
  },
  breed: {
    type: String,
    required: true,
  },
  secondaryText: {
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

<style module lang="scss" src="./ProfileHorseItem.module.scss"></style>
