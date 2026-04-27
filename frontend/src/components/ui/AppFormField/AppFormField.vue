<template>
  <div :class="$style.fieldGroup">
    <label v-if="label" :class="$style.label">
      {{ label }}
    </label>

    <slot />
  </div>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    default: '',
  },
})
</script>

<style module lang="scss" src="./AppFormField.module.scss"></style>
