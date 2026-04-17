<template>
  <div :class="[$style.badge, $style[tone] || $style.default]">
    {{ label }}
  </div>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    required: true,
  },
  tone: {
    type: String,
    default: 'default',
  },
})
</script>

<style module lang="scss" src="./AppStatusBadge.module.scss"></style>
