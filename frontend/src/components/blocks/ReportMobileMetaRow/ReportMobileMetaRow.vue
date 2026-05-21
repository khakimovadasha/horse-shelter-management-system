<template>
  <div :class="[stacked ? $style.rowStacked : $style.row]">
    <span :class="$style.label">{{ label }}</span>
    <span :class="[stacked ? $style.valueStacked : $style.value]">
      <slot>{{ value }}</slot>
    </span>
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
  stacked: {
    type: Boolean,
    default: false,
  },
})
</script>

<style module lang="scss" src="./ReportMobileMetaRow.module.scss"></style>
