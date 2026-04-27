<template>
  <q-file
    v-bind="$attrs"
    :class="$style.root"
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
  </q-file>
</template>

<script setup>
defineOptions({
  inheritAttrs: false,
})

defineProps({
  modelValue: {
    type: [Object, Array, null],
    default: null,
  },
})

defineEmits(['update:modelValue'])
</script>

<style module lang="scss" src="./AppFileField.module.scss"></style>
