<template>
  <q-checkbox
    v-bind="$attrs"
    :class="$style.root"
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
  </q-checkbox>
</template>

<script setup>
defineOptions({
  inheritAttrs: false,
})

defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['update:modelValue'])
</script>

<style module lang="scss" src="./AppCheckboxField.module.scss"></style>
