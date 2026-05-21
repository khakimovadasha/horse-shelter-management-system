<template>
  <article :class="$style.card">
    <div :class="$style.header">
      <div :class="$style.main">
        <div :class="$style.title">{{ title }}</div>
        <div v-if="subtitle" :class="$style.subtitle">{{ subtitle }}</div>
      </div>

      <div v-if="$slots.aside" :class="$style.aside">
        <slot name="aside" />
      </div>
    </div>

    <div :class="$style.body">
      <slot />
    </div>
  </article>
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

<style module lang="scss" src="./ReportMobileCard.module.scss"></style>
