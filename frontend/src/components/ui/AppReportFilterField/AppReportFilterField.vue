<template>
  <div :class="$style.control">
    <AppSelectField
      v-if="fieldType === 'select'"
      v-bind="$attrs"
      :class="$style.reportField"
      :model-value="modelValue"
      :options="options"
      @update:model-value="$emit('update:modelValue', $event)"
    />

    <AppTextField
      v-else
      v-bind="$attrs"
      :class="$style.reportField"
      type="date"
      :model-value="modelValue"
      @update:model-value="$emit('update:modelValue', $event)"
    />
  </div>
</template>

<script setup>
import AppSelectField from 'src/components/ui/AppSelectField/AppSelectField.vue'
import AppTextField from 'src/components/ui/AppTextField/AppTextField.vue'

defineOptions({
  inheritAttrs: false,
})

defineProps({
  fieldType: {
    type: String,
    default: 'select',
    validator: (value) => ['select', 'date'].includes(value),
  },
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

<style module lang="scss" src="./AppReportFilterField.module.scss"></style>
