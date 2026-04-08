<template>
  <q-input
    v-bind="$attrs"
    outlined
    dense
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <template
      v-for="(_, slotName) in $slots"
      #[slotName]="slotProps"
      :key="slotName"
    >
      <slot :name="slotName" v-bind="slotProps || {}" />
    </template>
  </q-input>
</template>

<script setup>
defineOptions({
  inheritAttrs: false,
})

defineProps({
  modelValue: {
    type: [String, Number, null],
    default: '',
  },
})

defineEmits(['update:modelValue'])
</script>
