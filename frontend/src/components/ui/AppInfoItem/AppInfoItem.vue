<template>
  <div :class="$style.root">
    <div :class="$style.label">{{ label }}</div>
    <div :class="$style.value">{{ value }}</div>
  </div>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    required: true,
  },
  value: {
    type: String,
    default: '',
  },
})
</script>

<style module lang="scss" src="./AppInfoItem.module.scss"></style>
