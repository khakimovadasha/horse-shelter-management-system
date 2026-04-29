<template>
  <q-card :class="[$style.root, 'app-card']">
    <div :class="$style.header">
      <div>
        <div :class="$style.title">{{ title }}</div>
        <div v-if="subtitle" :class="$style.subtitle">{{ subtitle }}</div>
      </div>

      <div v-if="$slots.actions" :class="$style.actions">
        <slot name="actions" />
      </div>
    </div>

    <div :class="$style.body">
      <slot />
    </div>
  </q-card>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
})
</script>

<style module lang="scss" src="./AppDataPanel.module.scss"></style>
