<template>
  <q-select
    v-bind="$attrs"
    outlined
    dense
    emit-value
    map-options
    :model-value="modelValue"
    :options="options"
    @update:model-value="$emit('update:modelValue', $event)"
  />
</template>

<script setup>
defineOptions({
  inheritAttrs: false,
})

defineProps({
  modelValue: {
    type: [String, Number, Boolean, Object, Array, null],
    default: null,
  },
  options: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['update:modelValue'])
</script>
