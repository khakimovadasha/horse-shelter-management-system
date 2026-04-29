<template>
  <div v-if="max > 1" :class="$style.root">
    <q-pagination
      :model-value="modelValue"
      :max="max"
      :max-pages="maxPages"
      direction-links
      boundary-links
      color="primary"
      active-design="unelevated"
      @update:model-value="emit('update:modelValue', $event)"
    />
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Number,
    required: true,
  },
  max: {
    type: Number,
    required: true,
  },
  maxPages: {
    type: Number,
    default: 6,
  },
})

const emit = defineEmits(['update:modelValue'])
</script>

<style module lang="scss" src="./AppPagination.module.scss"></style>
