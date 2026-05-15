<template>
  <q-card :class="[$style.root, 'app-card']">
    <div :class="$style.header">
      <div :class="$style.heading">
        <div :class="$style.title">{{ title }}</div>
        <div v-if="subtitle" :class="$style.subtitle">{{ subtitle }}</div>
      </div>

      <RouterLink
        v-if="actionLabel && actionTo"
        :to="actionTo"
        :class="$style.actionLink"
      >
        <span>{{ actionLabel }}</span>
        <q-icon name="arrow_forward" size="20px" />
      </RouterLink>

      <button
        v-else-if="actionLabel"
        type="button"
        :class="$style.actionLink"
        @click="$emit('action-click')"
      >
        <span>{{ actionLabel }}</span>
        <q-icon name="arrow_forward" size="20px" />
      </button>
    </div>

    <div :class="$style.body">
      <slot />
    </div>
  </q-card>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineEmits(['action-click'])

defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
  actionLabel: {
    type: String,
    default: '',
  },
  actionTo: {
    type: String,
    default: '',
  },
})
</script>

<style module lang="scss" src="./AppDashboardSection.module.scss"></style>
